--!strict
-- EnergyService: every robot's energy (docs/NEXUS_01_CITY.md §2), server authoritative. Rules: Shared.EnergyRules.
--   * Drains slowly while the robot is out and about (not while held in its pod or before activation).
--   * Standing on the Charge Bay's platform (anchor "ChargePad") charges it quickly, for free.
--   * At 0 the robot walks at EnergyRules.EMPTY_SPEED; nothing worse.
--   * Energy cells (ItemCatalog "energy_cell", bought at the market): PZ_Remotes.Energy ("useCell") adds 50.
-- Saved in profile.status.energy; mirrored to the player attribute PZ_Energy (rounded) and PZ_Charging for the HUD.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local StarterPlayer = game:GetService("StarterPlayer")

local EnergyRules = require(ReplicatedStorage.Shared.EnergyRules)
local ItemCatalog = require(ReplicatedStorage.Shared.ItemCatalog)
local PlayerDataService = require(script.Parent.PlayerDataService)
local CityService = require(script.Parent.CityService)

local EnergyService = {}

local TICK = 0.5
local PAD_RADIUS = 5     -- horizontal distance from the pad centre that counts as "on the platform"
local PAD_HEIGHT = 8
local COOLDOWN = 0.5
local lastUse: { [Player]: number } = {}

function EnergyService.Get(player: Player): number
	local p = PlayerDataService.GetProfile(player)
	return if p then p.status.energy else EnergyRules.MAX
end

local function publish(player: Player, energy: number, charging: boolean)
	player:SetAttribute("PZ_Energy", math.floor(energy + 0.5))
	player:SetAttribute("PZ_Charging", charging)
	player:SetAttribute("PZ_EnergyCells", ItemCatalog.count(PlayerDataService.GetProfile(player) or {}, "energy_cell"))
end

local function onPad(root: BasePart): boolean
	local pad = CityService.Anchor("ChargePad")
	if not pad then return false end
	local d = root.Position - pad.Position
	return Vector3.new(d.X, 0, d.Z).Magnitude <= PAD_RADIUS and d.Y > -2 and d.Y < PAD_HEIGHT
end

local function step(player: Player, dt: number)
	local profile = PlayerDataService.GetProfile(player)
	local c = player.Character
	local root = c and c:FindFirstChild("HumanoidRootPart") :: BasePart?
	local hum = c and c:FindFirstChildOfClass("Humanoid")
	if not profile or not root or not hum or hum.Health <= 0 then return end
	if not profile.progress.activated or root.Anchored then
		publish(player, profile.status.energy, false) -- in the pod / cinematic: no drain
		return
	end
	local charging = onPad(root)
	local e = profile.status.energy
	local new = if charging then EnergyRules.charge(e, dt) else EnergyRules.drain(e, dt)
	if new ~= e then
		PlayerDataService.Update(player, function(p) p.status.energy = new end)
	end
	hum.WalkSpeed = StarterPlayer.CharacterWalkSpeed * EnergyRules.speedFactor(new)
	publish(player, new, charging)
end

local function useCell(player: Player)
	local now = os.clock()
	if lastUse[player] and now - lastUse[player] < COOLDOWN then return end
	lastUse[player] = now
	local profile = PlayerDataService.GetProfile(player)
	if not profile or profile.status.energy >= EnergyRules.MAX then return end
	PlayerDataService.Update(player, function(p)
		if ItemCatalog.useOne(p, "energy_cell") then
			p.status.energy = EnergyRules.addCell(p.status.energy)
		end
	end)
	publish(player, profile.status.energy, false)
end

function EnergyService.Start()
	local remote = Instance.new("RemoteEvent")
	remote.Name = "Energy"
	remote.Parent = ReplicatedStorage:WaitForChild("PZ_Remotes")
	remote.OnServerEvent:Connect(function(player, action)
		if action == "useCell" then useCell(player) end
	end)
	Players.PlayerRemoving:Connect(function(p) lastUse[p] = nil end)
	task.spawn(function()
		while true do
			task.wait(TICK)
			for _, p in ipairs(Players:GetPlayers()) do
				local ok, err = pcall(step, p, TICK)
				if not ok then warn("[Energy] " .. tostring(err)) end
			end
		end
	end)
end

return EnergyService
