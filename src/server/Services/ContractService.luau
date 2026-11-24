--!strict
-- ContractService: civilian jobs in the Founders' Quarter (docs/NEXUS_01_CITY.md §2). Rules: Shared.ContractRules.
--   * Patch stands at the workbench inside the workshop interior. "Talk" starts the best contract the player can do
--     (C02 if unlocked, else C01), reminds them of an active one, or pays them when they report back.
--   * After M01, a player who has never done C01 gets the objective "Find Patch" (the first ten minutes, v2 §42).
--   * Each player has their own contract and targets. The client makes its own prompts for them (crate, lights, bay
--     arms) and asks the server here; the server checks distance and the rules before anything changes.
--   * Carrying a power cell shows the cell in the robot's right hand (welded on the server, so everyone sees it).
-- Remotes (ReplicatedStorage.PZ_Remotes):
--   Contract (RemoteEvent) client -> server: ("take_cell") | ("install", lightId) | ("calibrate", armId)
--                          server -> client: ("state", { id, step, targets = {ids}, done = {ids}, carrying } | nil)
--   Mission (existing): objectives and Patch's lines go through the mission HUD (heading "CONTRACT · …").

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")

local ContractRules = require(ReplicatedStorage.Shared.ContractRules)
local CityLayout = require(ReplicatedStorage.Shared.CityLayout)
local PlayerDataService = require(script.Parent.PlayerDataService)
local CityService = require(script.Parent.CityService)
local NpcService = require(script.Parent.NpcService)

local ContractService = {}

local REACH = 9          -- studs from a crate / light / arm to use it
local COOLDOWN = 0.3
local PATCH = "PATCH"
local remote: RemoteEvent
local mission: RemoteEvent
local active: { [Player]: ContractRules.State } = {}
local last: { [Player]: number } = {}
local rng = Random.new()

local function say(player: Player, lines: { string })
	local beats = {}
	for _, l in ipairs(lines) do
		if l ~= "" then
			table.insert(beats, { kind = "source", speaker = PATCH, text = l, seconds = math.clamp(#l / 16, 2.5, 5) })
		end
	end
	mission:FireClient(player, "dialogue", beats)
end

local function targetPart(id: string): BasePart?
	local light = CityService.Light(id)
	if light then return light.PrimaryPart end
	return CityService.Anchor(id)
end

local function sendState(player: Player)
	local s = active[player]
	if not s then
		remote:FireClient(player, "state", nil)
		return
	end
	local done = {}
	for t in pairs(s.done) do table.insert(done, t) end
	remote:FireClient(player, "state", { id = s.id, step = s.step, targets = s.targets, done = done, carrying = s.carrying })
	local o = ContractRules.objective(s)
	local parts = {}
	for _, t in ipairs(o.targets) do
		local p = targetPart(t)
		if p then table.insert(parts, p) end
	end
	local target = if s.step == "report" then CityService.Anchor("WorkshopDoor")
		elseif o.pickup then CityService.Anchor("WorkshopCrate") else nil
	mission:FireClient(player, "objective", { heading = "CONTRACT  ·  " .. string.upper(o.title), title = o.title, hint = o.hint,
		target = target, targets = if target then nil else parts, npc = if s.step == "report" then "Patch" else nil })
end

local function setCarrying(player: Player, on: boolean)
	local c = player.Character
	if not c then return end
	local old = c:FindFirstChild("PZ_CarriedCell")
	if old then old:Destroy() end
	if not on then return end
	local hand = c:FindFirstChild("RightHand") :: BasePart?
	if not hand then return end
	local src = ServerStorage:FindFirstChild("City") and ServerStorage.City:FindFirstChild("PZ_PowerCell")
	local cell: Instance
	if src then
		cell = src:Clone()
	else
		local p = Instance.new("Part")
		p.Size = Vector3.new(0.9, 1.3, 0.9); p.Color = Color3.fromHex("#F2B33D"); p.Material = Enum.Material.Neon
		cell = p
	end
	cell.Name = "PZ_CarriedCell"
	for _, d in ipairs(if cell:IsA("BasePart") then { cell } else cell:GetDescendants()) do
		if d:IsA("BasePart") then
			d.Anchored = false; d.Massless = true; d.CanCollide = false; d.CanQuery = false; d.CanTouch = false
		end
	end
	local main = if cell:IsA("BasePart") then cell else (cell :: Model).PrimaryPart or cell:FindFirstChildWhichIsA("BasePart", true)
	if not main then return end
	if cell:IsA("Model") then cell:PivotTo(hand.CFrame * CFrame.new(0, -0.7, -0.3)) else (cell :: BasePart).CFrame = hand.CFrame * CFrame.new(0, -0.7, -0.3) end
	for _, d in ipairs(if cell:IsA("BasePart") then { cell } else cell:GetDescendants()) do
		if d:IsA("BasePart") then
			local w = Instance.new("Weld"); w.Part0 = hand; w.Part1 = d; w.C0 = hand.CFrame:ToObjectSpace(d.CFrame); w.Parent = d
		end
	end
	cell.Parent = c
end

local function pickTargets(id: string): { string }
	local c = ContractRules.CONTRACTS[id]
	if c.kind == "calibrate" then
		return { "BayArm1", "BayArm2", "BayArm3" }
	end
	local ids = {}
	for _, l in ipairs(CityLayout.LIGHTS) do table.insert(ids, l.id) end
	for i = #ids, 2, -1 do
		local j = rng:NextInteger(1, i)
		ids[i], ids[j] = ids[j], ids[i]
	end
	return { ids[1], ids[2], ids[3] }
end

local INTRO = {
	C01 = { "You're one of the sleepers, aren't you? Welcome to the Founders' Quarter. I'm Patch.",
		"Three street lights are dark again. Take a power cell from my crate by the door, one at a time, and swap them in.",
		"Hold your hand on the socket until it clicks. I'll pay you in NEXUS Credits. Honest work." },
	C02 = { "You bought a toolkit. Good. The Charge Bay's arms drift out of line every few hours.",
		"Calibrate all three, then come back and tell me." },
}

local function talk(player: Player)
	local profile = PlayerDataService.GetProfile(player)
	if not profile then return end
	local s = active[player]
	if s and s.step == "report" then
		ContractRules.apply(s, "report")
		local id = s.id
		local now = os.time()
		local reward
		PlayerDataService.Update(player, function(p) reward = ContractRules.reward(p, id, now) end)
		active[player] = nil
		setCarrying(player, false)
		say(player, { if reward.first then "That's the street lit again. Here, your first pay. You've got a knack for this."
			else "Good work, as always.",
			("+%d NEXUS Credits  ·  +%d engineering experience"):format(reward.credits, reward.xp) })
		sendState(player)
		mission:FireClient(player, "objective", nil)
		return
	elseif s then
		say(player, { ContractRules.objective(s).hint })
		return
	end
	local now = os.time()
	for _, id in ipairs({ "C02", "C01" }) do
		local ok, why = ContractRules.canStart(profile, id, now)
		if ok then
			active[player] = ContractRules.new(id, pickTargets(id))
			local first = not (profile.contracts[id] and profile.contracts[id].completions > 0)
			say(player, if first then INTRO[id] else { "Same job as before. Lights first, then come back." })
			sendState(player)
			return
		elseif id == "C01" and why == "cooldown" then
			say(player, { "The street's lit for now. Come back in a few minutes.",
				if profile.items.toolkit_engineering then "" else "If you want real repairs, get a toolkit at the Circuit Market." })
			return
		end
	end
end

local function near(player: Player, part: BasePart?): boolean
	local r = player.Character and player.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	return r ~= nil and part ~= nil and (r.Position - part.Position).Magnitude <= REACH
end

local function onRequest(player: Player, action: any, arg: any)
	local now = os.clock()
	if last[player] and now - last[player] < COOLDOWN then return end
	last[player] = now
	local s = active[player]
	if not s or type(action) ~= "string" then return end
	local effects
	if action == "take_cell" and near(player, CityService.Anchor("WorkshopCrate")) then
		effects = ContractRules.apply(s, "take_cell")
	elseif (action == "install" or action == "calibrate") and type(arg) == "string" and near(player, targetPart(arg)) then
		effects = ContractRules.apply(s, action, arg)
	else
		return
	end
	for _, e in ipairs(effects) do
		if e == "carrying" then setCarrying(player, true) end
		if type(e) == "table" and e[1] == "done" and action == "install" then setCarrying(player, false) end
	end
	if #effects > 0 then sendState(player) end
end

-- After M01: point new robots at Patch (once they've never done a contract).
local function guide(player: Player)
	local profile = PlayerDataService.GetProfile(player)
	if not profile or active[player] then return end
	if profile.progress.missions.M01 == "complete" and not profile.contracts.C01 then
		mission:FireClient(player, "objective", { heading = "NEXUS-01  ·  FOUNDERS' QUARTER", title = "Find Patch",
			hint = "Patch's workshop is on the left side of the street. Go in and say hello.", target = CityService.Anchor("WorkshopDoor"),
			npc = "Patch" })
	end
end

function ContractService.Start(missionCompleted: RBXScriptSignal?)
	local folder = ReplicatedStorage:WaitForChild("PZ_Remotes")
	mission = folder:WaitForChild("Mission") :: RemoteEvent
	remote = Instance.new("RemoteEvent")
	remote.Name = "Contract"
	remote.Parent = folder
	remote.OnServerEvent:Connect(onRequest)
	if not CityService.Ready() then return end
	local spot = CityService.InteriorSpot("Patch")
	local door = CityService.InteriorSpot("Spawn")
	if spot and door then
		local look = CFrame.lookAt(spot.Position, Vector3.new(door.Position.X, spot.Position.Y, door.Position.Z))
		local model = NpcService.SpawnAt("Patch", "PatchNPC", look - Vector3.new(0, 0.5, 0), "PATCH", { anchored = true })
		local anchor = (model and model:FindFirstChild("HumanoidRootPart")) or spot
		local p = Instance.new("ProximityPrompt")
		p.ActionText = "Talk"; p.ObjectText = "Patch"; p.MaxActivationDistance = 9; p.RequiresLineOfSight = false
		p.Parent = anchor
		p.Triggered:Connect(talk)
	end
	if missionCompleted then
		missionCompleted:Connect(function(player) task.delay(6, guide, player) end)
	end
	PlayerDataService.ProfileLoaded:Connect(function(player) task.delay(3, guide, player) end)
	for _, pl in ipairs(Players:GetPlayers()) do task.delay(3, guide, pl) end
	Players.PlayerRemoving:Connect(function(pl) active[pl], last[pl] = nil, nil end)
end

return ContractService
