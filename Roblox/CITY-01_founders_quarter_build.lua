-- CITY-01 Founders' Quarter builder (edit time). Run in Studio's Edit mode (command bar or MCP execute_luau).
-- Builds workspace.PZ_FoundersQuarter from Shared.CityLayout (docs/NEXUS_01_CITY.md): ground, street, sidewalks,
-- plaza, street lights, the arrival sign, anchors for gameplay spots, and the buildings, cloned from
-- ServerStorage.City.<model> (each model's pivot = centre of its base, front facing -Z in its own frame).
-- A building whose model is missing gets a labelled grey block, so the layout can be walked before every model is in.
-- Also builds the workshop interior shell at CityLayout.INTERIOR (the INT-03 model goes inside when present).
-- Safe to re-run: the old folder is replaced. Runtime services only look parts up by name.

local ServerStorage = game:GetService("ServerStorage")
local L = require(game:GetService("ReplicatedStorage").Shared.CityLayout)

local old = workspace:FindFirstChild("PZ_FoundersQuarter")
if old then old:Destroy() end
local root = Instance.new("Folder"); root.Name = "PZ_FoundersQuarter"

local function folder(name, parent)
	local f = Instance.new("Folder"); f.Name = name; f.Parent = parent or root; return f
end
local ground, lightsF, buildings = folder("Ground"), folder("Lights"), folder("Buildings")
-- Gameplay anchors and street lights stay loaded for every player (StreamingEnabled is on): contract prompts and
-- objective markers are made for them on the client, so they must exist even when far away.
local anchors = Instance.new("Model"); anchors.Name = "Anchors"; anchors.ModelStreamingMode = Enum.ModelStreamingMode.Persistent; anchors.Parent = root

local function part(name, size, cf, colour, material, parent, props)
	local p = Instance.new("Part")
	p.Name = name; p.Size = size; p.CFrame = cf; p.Anchored = true; p.Color = colour
	p.Material = material or Enum.Material.SmoothPlastic; p.TopSurface = Enum.SurfaceType.Smooth
	for k, v in pairs(props or {}) do p[k] = v end
	p.Parent = parent
	return p
end

local ROAD, WALK, LINE, GRASS = Color3.fromHex("#1F242B"), Color3.fromHex("#8A9199"), Color3.fromHex("#22D3EE"), Color3.fromHex("#2E3A3F")
local len = L.LENGTH

-- ground, road, sidewalks ---------------------------------------------------------------------------------
part("Base", Vector3.new(280, 1, len + 30), CFrame.new(L.at(0, -len / 2 + 5, -0.5)), GRASS, Enum.Material.Concrete, ground)
part("Road", Vector3.new(L.ROAD_HALF * 2, 0.2, len), CFrame.new(L.at(0, -len / 2, 0.1)), ROAD, Enum.Material.Asphalt, ground)
for _, side in ipairs({ -1, 1 }) do
	local cx = side * (L.ROAD_HALF + L.WALK_HALF) / 2
	part("Sidewalk" .. (side < 0 and "W" or "E"), Vector3.new(L.WALK_HALF - L.ROAD_HALF, 0.5, len),
		CFrame.new(L.at(cx, -len / 2, 0.25)), WALK, Enum.Material.Concrete, ground)
	part("Kerb" .. (side < 0 and "W" or "E"), Vector3.new(0.3, 0.55, len), CFrame.new(L.at(side * L.ROAD_HALF, -len / 2, 0.27)),
		LINE, Enum.Material.Neon, ground)
end
for z = -6, -len + 6, -12 do -- centre dashes
	part("Dash", Vector3.new(0.4, 0.05, 6), CFrame.new(L.at(0, z, 0.22)), Color3.fromHex("#E8EEF2"), Enum.Material.Neon, ground)
end
local plaza = part("Plaza", Vector3.new(0.3, L.PLAZA.radius * 2, L.PLAZA.radius * 2),
	CFrame.new(L.at(L.PLAZA.x, L.PLAZA.z, 0.3)) * CFrame.Angles(0, 0, math.rad(90)), Color3.fromHex("#B8C0C8"), Enum.Material.Concrete, ground)
plaza.Shape = Enum.PartType.Cylinder
local ring = part("PlazaRing", Vector3.new(0.35, L.PLAZA.radius * 2 - 6, L.PLAZA.radius * 2 - 6),
	CFrame.new(L.at(L.PLAZA.x, L.PLAZA.z, 0.31)) * CFrame.Angles(0, 0, math.rad(90)), LINE, Enum.Material.Neon, ground)
ring.Shape = Enum.PartType.Cylinder
part("PlazaInner", Vector3.new(0.4, L.PLAZA.radius * 2 - 7, L.PLAZA.radius * 2 - 7),
	CFrame.new(L.at(L.PLAZA.x, L.PLAZA.z, 0.32)) * CFrame.Angles(0, 0, math.rad(90)), Color3.fromHex("#B8C0C8"), Enum.Material.Concrete, ground).Shape = Enum.PartType.Cylinder

-- street lights ---------------------------------------------------------------------------------------------
for _, l in ipairs(L.LIGHTS) do
	local m = Instance.new("Model"); m.Name = l.id
	local base = L.at(l.x, l.z, 0.5)
	local toRoad = if l.x < 0 then 1 else -1
	part("Pole", Vector3.new(0.6, 12, 0.6), CFrame.new(base + Vector3.new(0, 6, 0)), Color3.fromHex("#3A3F47"), Enum.Material.Metal, m)
	part("Arm", Vector3.new(3, 0.4, 0.4), CFrame.new(base + Vector3.new(toRoad * 1.5, 12, 0)), Color3.fromHex("#3A3F47"), Enum.Material.Metal, m)
	local head = part("Head", Vector3.new(1.6, 0.5, 1.2), CFrame.new(base + Vector3.new(toRoad * 2.8, 11.8, 0)), LINE, Enum.Material.Neon, m)
	local pl = Instance.new("PointLight"); pl.Color = LINE; pl.Range = 22; pl.Brightness = 1.4; pl.Parent = head
	local socket = part("Socket", Vector3.new(1, 1.4, 1), CFrame.new(base + Vector3.new(0, 1.2, 0)), Color3.fromHex("#2B2F36"), Enum.Material.Metal, m)
	part("SocketLight", Vector3.new(0.2, 0.6, 0.6), socket.CFrame * CFrame.new(toRoad * 0.55, 0.2, 0), LINE, Enum.Material.Neon, m)
	m.PrimaryPart = socket
	m.ModelStreamingMode = Enum.ModelStreamingMode.Persistent
	m.Parent = lightsF
end

-- arrival sign ----------------------------------------------------------------------------------------------
do
	local s = L.SPOTS.Sign
	local board = part("ArrivalSign", Vector3.new(30, 4, 0.5), CFrame.new(L.at(s.x, s.z, s.y)), Color3.fromHex("#12161C"), Enum.Material.Metal, root)
	for _, side in ipairs({ -1, 1 }) do
		part("SignPost", Vector3.new(0.8, s.y, 0.8), CFrame.new(L.at(side * 15.5, s.z, s.y / 2)), Color3.fromHex("#3A3F47"), Enum.Material.Metal, board)
	end
	for _, face in ipairs({ Enum.NormalId.Front, Enum.NormalId.Back }) do
		local g = Instance.new("SurfaceGui"); g.Face = face; g.LightInfluence = 0; g.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud; g.PixelsPerStud = 30
		local t = Instance.new("TextLabel"); t.Size = UDim2.fromScale(1, 1); t.BackgroundTransparency = 1; t.Font = Enum.Font.GothamBold
		t.TextScaled = true; t.TextColor3 = LINE; t.Text = "NEXUS-01  ·  FOUNDERS' QUARTER"; t.Parent = g
		g.Parent = board
	end
end

-- anchors (invisible, non-colliding: runtime services attach prompts and behaviour to them) ---------------
for name, s in pairs(L.SPOTS) do
	if name ~= "Sign" then
		part(name, Vector3.new(1, 1, 1), CFrame.new(L.at(s.x, s.z, (s.y or 0) + 0.5)), LINE, Enum.Material.SmoothPlastic, anchors,
			{ Transparency = 1, CanCollide = false, CanQuery = false, CanTouch = false })
	end
end

-- props at the anchors: Patch's supply crate and the market kiosk -------------------------------------------
local props = folder("Props")
do
	local s = L.SPOTS.WorkshopCrate
	local c = L.at(s.x, s.z, 0.5)
	part("Crate", Vector3.new(3, 1.6, 2.4), CFrame.new(c + Vector3.new(0, 0.8, 0)), Color3.fromHex("#3A3F47"), Enum.Material.Metal, props)
	part("CrateStripe", Vector3.new(3.05, 0.25, 2.45), CFrame.new(c + Vector3.new(0, 1.1, 0)), Color3.fromHex("#F28C28"), Enum.Material.SmoothPlastic, props)
	for i = -1, 1 do
		part("Cell", Vector3.new(0.6, 0.9, 0.6), CFrame.new(c + Vector3.new(i * 0.9, 2.05, 0)), Color3.fromHex("#F2B33D"), Enum.Material.Neon, props)
	end
	local m = L.SPOTS.MarketCounter
	local k = L.at(m.x, m.z, 0.5)
	part("Kiosk", Vector3.new(2.5, 3.2, 7), CFrame.new(k + Vector3.new(-1, 1.6, 0)), Color3.fromHex("#E8EEF2"), Enum.Material.SmoothPlastic, props)
	part("KioskTop", Vector3.new(2.7, 0.3, 7.2), CFrame.new(k + Vector3.new(-1, 3.35, 0)), Color3.fromHex("#F28C28"), Enum.Material.SmoothPlastic, props)
	local sign = part("KioskSign", Vector3.new(0.3, 1.6, 7), CFrame.new(k + Vector3.new(-1.9, 5.2, 0)), Color3.fromHex("#12161C"), Enum.Material.Metal, props)
	local g = Instance.new("SurfaceGui"); g.Face = Enum.NormalId.Right; g.LightInfluence = 0
	g.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud; g.PixelsPerStud = 40
	local t = Instance.new("TextLabel"); t.Size = UDim2.fromScale(1, 1); t.BackgroundTransparency = 1; t.Font = Enum.Font.GothamBold
	t.TextScaled = true; t.TextColor3 = LINE; t.Text = "CIRCUIT MARKET  ·  TRADE"; t.Parent = g; g.Parent = sign
end

-- buildings -------------------------------------------------------------------------------------------------
local cityModels = ServerStorage:FindFirstChild("City")
for name, b in pairs(L.BUILDINGS) do
	local src = cityModels and cityModels:FindFirstChild(b.model)
	local cf = CFrame.new(L.at(b.x, b.z, 0)) * CFrame.Angles(0, math.rad(b.yaw), 0)
	if src then
		local m = src:Clone(); m.Name = name
		m:PivotTo(cf)
		m.Parent = buildings
	else
		local m = Instance.new("Model"); m.Name = name
		local block = part("Placeholder", Vector3.new(b.length, b.length * 0.4, b.length * 0.55), cf * CFrame.new(0, b.length * 0.2, 0),
			Color3.fromHex("#5A616B"), Enum.Material.SmoothPlastic, m)
		local g = Instance.new("SurfaceGui"); g.Face = Enum.NormalId.Top; g.LightInfluence = 0
		local t = Instance.new("TextLabel"); t.Size = UDim2.fromScale(1, 1); t.BackgroundTransparency = 1; t.TextScaled = true
		t.TextColor3 = Color3.new(1, 1, 1); t.Text = name .. " (model pending)"; t.Parent = g; g.Parent = block
		m.Parent = buildings
	end
end

-- workshop interior shell -----------------------------------------------------------------------------------
do
	local I = folder("WorkshopInterior")
	local c = L.INTERIOR
	part("Floor", Vector3.new(44, 1, 40), CFrame.new(c + Vector3.new(0, -0.5, 0)), Color3.fromHex("#3A3F47"), Enum.Material.Metal, I)
	part("Ceiling", Vector3.new(44, 1, 40), CFrame.new(c + Vector3.new(0, 22.5, 0)), Color3.fromHex("#2B2F36"), Enum.Material.Metal, I)
	for _, w in ipairs({ { 0, -20, 44, 1 }, { 0, 20, 44, 1 }, { -22, 0, 1, 40 }, { 22, 0, 1, 40 } }) do
		part("Wall", Vector3.new(w[3], 23, w[4]), CFrame.new(c + Vector3.new(w[1], 11, w[2])), Color3.fromHex("#C9CED4"), Enum.Material.Metal, I)
	end
	local lamp = part("Lamp", Vector3.new(10, 0.3, 2), CFrame.new(c + Vector3.new(0, 21.8, 0)), Color3.new(1, 1, 1), Enum.Material.Neon, I)
	local pl = Instance.new("PointLight"); pl.Range = 40; pl.Brightness = 2; pl.Parent = lamp
	local src = cityModels and cityModels:FindFirstChild("PZ_WorkshopInterior")
	if src then
		local m = src:Clone(); m.Name = "InteriorModel"; m:PivotTo(CFrame.new(c)); m.Parent = I
	end
	for name, s in pairs(L.INTERIOR_SPOTS) do
		part(name, Vector3.new(1, 1, 1), CFrame.new(c + Vector3.new(s.x, 0.5, s.z)), LINE, Enum.Material.SmoothPlastic, I,
			{ Transparency = 1, CanCollide = false, CanQuery = false, CanTouch = false })
	end
end

root.Parent = workspace
return "built PZ_FoundersQuarter"
