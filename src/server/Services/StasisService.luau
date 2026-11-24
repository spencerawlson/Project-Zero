--!strict
-- StasisService: puts each player's starter chassis in their own stasis pod and runs the first activation.
--
-- Facility: Workspace.PZ_StasisFacility. Player pods are the Models whose "Role" attribute starts with
-- "Player pod" (P02, P03, P04, P06 = player pods 1-4; P01 Cypher, P05 Sentinel, P07/P08 dormant).
-- One mission instance holds a party of 1-4 (decision D5), so pods are assigned per player by PodRoster.
--
-- Behaviour (server authoritative):
--   * New player (profile.progress.activated == false): the character is held (root anchored) inside the
--     closed pod, facing the room. The pod's glass carries an "Activate" ProximityPrompt; only the pod's
--     holder can trigger it. Activation opens the glass, frees the character, and saves activated = true.
--   * Returning player (activated == true): the character stands on the floor in front of their pod,
--     whose glass is open.
--   * Leaving releases the pod and closes its glass for the next occupant.
-- Pod attributes for clients and tests: State ("Stasis" | "Open"), OccupantUserId (0 = none).
-- Player attribute: PZ_Pod (pod id). PZ_Activated is mirrored by PlayerDataService.

local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")

local PlayerDataService = require(script.Parent.PlayerDataService)
local PodRoster = require(game:GetService("ReplicatedStorage").Shared.PodRoster)

local PROFILE_WAIT = 15 -- seconds to wait for the profile before placing a character
local OPEN_COLOUR = Color3.fromRGB(0, 230, 200)

local StasisService = {}

type Pod = {
	id: string,
	model: Model,
	glass: BasePart,
	band: BasePart?,
	floorY: number,
	centre: Vector3,
	facing: Vector3,
	glassTransparency: number,
	bandColour: Color3?,
	prompt: ProximityPrompt,
}

local pods: { [string]: Pod } = {}
local roster

local function verticalExtent(part: BasePart): number
	local cf, s = part.CFrame, part.Size
	return math.abs(cf.RightVector.Y) * s.X + math.abs(cf.UpVector.Y) * s.Y + math.abs(cf.LookVector.Y) * s.Z
end

local function setOpen(pod: Pod, open: boolean, animate: boolean)
	local target = if open then 1 else pod.glassTransparency
	pod.glass.CanCollide = not open
	if animate then
		TweenService:Create(pod.glass, TweenInfo.new(1.2, Enum.EasingStyle.Sine), { Transparency = target }):Play()
	else
		pod.glass.Transparency = target
	end
	if pod.band then
		pod.band.Color = if open then OPEN_COLOUR else (pod.bandColour :: Color3)
	end
	pod.model:SetAttribute("State", if open then "Open" else "Stasis")
end

local function discoverPods(): { string }
	local facility = workspace:WaitForChild("PZ_StasisFacility", 30)
	assert(facility, "StasisService: Workspace.PZ_StasisFacility not found")
	local fcf = (facility :: Model):GetBoundingBox()
	local found = {}
	for _, m in ipairs(facility:GetDescendants()) do
		local role = m:GetAttribute("Role")
		local n = if m:IsA("Model") and type(role) == "string" then tonumber(role:match("^Player pod (%d+)")) else nil
		if n then
			local glass = m:FindFirstChild("Glass") :: BasePart
			local plinth = m:FindFirstChild("Plinth") :: BasePart
			assert(glass and plinth, "StasisService: pod " .. m.Name .. " needs Glass and Plinth parts")
			local centre = Vector3.new(glass.Position.X, 0, glass.Position.Z)
			local toRoom = fcf.Position.X - centre.X
			local prompt = Instance.new("ProximityPrompt")
			prompt.Name = "ActivatePrompt"
			prompt.ActionText = "Activate"
			prompt.ObjectText = "Stasis pod " .. m.Name
			prompt.HoldDuration = 0.5
			prompt.MaxActivationDistance = 8
			prompt.RequiresLineOfSight = false
			prompt.Enabled = false
			prompt.Parent = glass
			local band = m:FindFirstChild("StatusBand") :: BasePart?
			pods[m.Name] = {
				id = m.Name,
				model = m :: Model,
				glass = glass,
				band = band,
				floorY = plinth.Position.Y + verticalExtent(plinth) / 2,
				centre = centre,
				facing = Vector3.new(if toRoom >= 0 then 1 else -1, 0, 0),
				glassTransparency = glass.Transparency,
				bandColour = band and band.Color or nil,
				prompt = prompt,
			}
			m:SetAttribute("OccupantUserId", 0)
			table.insert(found, { n = n, id = m.Name })
		end
	end
	table.sort(found, function(a, b) return a.n < b.n end)
	local ids = {}
	for _, f in ipairs(found) do table.insert(ids, f.id) end
	assert(#ids > 0, "StasisService: no player pods found")
	return ids
end

local function waitForProfile(player: Player)
	local deadline = os.clock() + PROFILE_WAIT
	local profile = PlayerDataService.GetProfile(player)
	while not profile and os.clock() < deadline and player.Parent do
		task.wait(0.2)
		profile = PlayerDataService.GetProfile(player)
	end
	return profile
end

-- Root height above the floor for a standing R15 character.
local function rootHeight(character: Model): number
	local hum = character:FindFirstChildOfClass("Humanoid") :: Humanoid
	local root = character:FindFirstChild("HumanoidRootPart") :: BasePart
	return hum.HipHeight + root.Size.Y / 2
end

local function placeCharacter(player: Player, character: Model)
	local root = character:WaitForChild("HumanoidRootPart", 10) :: BasePart?
	local hum = character:WaitForChild("Humanoid", 10) :: Humanoid?
	if not root or not hum then
		return
	end
	local profile = waitForProfile(player)
	if not profile or character.Parent == nil then
		return
	end
	local podId = roster:claim(player.UserId)
	if not podId then
		warn(("[StasisService] no free player pod for %s; leaving them at the default spawn"):format(player.Name))
		return
	end
	local pod = pods[podId]
	player:SetAttribute("PZ_Pod", podId)
	pod.model:SetAttribute("OccupantUserId", player.UserId)
	local h = rootHeight(character)
	if profile.progress.activated then
		setOpen(pod, true, false)
		pod.prompt.Enabled = false
		local spot = pod.centre + pod.facing * 7
		local hit = workspace:Raycast(spot + Vector3.new(0, 20, 0), Vector3.new(0, -60, 0))
		local floorY = if hit then hit.Position.Y else pod.floorY
		local pos = Vector3.new(spot.X, floorY + h, spot.Z)
		root.CFrame = CFrame.lookAt(pos, pos + pod.facing) -- move the root, not the model pivot (Auto Setup rigs have an offset pivot)
	else
		setOpen(pod, false, false)
		local pos = Vector3.new(pod.centre.X, pod.floorY + h, pod.centre.Z)
		root.CFrame = CFrame.lookAt(pos, pos + pod.facing) -- move the root, not the model pivot (Auto Setup rigs have an offset pivot)
		root.Anchored = true
		pod.prompt.Enabled = true
	end
end

local function activate(player: Player, pod: Pod)
	if roster:holderOf(pod.id) ~= player.UserId then
		return -- only the pod's own robot can wake it
	end
	local profile = PlayerDataService.GetProfile(player)
	if not profile or profile.progress.activated then
		return
	end
	pod.prompt.Enabled = false
	setOpen(pod, true, true)
	PlayerDataService.Update(player, function(p)
		p.progress.activated = true
	end)
	local character = player.Character
	local root = character and character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if root then
		task.delay(1.2, function()
			if root.Parent then
				root.Anchored = false
			end
		end)
	end
end

local function release(player: Player)
	local podId = roster:release(player.UserId)
	if podId then
		local pod = pods[podId]
		pod.prompt.Enabled = false
		pod.model:SetAttribute("OccupantUserId", 0)
		setOpen(pod, false, false)
	end
end

function StasisService.Start()
	roster = PodRoster.new(discoverPods())
	for _, pod in pairs(pods) do
		local p = pod
		p.prompt.Triggered:Connect(function(player)
			activate(player, p)
		end)
	end
	local function onPlayer(player: Player)
		player.CharacterAdded:Connect(function(character)
			placeCharacter(player, character)
		end)
		if player.Character then
			task.spawn(placeCharacter, player, player.Character)
		end
	end
	Players.PlayerAdded:Connect(onPlayer)
	for _, p in ipairs(Players:GetPlayers()) do
		onPlayer(p)
	end
	Players.PlayerRemoving:Connect(release)
end

return StasisService
