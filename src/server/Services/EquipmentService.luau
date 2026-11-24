--!strict
-- EquipmentService: puts equipped items on robots (owner decision 2026-11-24: wings mount on the back of any
-- basic robot, Cypher-style and Sentinel bodies alike).
--
-- Mounting: the item is a Model placed so its mount point sits on the R15 UpperTorso's "BodyBackAttachment"
-- (both robot rigs have it), then every part is welded straight to the UpperTorso with a classic Weld
-- (explicit offset). Parts are massless and non-colliding, so flight and walking are unchanged.
-- (Roblox Accessories were tried first: AddAccessory rescales accessory parts on R15 bodies and two of the
-- seven placeholder parts lost their joints and fell away in the playtest, so items are welded directly.)
-- Size: scale = UpperTorso height / REFERENCE_TORSO (the Cypher frame's), so Sentinel gets larger wings.
-- Item models: ServerStorage.Items.<name> (a Model with a "Mount" Attachment; +Z of the mount points away from
-- the robot's back). The owner's wing model goes there as ServerStorage.Items.WingsBasic. Until then a
-- built-in placeholder (two angled panels with cyan edges) is used.
-- Attributes for clients: character "PZ_CanFly" = true while wings are on (FlightController reads it).

local Players = game:GetService("Players")
local ServerStorage = game:GetService("ServerStorage")

local PlayerDataService = require(script.Parent.PlayerDataService)

local EquipmentService = {}

local REFERENCE_TORSO = 1.6755 -- CypherFrame UpperTorso height (studs)
local MODELS = { wings_basic = "WingsBasic" }

local function addPart(model: Model, name: string, size: Vector3, cf: CFrame, colour: Color3, material: Enum.Material)
	local p = Instance.new("Part")
	p.Name = name; p.Size = size; p.CFrame = cf; p.Color = colour; p.Material = material
	p.Parent = model
end

-- Placeholder wings in their own frame: origin = mount point, +Z = away from the robot's back.
local function placeholderWings(): Model
	local m = Instance.new("Model")
	m.Name = "WingsBasic"
	local mountPart = Instance.new("Part")
	mountPart.Name = "MountPart"; mountPart.Size = Vector3.new(0.4, 0.4, 0.2); mountPart.Transparency = 1
	mountPart.CFrame = CFrame.new(); mountPart.Parent = m
	local mount = Instance.new("Attachment"); mount.Name = "Mount"; mount.Parent = mountPart
	local dark, cyan = Color3.fromRGB(43, 47, 54), Color3.fromHex("#22D3EE")
	addPart(m, "Spine", Vector3.new(0.5, 1.4, 0.5), CFrame.new(0, 0, 0.3), dark, Enum.Material.Metal)
	for _, side in ipairs({ -1, 1 }) do
		local root = CFrame.new(side * 0.4, 0.2, 0.4) * CFrame.Angles(0, side * math.rad(-20), side * math.rad(-25))
		local s = if side < 0 then "L" else "R"
		addPart(m, "Wing" .. s, Vector3.new(3.2, 1.6, 0.15), root * CFrame.new(side * 1.6, 0, 0), dark, Enum.Material.Metal)
		addPart(m, "Edge" .. s, Vector3.new(3.2, 0.18, 0.2), root * CFrame.new(side * 1.6, 0.8, 0), cyan, Enum.Material.Neon)
		addPart(m, "Tip" .. s, Vector3.new(1.8, 1.0, 0.12), root * CFrame.new(side * 3.4, -0.5, 0) * CFrame.Angles(0, 0, side * math.rad(-25)), dark, Enum.Material.Metal)
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

-- Put `itemId` on any R15 robot model (player character or NPC). Replaces whatever is on its back.
function EquipmentService.Mount(model: Model, itemId: string?)
	local torso = model:FindFirstChild("UpperTorso") :: BasePart?
	local back = torso and torso:FindFirstChild("BodyBackAttachment") :: Attachment?
	if not torso or not back then return end
	local old = model:FindFirstChild("PZ_Back")
	if old then old:Destroy() end
	model:SetAttribute("PZ_CanFly", false)
	if not itemId then return end
	local item = itemModel(itemId)
	if not item then return end
	local mount = item:FindFirstChild("Mount", true) :: Attachment
	local s = torso.Size.Y / REFERENCE_TORSO
	-- place every part relative to the mount, scaled, onto the robot's back attachment
	local mountWorld = mount.WorldCFrame
	local target = back.WorldCFrame
	for _, d in ipairs(item:GetDescendants()) do
		if d:IsA("BasePart") then
			local rel = mountWorld:ToObjectSpace(d.CFrame)
			d.Size *= s
			d.CFrame = target * (rel - rel.Position + rel.Position * s)
			d.Anchored = false; d.Massless = true
			d.CanCollide = false; d.CanQuery = false; d.CanTouch = false
			local w = Instance.new("Weld")
			w.Part0, w.Part1 = torso, d
			w.C0 = torso.CFrame:ToObjectSpace(d.CFrame)
			w.Parent = d
		end
	end
	item.Name = "PZ_Back"
	item:SetAttribute("ItemId", itemId)
	item.Parent = model
	model:SetAttribute("PZ_CanFly", itemId == "wings_basic")
end

function EquipmentService.Refresh(player: Player)
	local profile = PlayerDataService.GetProfile(player)
	local character = player.Character
	if profile and character then
		EquipmentService.Mount(character, profile.equipped.back)
	end
end

function EquipmentService.Start()
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
