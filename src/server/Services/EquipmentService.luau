--!strict
-- EquipmentService: puts equipped items on robots (owner decision 2026-11-24: wings mount on the back of any
-- basic robot, Cypher-style and Sentinel bodies alike).
--
-- Wings are only visible while flying (owner feedback 2026-11-24: the always-on wings looked like a glitch,
-- not part of the robot, and should be an option, not something that stays there):
--   * A back module (dark housing, cyan core, two hinge pins) sits on the upper back at the R15 UpperTorso's
--     "BodyBackAttachment"; the wings hinge from it, raised to the shoulder blades and set back from the arms.
--   * Everything starts stowed (invisible). The character attribute PZ_WingsOut = true deploys it: every
--     client's WingVisuals script unfolds the wings out of the module (and folds them back when it turns false).
--   * FlightController asks for deploy / stow on PZ_Remotes.Flight ("deploy" | "stow"); the server only
--     deploys wings on a character that has them (PZ_CanFly).
-- Mounting: every part is welded straight to the UpperTorso with a classic Weld (explicit offset). Parts are
-- massless and non-colliding, so walking and flight are unchanged. (Roblox Accessories were tried first:
-- AddAccessory rescales accessory parts on R15 bodies and dropped parts in the playtest.)
-- Size: scale = UpperTorso height / REFERENCE_TORSO (the Cypher frame's), so Sentinel gets larger wings.
-- Item models: ServerStorage.Items.<name> (a Model with a "Mount" Attachment at the wings' spine). The owner's
-- Nightwing model is ServerStorage.Items.WingsBasic; a built-in placeholder is used if it is missing.
-- What WingVisuals reads (set here, never changed afterwards):
--   PZ_Back model: attribute PZ_Hinge (CFrame, torso space: the wings' fold axis)
--   each part: PZ_Role ("core" | "wing"), PZ_FullC0 (CFrame), PZ_FullSize (Vector3), PZ_Side (-1 | 1, wings)
-- Attributes on the character: PZ_CanFly (wings on), PZ_WingsOut (deployed).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")

local PlayerDataService = require(script.Parent.PlayerDataService)

local EquipmentService = {}

local REFERENCE_TORSO = 1.6755 -- CypherFrame UpperTorso height (studs)
local MODELS = { wings_basic = "WingsBasic" }
-- Wing layout at Cypher scale (studs / degrees). Chosen by eye on both robot bodies (2026-11-24).
local LIFT = 0.35     -- hinge above the back attachment (shoulder blades)
local BACK = 0.45     -- wings this far behind the back, clear of the swinging arms
local WING_SCALE = 0.8
local TILT = 12       -- each wing raised this much at the tip
local DARK, CYAN = Color3.fromHex("#2B2F36"), Color3.fromHex("#22D3EE")

local function placeholderWings(): Model
	local m = Instance.new("Model")
	m.Name = "WingsBasic"
	local mountPart = Instance.new("Part")
	mountPart.Name = "MountPart"; mountPart.Size = Vector3.new(0.4, 0.4, 0.2); mountPart.Transparency = 1
	mountPart.Parent = m
	local mount = Instance.new("Attachment"); mount.Name = "Mount"; mount.Parent = mountPart
	for _, side in ipairs({ -1, 1 }) do
		local p = Instance.new("Part")
		p.Name = if side < 0 then "WingL" else "WingR"; p.Size = Vector3.new(3.4, 1.8, 0.15)
		p.CFrame = CFrame.new(side * 1.8, 0.2, 0); p.Color = DARK; p.Material = Enum.Material.Metal
		p.Parent = m
	end
	return m
end

local function itemModel(itemId: string): Model?
	local name = MODELS[itemId]
	if not name then return nil end
	local folder = ServerStorage:FindFirstChild("Items")
	local asset = folder and folder:FindFirstChild(name)
	if asset and asset:IsA("Model") and asset:FindFirstChild("Mount", true) then
		return asset:Clone()
	end
	return placeholderWings()
end

local function weldTo(torso: BasePart, d: BasePart, role: string)
	d.Anchored = false; d.Massless = true
	d.CanCollide = false; d.CanQuery = false; d.CanTouch = false
	d.CastShadow = role == "wing"
	local w = Instance.new("Weld")
	w.Name = "PZ_Weld"
	w.Part0, w.Part1 = torso, d
	w.C0 = torso.CFrame:ToObjectSpace(d.CFrame)
	w.Parent = d
	d:SetAttribute("PZ_Role", role)
	d:SetAttribute("PZ_FullC0", w.C0)
	d:SetAttribute("PZ_FullSize", d.Size)
	d:SetAttribute("PZ_BaseTransparency", d.Transparency)
	d.Transparency = 1 -- stowed until PZ_WingsOut
end

-- The back module the wings fold out of, built around the hinge (world CFrame), at scale s.
local function backModule(parent: Model, hinge: CFrame, s: number): { BasePart }
	local parts = {}
	local function add(name: string, size: Vector3, cf: CFrame, colour: Color3, material: Enum.Material, shape: Enum.PartType?)
		local p = Instance.new("Part")
		p.Name = name; p.Size = size * s; p.CFrame = cf; p.Color = colour; p.Material = material
		if shape then p.Shape = shape end
		p.Parent = parent
		table.insert(parts, p)
		return p
	end
	local core = add("Core", Vector3.new(0.85, 1.05, 0.42), hinge * CFrame.new(0, 0, 0.18 * s), DARK, Enum.Material.Metal)
	add("CoreLight", Vector3.new(0.12, 0.75, 0.06), core.CFrame * CFrame.new(0, 0, 0.21 * s), CYAN, Enum.Material.Neon)
	for _, side in ipairs({ -1, 1 }) do
		add(if side < 0 then "HingeL" else "HingeR", Vector3.new(0.5, 0.36, 0.36),
			core.CFrame * CFrame.new(side * 0.42 * s, 0.25 * s, 0.05 * s) * CFrame.Angles(0, math.rad(90), 0),
			Color3.fromHex("#3A3F47"), Enum.Material.Metal, Enum.PartType.Cylinder)
	end
	return parts
end

-- Put `itemId` on any R15 robot model (player character or NPC), stowed. Replaces whatever is on its back.
function EquipmentService.Mount(model: Model, itemId: string?)
	local torso = model:FindFirstChild("UpperTorso") :: BasePart?
	local back = torso and torso:FindFirstChild("BodyBackAttachment") :: Attachment?
	if not torso or not back then return end
	local old = model:FindFirstChild("PZ_Back")
	if old then old:Destroy() end
	model:SetAttribute("PZ_CanFly", false)
	model:SetAttribute("PZ_WingsOut", false)
	if not itemId then return end
	local item = itemModel(itemId)
	if not item then return end
	local mount = item:FindFirstChild("Mount", true) :: Attachment
	local s = torso.Size.Y / REFERENCE_TORSO
	local k = s * WING_SCALE
	local hinge = back.WorldCFrame * CFrame.new(0, LIFT * s, 0)
	local wingRoot = hinge * CFrame.new(0, 0, BACK * s)
	local mountWorld = mount.WorldCFrame
	for _, d in ipairs(item:GetDescendants()) do
		if d:IsA("BasePart") then
			local rel = mountWorld:ToObjectSpace(d.CFrame)
			local side = if rel.Position.X < 0 then -1 else 1
			d.Size *= k
			d.CFrame = wingRoot * CFrame.Angles(0, 0, side * math.rad(TILT)) * (rel - rel.Position + rel.Position * k)
			weldTo(torso, d, "wing")
			d:SetAttribute("PZ_Side", side)
		end
	end
	for _, p in ipairs(backModule(item, hinge, s)) do
		weldTo(torso, p, "core")
	end
	item.Name = "PZ_Back"
	item:SetAttribute("ItemId", itemId)
	item:SetAttribute("PZ_Hinge", torso.CFrame:ToObjectSpace(wingRoot))
	item.Parent = model
	model:SetAttribute("PZ_CanFly", itemId == "wings_basic")
end

-- Deploy (true) or stow (false) the wings of a robot that has them.
function EquipmentService.SetDeployed(model: Model, out: boolean)
	model:SetAttribute("PZ_WingsOut", out and model:GetAttribute("PZ_CanFly") == true)
end

function EquipmentService.Refresh(player: Player)
	local profile = PlayerDataService.GetProfile(player)
	local character = player.Character
	if profile and character then
		EquipmentService.Mount(character, profile.equipped.back)
	end
end

function EquipmentService.Start()
	local remote = Instance.new("RemoteEvent")
	remote.Name = "Flight"
	remote.Parent = ReplicatedStorage:WaitForChild("PZ_Remotes")
	remote.OnServerEvent:Connect(function(player, action)
		local c = player.Character
		if c and (action == "deploy" or action == "stow") then
			EquipmentService.SetDeployed(c, action == "deploy")
		end
	end)
	local function onCharacter(player: Player, character: Model)
		character:WaitForChild("UpperTorso", 10)
		local deadline = os.clock() + 15
		while not PlayerDataService.GetProfile(player) and os.clock() < deadline and player.Parent do
			task.wait(0.2)
		end
		EquipmentService.Refresh(player)
	end
	local function onPlayer(player: Player)
		player.CharacterAdded:Connect(function(c) onCharacter(player, c) end)
		if player.Character then task.spawn(onCharacter, player, player.Character) end
	end
	Players.PlayerAdded:Connect(onPlayer)
	for _, p in ipairs(Players:GetPlayers()) do onPlayer(p) end
end

return EquipmentService
