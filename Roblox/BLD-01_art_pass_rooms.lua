-- BLD-01 art pass for every room except R04 (which has its own script, BLD-01_art_pass_R04.lua). Run in Studio's
-- Edit mode after the R04 pass (it needs the MaterialVariants PZ_FloorPanel and PZ_WallPanel). Owner feedback
-- 2026-11-24: the facility looked dull and unfinished (greybox) next to the owner's models.
-- Per room: panelled floor, panelled walls, a darker panelled ceiling, a grid of ceiling light panels (tagged so
-- FacilityService drives them with the mission lighting states), a dark skirting board and a cyan light line along
-- every wall with gaps at the doorways, and door frames on both sides of every door.
-- Output: workspace.PZ_StasisFacility.ArtPass.Rooms (replaced on re-run). Room rectangles: Blender/scripts/pz_layout.py
-- (facility frame x, y -> Studio x, z = -y). Exterior walls are 2 thick, interior walls 1.

local CollectionService = game:GetService("CollectionService")
local F = workspace.PZ_StasisFacility
local root = F:FindFirstChild("ArtPass") or Instance.new("Folder")
root.Name = "ArtPass"; root.Parent = F
local old = root:FindFirstChild("Rooms"); if old then old:Destroy() end
local OUT = Instance.new("Folder"); OUT.Name = "Rooms"

local GUN, DARK, CYAN, WHITE = Color3.fromHex("#3A3F47"), Color3.fromHex("#22262C"), Color3.fromHex("#22D3EE"), Color3.fromRGB(225, 238, 255)
local EXT = { x = { [-52] = true, [52] = true }, y = { [0] = true, [120] = true } }

-- name, x0, x1, y0, y1 (facility frame), ceiling height (measured in Studio)
local ROOMS = {
	{ "R01", -32, 32, 0, 24, 20 }, { "R02", -52, -32, 0, 24, 20 }, { "R03", 32, 52, 0, 24, 20 },
	{ "R05", -40, -32, 24, 104, 18 }, { "R06", -52, -40, 24, 72, 18 }, { "R07", -52, -40, 72, 88, 18 },
	{ "R08", -52, -40, 88, 104, 18 }, { "R09", 32, 52, 24, 60, 18 }, { "R10", 32, 52, 60, 96, 18 },
	{ "R11", 32, 52, 96, 120, 22 }, { "R12", -32, 32, 104, 120, 22 }, { "R13", -52, -32, 104, 120, 22 },
}

local function part(name, size, cf, colour, material, parent, solid)
	local p = Instance.new("Part")
	p.Name = name; p.Size = size; p.CFrame = cf; p.Anchored = true; p.Color = colour
	p.Material = material or Enum.Material.Metal; p.TopSurface = Enum.SurfaceType.Smooth; p.BottomSurface = Enum.SurfaceType.Smooth
	if not solid then p.CanCollide = false; p.CanQuery = false; p.CanTouch = false end
	p.Parent = parent
	return p
end

-- door openings on a wall line: returns sorted { {a, b} } intervals along the wall
local doorParts = {}
for _, d in ipairs(F.Doors:GetChildren()) do if d:IsA("BasePart") then table.insert(doorParts, d) end end
local function gapsOn(axis: string, coord: number, lo: number, hi: number)
	local gaps = {}
	for _, d in ipairs(doorParts) do
		local p, s = d.Position, d.Size
		if axis == "x" and math.abs(p.X - coord) < 1.6 and s.X < s.Z then -- wall along Z at x = coord
			table.insert(gaps, { p.Z - s.Z / 2 - 1.6, p.Z + s.Z / 2 + 1.6 })
		elseif axis == "z" and math.abs(p.Z - coord) < 1.6 and s.Z < s.X then -- wall along X at z = coord
			table.insert(gaps, { p.X - s.X / 2 - 1.6, p.X + s.X / 2 + 1.6 })
		end
	end
	table.sort(gaps, function(a, b) return a[1] < b[1] end)
	local segs, cur = {}, lo
	for _, g in ipairs(gaps) do
		if g[2] > lo and g[1] < hi then
			if g[1] > cur then table.insert(segs, { cur, g[1] }) end
			cur = math.max(cur, g[2])
		end
	end
	if cur < hi then table.insert(segs, { cur, hi }) end
	return segs
end

local panels = 0
for _, r in ipairs(ROOMS) do
	local name, x0, x1, y0, y1, ceil = r[1], r[2], r[3], r[4], r[5], r[6]
	local R = Instance.new("Folder"); R.Name = name; R.Parent = OUT
	-- inner faces of the room's walls
	local ix0 = x0 + (if EXT.x[x0] then 1 else 0.5)
	local ix1 = x1 - (if EXT.x[x1] then 1 else 0.5)
	local iz0 = -y0 - (if EXT.y[y0] then 1 else 0.5) -- Studio z of the y0 wall's inner face
	local iz1 = -y1 + (if EXT.y[y1] then 1 else 0.5)
	local w, d = ix1 - ix0, iz0 - iz1
	local cx, cz = (ix0 + ix1) / 2, (iz0 + iz1) / 2

	-- ceiling light panels: a grid about every 12 studs
	local nx = math.max(1, math.floor(w / 12 + 0.5))
	local nz = math.max(1, math.floor(d / 12 + 0.5))
	for i = 1, nx do
		for j = 1, nz do
			local x = ix0 + w * (i - 0.5) / nx
			local z = iz1 + d * (j - 0.5) / nz
			local long = if w >= d then Vector3.new(math.min(7, w / nx - 3), 0.25, 1.6) else Vector3.new(1.6, 0.25, math.min(7, d / nz - 3))
			part("PanelHousing", long + Vector3.new(0.6, 0.35, 0.6), CFrame.new(x, ceil - 0.35, z), DARK, Enum.Material.Metal, R)
			local tube = part("PanelLight", long, CFrame.new(x, ceil - 0.62, z), WHITE, Enum.Material.Neon, R)
			tube.CastShadow = false
			CollectionService:AddTag(tube, "PZ_FacilityNeon")
			local sl = Instance.new("SurfaceLight"); sl.Face = Enum.NormalId.Bottom; sl.Range = 20; sl.Angle = 120
			sl.Brightness = 1.4; sl.Color = WHITE; sl.Shadows = false; sl.Parent = tube -- no shadows: 54 panels, low-end GPUs
			CollectionService:AddTag(sl, "PZ_FacilityLight")
			panels += 1
		end
	end

	-- skirting and cyan light line along the four walls, with doorway gaps
	local edges = {
		{ "z", iz0, ix0, ix1, 1 }, { "z", iz1, ix0, ix1, -1 }, -- walls along X (facility y0 / y1 sides)
		{ "x", ix0, iz1, iz0, 1 }, { "x", ix1, iz1, iz0, -1 }, -- walls along Z
	}
	for _, e in ipairs(edges) do
		local axis, coord, lo, hi = e[1], e[2], e[3], e[4]
		local wallCoord = if axis == "z" then coord + (if e[5] > 0 then 0.5 else -0.5) else coord + (if e[5] > 0 then -0.5 else 0.5)
		for _, s in ipairs(gapsOn(axis, wallCoord, lo, hi)) do
			local len, mid = s[2] - s[1], (s[1] + s[2]) / 2
			if len > 1 then
				local inward = 0.15 * e[5] * (if axis == "z" then -1 else 1)
				if axis == "z" then
					part("Skirting", Vector3.new(len, 0.7, 0.3), CFrame.new(mid, 0.55, coord + inward), DARK, Enum.Material.Metal, R)
					part("WallLine", Vector3.new(len, 0.15, 0.32), CFrame.new(mid, 3.2, coord + inward), CYAN, Enum.Material.Neon, R)
				else
					part("Skirting", Vector3.new(0.3, 0.7, len), CFrame.new(coord + inward, 0.55, mid), DARK, Enum.Material.Metal, R)
					part("WallLine", Vector3.new(0.32, 0.15, len), CFrame.new(coord + inward, 3.2, mid), CYAN, Enum.Material.Neon, R)
				end
			end
		end
	end

	local fl = F.Floors:FindFirstChild(name .. "_Floor")
	if fl then fl.Material = Enum.Material.Metal; fl.MaterialVariant = "PZ_FloorPanel"; fl.Color = Color3.fromRGB(190, 195, 205) end
end

-- door frames on both faces of every door (R04's two doors already have the R04 frames on their room side)
local Frames = Instance.new("Folder"); Frames.Name = "DoorFrames"; Frames.Parent = OUT
for _, dp in ipairs(doorParts) do
	local p, s = dp.Position, dp.Size
	local alongX = s.X > s.Z -- the door spans X (in a wall along X)
	local width, height = (if alongX then s.X else s.Z), s.Y
	local base = p.Y - height / 2
	-- doors in the 2-thick exterior walls need the frame further out, or it ends up inside the wall
	local exterior = (alongX and (math.abs(p.Z) < 1.5 or math.abs(p.Z + 120) < 1.5)) or (not alongX and math.abs(math.abs(p.X) - 52) < 1.5)
	for _, face in ipairs({ -1, 1 }) do
		local off = face * (if exterior then 1.35 else 0.9)
		-- R04's side of D02 / D03 already has the R04 art-pass frame
		if (dp.Name == "D02" and face == -1) or (dp.Name == "D03" and face == 1) then continue end
		for _, side in ipairs({ -1, 1 }) do
			local along = side * (width / 2 + 0.6)
			local cf = if alongX then CFrame.new(p.X + along, base + (height + 0.6) / 2, p.Z + off) else CFrame.new(p.X + off, base + (height + 0.6) / 2, p.Z + along)
			part(dp.Name .. "_Jamb", if alongX then Vector3.new(1.2, height + 0.6, 0.6) else Vector3.new(0.6, height + 0.6, 1.2), cf, GUN, Enum.Material.Metal, Frames, true)
		end
		local hcf = if alongX then CFrame.new(p.X, base + height + 0.6, p.Z + off) else CFrame.new(p.X + off, base + height + 0.6, p.Z)
		part(dp.Name .. "_Head", if alongX then Vector3.new(width + 2.4, 1, 0.6) else Vector3.new(0.6, 1, width + 2.4), hcf, GUN, Enum.Material.Metal, Frames, true)
		local scf = if alongX then CFrame.new(p.X, base + height + 0.6, p.Z + off + face * 0.32) else CFrame.new(p.X + off + face * 0.32, base + height + 0.6, p.Z)
		local st = part(dp.Name .. "_Status", if alongX then Vector3.new(2, 0.25, 0.1) else Vector3.new(0.1, 0.25, 2), scf, CYAN, Enum.Material.Neon, Frames)
		CollectionService:AddTag(st, "PZ_FacilityNeon")
	end
end

-- walls (all, outside R04 too) and the roof underside
local walls = 0
for _, w in ipairs(F.Walls:GetChildren()) do
	if w:IsA("BasePart") and w.MaterialVariant ~= "PZ_WallPanel" then
		w.Material = Enum.Material.Metal; w.MaterialVariant = "PZ_WallPanel"; w.Color = Color3.fromRGB(205, 210, 218)
		walls += 1
	end
end
for _, rf in ipairs(F.Roof:GetChildren()) do
	if rf:IsA("BasePart") then rf.Material = Enum.Material.Metal; rf.MaterialVariant = "PZ_WallPanel"; rf.Color = Color3.fromRGB(70, 76, 86) end
end

OUT.Parent = root
local n = 0; for _, x in ipairs(OUT:GetDescendants()) do if x:IsA("BasePart") then n += 1 end end
return ("rooms art pass: %d parts, %d light panels, %d walls retextured"):format(n, panels, walls)
