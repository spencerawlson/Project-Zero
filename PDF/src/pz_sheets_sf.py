"""SF-01, SF-03, SF-05 composers (Stasis Facility)."""
from pz_sheet_kit import *
import matplotlib.patches as mp
from PIL import ImageEnhance

RD = os.path.join(ROOT, "Stasis_Facility", "renders")
SD = os.path.join(ROOT, "Stasis_Facility", "sheets")
R = lambda n: os.path.join(RD, n + ".png")
A = lambda shot: load_meta(RD, shot)["anchors"]

# ---------------------------------------------------------------- pixel maps
EPX = 15.0
def ez(z): return 500 - (z - 22) * EPX
def efront(x, z): return (1200 + x * EPX, ez(z))
def erear(x, z): return (1200 - x * EPX, ez(z))
def eleft(y, z): return (1200 - (y - 60) * EPX, ez(z))
def eright(y, z): return (1200 + (y - 60) * EPX, ez(z))
RPX = 2000 / 150.0
def roof(x, y): return (750 + x * RPX, 1000 - (y - 60) * RPX)
SPX = 2400 / 110.0
def sec(x, z): return (1200 + x * SPX, 600 - (z - 20) * SPX)

def brighten(src, dst, f=1.35, c=1.08):
    im = Image.open(src).convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(f)
    im = ImageEnhance.Contrast(im).enhance(c)
    im.save(dst)
    return dst

def levels(ax, fn, zs, x_at, crop_x1):
    """Horizontal level markers across an elevation."""
    ox, oy = ax._pz_off
    for z, t in zs:
        x0, y = fn(x_at, z)
        ax.plot([x0 - ox, crop_x1 - ox], [y - oy, y - oy], color=C["amber"], lw=0.45, ls=(0, (3, 3)), zorder=5)
        ax.text(x0 - ox - 6, y - oy, t, fontsize=6.2, color=C["amber"], ha="right", va="center", weight="bold", zorder=6)

def scalebar(ax, x, y, px_per_stud, studs=(8, 16, 32)):
    ox, oy = ax._pz_off
    x -= ox; y -= oy
    prev = 0
    for i, s in enumerate(studs):
        ax.add_patch(mp.Rectangle((x + prev * px_per_stud, y), (s - prev) * px_per_stud, 6,
                                  fc=C["text"] if i % 2 == 0 else C["panel"], ec=C["text"], lw=0.5, zorder=6))
        prev = s
    ax.text(x, y + 10, "0", fontsize=5.6, color=C["muted"], ha="center", va="top")
    for s in studs:
        ax.text(x + s * px_per_stud, y + 10, str(s), fontsize=5.6, color=C["muted"], ha="center", va="top")
    ax.text(x + studs[-1] * px_per_stud + 10, y + 3, "studs", fontsize=5.6, color=C["muted"], va="center")

# ================================================================ SF-01
def sf01a():
    fig = new_sheet()
    frame(fig, "SF-01", "STASIS FACILITY — EXTERIOR DESIGN", "Chapter One · The Awakening · cinematic render + roof plan (same Blender model as all technical views)", 1, 2)
    panel(fig, (0.012, 0.3, 0.645, 0.612), "CINEMATIC VIEW  ·  SOUTH-WEST", "Cycles render of the production blockout — concept intent, not a final art pass")
    ax = image_axes(fig, (0.012, 0.3, 0.645, 0.612), R("ext_hero"), crop=(160, 190, 1760, 1080))
    an = A("ext_hero")
    for k, t, d, col in (("signage", "Illuminated ID signage", (-40, -160), C["cyan"]),
                         ("D01", "Octagonal main portal 12×14", (-260, -60), C["cyan"]),
                         ("banners", "Orange ZERO banners + amber emblem", (120, -200), C["orange"]),
                         ("vault", "Ribbed barrel vault, crown +32", (-200, -120), C["cyan"]),
                         ("cryo_tanks", "Cryo coolant tanks (W wing roof)", (-160, -150), C["cyan"]),
                         ("antenna", "Comms mast + red beacon", (140, -40), C["red"]),
                         ("D05", "Emergency exit W (always openable)", (-80, 140), C["green"]),
                         ("apron", "Entry apron, amber guide lights", (160, 90), C["amber"])):
        if k in an and 0 < an[k][0] < 1920 and 0 < an[k][1] < 1080:
            callout(ax, an[k][:2], t, d, col, fs=7)
    panel(fig, (0.665, 0.05, 0.323, 0.862), "ROOF PLAN", "N ↑ · 13.3 px / stud")
    ax = image_axes(fig, (0.665, 0.05, 0.323, 0.862), R("roof_plan"), crop=(60, 0, 1440, 2000))
    callout(ax, roof(0, 92), "ridge skylight (cyan)", (90, -60), fs=6.4)
    callout(ax, roof(-35, 43), "cryo tanks ×2", (-30, 170), fs=6.4)
    callout(ax, roof(34, 46), "cooling units ×3", (-40, 210), fs=6.4)
    callout(ax, roof(36, 8), "exhaust vents ×4", (-60, -110), fs=6.4)
    callout(ax, roof(-34, 112), "comms mast", (50, -70), fs=6.4)
    callout(ax, roof(20, 112), "rear HVAC", (40, -80), fs=6.4)
    callout(ax, roof(-27, 70), "W pipe run", (-10, -330), fs=6.4)
    dim(ax, roof(-44, 0), roof(44, 0), "88", off=40, fs=6.6)
    dim(ax, roof(44, 0), roof(44, 120), "120", off=40, vertical=True, fs=6.6)
    panel(fig, (0.012, 0.05, 0.645, 0.242), "EXTERIOR DESIGN NOTES", None)
    text_block(fig, 0.022, 0.262, [
        ("Massing", "o"),
        "Long ribbed barrel vault (the pod hall) flanked by flat-roofed",
        "service wings; taller front and rear blocks frame it. One landmark",
        "silhouette from the plaza, matching the page-10 reference hall.",
        ("Entrance", "o"),
        "Octagonal portal echoes the interior containment door (D03).",
    ], fs=7.4, lh=0.0195)
    text_block(fig, 0.34, 0.262, [
        ("Facade", "o"),
        "Graphite panels on 8-stud steel pilasters; cyan window strips",
        "at +10; orange base band and parapet caps; cyan band at +18.",
        ("Reference fidelity (page 10)", "o"),
        "Kept: octagonal doors, orange banners with diamond emblem,",
        "ribbed vault, cyan pods, amber floor strips, orange arms.",
    ], fs=7.4, lh=0.0195)
    save(fig, os.path.join(SD, "SF-01_Exterior_1_Render_Roof.png"))

def sf01b():
    fig = new_sheet()
    frame(fig, "SF-01", "STASIS FACILITY — ELEVATIONS & DETAILS", "Orthographic elevations (Workbench renders, 15 px/stud source) · entrance and vault structure details", 2, 2)
    lv = [(0, "+0"), (18, "+18 spring"), (32, "+32 crown")]
    # front + rear
    for i, (shot, fn, title) in enumerate((("elev_front", efront, "FRONT ELEVATION (SOUTH)"), ("elev_rear", erear, "REAR ELEVATION (NORTH)"))):
        rect = (0.012 + i * 0.318, 0.6, 0.31, 0.312)
        panel(fig, rect, title, None)
        ax = image_axes(fig, rect, R(shot), crop=(330, 190, 2010, 900))
        levels(ax, fn, lv, -52, 2010)
        dim(ax, fn(-44 if i == 0 else 44, 0), fn(44 if i == 0 else -44, 0), "88", off=28, fs=6.6)
        scalebar(ax, 1440, 860, EPX, (8, 16, 32))
    for j, (shot, fn, title, lab) in enumerate((("elev_left", eleft, "LEFT ELEVATION (WEST)", ("REAR", "FRONT")),
                                               ("elev_right", eright, "RIGHT ELEVATION (EAST)", ("FRONT", "REAR")))):
        rect = (0.012, 0.325 - j * 0.275, 0.628, 0.267)
        panel(fig, rect, title, None)
        ax = image_axes(fig, rect, R(shot), crop=(60, 190, 2340, 905))
        levels(ax, fn, lv, -2 if j == 0 else 122, 2340)
        p0, p1 = fn(0, 0), fn(120, 0)
        dim(ax, p0, p1, "120 overall", off=52, fs=6.6)
        for a, b in ((0, 24), (24, 104), (104, 120)):
            dim(ax, fn(a, 0), fn(b, 0), str(b - a), off=14, fs=5.8, ext=False)
        scalebar(ax, 1720, 880, EPX, (8, 16, 32))
    # entrance detail
    panel(fig, (0.648, 0.49, 0.34, 0.422), "DETAIL A  ·  MAIN ENTRANCE", "front elevation, enlarged")
    ax = image_axes(fig, (0.648, 0.49, 0.34, 0.422), R("elev_front"), crop=(790, 220, 1610, 860))
    dim(ax, efront(-6, 0), efront(6, 0), "12", off=18, fs=6.6)
    dim(ax, efront(6, 0), efront(6, 14), "14", off=40, vertical=True, fs=6.6)
    dim(ax, efront(-8.5, 0), efront(-8.5, 16.5), "frame 17", off=-30, vertical=True, fs=6.2)
    callout(ax, efront(0, 16.6), "ID signage, cyan Neon", (90, -50), fs=6.2)
    callout(ax, efront(-13, 12.5), "banner 4×10 + emblem", (-10, -150), C["orange"], fs=6.2)
    callout(ax, efront(19, 10), "pylon 3×3, cyan strip", (-40, -190), fs=6.2)
    callout(ax, efront(0, 7.7), "orange door band", (150, 40), C["orange"], fs=6.2)
    callout(ax, efront(-22, 0.6), "orange base band", (60, -50), C["orange"], fs=6.2)
    # vault structure detail
    panel(fig, (0.648, 0.05, 0.34, 0.432), "DETAIL B  ·  VAULT & WALL STRUCTURE", "section at Y = 61, looking north")
    ax = image_axes(fig, (0.648, 0.05, 0.34, 0.432), R("section_chamber"), crop=(500, 210, 1900, 1075))
    dim(ax, sec(-24, 0), sec(24, 0), "48 clear span", off=30, fs=6.4)
    dim(ax, sec(-24, 0), sec(-24, 18), "18", off=-50, vertical=True, fs=6.4)
    dim(ax, sec(-24, 18), sec(-24, 32), "14 rise", off=-50, vertical=True, fs=6.4)
    callout(ax, sec(-16, 29.3), "vault shell 1.0, ribs 1.2 @ 8 c/c", (-30, -70), fs=6.0, ha="center")
    callout(ax, sec(0, 31.5), "ridge skylight", (120, -40), fs=6.0)
    callout(ax, sec(14, 25.5), "crane rail +25", (130, 10), C["orange"], fs=6.0)
    callout(ax, sec(23.5, 9), "pilaster 1×1 @ 8", (-120, 110), fs=6.0)
    callout(ax, sec(34, 18.5), "wing roof +18", (40, -60), fs=6.0)
    save(fig, os.path.join(SD, "SF-01_Exterior_2_Elevations.png"))

# ================================================================ SF-03
def sf03a():
    fig = new_sheet()
    frame(fig, "SF-03", "STASIS FACILITY — INTERIOR: MAIN POD CHAMBER", "R04 · camera at P01 looking north to containment door D03 · lighting design and states", 1, 2)
    panel(fig, (0.012, 0.05, 0.64, 0.862), "MAIN CHAMBER  ·  NORMAL STATE", "Cycles render — direct reinterpretation of NEXUS-01 page-10 reference")
    ax = image_axes(fig, (0.012, 0.05, 0.64, 0.862), R("int_chamber"))
    an = A("int_chamber")
    for k, t, d, col in (("P02", "Stasis pod bay (8 total, 4 per side)", (60, -60), C["cyan"]),
                         ("arm", "Orange manipulator on crane trolley", (120, 70), C["orange"]),
                         ("D03", "Octagonal containment door D03", (210, -40), C["cyan"]),
                         ("aisle", "12-stud aisle grate, amber edge strips", (160, -60), C["amber"]),
                         ("ribs", "Inner ribs + pilasters @ 8", (-30, 80), C["cyan"]),
                         ("P06", "Pod front console + diag. unit", (-60, 80), C["cyan"])):
        if k in an and 0 < an[k][0] < 1920 and 0 < an[k][1] < 1080 and an[k][2] > 0:
            callout(ax, an[k][:2], t, d, col, fs=7)
    # lighting states
    panel(fig, (0.66, 0.36, 0.328, 0.552), "LIGHTING STATES  (driven by server-owned Power state)", None)
    st = [("light_normal", "NORMAL / ONLINE", C["cyan"]), ("light_wake", "WAKE SEQUENCE", C["amber"]),
          ("light_lockdown", "LOCKDOWN (ZERO)", C["red"]), ("light_offline", "POWER OFFLINE", "#5E7FA8")]
    for i, (shot, t, col) in enumerate(st):
        cx = 0.666 + (i % 2) * 0.161
        cy = 0.635 - (i // 2) * 0.255
        image_axes(fig, (cx, cy, 0.157, 0.24), R(shot), pad_top=0.022, pad=0.002)
        fig.text(cx + 0.004, cy + 0.228, t, fontsize=7.4, color=col, weight="bold")
    panel(fig, (0.66, 0.05, 0.328, 0.302), "LIGHTING DESIGN", None)
    rows = [("L1", "Pod cap bands + deck", "Neon #22D3EE", "PointLight 1.5 / r 10"),
            ("L2", "Ridge skylight", "Neon #22D3EE", "SurfaceLight ↓ 2 / r 30"),
            ("L3", "Ceiling lamps ×5", "Neon disc", "SpotLight 3 / 60° / r 40"),
            ("L4", "Aisle edge strips", "Neon #FFB020", "no Light object"),
            ("L5", "Door banners / D03", "Neon #FFB020", "PointLight 1 / r 12"),
            ("L6", "Emergency", "Neon #E5383B", "enabled in Lockdown only")]
    table(fig, (0.666, 0.115, 0.316, 0.205), ["ID", "SOURCE", "MATERIAL", "ROBLOX LIGHT"], rows, [0.09, 0.33, 0.25, 0.33], fs=6.4)
    text_block(fig, 0.668, 0.1, [("Budget: ≤ 12 shadow-casting lights in R04. Lighting = Future;", "m"),
                                 ("Atmosphere density 0.35, cyan tint #0E2A33.", "m")], fs=6.6, lh=0.016)
    save(fig, os.path.join(SD, "SF-03_Interior_1_Chamber_Lighting.png"))

def sf03b():
    fig = new_sheet()
    frame(fig, "SF-03", "STASIS FACILITY — INTERIOR CONSTRUCTION & SYSTEMS", "Cutaway axonometric (walls cut at +12) · chamber section · mechanical and cryogenic support", 2, 2)
    src = brighten(R("cutaway_axo"), os.path.join(RD, "cutaway_axo_sheet.png"))
    panel(fig, (0.012, 0.05, 0.56, 0.862), "CUTAWAY AXONOMETRIC  ·  FROM SOUTH-EAST", "roofs removed, all walls cut at +12")
    ax = image_axes(fig, (0.012, 0.05, 0.56, 0.862), src, crop=(100, 60, 1900, 1260))
    an = A("cutaway_axo")
    lab = {"R01": "R01 Reception", "R02": "R02 Security", "R03": "R03 Lockers", "R04": "R04 Pod chamber",
           "R05": "R05 Maint. corridor", "R06": "R06 Cryo plant", "R09": "R09 Medical", "R10": "R10 Energy ctrl",
           "R12": "R12 Service bay", "R13": "R13 Service stair", "R11": "R11 Exit E"}
    offs = {"R04": (-90, -230), "R06": (-80, -120), "R05": (-60, -170), "R10": (150, -80), "R09": (170, 40),
            "R12": (40, -110), "R13": (-60, -80), "R01": (-80, 110), "R02": (-120, 60), "R03": (120, 90), "R11": (120, -60)}
    for k, t in lab.items():
        if k in an:
            callout(ax, an[k][:2], t, offs.get(k, (60, -60)), C["cyan"], fs=7)
    if "mezzanine" in an:
        callout(ax, an["mezzanine"][:2], "Observation mezzanine +12", (-40, 120), C["text"], fs=7)
    if "power_core" in an:
        callout(ax, an["power_core"][:2], "Power core", (120, -120), C["cyan"], fs=7)
    panel(fig, (0.58, 0.48, 0.408, 0.432), "SECTION Y = 61  ·  WALL & CEILING CONSTRUCTION", None)
    ax = image_axes(fig, (0.58, 0.48, 0.408, 0.432), R("section_chamber"), crop=(160, 180, 2240, 1080))
    callout(ax, sec(-38, 6), "R06 cryo tanks Ø6.4", (90, 190), fs=6.2)
    callout(ax, sec(-24.5, 10), "1-stud graphite partition", (-40, 200), fs=6.2)
    callout(ax, sec(-17, 12), "pod P03 beyond", (60, 130), fs=6.2)
    callout(ax, sec(0, 9), "D03 containment door", (0, 180), fs=6.2, ha="center")
    callout(ax, sec(34, 8), "power core R10", (-60, 200), fs=6.2)
    callout(ax, sec(0, 26.5), "crane bridge (orange)", (180, -60), C["orange"], fs=6.2)
    callout(ax, sec(-14, 30.4), "vault 1.0 + inner rib 1.2", (-200, -50), fs=6.2)
    panel(fig, (0.58, 0.05, 0.408, 0.422), "MECHANICAL & CRYOGENIC SUPPORT SYSTEMS", None)
    rows = [("M1", "Cryo plant", "4 tanks Ø6.4×13 (R06) + 2 roof tanks", "Cooling: Normal/Warning/Critical"),
            ("M2", "Coolant loop", "steel + blue pipes, R05 corridor", "steam VFX at Warning"),
            ("M3", "Pod services", "2 coolant + 1 power per pod (rear)", "hatch repair objective"),
            ("M4", "Power core", "Ø4.4 cyan core in cage (R10)", "Power: Online/Degraded/Offline"),
            ("M5", "Breaker cabinets", "5 cabinets, amber/cyan LEDs (R10)", "breaker puzzle"),
            ("M6", "Roof cooling", "3 fan units 12×10×4 (E wing)", "fans stop when Offline"),
            ("M7", "Overhead crane", "rails +25, bridge + 2-segment arm", "scripted path, no physics"),
            ("M8", "Vitals / data", "console per pod → R09", "Data: Connected/Jammed"),
            ("M9", "Ventilation", "4 roof stacks, rear HVAC", "ambient audio only")]
    table(fig, (0.586, 0.06, 0.396, 0.375), ["ID", "SYSTEM", "EQUIPMENT", "GAME STATE / HOOK"], rows,
          [0.07, 0.19, 0.42, 0.32], fs=6.4)
    save(fig, os.path.join(SD, "SF-03_Interior_2_Construction_Systems.png"))

# ================================================================ SF-05
def sf05a():
    fig = new_sheet()
    frame(fig, "SF-05", "STASIS FACILITY — ROBLOX CONSTRUCTION: MODULAR KIT", "8-stud grid · module dimensions in studs · collision fidelity · part counts (design assumptions)", 1, 2)
    panel(fig, (0.012, 0.43, 0.6, 0.482), "MODULAR KIT  ·  AXONOMETRIC", "all modules at true relative scale; Cypher = 6.0 studs")
    ax = image_axes(fig, (0.012, 0.43, 0.6, 0.482), R("kit_axo"), crop=(150, 80, 2500, 1440))
    an = A("kit_axo")
    nm = {"K01": "K01 floor 8×8", "K02": "K02 wall 8×18", "K03": "K03 vault panel", "K04": "K04 vault rib",
          "K05": "K05 aisle grate", "K06": "K06 stasis pod", "K07": "K07 octagonal door", "K08": "K08 mezzanine bay",
          "K09": "K09 crane rail", "K10": "K10 console", "K_human": "Cypher 6.0 (scale ref.)"}
    off = {"K03": (-120, -60), "K04": (120, -60), "K06": (60, -80), "K07": (-80, -60), "K_human": (60, -40),
           "K01": (-60, 50), "K05": (-40, 70), "K10": (40, 60), "K08": (-40, -70), "K09": (60, -60), "K02": (-60, -60)}
    for k, t in nm.items():
        if k in an:
            callout(ax, an[k][:2], t, off.get(k, (60, -60)), C["amber"] if k == "K_human" else C["cyan"], fs=7)
    panel(fig, (0.62, 0.43, 0.368, 0.482), "COLLISION REQUIREMENTS", None)
    text_block(fig, 0.628, 0.875, [
        ("Rule: collision comes from simple Studio parts; meshes never collide unless listed.", "b"),
        ("Walls, floors, slabs", "o"), "Part, CanCollide on, Anchored. 1-stud walls; no gaps > 0.2.",
        ("Vault, ribs, roof equipment", "o"), "MeshPart CanCollide OFF + invisible box roof at +31 (CanCollide on).",
        ("Stasis pod", "o"), "Plinth = cylinder Part. Glass = Box fidelity, OFF while open.",
        "Occupant cavity Ø6 kept clear for the wake animation.",
        ("Doors", "o"), "One invisible blocker per leaf, moved by the same tween as the leaf.",
        ("Props < 2 studs", "o"), "CanCollide, CanTouch and CanQuery OFF (decoration only).",
        ("Player-blocking volumes", "o"), "Invisible Parts around crane arm sweep and the power core.",
        ("Camera", "o"), "Vault interior must stay ≥ 8 studs above the player camera path; mezzanine",
        "underside uses CanQuery OFF so the camera does not snap.",
    ], fs=7.0, lh=0.0182)
    panel(fig, (0.012, 0.05, 0.976, 0.372), "MODULE SCHEDULE", "Part = Studio primitive · Mesh = Meshy → Blender → MeshPart")
    rows = [("K01", "Floor tile", "8 × 8 × 0.5", "Part", "Box", "165", "Snaps to grid; chamber tiles darker variant"),
            ("K02", "Wall panel + pilaster", "8 × 18 × 1", "Part ×2", "Box", "≈ 60", "Window-strip variant; door-opening variant"),
            ("K03", "Vault shell module", "48 span × 8 × 1", "Mesh", "None", "10", "Invisible roof box provides collision"),
            ("K04", "Vault rib", "50 span × 1.2", "Mesh", "None", "11 + 11", "Outer + inner ribs, 8-stud centres"),
            ("K05", "Aisle grate", "12 × 8 × 0.2", "Part + Neon", "Box", "10", "Amber Neon edge strips"),
            ("K06", "Stasis pod", "11 × 9.7 × 14.5", "Mesh + Parts", "Hull / Box", "8", "Model with Hinge part; see SF-04"),
            ("K07", "Octagonal door", "17 × 17 frame, 12 × 14 leaf", "Mesh frame + Part leaves", "Box", "2 (+1 ext.)", "D01, D02, D03"),
            ("K08", "Mezzanine bay", "8 × 8, deck +12", "Part", "Box", "6", "Rail 3.2 high; stair 12 risers"),
            ("K09", "Crane rail", "16 × 1.2 × 1.2", "Part", "None", "10", "Above play space; no collision"),
            ("K10", "Console", "2 × 2 × 3.8", "Mesh", "Box", "≈ 14", "ProximityPrompt attachment on screen")]
    table(fig, (0.02, 0.06, 0.96, 0.33), ["ID", "MODULE", "SIZE (STUDS)", "BUILD", "COLLISION", "COUNT", "NOTES"], rows,
          [0.05, 0.15, 0.17, 0.16, 0.09, 0.08, 0.30], fs=7.0)
    save(fig, os.path.join(SD, "SF-05_Roblox_1_Kit_Collision.png"))

def sf05b():
    fig = new_sheet()
    frame(fig, "SF-05", "STASIS FACILITY — ROBLOX IMPLEMENTATION SPEC", "Interactive elements · animations · lighting states · hierarchy · performance budget", 2, 2)
    panel(fig, (0.012, 0.5, 0.56, 0.412), "INTERACTIVE ELEMENTS  (server-authoritative)", None)
    rows = [("I1", "Player pods P02–04, P06", "Own wake sequence", "Server assigns pod on join; once per player"),
            ("I2", "P01 Cypher / P05 Sentinel", "Guide cue / rescue", "P01 scripted first; P05 opens on power"),
            ("I3", "Scanner arch", "Clearance check", "Server validates distance + clearance"),
            ("I4", "Containment door D03", "Opens on power restore", "Reads Power state; never client-set"),
            ("I5", "Breaker cabinets", "3-step puzzle → Power Online", "Server checks order; rate-limited"),
            ("I6", "Med consoles", "Memory fragment pickup", "Persistent unlock (DataStore)"),
            ("I7", "Service hatch", "Repair objective", "Hold prompt 2 s; server timer"),
            ("I8", "Roll-up door D04", "Mission exit / extraction", "TeleportService hand-off"),
            ("I9", "Exit doors D05/D06", "Always openable", "Failsafe — ignores Lockdown")]
    table(fig, (0.018, 0.508, 0.548, 0.37), ["ID", "ELEMENT", "PLAYER ACTION", "AUTHORITY / VALIDATION"], rows,
          [0.06, 0.24, 0.3, 0.4], fs=6.8)
    panel(fig, (0.58, 0.5, 0.408, 0.412), "DOOR & POD ANIMATIONS", "TweenService, server-owned target state")
    rows = [("A1", "Octagonal doors", "leaves slide 6.2 apart", "0.9 s Quad Out"),
            ("A2", "Roll-up D04", "shutter +14 Y", "2.5 s Linear"),
            ("A3", "Pod glass", "hinge rotate 165°", "1.6 s Quad Out"),
            ("A4", "Pod thaw", "band Color + Brightness", "1.2 s Sine InOut"),
            ("A5", "Crane bridge", "Y 30 ↔ 96 patrol", "12 s Sine InOut, loop"),
            ("A6", "Manipulator arm", "2-joint pose cycle", "AnimationController"),
            ("A7", "Lockdown", "red Neon + shutters", "0.4 s; alarm SFX"),
            ("A8", "Emergency exits", "swing 95°", "0.6 s Back Out")]
    table(fig, (0.586, 0.508, 0.396, 0.37), ["ID", "TARGET", "MOTION", "TIMING"], rows, [0.07, 0.3, 0.36, 0.27], fs=6.8)
    panel(fig, (0.012, 0.05, 0.31, 0.442), "LIGHTING STATES", "from District Power / Security")
    rows = [("Online", "#22D3EE", "pods steady, doors open"), ("Wake", "#FFB020", "per-player pod sequence, amber wash"),
            ("Degraded", "#22D3EE", "50% brightness, flicker"), ("Lockdown", "#E5383B", "red Neon, D01/D03 locked"),
            ("Offline", "#1E88E5", "10%, emergency strips only")]
    y = 0.44
    for n, hx, d in rows:
        fig.patches.append(mp.Rectangle((0.022, y - 0.032), 0.028, 0.036, transform=fig.transFigure, fc=hx, ec=C["line"]))
        fig.text(0.056, y - 0.006, n.upper(), fontsize=7.6, weight="bold", color=C["text"])
        fig.text(0.056, y - 0.024, f"{hx} · {d}", fontsize=6.8, color=C["muted"])
        y -= 0.06
    text_block(fig, 0.022, 0.13, [("Client renders; server owns state. Each outage", "m"), ("has a recovery path (NEXUS-01 bible §7).", "m")], fs=6.8, lh=0.016)
    panel(fig, (0.33, 0.05, 0.3, 0.442), "INSTANCE HIERARCHY", "Workspace")
    tree = ["NEXUS01/", "└ AWK_StasisFacility  (Model, PrimaryPart = Origin)",
            "   ├ Shell/        K01 K02 K03 K04 + roof boxes", "   ├ Rooms/R01…R13/  props, Attachments",
            "   ├ Pods/P01…P08   (PZ_AWK_StasisPod_A)", "   │   └ Hinge, Glass, Cap, Console, Prompt",
            "   ├ Doors/D01…D18  Leaves + Blockers", "   ├ Crane/         Rail, Bridge, Arm",
            "   ├ Lights/        grouped by state tag", "   ├ Interactables/ CollectionService tags",
            "   └ Streaming/     LOD proxy (Model)", "ServerScriptService/", "└ StasisFacilityService (state, prompts)",
            "ReplicatedStorage/Shared/", "└ StasisConfig, Remotes (typed)"]
    for i, t in enumerate(tree):
        fig.text(0.338, 0.445 - i * 0.0245, t, fontsize=6.9, family="DejaVu Sans Mono", color=C["text"] if "/" in t[:4] else C["muted"] if t.startswith(" ") else C["cyan"])
    panel(fig, (0.638, 0.05, 0.35, 0.442), "PERFORMANCE CONSTRAINTS  (targets, to be profiled)", None)
    rows = [("Parts + MeshParts", "≤ 1,800", "whole facility"), ("Triangles (meshes)", "≤ 90 k", "pod ≤ 6 k each"),
            ("Unique textures", "≤ 12 @ 1024²", "trim sheet + atlas"), ("Light objects", "≤ 24 total", "≤ 6 shadows"),
            ("Moving parts", "≤ 40", "tweens, no physics"), ("Draw distance", "StreamingEnabled", "LOD proxy > 400 st"),
            ("Mobile frame", "≥ 30 fps", "mid-tier phone"), ("Desktop frame", "≥ 60 fps", "integrated GPU"),
            ("Server scripts", "event-driven", "no per-frame loops")]
    table(fig, (0.644, 0.06, 0.338, 0.395), ["METRIC", "BUDGET", "NOTE"], rows, [0.4, 0.28, 0.32], fs=6.8)
    save(fig, os.path.join(SD, "SF-05_Roblox_2_Implementation.png"))
