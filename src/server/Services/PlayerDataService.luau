--!strict
-- PlayerDataService: loads a session-locked profile when a player joins, autosaves, and saves + releases on leave
-- and on server shutdown. Other server services read/modify profiles through GetProfile / Update.
--
-- Persistence honesty: if DataStores are unavailable (e.g. Studio without "Enable Studio Access to API Services"),
-- the player gets an in-memory profile and the attribute PZ_PersistentSave = false. Nothing claims to be saved.

local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local RunService = game:GetService("RunService")

local ProfileStore = require(script.Parent.Parent.ProfileStore)
local ProfileSchema = require(game:GetService("ReplicatedStorage").Shared.ProfileSchema)

local STORE_NAME = "PZ_Profiles_v1"
local AUTOSAVE_SECONDS = 120
local LOAD_ATTEMPTS = 5

local PlayerDataService = {}
local profiles: { [Player]: any } = {}
local persistent: { [Player]: boolean } = {}
local changed = Instance.new("BindableEvent")
PlayerDataService.ProfileLoaded = changed.Event -- fires (player, profile)

local store
local function getStore()
	if store == nil then
		local ok, ds = pcall(function()
			return DataStoreService:GetDataStore(STORE_NAME)
		end)
		store = if ok then ProfileStore.new({
			store = ds,
			jobId = if game.JobId ~= "" then game.JobId else ("studio-" .. tostring(os.time())),
			now = os.time,
		}) else false
	end
	return store
end

local function withRetries(fn: () -> ...any, attempts: number)
	local lastErr
	for i = 1, attempts do
		local results = table.pack(pcall(fn))
		if results[1] then
			return true, table.unpack(results, 2, results.n)
		end
		lastErr = results[2]
		task.wait(math.min(2 ^ i, 10))
	end
	return false, lastErr
end

local function onPlayerAdded(player: Player)
	local s = getStore()
	local profile, reason
	if s then
		-- Retry both store errors and a lock still held by a server that is shutting down.
		for attempt = 1, LOAD_ATTEMPTS do
			local ok, p, r = pcall(function()
				return s:load(player.UserId)
			end)
			if ok and p then
				profile, persistent[player] = p, true
				break
			end
			reason = if ok then r else tostring(p)
			if not ok and (string.find(reason, "Studio", 1, true) or string.find(reason, "403", 1, true)) then
				break -- permission errors (e.g. Studio API access off) will not succeed on retry
			end
			if attempt < LOAD_ATTEMPTS then
				task.wait(math.min(2 ^ attempt, 10))
			end
		end
		if profile == nil and reason == "locked" then
			player:Kick("Your Project Zero profile is still open on another server. Please rejoin in a moment.")
			return
		end
	end
	if profile == nil then
		warn(string.format("[PlayerDataService] DataStore unavailable for %s (%s); using an unsaved session profile",
			player.Name, reason or "no store"))
		profile = ProfileSchema.default(player.UserId, os.time())
		profile.stats.sessions = 1
		persistent[player] = false
	end
	if not player.Parent then
		return -- left while loading
	end
	profiles[player] = profile
	player:SetAttribute("PZ_PersistentSave", persistent[player])
	player:SetAttribute("PZ_Activated", profile.progress.activated)
	player:SetAttribute("PZ_Sessions", profile.stats.sessions)
	changed:Fire(player, profile)
end

local function saveProfile(player: Player, release: boolean)
	local profile = profiles[player]
	if not profile or not persistent[player] then
		return
	end
	local s = getStore()
	local ok, saved, reason = withRetries(function()
		return s:save(player.UserId, profile, release)
	end, 3)
	if not ok or not saved then
		warn(string.format("[PlayerDataService] save failed for %s: %s", player.Name, tostring(reason or saved)))
	end
end

function PlayerDataService.GetProfile(player: Player)
	return profiles[player]
end

-- Apply a change to a loaded profile on the server. fn(profile) mutates it; attributes mirror key flags for clients.
function PlayerDataService.Update(player: Player, fn: (any) -> ())
	local profile = profiles[player]
	if not profile then
		return false
	end
	fn(profile)
	player:SetAttribute("PZ_Activated", profile.progress.activated)
	return true
end

function PlayerDataService.IsPersistent(player: Player): boolean
	return persistent[player] == true
end

-- Studio-only test hook: ServerStorage.PZ_DevProfile (BindableFunction, server-side only, never created in live games).
-- Lets playtest assertions read and change the LIVE service state (a test `require` gets a separate module copy).
--   Invoke("get", userId)               -> profile table copy (or nil)
--   Invoke("setMission", userId, id, v) -> true if the profile was updated (v = nil removes the entry)
local function createDevHook()
	if not RunService:IsStudio() then
		return
	end
	local hook = Instance.new("BindableFunction")
	hook.Name = "PZ_DevProfile"
	hook.OnInvoke = function(action: string, userId: number, ...)
		local player = Players:GetPlayerByUserId(userId)
		if not player then
			return nil
		end
		if action == "get" then
			return profiles[player]
		elseif action == "setMission" then
			local id, value = ...
			return PlayerDataService.Update(player, function(p)
				p.progress.missions[id] = value
			end)
		end
		return nil
	end
	hook.Parent = game:GetService("ServerStorage")
end

function PlayerDataService.Start()
	createDevHook()
	Players.PlayerAdded:Connect(onPlayerAdded)
	for _, p in ipairs(Players:GetPlayers()) do
		task.spawn(onPlayerAdded, p)
	end
	Players.PlayerRemoving:Connect(function(player)
		saveProfile(player, true)
		profiles[player], persistent[player] = nil, nil
	end)
	game:BindToClose(function()
		local threads = {}
		for player in pairs(profiles) do
			table.insert(threads, task.spawn(saveProfile, player, true))
		end
		local deadline = os.clock() + (if RunService:IsStudio() then 5 else 25)
		while os.clock() < deadline and next(threads) do
			task.wait(0.5)
			for i = #threads, 1, -1 do
				if coroutine.status(threads[i]) == "dead" then table.remove(threads, i) end
			end
		end
	end)
	task.spawn(function()
		while true do
			task.wait(AUTOSAVE_SECONDS)
			for player in pairs(profiles) do
				task.spawn(saveProfile, player, false)
			end
		end
	end)
end

return PlayerDataService
