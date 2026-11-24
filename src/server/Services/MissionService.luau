--!strict
-- MissionService: runs mission M01 "The Awakening" for the party in this server (decision D5: a mission instance
-- holds a party of 1-4). Rules and dialogue live in Shared.MissionM01 (pure, unit tested); this service turns
-- world input into mission events, applies the resulting effects, and saves checkpoints.
--
-- Start: the first player who has woken (StasisService.Activated, or already activated on join) starts the
-- mission from their saved checkpoint (profile.progress.missions.M01 = step id, or "complete" = free roam).
-- Later players join the running mission. Checkpoints are saved to every present player on each step change.
-- Inputs: reach pod P01 (find_cypher); breaker prompts B1-B3; release prompt on P05; medical console (optional
-- MF-002, per player); standing in the exit zone (each player completes on their own).
-- Client messages on ReplicatedStorage.PZ_Remotes.Mission (RemoteEvent, server -> client only):
--   ("objective", { step, title, hint, target: Instance?, optional: { title, hint, target }? })
--   ("dialogue", beats)        ("complete", { mission = "M01" })

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local M = require(ReplicatedStorage.Shared.MissionM01)
local PlayerDataService = require(script.Parent.PlayerDataService)
local StasisService = require(script.Parent.StasisService)
local FacilityService = require(script.Parent.FacilityService)
local NpcService = require(script.Parent.NpcService)

local MissionService = {}

local REACH_RANGE = 5
local remote: RemoteEvent
local state: M.State? = nil
local freeRoam = false
local joined: { [Player]: boolean } = {}
local completed: { [Player]: boolean } = {}
local rng = Random.new()

local function pods(): Folder
	return workspace:WaitForChild("PZ_StasisFacility"):FindFirstChild("Pods", true) :: Folder
end

local function targetOf(name: string?): Instance?
	if not name then return nil end
	local pod = pods():FindFirstChild(name)
	if pod then return pod:FindFirstChild("Plinth") end
	return FacilityService.Prop(name)
end

local function objectiveFor(player: Player)
	if not state or completed[player] then
		return nil
	end
	local o = M.OBJECTIVES[state.step]
	local opt = nil
	local profile = PlayerDataService.GetProfile(player)
	if M.optionalAvailable(state.step) and profile and not profile.progress.memoryFragments[M.OPTIONAL.mf002.fragment] then
		opt = { title = M.OPTIONAL.mf002.title, hint = M.OPTIONAL.mf002.hint, target = targetOf(M.OPTIONAL.mf002.target) }
	end
	return { step = state.step, title = o.title, hint = o.hint, target = targetOf(o.target), optional = opt }
end

local function sendObjective(player: Player)
	if joined[player] then
		remote:FireClient(player, "objective", objectiveFor(player))
	end
end

local function saveCheckpoint(player: Player)
	if not state then return end
	local step = state.step
	PlayerDataService.Update(player, function(p)
		if p.progress.missions[M.ID] ~= "complete" then
			p.progress.missions[M.ID] = step
		end
	end)
end

local function setPrompts()
	local step = state and state.step or ""
	for _, id in ipairs(M.BREAKERS) do
		FacilityService.EnablePrompt(id, step == "restore_power")
	end
	FacilityService.EnablePrompt("MedConsole", state ~= nil and M.optionalAvailable(step))
	local p05 = pods():FindFirstChild("P05")
	local pr = p05 and p05:FindFirstChild("Glass") and (p05 :: any).Glass:FindFirstChild("ReleasePrompt") :: ProximityPrompt?
	if pr then pr.Enabled = step == "free_sentinel" end
end

local function applyWorld(effect: string, instant: boolean)
	if effect == "wake_cypher" then
		NpcService.Wake("Cypher", instant)
	elseif effect == "power_on" then
		FacilityService.PowerOn()
	elseif effect == "wake_sentinel" then
		NpcService.Wake("Sentinel", instant)
	elseif effect == "lockdown" then
		FacilityService.Lockdown()
	end
end

local function run(effects: { any }, player: Player?)
	for _, e in ipairs(effects) do
		local name, arg = if type(e) == "table" then e[1] else e, if type(e) == "table" then e[2] else nil
		if name == "objective" then
			for p in pairs(joined) do
				saveCheckpoint(p)
				sendObjective(p)
			end
			setPrompts()
		elseif name == "dialogue" then
			local beats = M.DIALOGUE[arg]
			if arg == "complete" and player then
				remote:FireClient(player, "dialogue", beats)
			else
				for p in pairs(joined) do remote:FireClient(p, "dialogue", beats) end
			end
		elseif name == "breaker_ok" then
			FacilityService.SetBreakerLamp(arg, "ok")
		elseif name == "breaker_reset" then
			for _, id in ipairs(M.BREAKERS) do FacilityService.SetBreakerLamp(id, "fault") end
			task.delay(1.2, function()
				if state and state.step == "restore_power" then
					for _, id in ipairs(M.BREAKERS) do FacilityService.SetBreakerLamp(id, "off") end
				end
			end)
		elseif name == "complete_player" and player then
			completed[player] = true
			PlayerDataService.Update(player, function(p) p.progress.missions[M.ID] = "complete" end)
			remote:FireClient(player, "complete", { mission = M.ID })
			remote:FireClient(player, "objective", nil)
		else
			applyWorld(name, false)
		end
	end
end

local function event(name: string, arg: any, player: Player?)
	if not state then return end
	run(M.apply(state, name, arg), player)
end

-- Start the mission for this server from `step` (a checkpoint) and rebuild the world for it.
local function start(step: string)
	if step == "complete" then
		freeRoam = true
		state = M.new("complete")
		for _, e in ipairs(M.worldEffectsFor("complete")) do applyWorld(e, true) end
		FacilityService.FreeRoam()
	else
		state = M.new(step, M.shuffledSequence(function(n) return rng:NextInteger(1, n) end))
		for _, e in ipairs(M.worldEffectsFor(step)) do applyWorld(e, true) end
		if step == "restore_power" then
			FacilityService.SetSequence((state :: M.State).sequence)
		end
	end
	setPrompts()
end

local function join(player: Player)
	if joined[player] then return end
	local profile = PlayerDataService.GetProfile(player)
	if not profile or not profile.progress.activated then return end
	local saved = profile.progress.missions[M.ID]
	if not state then
		start(if type(saved) == "string" and M.stepIndex(saved) then saved else "find_cypher")
	end
	joined[player] = true
	if saved == "complete" then
		completed[player] = true
	elseif state and not freeRoam then
		saveCheckpoint(player)
	end
	if state and state.step == "restore_power" then
		FacilityService.SetSequence(state.sequence)
	end
	sendObjective(player)
end

local function watchPositions()
	task.spawn(function()
		while true do
			task.wait(0.25)
			if state and not freeRoam then
				for p in pairs(joined) do
					local r = p.Character and p.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
					if r and not r.Anchored then
						if state.step == "find_cypher" then
							-- a spot just in front of Cypher's pod (pods are only ~9 studs apart, so not the pod itself)
							local plinth = targetOf("P01") :: BasePart?
							local front = plinth and Vector3.new(plinth.Position.X + (if plinth.Position.X < 0 then 4 else -4), 0, plinth.Position.Z)
							if front and (Vector3.new(r.Position.X, 0, r.Position.Z) - front).Magnitude < REACH_RANGE then
								event("reached_cypher", nil, p)
								FacilityService.SetSequence(state.sequence)
							end
						elseif state.step == "escape" and not completed[p] and FacilityService.InExitZone(r.Position) then
							event("exited", nil, p)
						end
					end
				end
			end
		end
	end)
end

function MissionService.Start()
	local folder = ReplicatedStorage:WaitForChild("PZ_Remotes")
	remote = Instance.new("RemoteEvent")
	remote.Name = "Mission"
	remote.Parent = folder

	FacilityService.Start()
	FacilityService.SetExtraCharacters(NpcService.Models)
	local podFolder = pods()
	-- Cypher keeps the reserved white (the only white robot); the dormant pods hold other-coloured frames
	NpcService.Spawn("Cypher", "CypherFrame", podFolder:WaitForChild("P01") :: Model, "CYPHER", 1, { colour = "arctic" })
	NpcService.Spawn("Sentinel", "SentinelNPC", podFolder:WaitForChild("P05") :: Model, "SENTINEL", 2)
	NpcService.Spawn("Dormant07", "CypherFrame", podFolder:WaitForChild("P07") :: Model, nil, 3, { colour = "crimson", dormant = true })
	NpcService.Spawn("Dormant08", "CypherFrame", podFolder:WaitForChild("P08") :: Model, nil, 4, { colour = "gold", dormant = true })
	local p05glass = (podFolder:WaitForChild("P05") :: Model):WaitForChild("Glass") :: BasePart
	local release = Instance.new("ProximityPrompt")
	release.Name = "ReleasePrompt"; release.ActionText = "Release"; release.ObjectText = "Sentinel (pod P05)"
	release.HoldDuration = 1; release.MaxActivationDistance = 9; release.RequiresLineOfSight = false; release.Enabled = false
	release.Parent = p05glass
	release.Triggered:Connect(function(player)
		if joined[player] then event("freed_sentinel", nil, player) end
	end)

	FacilityService.PromptTriggered:Connect(function(name, player)
		if not joined[player] or not state then return end
		if table.find(M.BREAKERS, name) then
			event("breaker", name, player)
		elseif name == "MedConsole" and M.optionalAvailable(state.step) then
			local frag = M.OPTIONAL.mf002.fragment
			local profile = PlayerDataService.GetProfile(player)
			if profile and not profile.progress.memoryFragments[frag] then
				PlayerDataService.Update(player, function(p) p.progress.memoryFragments[frag] = true end)
				remote:FireClient(player, "dialogue", M.DIALOGUE.mf002)
				sendObjective(player)
			end
		end
	end)

	StasisService.Activated:Connect(join)
	PlayerDataService.ProfileLoaded:Connect(function(player)
		task.defer(join, player)
	end)
	for _, p in ipairs(Players:GetPlayers()) do task.defer(join, p) end
	Players.PlayerRemoving:Connect(function(p)
		joined[p], completed[p] = nil, nil
	end)
	watchPositions()
end

-- Studio test helper (read-only): current step and breaker sequence.
function MissionService.Debug()
	return state and { step = state.step, sequence = state.sequence, pressed = state.pressed, freeRoam = freeRoam } or nil
end

return MissionService
