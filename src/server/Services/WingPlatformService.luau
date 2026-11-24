--!strict
-- WingPlatformService: where robots get their wings (owner request 2026-11-24). No robot starts with wings and
-- they are not sold: the wing platform (the owner's "Pod Standing Platform" model) stands in R03, the side room
-- off Reception, with a hologram of the Nightwing turning above it. A robot that stands in the platform's centre
-- ring until the ring of light completes (HOLD seconds) gets the wings (ItemCatalog.grant, saved).
--
-- The platform runs on facility power: it is dark while the facility lighting is "Degraded" (start of M01) and
-- comes on when main power is restored (FacilityService.PowerOn) or in free roam.
-- Server authoritative: this service measures who stands in the ring; clients only draw it.
-- World (built at start, in PZ_StasisFacility.WingPlatform):
--   Platform (clone of ServerStorage.Props.WingPlatform: the baked MeshParts, base centred at the pivot),
--   PadFloor (invisible standing disc), Ring (SEGMENTS neon segments), Hologram (wing model, hologram look,
--   at wing height: a robot standing in the centre stands "inside" it while the wings install), Info (anchor for
--   the client's label). Attribute Powered (boolean) on the model.
-- The room's name sign (Labels.R03_Label, a billboard at the room centre) is moved to the back wall so it does
-- not cover the platform.
-- ReplicatedStorage.PZ_Remotes.WingPlatform (RemoteEvent), server -> client:
--   ("status", { state = "charging", seconds = remaining } | { state = "cancel" } | { state = "granted" }
--              | { state = "owned" } | { state = "nopower" })
-- Client: WingPlatform.client.luau (hologram motion, ring progress, label, "acquired" banner).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local ServerStorage = game:GetService("ServerStorage")

local ItemCatalog = require(ReplicatedStorage.Shared.ItemCatalog)
local PlayerDataService = require(script.Parent.PlayerDataService)
local EquipmentService = require(script.Parent.EquipmentService)

local WingPlatformService = {}

local ITEM = "wings_basic"
local CENTRE = Vector3.new(43, 0.2, -12) -- R03 floor, facility frame (x 43, y 12); door D08 is to the west
local WIDTH = 15           -- platform diameter (studs), set in the Blender prep (pz_vehicle_prep.py length 15)
local PAD_TOP = 0.184 * WIDTH -- centre disc height above the base (measured on the model: 18.4 % of its width)
local INNER_R = 0.18 * WIDTH  -- centre disc radius (18 % of the width)
local HOLD = 5             -- seconds standing in the ring
local SEGMENTS = 36
local HOLO_HEIGHT = 5.2    -- hologram centre above the pad: wing height on a standing robot
local HOLO_SCALE = 0.9
local LABEL_SPOT = Vector3.new(42, 14, -22.5) -- R03 sign, against the south wall
local CYAN = Color3.fromHex("#22D3EE")

local remote: RemoteEvent
local model: Model
type Tracker = { t: number, state: string }
local trackers: { [Player]: Tracker } = {}

local function part(name: string, size: Vector3, cf: CFrame, parent: Instance): Part
	local p = Instance.new("Part")
	p.Name = name; p.Size = size; p.CFrame = cf; p.Anchored = true
	p.CanCollide = false; p.CanQuery = false; p.CanTouch = false; p.CastShadow = false
	p.Material = Enum.Material.Neon; p.Color = CYAN
	p.Parent = parent
	return p
end

local function hologram(top: number): Model?
	local items = ServerStorage:FindFirstChild("Items")
	local src = items and items:FindFirstChild("WingsBasic")
	if not src then return nil end
	local h = src:Clone() :: Model
	h.Name = "Hologram"
	for _, d in ipairs(h:GetDescendants()) do
		if d:IsA("SurfaceAppearance") or d:IsA("Attachment") then
			d:Destroy()
		elseif d:IsA("BasePart") then
			d.Anchored = true; d.CanCollide = false; d.CanQuery = false; d.CanTouch = false; d.CastShadow = false
			if d.Name == "MountPart" then
				d.Transparency = 1
			else
				if d:IsA("MeshPart") then d.TextureID = "" end
				d.Material = Enum.Material.ForceField; d.Color = CYAN; d.Transparency = 0
			end
		end
	end
	h:ScaleTo(HOLO_SCALE)
	h:PivotTo(CFrame.new(CENTRE.X, top + HOLO_HEIGHT, CENTRE.Z))
	local light = Instance.new("PointLight")
	light.Color = CYAN; light.Range = 14; light.Brightness = 1.5
	light.Parent = h:FindFirstChildWhichIsA("BasePart", true)
	return h
end

local function build()
	local facility = workspace:WaitForChild("PZ_StasisFacility", 30) :: Model
	local old = facility:FindFirstChild("WingPlatform")
	if old then old:Destroy() end
	model = Instance.new("Model")
	model.Name = "WingPlatform"
	local props = ServerStorage:FindFirstChild("Props")
	local template = props and props:FindFirstChild("WingPlatform") :: Model?
	if template then
		local p = template:Clone()
		p.Name = "Platform"
		p:PivotTo(CFrame.new(CENTRE))
		p.Parent = model
	else
		warn("[WingPlatform] ServerStorage.Props.WingPlatform missing; using a plain disc")
		local disc = part("Platform", Vector3.new(PAD_TOP, WIDTH, WIDTH), CFrame.new(CENTRE + Vector3.new(0, PAD_TOP / 2, 0)) * CFrame.Angles(0, 0, math.rad(90)), model)
		disc.Shape = Enum.PartType.Cylinder; disc.Material = Enum.Material.Metal; disc.Color = Color3.fromHex("#2B2F36")
		disc.CanCollide = true; disc.CanQuery = true
	end
	local top = CENTRE.Y + PAD_TOP
	-- invisible standing disc, so the centre is always solid whatever the mesh collision does
	local floor = part("PadFloor", Vector3.new(0.4, INNER_R * 2, INNER_R * 2), CFrame.new(CENTRE.X, top - 0.2, CENTRE.Z) * CFrame.Angles(0, 0, math.rad(90)), model)
	floor.Shape = Enum.PartType.Cylinder; floor.Transparency = 1; floor.CanCollide = true; floor.CanQuery = true
	local ring = Instance.new("Folder"); ring.Name = "Ring"; ring.Parent = model
	local r = INNER_R - 0.35
	for i = 1, SEGMENTS do
		local a = (i - 0.5) / SEGMENTS * math.pi * 2
		local cf = CFrame.new(CENTRE.X, top + 0.04, CENTRE.Z) * CFrame.Angles(0, -a, 0) * CFrame.new(0, 0, -r)
		local seg = part(("S%02d"):format(i), Vector3.new(2 * math.pi * r / SEGMENTS * 0.7, 0.08, 0.22), cf, ring)
		seg.Transparency = 0.75
	end
	part("Info", Vector3.new(0.2, 0.2, 0.2), CFrame.new(CENTRE.X, top + HOLO_HEIGHT + 3.3, CENTRE.Z), model).Transparency = 1
	local labels = facility:FindFirstChild("Labels")
	local sign = labels and labels:FindFirstChild("R03_Label") :: BasePart?
	if sign then sign.Position = LABEL_SPOT end
	local h = hologram(top)
	if h then h.Parent = model end
	model.Parent = facility
	local function power()
		local on = facility:GetAttribute("Lighting") ~= "Degraded"
		model:SetAttribute("Powered", on)
	end
	facility:GetAttributeChangedSignal("Lighting"):Connect(power)
	power()
end

local function owns(player: Player): boolean
	local p = PlayerDataService.GetProfile(player)
	return p ~= nil and p.items[ITEM] == true
end

local function send(player: Player, info: { [string]: any })
	remote:FireClient(player, "status", info)
end

local function standingIn(player: Player): boolean
	local c = player.Character
	local root = c and c:FindFirstChild("HumanoidRootPart") :: BasePart?
	local hum = c and c:FindFirstChildOfClass("Humanoid")
	if not root or not hum or hum.Health <= 0 then return false end
	local flat = Vector3.new(root.Position.X - CENTRE.X, 0, root.Position.Z - CENTRE.Z)
	local h = root.Position.Y - (CENTRE.Y + PAD_TOP)
	return flat.Magnitude <= INNER_R and h > 0 and h < 10
end

local function grant(player: Player)
	local ok = false
	PlayerDataService.Update(player, function(p)
		ok = (ItemCatalog.grant(p, ITEM))
	end)
	if ok then
		EquipmentService.Refresh(player)
		send(player, { state = "granted" })
		print(("[WingPlatform] %s acquired the Nightwing"):format(player.Name))
	end
end

local function step(dt: number)
	local powered = model:GetAttribute("Powered") == true
	for _, player in ipairs(Players:GetPlayers()) do
		local tr = trackers[player]
		if not tr then
			tr = { t = 0, state = "out" }; trackers[player] = tr
		end
		local inside = standingIn(player)
		local want = if not inside then "out" elseif not powered then "nopower" elseif owns(player) then "owned" else "charging"
		if want ~= tr.state then
			if tr.state == "charging" then send(player, { state = "cancel" }) end
			tr.state, tr.t = want, 0
			if want == "charging" then
				send(player, { state = "charging", seconds = HOLD })
			elseif want == "nopower" or want == "owned" then
				send(player, { state = want })
			end
		elseif want == "charging" then
			tr.t += dt
			if tr.t >= HOLD then
				tr.state = "owned"
				grant(player)
			end
		end
	end
end

function WingPlatformService.Start()
	remote = Instance.new("RemoteEvent")
	remote.Name = "WingPlatform"
	remote.Parent = ReplicatedStorage:WaitForChild("PZ_Remotes")
	build()
	Players.PlayerRemoving:Connect(function(p) trackers[p] = nil end)
	local acc = 0
	RunService.Heartbeat:Connect(function(dt)
		acc += dt
		if acc < 0.1 then return end
		step(acc)
		acc = 0
	end)
end

return WingPlatformService
