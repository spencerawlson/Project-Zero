--!strict
-- NpcService: the mission's companion robots (Cypher, Sentinel), server owned.
--
-- Bodies: ServerStorage.Chassis.CypherFrame and ServerStorage.Chassis.SentinelNPC (R15 rigs made with Roblox
-- Avatar Auto Setup from the canonical meshes; the canonical models are never changed). Each NPC starts held
-- in its stasis pod (root anchored inside the pod's field, facing the aisle). Wake: the field fades, the NPC is
-- released and follows the nearest player: PathfindingService path to a spot behind the player (auto doors are
-- passable through their PathfindingModifier), re-planned while walking; if no path or stuck for STUCK_SECONDS,
-- or the player is more than CATCH_UP studs away, the NPC is placed behind the player.
-- Animations: the rig's own idle / walk tracks, played on the server (they replicate).
-- NpcService.SpawnAt places city NPCs (Patch, citizens) at a spot instead of a pod.

local Players = game:GetService("Players")
local PathfindingService = game:GetService("PathfindingService")
local ServerStorage = game:GetService("ServerStorage")
local TweenService = game:GetService("TweenService")

local ChassisColors = require(game:GetService("ReplicatedStorage").Shared.ChassisColors)

local NpcService = {}

local FOLLOW_DISTANCE = 9
local CATCH_UP = 50
local STUCK_SECONDS = 3
local WALK_SPEED = 18

type Npc = {
	name: string,
	model: Model,
	humanoid: Humanoid,
	root: BasePart,
	pod: Model,
	awake: boolean,
	slot: number,
	idle: AnimationTrack?,
	walk: AnimationTrack?,
}
local npcs: { [string]: Npc } = {}

local function animationFrom(template: Model, group: string, name: string?): Animation?
	for _, d in ipairs(template:GetDescendants()) do
		if d:IsA("Animation") and d.Parent and d.Parent.Name == group and (name == nil or d.Name == name) then
			return d
		end
	end
	return nil
end

-- Name tag: small (owner feedback 2026-11-24: the tags were too big) and hidden by default. Each player's
-- MissionHUD shows it only while their current objective is about this character or while it is speaking.
local function nameplate(model: Model, text: string)
	local head = model:FindFirstChild("Head") :: BasePart?
	if not head then return end
	local g = Instance.new("BillboardGui")
	g.Name = "Nameplate"; g.Size = UDim2.fromOffset(96, 18); g.StudsOffset = Vector3.new(0, 1.9, 0)
	g.MaxDistance = 80; g.LightInfluence = 0; g.AlwaysOnTop = false; g.Enabled = false
	local t = Instance.new("TextLabel")
	t.Size = UDim2.fromScale(1, 1); t.BackgroundTransparency = 1; t.Font = Enum.Font.GothamBold
	t.TextColor3 = Color3.fromHex("#22D3EE"); t.TextStrokeTransparency = 0.3; t.TextSize = 13; t.Text = text
	t.Parent = g
	g.Parent = head
end

local function podSpot(pod: Model, hum: Humanoid, root: BasePart): CFrame
	local plinth = pod:FindFirstChild("Plinth") :: BasePart
	local top = plinth.Position.Y + plinth.Size.Y / 2
	local pos = Vector3.new(plinth.Position.X, top + hum.HipHeight + root.Size.Y / 2, plinth.Position.Z)
	local facing = Vector3.new(if pos.X < 0 then 1 else -1, 0, 0)
	return CFrame.lookAt(pos, pos + facing)
end

-- Spawn `name` from ServerStorage.Chassis[templateName] inside `pod`, held (anchored), with its field closed.
-- opts.colour: ChassisColors id to tint the body (nil = the model's own colours).
-- opts.dormant: a sleeping robot that never wakes (no animation, no nameplate when label is nil).
function NpcService.Spawn(name: string, templateName: string, pod: Model, label: string?, slot: number,
	opts: { colour: string?, dormant: boolean? }?)
	local existing = npcs[name]
	if existing then existing.model:Destroy() end
	local template = ServerStorage:WaitForChild("Chassis"):WaitForChild(templateName) :: Model
	local model = template:Clone()
	model.Name = "NPC_" .. name
	for _, d in ipairs(model:GetDescendants()) do
		if d:IsA("LocalScript") or d:IsA("Script") then d:Destroy() end -- the rig's client Animate script
		if d:IsA("BasePart") then d.Anchored = false end
	end
	local hum = model:FindFirstChildOfClass("Humanoid") :: Humanoid
	local root = model:FindFirstChild("HumanoidRootPart") :: BasePart
	hum.WalkSpeed = WALK_SPEED
	hum.DisplayDistanceType = Enum.HumanoidDisplayDistanceType.None
	model.PrimaryPart = root
	root.CFrame = podSpot(pod, hum, root)
	root.Anchored = true
	model:SetAttribute("NpcName", name)
	if opts and opts.colour then
		local colour = ChassisColors.color3(opts.colour)
		for _, d in ipairs(model:GetDescendants()) do
			if d:IsA("SurfaceAppearance") then d.Color = colour end
		end
		model:SetAttribute("ChassisColour", opts.colour)
	end
	model.Parent = workspace
	if label then nameplate(model, label) end
	local npc: Npc = { name = name, model = model, humanoid = hum, root = root, pod = pod, awake = false, slot = slot }
	if not (opts and opts.dormant) then
		local animator = hum:FindFirstChildOfClass("Animator") or Instance.new("Animator", hum)
		local idleA, walkA = animationFrom(template, "idle", "Animation1"), animationFrom(template, "walk", nil)
		if idleA then npc.idle = (animator :: Animator):LoadAnimation(idleA) end
		if walkA then npc.walk = (animator :: Animator):LoadAnimation(walkA) end
		if npc.idle then (npc.idle :: AnimationTrack):Play() end
	end
	hum.Running:Connect(function(speed)
		if speed > 0.5 then
			if npc.walk and not npc.walk.IsPlaying then npc.walk:Play(0.2) end
			if npc.idle and npc.idle.IsPlaying then npc.idle:Stop(0.2) end
		else
			if npc.walk and npc.walk.IsPlaying then npc.walk:Stop(0.2) end
			if npc.idle and not npc.idle.IsPlaying then npc.idle:Play(0.2) end
		end
	end)
	local glass = pod:FindFirstChild("Glass") :: BasePart?
	if glass then glass.Transparency = 0; glass.CanCollide = true end
	pod:SetAttribute("State", "Stasis")
	npcs[name] = npc
end

-- City NPCs (Patch, citizens; docs/NEXUS_01_CITY.md): spawn `name` from ServerStorage.Chassis[templateName] (or
-- ServerStorage.Citizens[templateName]) standing at `cframe` on the ground, as a direct child of workspace (the
-- client's tag logic looks there). opts.anchored keeps it in place (Patch at the workbench); otherwise it is free
-- to walk (citizens) and owned by the server. Plays the rig's idle / walk animations. Returns the model and humanoid.
function NpcService.SpawnAt(name: string, templateName: string, cframe: CFrame, label: string?,
	opts: { anchored: boolean?, colour: string? }?): (Model?, Humanoid?)
	local template = (ServerStorage:FindFirstChild("Chassis") and ServerStorage.Chassis:FindFirstChild(templateName))
		or (ServerStorage:FindFirstChild("Citizens") and ServerStorage.Citizens:FindFirstChild(templateName))
	if not template or not template:IsA("Model") then
		warn("[NPC] template missing: " .. templateName)
		return nil, nil
	end
	local old = workspace:FindFirstChild("NPC_" .. name)
	if old then old:Destroy() end
	local model = template:Clone()
	model.Name = "NPC_" .. name
	for _, d in ipairs(model:GetDescendants()) do
		if d:IsA("LocalScript") or d:IsA("Script") then d:Destroy() end
		if d:IsA("BasePart") then d.Anchored = false end
	end
	local hum = model:FindFirstChildOfClass("Humanoid") :: Humanoid
	local root = model:FindFirstChild("HumanoidRootPart") :: BasePart
	hum.DisplayDistanceType = Enum.HumanoidDisplayDistanceType.None
	model.PrimaryPart = root
	local pos = cframe.Position + Vector3.new(0, hum.HipHeight + root.Size.Y / 2, 0)
	root.CFrame = CFrame.lookAt(pos, pos + cframe.LookVector * Vector3.new(1, 0, 1))
	root.Anchored = opts ~= nil and opts.anchored == true
	model:SetAttribute("NpcName", name)
	if opts and opts.colour then
		local colour = ChassisColors.color3(opts.colour)
		for _, d in ipairs(model:GetDescendants()) do
			if d:IsA("SurfaceAppearance") then d.Color = colour end
		end
	end
	model.Parent = workspace
	if label then nameplate(model, label) end
	if not root.Anchored then
		pcall(function() root:SetNetworkOwner(nil) end)
	end
	local animator = hum:FindFirstChildOfClass("Animator") or Instance.new("Animator", hum)
	local idleA, walkA = animationFrom(template, "idle", "Animation1"), animationFrom(template, "walk", nil)
	local idle = idleA and (animator :: Animator):LoadAnimation(idleA)
	local walk = walkA and (animator :: Animator):LoadAnimation(walkA)
	if idle then idle:Play() end
	hum.Running:Connect(function(speed)
		if speed > 0.5 then
			if walk and not walk.IsPlaying then walk:Play(0.2) end
			if idle and idle.IsPlaying then idle:Stop(0.2) end
		else
			if walk and walk.IsPlaying then walk:Stop(0.2) end
			if idle and not idle.IsPlaying then idle:Play(0.2) end
		end
	end)
	return model, hum
end

local function nearestPlayerRoot(from: Vector3): BasePart?
	local best, bestD = nil, math.huge
	for _, p in ipairs(Players:GetPlayers()) do
		local r = p.Character and p.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		local h = p.Character and p.Character:FindFirstChildOfClass("Humanoid")
		if r and h and h.Health > 0 then
			local d = (r.Position - from).Magnitude
			if d < bestD then best, bestD = r, d end
		end
	end
	return best
end

local function behind(target: BasePart, npc: Npc): Vector3
	local side = if npc.slot % 2 == 0 then 1 else -1
	return target.Position - target.CFrame.LookVector * 5 + target.CFrame.RightVector * 3 * side
end

local function placeNear(npc: Npc, target: BasePart)
	local spot = behind(target, npc)
	local hit = workspace:Raycast(spot + Vector3.new(0, 3, 0), Vector3.new(0, -12, 0))
	local y = (if hit then hit.Position.Y else target.Position.Y - 3) + npc.humanoid.HipHeight + npc.root.Size.Y / 2
	npc.root.CFrame = CFrame.lookAt(Vector3.new(spot.X, y, spot.Z), Vector3.new(target.Position.X, y, target.Position.Z))
end

local function follow(npc: Npc)
	local _, size = npc.model:GetBoundingBox()
	local path = PathfindingService:CreatePath({
		AgentRadius = math.max(size.X, size.Z) / 2 + 0.3, AgentHeight = size.Y + 0.5,
		AgentCanJump = false, WaypointSpacing = 4,
	})
	local lastProgress, lastPos = os.clock(), npc.root.Position
	while npc.awake and npc.model.Parent do
		local target = nearestPlayerRoot(npc.root.Position)
		if target then
			local d = (target.Position - npc.root.Position).Magnitude
			if (npc.root.Position - lastPos).Magnitude > 1 then
				lastProgress, lastPos = os.clock(), npc.root.Position
			end
			if d > CATCH_UP or (d > FOLLOW_DISTANCE and os.clock() - lastProgress > STUCK_SECONDS) then
				placeNear(npc, target)
				lastProgress, lastPos = os.clock(), npc.root.Position
			elseif d > FOLLOW_DISTANCE then
				local goal = behind(target, npc)
				local ok = pcall(function() path:ComputeAsync(npc.root.Position, goal) end)
				if ok and path.Status == Enum.PathStatus.Success then
					local wps = path:GetWaypoints()
					for i = 2, math.min(#wps, 5) do
						npc.humanoid:MoveTo(wps[i].Position)
						local t0 = os.clock()
						while os.clock() - t0 < 1.2 and (npc.root.Position - wps[i].Position).Magnitude > 2.5 do
							task.wait(0.1)
						end
					end
				else
					npc.humanoid:MoveTo(goal)
					task.wait(0.4)
				end
			else
				npc.humanoid:MoveTo(npc.root.Position)
				task.wait(0.3)
			end
		else
			task.wait(0.5)
		end
	end
end

-- Wake `name`: open its field (animated unless instant), release it, and start following.
function NpcService.Wake(name: string, instant: boolean?)
	local npc = npcs[name]
	if not npc or npc.awake then return end
	npc.awake = true
	local glass = npc.pod:FindFirstChild("Glass") :: BasePart?
	if glass then
		glass.CanCollide = false
		if instant then glass.Transparency = 1
		else TweenService:Create(glass, TweenInfo.new(1.2, Enum.EasingStyle.Sine), { Transparency = 1 }):Play() end
	end
	local band = npc.pod:FindFirstChild("StatusBand") :: BasePart?
	if band then band.Color = Color3.fromRGB(0, 230, 200) end
	npc.pod:SetAttribute("State", "Open")
	task.delay(if instant then 0 else 1.2, function()
		npc.root.Anchored = false
		pcall(function() npc.root:SetNetworkOwner(nil) end) -- server-driven movement; no client ownership jitter
		task.spawn(follow, npc)
	end)
end

function NpcService.IsAwake(name: string): boolean
	return npcs[name] ~= nil and npcs[name].awake
end

function NpcService.Models(): { Model }
	local out = {}
	for _, n in pairs(npcs) do
		if n.awake then table.insert(out, n.model) end
	end
	return out
end

function NpcService.Model(name: string): Model?
	return npcs[name] and npcs[name].model
end

return NpcService
