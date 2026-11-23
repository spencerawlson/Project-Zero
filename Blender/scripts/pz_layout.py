"""PZ_STA_StasisFacility — single source of truth for layout.

ALL DIMENSIONS ARE DESIGN ASSUMPTIONS IN ROBLOX STUDS (1 Blender unit = 1 stud).
They are NOT measurements extracted from concept art. Targets derive from the
Asset Reference Bible (120 x 85 x 32 studs), adjusted to 120 x 88 so the plan
snaps to the NEXUS-01 8-stud modular grid.

Axes: X = width (west -44 .. east +44), Y = depth (front/south 0 .. rear/north 120),
Z = up. Main entrance faces -Y (front elevation).
"""

GRID = 8
W, D = 88, 120              # footprint
X0, X1 = -44, 44
Y0, Y1 = 0, 120
WALL = 1.0                  # interior wall thickness
EXT_WALL = 2.0              # exterior wall thickness

# Volumes: (name, x0, x1, y0, y1, roof_height)
VOLUMES = [
    ("Front block",   -44, 44,   0,  24, 20),
    ("West wing",     -44, -24, 24, 104, 18),
    ("East wing",      24, 44,  24, 104, 18),
    ("Rear block",    -44, 44, 104, 120, 22),
]
CHAMBER = dict(x0=-24, x1=24, y0=24, y1=104, spring=18, crown=32)  # barrel vault
RIB_STEP = 8

# Rooms: id, label, x0, x1, y0, y1, colour key
ROOMS = [
    ("R01", "RECEPTION & SECURITY",    -24, 24,   0,  24, "civic"),
    ("R02", "SECURITY OFFICE",         -44, -24,  0,  24, "security"),
    ("R03", "STAFF / DECON LOCKERS",    24, 44,   0,  24, "support"),
    ("R04", "STASIS POD CHAMBER",      -24, 24,  24, 104, "chamber"),
    ("R05", "MAINTENANCE CORRIDOR",    -32, -24, 24, 104, "service"),
    ("R06", "CRYOGENIC PLANT",         -44, -32, 24,  72, "plant"),
    ("R07", "EMERGENCY EXIT (W)",      -44, -32, 72,  88, "egress"),
    ("R08", "SPARES STORE",            -44, -32, 88, 104, "support"),
    ("R09", "MEDICAL MONITORING",       24, 44,  24,  60, "medical"),
    ("R10", "ENERGY CONTROL ROOM",      24, 44,  60,  96, "energy"),
    ("R11", "EMERGENCY EXIT (E)",       24, 44,  96, 120, "egress"),
    ("R12", "SERVICE ACCESS BAY",      -24, 24, 104, 120, "service"),
    ("R13", "SERVICE STAIR / RISER",   -44, -24, 104, 120, "service"),
]

# Doors: id, label, wall axis ('x' = wall runs along X at y, 'y' = wall runs along Y at x),
#        position (centre along wall), fixed coord, width, height, kind
DOORS = [
    ("D01", "Main entrance (octagonal portal)", "x", 0,   0,   12, 14, "main"),
    ("D02", "Security airlock",                 "x", 0,   24,  10, 12, "blast"),
    ("D03", "Containment door (octagonal)",     "x", 0,   104, 12, 14, "blast"),
    ("D04", "Service roll-up door",             "x", 0,   120, 16, 14, "rollup"),
    ("D05", "Emergency exit W",                 "y", 80,  -44, 6,  10, "egress"),
    ("D06", "Emergency exit E",                 "y", 112, 44,  6,  10, "egress"),
    ("D07", "Security office",                  "y", 12,  -24, 6,  10, "std"),
    ("D08", "Lockers",                          "y", 12,  24,  6,  10, "std"),
    ("D09", "Medical monitoring",               "y", 30,  24,  6,  10, "std"),
    ("D10", "Energy control",                   "y", 90,  24,  6,  10, "std"),
    ("D11", "Maint. corridor N",                "x", -28, 104, 6,  10, "std"),
    ("D12", "Cryo plant",                       "y", 48,  -32, 6,  10, "std"),
    ("D13", "Exit W vestibule",                 "y", 80,  -32, 6,  10, "std"),
    ("D14", "Spares store",                     "y", 96,  -32, 6,  10, "std"),
    ("D15", "Exit E vestibule",                 "x", 34,  96,  6,  10, "std"),
    ("D16", "Service stair",                    "y", 112, -24, 6,  10, "std"),
    ("D17", "Maint. corridor S hatch",          "x", -28, 24,  6,  10, "std"),
    ("D18", "Medical -> energy",                "x", 34,  60,  6,  10, "std"),
]

# Stasis pods: 8 bays, 4 per side, facing aisle.
POD_X = 17
POD_YS = [40, 54, 68, 82]
PODS = [(f"P{i+1:02d}", -POD_X if i < 4 else POD_X, POD_YS[i % 4], "E" if i < 4 else "W")
        for i in range(8)]
AISLE_HALF = 6              # 12-stud centre aisle
MEZZANINE = dict(y0=24, y1=32, z=12)
CRANE = dict(rail_x=14, z=25, bridge_y=60)
OBS_WINDOW = dict(x=24, y0=34, y1=56, z0=4, z1=10)

# Pod dimensions (SF-04)
POD = dict(
    plinth_d=9.0, plinth_h=2.5,
    glass_d=6.4, glass_h=8.5,
    cap_d=8.0, cap_h=2.5,
    total_h=2.5 + 8.5 + 2.5 + 1.0,    # + top housing = 14.5
    footprint=(10, 10),
)

PALETTE = {
    "graphite":   "#2B2F36",
    "panel_dark": "#1C1F24",
    "steel":      "#8A9099",
    "concrete":   "#5A5E63",
    "floor":      "#3A3F46",
    "orange":     "#E8731A",
    "amber":      "#FFB020",
    "cyan":       "#22D3EE",
    "blue":       "#1E88E5",
    "red":        "#E5383B",
    "glass":      "#9FE8F5",
}

ROOM_COLOURS = {
    "civic": "#3B4654", "security": "#4A2E33", "support": "#3A3F46",
    "chamber": "#173847", "service": "#3D3A2E", "plant": "#1F3A4A",
    "egress": "#2E4A33", "medical": "#24404A", "energy": "#2A3550",
}

# Canonical robot family (user-owned Meshy models; never modified, only instanced + uniformly scaled).
# Heights in studs are DESIGN ASSUMPTIONS for in-game scale (Meshy export heights are normalised).
ROBOTS = {
    "Cypher":   dict(file="Rigged_Cypher.glb",   height=6.0, role="Intelligence / exploration"),
    "Sentinel": dict(file="Rigged_Sentinel.glb", height=7.5, role="Security / protection"),
    "Patch":    dict(file="Patch_LowPoly.glb",   height=4.5, role="Engineering / repair"),
}
ROBOT_SRC_DIR = r"D:\Project Zero_Roblox"
# Pod roles (approved 2026-11-19): each player wakes in their own pod as their custom robot;
# Cypher (NPC) wakes first in P01 and guides them; Sentinel is trapped in P05 (rescue objective);
# P07–P08 hold dormant memory-wiped family robots (amber visor). Player pods are assigned by the server.
POD_ROLES = {"P01": "Cypher (NPC guide, opens first)", "P02": "Player pod 1", "P03": "Player pod 2",
             "P04": "Player pod 3", "P05": "Sentinel (trapped, rescue)", "P06": "Player pod 4",
             "P07": "Dormant (amber visor)", "P08": "Dormant (amber visor)"}
# Render occupants: player pods show example frames (Patch/Sentinel/Cypher) — the live game swaps in each player's robot.
# Other pods hold memory-wiped family robots; the canonical models stand in until NPC variants exist.
POD_OCCUPANTS = {"P01": "Cypher", "P02": "Patch", "P03": "Sentinel", "P04": "Cypher",
                 "P05": "Sentinel", "P06": "Patch", "P07": "Cypher", "P08": "Sentinel"}
