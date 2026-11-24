-- BLD-01 art pass, room R04 (Stasis Pod Chamber). Run in Studio's Edit mode. Owner feedback 2026-11-24: the pod room
-- looked dull and unfinished next to the owner's chamber models (greybox walls, flat floor, debug labels).
-- Adds, in workspace.PZ_StasisFacility.ArtPass.R04 (replaced on re-run):
--   * suspended light bars over the aisle (neon + SurfaceLight, tagged so FacilityService drives them with the
--     mission lighting states: Degraded / Online / Lockdown),
--   * cable trays under the vault, door frames with orange trim and a status light, wall plaques at both doors,
--   * vertical ribs on the two end walls.
-- Materials: floors use the MaterialVariant "PZ_FloorPanel" (generated in Studio); walls get "PZ_WallPanel" when it
-- exists in MaterialService.
-- Studio frame for R04: x -32..32, z -24..-104 (facility y 24..104), floor top y 0.2, vault top y 31.6.

local CollectionService = game:GetService("CollectionService")
local F = workspace.PZ_StasisFacility
local root = F:FindFirstChild("ArtPass") or Instance.new("Folder")
root.Name = "ArtPass"; root.Parent = F
local old = root:FindFirstChild("R04"); if old then old:Destroy() end
local R = Instance.new("Folder"); R.Name = "R04"

local GUN, DARK, ORANGE, CYAN, WHITE = Color3.fromHex("#3A3F47"), Color3.fromHex("#22262C"), Color3.fromHex("#F28C28"), Color3.fromHex("#22D3EE"), Color3.fromRGB(225, 238, 255)

local function part(name, size, cf, colour, material, parent)
	local p = Instance.new("Part")
	p.Name = name; p.Size = size; p.CFrame = cf; p.Anchored = true; p.Color = colour
	p.Material = material or Enum.Material.Metal; p.TopSurface = Enum.SurfaceType.Smooth; p.BottomSurface = Enum.SurfaceType.Smooth
	p.Parent = parent or R
	return p
end
local function deco(p) p.CanCollide = false; p.CanQuery = false; p.CanTouch = false; return p end

-- light bars over the aisle -----------------------------------------------------------------------------------
for i, z in ipairs({ -34, -46, -58, -70, -82, -94 }) do
	local y = 21
	deco(part("BarHousing" .. i, Vector3.new(12, 0.6, 1.4), CFrame.new(0, y + 0.35, z), DARK))
	local tube = deco(part("BarLight" .. i, Vector3.new(11, 0.25, 0.9), CFrame.new(0, y, z), WHITE, Enum.Material.Neon))
	tube.CastShadow = false
	CollectionService:AddTag(tube, "PZ_FacilityNeon")
	local sl = Instance.new("SurfaceLight"); sl.Face = Enum.NormalId.Bottom; sl.Range = 24; sl.Angle = 120; sl.Brightness = 1.6
	sl.Color = WHITE; sl.Shadows = true; sl.Parent = tube
	CollectionService:AddTag(sl, "PZ_FacilityLight")
	for _, x in ipairs({ -5.5, 5.5 }) do -- hanging cables up to the vault
		deco(part("Cable", Vector3.new(0.12, 31.6 - y, 0.12), CFrame.new(x, (31.6 + y) / 2, z), DARK))
	end
end

-- cable trays along the room under the vault ---------------------------------------------------------------
for _, x in ipairs({ -9, 9 }) do
	deco(part("Tray", Vector3.new(2.2, 0.3, 78), CFrame.new(x, 22.6, -64), GUN))
	for k, dy in ipairs({ 0.35, 0.6 }) do
		local c = deco(part("TrayCable" .. k, Vector3.new(78, 0.35, 0.35), CFrame.new(x - 0.5 + k * 0.4, 22.6 + dy, -64) * CFrame.Angles(0, math.rad(90), 0),
			if k == 1 then DARK else Color3.fromHex("#1B3A44"), Enum.Material.SmoothPlastic))
		c.Shape = Enum.PartType.Cylinder
	end
	for z = -26, -102, -8 do -- hangers
		deco(part("TrayHanger", Vector3.new(0.15, 31.6 - 22.6, 0.15), CFrame.new(x, (31.6 + 22.6) / 2, z), DARK))
	end
end

-- door frames, status lights and plaques -------------------------------------------------------------------
local doors = {
	{ name = "D02", z = -24, width = 10, height = 11.8, inward = -1, plaque = "R04  ·  STASIS POD CHAMBER" },
	{ name = "D03", z = -104, width = 12, height = 13.8, inward = 1, plaque = "R04  ·  CONTAINMENT DOOR D03  ·  SERVICE BAY" },
}
for _, d in ipairs(doors) do
	local face = d.z + d.inward * 0.75 -- just inside the room
	for _, side in ipairs({ -1, 1 }) do
		local x = side * (d.width / 2 + 0.7)
		part(d.name .. "_Jamb", Vector3.new(1.4, d.height + 0.6, 0.8), CFrame.new(x, 0.2 + (d.height + 0.6) / 2, face), GUN)
		deco(part(d.name .. "_Trim", Vector3.new(0.2, d.height, 0.85), CFrame.new(x - side * 0.6, 0.2 + d.height / 2, face), ORANGE, Enum.Material.SmoothPlastic))
	end
	part(d.name .. "_Head", Vector3.new(d.width + 2.8, 1.2, 0.8), CFrame.new(0, 0.2 + d.height + 0.6, face), GUN)
	local status = deco(part(d.name .. "_Status", Vector3.new(2.4, 0.3, 0.2), CFrame.new(0, 0.2 + d.height + 0.6, face + d.inward * 0.45), CYAN, Enum.Material.Neon))
	CollectionService:AddTag(status, "PZ_FacilityNeon")
	local plaque = part(d.name .. "_Plaque", Vector3.new(14, 1.6, 0.2), CFrame.new(0, 0.2 + d.height + 2.6, face + d.inward * 0.2), DARK, Enum.Material.SmoothPlastic)
	local g = Instance.new("SurfaceGui"); g.Face = if d.inward > 0 then Enum.NormalId.Back else Enum.NormalId.Front
	g.LightInfluence = 0; g.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud; g.PixelsPerStud = 40
	local t = Instance.new("TextLabel"); t.Size = UDim2.fromScale(1, 1); t.BackgroundTransparency = 1; t.Font = Enum.Font.GothamBold
	t.TextScaled = true; t.TextColor3 = CYAN; t.Text = d.plaque; t.Parent = g
	local pad = Instance.new("UIPadding"); pad.PaddingLeft = UDim.new(0, 12); pad.PaddingRight = UDim.new(0, 12); pad.PaddingTop = UDim.new(0, 8); pad.PaddingBottom = UDim.new(0, 8); pad.Parent = t
	g.Parent = plaque
end

-- vertical ribs on the end walls (break up the flat surfaces) ----------------------------------------------
for _, d in ipairs(doors) do
	local face = d.z + d.inward * 0.6
	for _, side in ipairs({ -1, 1 }) do
		for x = d.width / 2 + 5, 30, 6 do
			part(d.name .. "_Rib", Vector3.new(0.8, 20, 0.6), CFrame.new(side * x, 10.2, face), GUN)
			deco(part(d.name .. "_RibLight", Vector3.new(0.15, 4, 0.65), CFrame.new(side * x, 8, face), CYAN, Enum.Material.Neon))
		end
	end
end

-- materials -------------------------------------------------------------------------------------------------
local MS = game:GetService("MaterialService")
local hasWall = MS:FindFirstChild("PZ_WallPanel", true) ~= nil
local walls = 0
for _, w in ipairs(F.Walls:GetChildren()) do
	local p = w.Position
	if w:IsA("BasePart") and p.X > -33 and p.X < 33 and p.Z < -23 and p.Z > -105 then
		w.Material = Enum.Material.Metal
		w.MaterialVariant = if hasWall then "PZ_WallPanel" else ""
		w.Color = Color3.fromRGB(196, 202, 210)
		walls += 1
	end
end
-- doors (all 18): gunmetal panels with the wall texture instead of flat greybox colours; a light tint keeps the
-- wayfinding colours (green emergency exits, orange main entrance, red containment, yellow service door).
-- FacilityService reads each door's colour at start and only switches to dark red Neon while a door is locked.
local tint = {
	D05 = Color3.fromRGB(78, 122, 96), D06 = Color3.fromRGB(78, 122, 96), D01 = Color3.fromRGB(132, 104, 82),
	D02 = Color3.fromRGB(118, 86, 92), D03 = Color3.fromRGB(118, 86, 92), D04 = Color3.fromRGB(126, 116, 82),
}
for _, d in ipairs(F.Doors:GetChildren()) do
	if d:IsA("BasePart") then
		d.Material = Enum.Material.Metal
		d.MaterialVariant = if hasWall then "PZ_WallPanel" else ""
		d.Color = tint[d.Name] or Color3.fromRGB(92, 100, 112)
	end
end

local fl = F.Floors:FindFirstChild("R04_Floor")
if fl then fl.Material = Enum.Material.Metal; fl.MaterialVariant = "PZ_FloorPanel"; fl.Color = Color3.fromRGB(190, 195, 205) end

R.Parent = root
local n = 0; for _, d in ipairs(R:GetDescendants()) do if d:IsA("BasePart") then n += 1 end end
return ("R04 art pass: %d parts, %d walls retextured (wall variant %s)"):format(n, walls, tostring(hasWall))
