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
  {"R01","RECEPTION & SECURITY",-24,24,0,24,"civic"}, {"R02","SECURITY OFFICE",-44,-24,0,24,"security"},
  {"R03","STAFF / DECON LOCKERS",24,44,0,24,"support"}, {"R04","STASIS POD CHAMBER",-24,24,24,104,"chamber"},
  {"R05","MAINTENANCE CORRIDOR",-32,-24,24,104,"service"}, {"R06","CRYOGENIC PLANT",-44,-32,24,72,"plant"},
  {"R07","EMERGENCY EXIT (W)",-44,-32,72,88,"egress"}, {"R08","SPARES STORE",-44,-32,88,104,"support"},
  {"R09","MEDICAL MONITORING",24,44,24,60,"medical"}, {"R10","ENERGY CONTROL ROOM",24,44,60,96,"energy"},
  {"R11","EMERGENCY EXIT (E)",24,44,96,120,"egress"}, {"R12","SERVICE ACCESS BAY",-24,24,104,120,"service"},
  {"R13","SERVICE STAIR / RISER",-44,-24,104,120,"service"},
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
  {"D05","Emergency exit W","y",80,-44,6,10,"egress"}, {"D06","Emergency exit E","y",112,44,6,10,"egress"},
  {"D07","Security office","y",12,-24,6,10,"std"}, {"D08","Lockers","y",12,24,6,10,"std"},
  {"D09","Medical monitoring","y",30,24,6,10,"std"}, {"D10","Energy control","y",90,24,6,10,"std"},
  {"D11","Maint. corridor N","x",-28,104,6,10,"std"}, {"D12","Cryo plant","y",48,-32,6,10,"std"},
  {"D13","Exit W vestibule","y",80,-32,6,10,"std"}, {"D14","Spares store","y",96,-32,6,10,"std"},
  {"D15","Exit E vestibule","x",34,96,6,10,"std"}, {"D16","Service stair","y",112,-24,6,10,"std"},
  {"D17","Maint. corridor S hatch","x",-28,24,6,10,"std"}, {"D18","Medical -> energy","x",34,60,6,10,"std"},
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
addOpening("y", 24, 45, 22, 4, 10) -- observation window: chamber -> medical monitoring
box(F.chamber, "ObservationWindow", 23.8, 24.2, 34, 56, 4, 10, PAL.glass, Enum.Material.Glass, {Transparency=0.55})

-- walls (axis, fixed, a0, a1, height, thickness, exterior) ------------------------
local RUNS = {
  {"x",0,-44,44,20,2,true}, {"x",120,-44,44,22,2,true},
  {"y",-44,0,24,20,2,true}, {"y",-44,24,104,18,2,true}, {"y",-44,104,120,22,2,true},
  {"y",44,0,24,20,2,true}, {"y",44,24,104,18,2,true}, {"y",44,104,120,22,2,true},
  {"x",24,-44,44,20,1}, {"x",104,-44,24,22,1}, {"x",72,-44,-32,18,1}, {"x",88,-44,-32,18,1},
  {"x",60,24,44,18,1}, {"x",96,24,44,18,1},
  {"y",-24,0,24,20,1}, {"y",-24,24,104,18,1}, {"y",-24,104,120,22,1},
  {"y",24,0,24,20,1}, {"y",24,24,104,18,1}, {"y",24,104,120,22,1}, {"y",-32,24,104,18,1},
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
box(F.roof, "Roof_FrontBlock", -44, 44, 0, 24, 20, 21, PAL.graphite, Enum.Material.Metal)
box(F.roof, "Roof_WestWing", -44, -24, 24, 104, 18, 19, PAL.graphite, Enum.Material.Metal)
box(F.roof, "Roof_EastWing", 24, 44, 24, 104, 18, 19, PAL.graphite, Enum.Material.Metal)
box(F.roof, "Roof_RearBlock", -44, 44, 104, 120, 22, 23, PAL.graphite, Enum.Material.Metal)

-- barrel vault over the chamber: half-span 24, spring 18, crown 32 --------------
local N = 12
local function arc(t) return 24 * math.cos(t), 18 + 14 * math.sin(t) end
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
  for s = 0, 11 do
    local x0 = -24 + s * 4; local xc = x0 + 2
    local top = 18 + 14 * math.sqrt(math.max(0, 1 - (xc / 24)^2))
    box(F.vault, string.format("Gable_y%d_%d", y, s), x0, x0 + 4, y - 0.5, y + 0.5, 18, top, PAL.concrete, Enum.Material.Concrete)
  end
end

-- chamber fit-out: aisle, mezzanine, crane ---------------------------------------
for _, s in ipairs({-1, 1}) do
  box(F.chamber, "AisleGuide_" .. (s < 0 and "W" or "E"), s * 6 - 0.2, s * 6 + 0.2, 26, 102, 0.2, 0.3, PAL.cyan, Enum.Material.Neon)
  box(F.chamber, "CraneRail_" .. (s < 0 and "W" or "E"), s * 14 - 0.5, s * 14 + 0.5, 24, 104, 24.5, 25.5, PAL.amber, Enum.Material.Metal)
end
box(F.chamber, "CraneBridge", -14.5, 14.5, 59, 61, 23.5, 24.5, PAL.amber, Enum.Material.Metal)
box(F.chamber, "Mezzanine_Deck", -24, 24, 24, 32, 11, 12, PAL.steel, Enum.Material.DiamondPlate)
box(F.chamber, "Mezzanine_Rail", -24, 24, 31.8, 32.1, 12, 13.1, PAL.orange, Enum.Material.Metal)

-- stasis pods (SF-04 dimensions) -------------------------------------------------
local ROLES = {P01="Cypher (NPC guide, opens first)", P02="Player pod 1", P03="Player pod 2", P04="Player pod 3",
  P05="Sentinel (trapped, rescue)", P06="Player pod 4", P07="Dormant (amber visor)", P08="Dormant (amber visor)"}
local YS = {40, 54, 68, 82}
local function cyl(parent, name, x, y, h0, h1, d, color, mat, extra)
  return part(parent, name, Vector3.new(h1 - h0, d, d),
    CFrame.new(P(x, y, (h0 + h1) / 2)) * CFrame.Angles(0, 0, math.rad(90)), color, mat, extra)
end
for i = 1, 8 do
  local id = string.format("P%02d", i)
  local x = (i <= 4) and -17 or 17
  local y = YS[(i - 1) % 4 + 1]
  local face = (i <= 4) and 1 or -1 -- toward the aisle
  local m = Instance.new("Model"); m.Name = id
  m:SetAttribute("Role", ROLES[id]); m:SetAttribute("State", "Stasis")
  local plinth = cyl(m, "Plinth", x, y, 0.2, 2.5, 9, PAL.graphite, Enum.Material.Metal)
  CS:AddTag(plinth, "PZ_Prompt_Pod")
  cyl(m, "Glass", x, y, 2.5, 11, 6.4, PAL.glass, Enum.Material.Glass, {Transparency=0.6})
  cyl(m, "Cap", x, y, 11, 13.5, 8, PAL.graphite, Enum.Material.Metal)
  box(m, "TopHousing", x - 3, x + 3, y - 3, y + 3, 13.5, 14.5, PAL.steel, Enum.Material.Metal)
  local band = (id == "P07" or id == "P08") and PAL.amber or PAL.cyan
  box(m, "StatusBand", x + face * 4.3 - 0.2, x + face * 4.3 + 0.2, y - 1.5, y + 1.5, 1.6, 2.2, band, Enum.Material.Neon)
  m.Parent = F.pods
end

root.WorldPivot = CFrame.new(0, 0, 0)
root.Parent = workspace

local spawn = workspace:FindFirstChild("SpawnLocation")
if spawn then spawn.CFrame = CFrame.new(0, 0.5, 30) end

if rec then CHS:FinishRecording(rec, Enum.FinishRecordingOperation.Commit) end

local count = 0
for _, d in ipairs(root:GetDescendants()) do if d:IsA("BasePart") then count += 1 end end
return string.format("Built PZ_StasisFacility: %d parts (%d wall pieces), %d doors, 8 pods, %d rooms", count, nWall, #DOORS, #ROOMS)
