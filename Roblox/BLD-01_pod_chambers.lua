-- PZ pod chambers: places two copies of the owner's Robot Containment Chamber in R04 and builds pods P01-P08
-- from them. Run in Studio (Edit) AFTER BLD-01_greybox_build.lua, with two inserted copies of the chamber asset
-- in Workspace named PZ_PodChamber_W and PZ_PodChamber_E.
--
-- Facility frame (pz_layout.py): x across (west -52 .. east +52), y depth (front 0 .. rear 120), h up.
-- Studio mapping: X = x, Y = h, Z = -y. R04 spans x -32..32, y 24..104 (widened 2026-11-23 for these chambers).
-- Chamber model frame (Roblox/../Roblox_Import/PZ_PodChamber_report.json): X = length, Y = depth (+Y = open
-- side), origin at floor centre. Pods are at (cx, cy) in that frame, platform tops at platform_z.
-- West chamber: back against the west wall, open side facing +x; its pods are P01..P04 from front to rear.
-- East chamber: mirrored; pods P05..P08 from front to rear. Pod roles as approved 2026-11-19.
local CS = game:GetService("CollectionService")
local CHS = game:GetService("ChangeHistoryService")

-- from PZ_PodChamber_report.json (pz_room_prep.py, 2026-11-23) -------------------------------------------
local REPORT = {
	size = Vector3.new(49.5, 25.53, 16.85), -- length (X), depth (Y), height
	pods = { -- chamber-frame centre x, y and platform top, ordered by x
		{ cx = -14.3, cy = -1.45, platform = 2.63 },
		{ cx = -5.0, cy = -1.45, platform = 2.71 },
		{ cx = 5.05, cy = -1.45, platform = 2.71 },
		{ cx = 14.3, cy = -1.45, platform = 2.71 },
	},
	glassRadius = 2.47,
}
local FLOOR = 0.2              -- top of the R04 floor slab
local WALL_INNER = 31.5        -- inner face of the R04 side walls (walls are 1 stud thick at x = +-32)
local CENTRE_Y = 64            -- R04 runs y 24..104
local GLASS_TRANSPARENCY = 0.45 -- the model's glass panels (decoration)
local FIELD_H = 7.8             -- stasis field height above the platform (measured glass height)
local ROLES = { P01 = "Cypher (NPC guide, opens first)", P02 = "Player pod 1", P03 = "Player pod 2", P04 = "Player pod 3",
	P05 = "Sentinel (trapped, rescue)", P06 = "Player pod 4", P07 = "Dormant (amber visor)", P08 = "Dormant (amber visor)" }
local CYAN, AMBER = Color3.fromHex("#22D3EE"), Color3.fromHex("#FFB020")

local function F(x, y, h) return Vector3.new(x, h, -y) end -- facility -> Studio

local function worldAABB(m)
	local mn, mx = Vector3.new(math.huge, math.huge, math.huge), Vector3.new(-math.huge, -math.huge, -math.huge)
	for _, d in ipairs(m:GetDescendants()) do
		if d:IsA("MeshPart") then
			local h = d.Size / 2
			for _, sx in ipairs({ -1, 1 }) do for _, sy in ipairs({ -1, 1 }) do for _, sz in ipairs({ -1, 1 }) do
				local w = d.CFrame:PointToWorldSpace(Vector3.new(h.X * sx, h.Y * sy, h.Z * sz)); mn = mn:Min(w); mx = mx:Max(w)
			end end end
		end
	end
	return mn, mx
end

-- Imports arrive at an arbitrary yaw. With MeshPart yaw = 180 deg the model frame maps (x, y, h) -> Studio
-- (x, h, -y) (same as the vehicles, see vehicle_crew_layer.lua); then turn it by `extraYaw` about its centre.
local function place(m, centreXZ, extraYaw)
	for _, d in ipairs(m:GetDescendants()) do if d:IsA("BasePart") then d.Anchored = true end end
	local _, yaw = m:FindFirstChildWhichIsA("MeshPart", true).CFrame:ToOrientation()
	local mn, mx = worldAABB(m); local c = (mn + mx) / 2
	m:PivotTo(CFrame.new(c) * CFrame.Angles(0, math.rad(180) - yaw + extraYaw, 0) * CFrame.new(-c) * m:GetPivot())
	mn, mx = worldAABB(m); c = (mn + mx) / 2
	m:PivotTo(m:GetPivot() + Vector3.new(centreXZ.X - c.X, FLOOR - mn.Y, centreXZ.Z - c.Z))
end

local facility = workspace:FindFirstChild("PZ_StasisFacility")
assert(facility, "run BLD-01_greybox_build.lua first")
local podsFolder = facility:FindFirstChild("Pods", true)
assert(podsFolder, "PZ_StasisFacility has no Pods folder")
podsFolder:ClearAllChildren()

local rec = CHS:TryBeginRecording("Place pod chambers")
local half = REPORT.size.Y / 2
local SIDES = {
	-- name, chamber centre x, extra yaw, facing (+1 = toward +x), pod ids by chamber order (pods[1]..pods[4])
	{ name = "PZ_PodChamber_W", cx = -WALL_INNER + half, yaw = math.rad(-90), facing = 1, ids = { "P04", "P03", "P02", "P01" } },
	{ name = "PZ_PodChamber_E", cx = WALL_INNER - half, yaw = math.rad(90), facing = -1, ids = { "P05", "P06", "P07", "P08" } },
}
local out = {}
for _, side in ipairs(SIDES) do
	local m = workspace:FindFirstChild(side.name)
	assert(m, "insert the chamber asset twice and name the copies PZ_PodChamber_W / PZ_PodChamber_E")
	place(m, F(side.cx, CENTRE_Y, 0), side.yaw)
	m.Parent = facility
	for _, d in ipairs(m:GetDescendants()) do
		if d:IsA("MeshPart") and not d.Name:find("Glass") then
			d.CanCollide = true
			d.CollisionFidelity = Enum.CollisionFidelity.PreciseConvexDecomposition
		end
	end
	-- pods: chamber frame (px, py) -> facility: west (x, y) = (cx + py, 64 - px); east = (cx - py, 64 + px)
	for k, p in ipairs(REPORT.pods) do
		local id = side.ids[k]
		local fx = side.cx + side.facing * p.cy
		local fy = CENTRE_Y - side.facing * p.cx
		local pod = Instance.new("Model"); pod.Name = id
		pod:SetAttribute("Role", ROLES[id]); pod:SetAttribute("State", "Stasis"); pod:SetAttribute("Chamber", side.name)
		-- The model's pod glass is a panel at the BACK of each bay (the round platform stands in front of it, open
		-- to the aisle), so it stays as decoration ("GlassPanel"). The pod is closed by a stasis field: a cyan
		-- ForceField cylinder on the platform ("Glass", which StasisService fades out on activation).
		local panel = m:FindFirstChild(("PZ_PodChamber_GlassP%d"):format(k), true)
		assert(panel, "missing glass piece " .. k .. " in " .. side.name)
		panel.Name = "GlassPanel"; panel.Transparency = GLASS_TRANSPARENCY; panel.CastShadow = false
		panel.CanCollide = true; panel.CollisionFidelity = Enum.CollisionFidelity.Hull
		panel.Parent = pod
		local top = FLOOR + p.platform
		local field = Instance.new("Part"); field.Name = "Glass"; field.Shape = Enum.PartType.Cylinder
		field.Anchored = true; field.CanCollide = true; field.CastShadow = false
		field.Material = Enum.Material.ForceField; field.Color = CYAN; field.Transparency = 0
		field.Size = Vector3.new(FIELD_H, 2 * REPORT.glassRadius, 2 * REPORT.glassRadius)
		field.CFrame = CFrame.new(F(fx, fy, top + FIELD_H / 2)) * CFrame.Angles(0, 0, math.rad(90))
		field:SetAttribute("Kind", "StasisField")
		field.Parent = pod
		local glass = panel
		local plinth = Instance.new("Part"); plinth.Name = "Plinth"; plinth.Anchored = true
		plinth.Size = Vector3.new(4, top, 4); plinth.CFrame = CFrame.new(F(fx, fy, top / 2))
		plinth.Transparency = 1; plinth.CanCollide = true; plinth.CastShadow = false; plinth.Parent = pod
		CS:AddTag(plinth, "PZ_Prompt_Pod")
		local band = Instance.new("Part"); band.Name = "StatusBand"; band.Anchored = true; band.CanCollide = false
		band.Material = Enum.Material.Neon; band.Color = (id == "P07" or id == "P08") and AMBER or CYAN
		band.Size = Vector3.new(0.3, 0.3, 2.4)
		band.CFrame = CFrame.new(F(fx + side.facing * (REPORT.glassRadius + 0.4), fy, top - 0.15))
		band.Parent = pod
		pod.Parent = podsFolder
		local g = glass.Position
		table.insert(out, string.format("%s at x %.1f y %.1f (glass centre %.1f, %.1f) platform %.2f", id, fx, fy, g.X, -g.Z, top))
	end
end
if rec then CHS:FinishRecording(rec, Enum.FinishRecordingOperation.Commit) end
return table.concat(out, "\n")
