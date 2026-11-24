-- PZ_StasisFacility greybox builder (run in Roblox Studio command bar or via MCP execute_luau, Edit mode).
-- Data mirrors Blender/scripts/pz_layout.py (single source of truth) — keep both in sync.
-- All dimensions are design assumptions in studs.
-- Mapping (pz_layout -> Studio): X = x, Y = height, Z = -y  (Blender -> glTF convention; entrance D01 faces +Z)
-- Rebuilds Workspace.PZ_StasisFacility from scratch; leaves robots and other models alone.
local CHS = game:GetService("ChangeHistoryService")
local CS = game:GetService("CollectionService")
local rec = CHS:TryBeginRecording("Build PZ_StasisFacility greybox")

local old = workspace:FindFirstChild("PZ_StasisFacility")
if old then old:Destroy() end

local function hex(h) return Color3.fromHex(h) end
local PAL = {graphite=hex("#2B2F36"), panel=hex("#1C1F24"), steel=hex("#8A9099"), concrete=hex("#5A5E63"),
  floor=hex("#3A3F46"), orange=hex("#E8731A"), amber=hex("#FFB020"), cyan=hex("#22D3EE"), red=hex("#E5383B"),
  glass=hex("#9FE8F5"), green=hex("#3DBB6B")}
local ROOMCOL = {civic="#3B4654", security="#4A2E33", support="#3A3F46", chamber="#173847", service="#3D3A2E",
  plant="#1F3A4A", egress="#2E4A33", medical="#24404A", energy="#2A3550"}

local function P(x, y, h) return Vector3.new(x, h, -y) end
local function part(parent, name, size, cf, color, mat, extra)
  local p = Instance.new("Part")
  p.Name = name; p.Anchored = true; p.Size = size; p.CFrame = cf
  p.Color = color; p.Material = mat or Enum.Material.SmoothPlastic
  p.TopSurface = Enum.SurfaceType.Smooth; p.BottomSurface = Enum.SurfaceType.Smooth
  if extra then for k, v in pairs(extra) do p[k] = v end end
  p.Parent = parent
  return p
end
local function box(parent, name, x0, x1, y0, y1, h0, h1, color, mat, extra)
  return part(parent, name, Vector3.new(x1 - x0, h1 - h0, y1 - y0),
    CFrame.new(P((x0 + x1) / 2, (y0 + y1) / 2, (h0 + h1) / 2)), color, mat, extra)
end

local root = Instance.new("Model"); root.Name = "PZ_StasisFacility"
root:SetAttribute("Source", "pz_layout.py (Project_Zero_Production_Bible)")
root:SetAttribute("Status", "Greybox - design assumptions in studs")
local function folder(name) local f = Instance.new("Folder"); f.Name = name; f.Parent = root; return f end
local F = {floors=folder("Floors"), walls=folder("Walls"), roof=folder("Roof"), vault=folder("Vault"),
  chamber=folder("Chamber"), pods=folder("Pods"), doors=folder("Doors"), labels=folder("Labels")}

-- rooms -------------------------------------------------------------------------
local ROOMS = {
  {"R01","RECEPTION & SECURITY",-32,32,0,24,"civic"}, {"R02","SECURITY OFFICE",-52,-32,0,24,"security"},
  {"R03","STAFF / DECON LOCKERS",32,52,0,24,"support"}, {"R04","STASIS POD CHAMBER",-32,32,24,104,"chamber"},
  {"R05","MAINTENANCE CORRIDOR",-40,-32,24,104,"service"}, {"R06","CRYOGENIC PLANT",-52,-40,24,72,"plant"},
  {"R07","EMERGENCY EXIT (W)",-52,-40,72,88,"egress"}, {"R08","SPARES STORE",-52,-40,88,104,"support"},
  {"R09","MEDICAL MONITORING",32,52,24,60,"medical"}, {"R10","ENERGY CONTROL ROOM",32,52,60,96,"energy"},
  {"R11","EMERGENCY EXIT (E)",32,52,96,120,"egress"}, {"R12","SERVICE ACCESS BAY",-32,32,104,120,"service"},
  {"R13","SERVICE STAIR / RISER",-52,-32,104,120,"service"},
}
for _, r in ipairs(ROOMS) do
  local f = box(F.floors, r[1] .. "_Floor", r[3], r[4], r[5], r[6], 0, 0.2, hex(ROOMCOL[r[7]]), Enum.Material.Concrete)
  f:SetAttribute("RoomId", r[1]); f:SetAttribute("RoomName", r[2])
  local a = box(F.labels, r[1] .. "_Label", (r[3]+r[4])/2 - 0.5, (r[3]+r[4])/2 + 0.5, (r[5]+r[6])/2 - 0.5, (r[5]+r[6])/2 + 0.5, 7, 8,
    PAL.steel, nil, {Transparency=1, CanCollide=false, CanQuery=false, CanTouch=false, CastShadow=false})
  local g = Instance.new("BillboardGui"); g.Size = UDim2.new(12, 0, 1.4, 0); g.LightInfluence = 0; g.MaxDistance = 140
  local t = Instance.new("TextLabel"); t.Size = UDim2.fromScale(1, 1); t.BackgroundColor3 = PAL.panel; t.BackgroundTransparency = 0.25
  t.TextColor3 = PAL.cyan; t.Font = Enum.Font.GothamBold; t.TextScaled = true; t.Text = r[1] .. "  " .. r[2]; t.Parent = g
  g.Parent = a
end

-- doors & openings (id, label, wall axis, centre along wall, fixed coord, width, height, kind) ---------
local DOORS = {
  {"D01","Main entrance (octagonal portal)","x",0,0,12,14,"main"}, {"D02","Security airlock","x",0,24,10,12,"blast"},
  {"D03","Containment door (octagonal)","x",0,104,12,14,"blast"}, {"D04","Service roll-up door","x",0,120,16,14,"rollup"},
  {"D05","Emergency exit W","y",80,-52,6,10,"egress"}, {"D06","Emergency exit E","y",112,52,6,10,"egress"},
  {"D07","Security office","y",12,-32,6,10,"std"}, {"D08","Lockers","y",12,32,6,10,"std"},
  {"D09","Medical monitoring","y",30,32,6,10,"std"}, {"D10","Energy control","y",90,32,6,10,"std"},
  {"D11","Maint. corridor N","x",-36,104,6,10,"std"}, {"D12","Cryo plant","y",48,-40,6,10,"std"},
  {"D13","Exit W vestibule","y",80,-40,6,10,"std"}, {"D14","Spares store","y",96,-40,6,10,"std"},
  {"D15","Exit E vestibule","x",42,96,6,10,"std"}, {"D16","Service stair","y",112,-32,6,10,"std"},
  {"D17","Maint. corridor S hatch","x",-36,24,6,10,"std"}, {"D18","Medical -> energy","x",42,60,6,10,"std"},
}
local KINDCOL = {main=PAL.orange, blast=PAL.red, rollup=PAL.amber, egress=PAL.green, std=PAL.steel}
local OPENINGS = {}
local function addOpening(axis, fixed, c, w, b, t)
  local k = axis .. "|" .. fixed
  OPENINGS[k] = OPENINGS[k] or {}
  table.insert(OPENINGS[k], {c=c, w=w, b=b, t=t})
end
for _, d in ipairs(DOORS) do
  local id, label, axis, c, fixed, w, h, kind = table.unpack(d)
  addOpening(axis, fixed, c, w, 0, h)
  local thick = (kind == "std") and 0.4 or 0.8
  local p
  if axis == "x" then p = box(F.doors, id, c - w/2, c + w/2, fixed - thick/2, fixed + thick/2, 0.2, h, KINDCOL[kind])
  else p = box(F.doors, id, fixed - thick/2, fixed + thick/2, c - w/2, c + w/2, 0.2, h, KINDCOL[kind]) end
  p.Transparency = 0.7; p.CanCollide = false; p.CastShadow = false; p.Material = Enum.Material.ForceField
  p:SetAttribute("DoorId", id); p:SetAttribute("Label", label); p:SetAttribute("Kind", kind)
  p:SetAttribute("Width", w); p:SetAttribute("Height", h); p:SetAttribute("NeverLocks", kind == "egress")
  CS:AddTag(p, kind == "egress" and "PZ_Door_Failsafe" or "PZ_Door_Auto")
end
addOpening("y", 32, 45, 22, 4, 10) -- observation window: chamber -> medical monitoring
box(F.chamber, "ObservationWindow", 31.8, 32.2, 34, 56, 4, 10, PAL.glass, Enum.Material.Glass, {Transparency=0.55})

-- walls (axis, fixed, a0, a1, height, thickness, exterior) ------------------------
local RUNS = {
  {"x",0,-52,52,20,2,true}, {"x",120,-52,52,22,2,true},
  {"y",-52,0,24,20,2,true}, {"y",-52,24,104,18,2,true}, {"y",-52,104,120,22,2,true},
  {"y",52,0,24,20,2,true}, {"y",52,24,104,18,2,true}, {"y",52,104,120,22,2,true},
  {"x",24,-52,52,20,1}, {"x",104,-52,32,22,1}, {"x",72,-52,-40,18,1}, {"x",88,-52,-40,18,1},
  {"x",60,32,52,18,1}, {"x",96,32,52,18,1},
  {"y",-32,0,24,20,1}, {"y",-32,24,104,18,1}, {"y",-32,104,120,22,1},
  {"y",32,0,24,20,1}, {"y",32,24,104,18,1}, {"y",32,104,120,22,1}, {"y",-40,24,104,18,1},
}
local nWall = 0
for i, r in ipairs(RUNS) do
  local axis, fixed, a0, a1, height, th, ext = table.unpack(r)
  local col = ext and PAL.graphite or PAL.concrete
  local name = string.format("%s_%s%d_%d", ext and "Ext" or "Int", axis == "x" and "Y" or "X", fixed, i)
  local ops = {}
  for _, o in ipairs(OPENINGS[axis .. "|" .. fixed] or {}) do
    if o.c > a0 and o.c < a1 then table.insert(ops, o) end
  end
  table.sort(ops, function(p, q) return p.c < q.c end)
  local function seg(s0, s1, h0, h1, suffix)
    if s1 - s0 < 0.05 or h1 - h0 < 0.05 then return end
    nWall += 1
    if axis == "x" then box(F.walls, name .. suffix, s0, s1, fixed - th/2, fixed + th/2, h0, h1, col, Enum.Material.Concrete)
    else box(F.walls, name .. suffix, fixed - th/2, fixed + th/2, s0, s1, h0, h1, col, Enum.Material.Concrete) end
  end
  local cur = a0
  for k, o in ipairs(ops) do
    local o0, o1 = o.c - o.w/2, o.c + o.w/2
    seg(cur, o0, 0, height, "_" .. k)
    seg(o0, o1, 0, o.b, "_" .. k .. "Sill")
    seg(o0, o1, o.t, height, "_" .. k .. "Lintel")
    cur = o1
  end
  seg(cur, a1, 0, height, "_End")
end

-- roofs (separate folder so it can be hidden to look inside) -------------------
box(F.roof, "Roof_FrontBlock", -52, 52, 0, 24, 20, 21, PAL.graphite, Enum.Material.Metal)
box(F.roof, "Roof_WestWing", -52, -32, 24, 104, 18, 19, PAL.graphite, Enum.Material.Metal)
box(F.roof, "Roof_EastWing", 32, 52, 24, 104, 18, 19, PAL.graphite, Enum.Material.Metal)
box(F.roof, "Roof_RearBlock", -52, 52, 104, 120, 22, 23, PAL.graphite, Enum.Material.Metal)

-- barrel vault over the chamber: half-span 32, spring 18, crown 32 --------------
local N = 12
local function arc(t) return 32 * math.cos(t), 18 + 14 * math.sin(t) end
for i = 0, N - 1 do
  local xa, ha = arc(math.pi * i / N); local xb, hb = arc(math.pi * (i + 1) / N)
  local len = math.sqrt((xb - xa)^2 + (hb - ha)^2)
  local ang = math.atan2(hb - ha, xb - xa)
  local mid = CFrame.new(P((xa + xb)/2, 64, (ha + hb)/2)) * CFrame.Angles(0, 0, ang)
  part(F.vault, "VaultSkin_" .. i, Vector3.new(len + 0.3, 0.8, 80), mid, PAL.graphite, Enum.Material.Metal)
  for y = 24, 104, 8 do
    local cf = CFrame.new(P((xa + xb)/2, y, (ha + hb)/2)) * CFrame.Angles(0, 0, ang) * CFrame.new(0, -0.8, 0)
    part(F.vault, string.format("Rib_y%d_%d", y, i), Vector3.new(len + 0.3, 1.2, 0.8), cf, PAL.steel, Enum.Material.Metal)
  end
end
for _, y in ipairs({24, 104}) do -- gable infill above the 18-stud spring line
  for s = 0, 15 do
    local x0 = -32 + s * 4; local xc = x0 + 2
    local top = 18 + 14 * math.sqrt(math.max(0, 1 - (xc / 32)^2))
    box(F.vault, string.format("Gable_y%d_%d", y, s), x0, x0 + 4, y - 0.5, y + 0.5, 18, top, PAL.concrete, Enum.Material.Concrete)
  end
end

-- chamber fit-out: aisle, mezzanine, crane ---------------------------------------
for _, s in ipairs({-1, 1}) do
  box(F.chamber, "AisleGuide_" .. (s < 0 and "W" or "E"), s * 6 - 0.2, s * 6 + 0.2, 26, 102, 0.2, 0.3, PAL.cyan, Enum.Material.Neon)
  box(F.chamber, "CraneRail_" .. (s < 0 and "W" or "E"), s * 14 - 0.5, s * 14 + 0.5, 24, 104, 24.5, 25.5, PAL.amber, Enum.Material.Metal)
end
box(F.chamber, "CraneBridge", -14.5, 14.5, 59, 61, 23.5, 24.5, PAL.amber, Enum.Material.Metal)
box(F.chamber, "Mezzanine_Deck", -32, 32, 24, 32, 11, 12, PAL.steel, Enum.Material.DiamondPlate)
box(F.chamber, "Mezzanine_Rail", -32, 32, 31.8, 32.1, 12, 13.1, PAL.orange, Enum.Material.Metal)

-- stasis pods: built by Roblox/BLD-01_pod_chambers.lua from the owner's Robot Containment Chamber model
-- (two chambers, four pods each, facing the aisle). This script only provides the Pods folder.

root.WorldPivot = CFrame.new(0, 0, 0)
root.Parent = workspace

local spawn = workspace:FindFirstChild("SpawnLocation")
if spawn then spawn.CFrame = CFrame.new(0, 0.5, 30) end

if rec then CHS:FinishRecording(rec, Enum.FinishRecordingOperation.Commit) end

local count = 0
for _, d in ipairs(root:GetDescendants()) do if d:IsA("BasePart") then count += 1 end end
return string.format("Built PZ_StasisFacility: %d parts (%d wall pieces), %d doors, %d rooms (pods: run BLD-01_pod_chambers.lua)", count, nWall, #DOORS, #ROOMS)
