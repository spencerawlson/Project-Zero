"""INF-01 … INF-12 city infrastructure. Front faces -Y. Family robots for scale/use."""
import math
from pz_asset_lib import *
from pz_build_stasis import M

# ------------------------------------------------------------------ INF-01 Robot Charging Station 10×8×12 (ref)
def inf01():
    ground("g", -12, 12, -12, 10)
    box("pad", -5, 5, -6, 2, 0, 0.3, M["graphite"]); box("pad_ring", -4, 4, -5, 1, 0.3, 0.35, M["cyan_e"])
    box("housing", -5, 5, 2, 4, 0, 12, M["graphite"])
    box("hood", -5.5, 5.5, -2, 4, 11, 12, M["panel"]); box("hood_l", -5, 5, -2.1, -1.9, 11.2, 11.6, M["cyan_e"])
    for s in (-1, 1):
        box(f"trim{s}", s * 5 - 0.3, s * 5 + 0.3, 1.8, 4.1, 0, 11, M["orange"])
    box("meter_bg", -1.5, 1.5, 1.9, 2.0, 3, 9, M["panel"])
    for k in range(6):
        box(f"meter{k}", -1.2, 1.2, 1.85, 1.9, 3.4 + k * 0.9, 4.0 + k * 0.9, M["cyan_e"] if k < 4 else M["panel"])
    box("panel", 3, 4.6, 0.5, 1.9, 4, 7, M["graphite"]); box("panel_s", 3.1, 4.5, 0.45, 0.5, 5, 6.5, M["cyan_soft"])
    cbox("battery", -3.4, 2.9, 2.5, 2, 1.6, 3, M["orange"])
    note("meter2", (0, 1.85, 6.5), "Charge meter (readable charge state)"); note("pad_ring", (3.5, -5, 0.35), "Dock pad with cyan ring")
    note("panel_s", (3.8, 0.45, 6.5), "Interface panel (ProximityPrompt)"); note("battery", (-3.4, 2, 3.5), "Replaceable battery module (repair objective)")
    note("hood_l", (0, -2, 11.6), "Canopy light bar")
    robot("user", "Cypher", 0, -2, 0.0, z=0.3)

# ------------------------------------------------------------------ INF-02 Energy Substation 24×16×16
def inf02():
    ground("g", -18, 18, -14, 14)
    box("slab", -12, 12, -8, 8, 0, 0.5, X["concrete2"])
    for k, x in enumerate((-7, 0, 7)):
        cyl(f"xfmr{k}", x, 1, 0.5, 9, 2.4, M["graphite"], 8)
        for j in range(3):
            cyl(f"ins{k}{j}", x - 1 + j, 1, 9.5, 2.5, 0.25, M["steel"], 10)
            sphere(f"insc{k}{j}", x - 1 + j, 1, 12.2, 0.35, M["cyan_e"])
        tube(f"band{k}", x, 1, 6, 0.5, 2.5, 0.2, M["orange"])
    for x in (-11.5, 11.5):
        box(f"fenceS{x}", -12, 12, -8, -7.8, 0.5, 6, M["steel"]) if x < 0 else None
    box("fence_S", -12, 12, -8, -7.85, 0.5, 6, M["glass"]); box("fence_top", -12, 12, -8.05, -7.8, 6, 6.3, M["orange"])
    box("gantry", -12, 12, 6.5, 7.5, 14, 15, M["graphite"])
    for x in (-12, 12):
        box(f"gpost{x}", x - 0.5, x + 0.5, 6.5, 7.5, 0, 14, M["graphite"])
    for x in (-8, 0, 8):
        box(f"cable{x}", x - 0.1, x + 0.1, 1, 7, 12.4, 14, M["steel"])
    box("control", 8, 12, -7, -3, 0.5, 4.5, M["panel"]); box("control_s", 7.9, 8, -6.5, -3.5, 2, 4, M["cyan_soft"])
    note("insc01", (-7, 1, 12.6), "Insulator heads glow by Power state"); note("xfmr1", (0, -1.4, 6), "Transformers ×3")
    note("fence_top", (-8, -8, 6.3), "Safety fence (orange top rail)"); note("control_s", (8, -5, 4), "Breaker control box (puzzle)")
    note("gantry", (0, 7, 15), "Line gantry to Spire grid")
    robot("tech", "Patch", 4, -10, 0.3)

# ------------------------------------------------------------------ INF-03 Communication Tower 8×8×64
def inf03():
    ground("g", -10, 10, -10, 10)
    box("base", -4, 4, -4, 4, 0, 4, M["graphite"])
    for (x, y) in ((-2.5, -2.5), (2.5, -2.5), (-2.5, 2.5), (2.5, 2.5)):
        cyl(f"leg{x}{y}", x, y, 4, 52, 0.35, M["steel"], 8, r2=0.25)
    for k in range(12):
        z = 6 + k * 4.2
        box(f"ring{k}", -2.8, 2.8, -2.8, 2.8, z, z + 0.3, M["orange"] if k % 3 == 0 else M["graphite"])
    for k, z in enumerate((30, 44)):
        for a in range(3):
            ang = 2 * math.pi * a / 3
            cyl(f"dish{k}{a}", 3.6 * math.cos(ang), 3.6 * math.sin(ang), z, 0.5, 1.6, M["white"], 20).rotation_euler = (math.radians(90), 0, ang + math.pi / 2)
    cyl("mast", 0, 0, 56, 8, 0.2, M["steel"], 8); sphere("beacon", 0, 0, 64.2, 0.6, M["red_e"])
    tube("halo", 0, 0, 52, 0.4, 3.4, 0.3, M["cyan_e"])
    note("dish00", (3.6, 0, 30.5), "Relay dishes ×6 (Data relay state)"); note("halo", (3.4, 0, 52.4), "Cyan status halo")
    note("beacon", (0, 0, 64.4), "Aviation beacon"); note("ring3", (2.8, 0, 18.9), "Lattice tower, orange marker rings")
    robot("tech", "Patch", 6, -6, 0.5)

# ------------------------------------------------------------------ INF-04 Security Access Gate 24×8×18 (ref)
def inf04():
    ground("g", -18, 18, -12, 12)
    for s in (-1, 1):
        box(f"pylon{s}", s * 12 - 3 if s > 0 else -12, s * 12 if s > 0 else -9, -4, 4, 0, 18, M["graphite"])
        box(f"pylon_l{s}", (s * 12 - 3 if s > 0 else -12) + (0 if s > 0 else 2.6), (s * 12 if s > 0 else -9) - (0 if s < 0 else 2.6), -4.1, -3.9, 2, 16, M["red_e"])
    box("lintel", -12, 12, -4, 4, 15, 18, M["graphite"])
    box("scan_arch", -9, 9, -0.5, 0.5, 14, 15, M["cyan_e"])
    box("blast", -9, 9, 2, 3, 0, 14, M["panel"]); box("blast_seam", -0.1, 0.1, 1.9, 2.0, 0.5, 13.5, M["red_e"])
    for k in range(6):
        box(f"haz{k}", -9 + k * 3, -7.5 + k * 3, 1.9, 2.0, 0, 1.2, M["orange"])
    text("code", "A-3", 0, -4.15, 16, 1.6, M["cyan_e"])
    emblem("emb", 0, -4.2, 11.5, 1.0, M["red_e"]) if False else None
    note("scan_arch", (0, 0, 15), "Scanning arch (clearance check)"); note("blast", (5, 2, 14), "Blast door 18 × 14 (Lockdown)")
    note("code", (0, -4.1, 17), "District code sign"); note("pylon_l1", (9.5, -4, 14), "Red alert strips (Security state)")
    robot("guard", "Sentinel", -6, -7, 0.3)

# ------------------------------------------------------------------ INF-05 Street Lighting System 2×2×14
def inf05():
    ground("g", -6, 6, -6, 6)
    box("base", -1, 1, -1, 1, 0, 0.8, M["graphite"])
    cyl("pole", 0, 0, 0.8, 12, 0.3, M["steel"], 12, r2=0.22)
    box("band", -0.35, 0.35, -0.35, 0.35, 3, 3.6, M["orange"])
    cbox("arm", 0, -1.4, 12.4, 0.4, 3.2, 0.4, M["graphite"])
    box("head", -0.8, 0.8, -3.8, -2.4, 12, 12.7, M["graphite"]); box("lamp", -0.7, 0.7, -3.7, -2.5, 11.9, 12.0, M["amber_e"])
    box("beacon", -0.25, 0.25, -0.25, 0.25, 12.8, 13.6, M["cyan_e"])
    box("sign", -0.8, 0.8, -0.35, -0.3, 5, 7, M["cyan_soft"])
    note("lamp", (0, -3.1, 11.9), "Amber civic lamp (Power: on / dim / off)"); note("beacon", (0, 0, 13.6), "Cyan network beacon")
    note("sign", (0, -0.35, 6), "Wayfinding plate"); note("band", (0.35, 0, 3.3), "Orange hazard band")
    robot("walker", "Cypher", 2.5, -2, 0.2)

# ------------------------------------------------------------------ INF-06 Holographic Signage 4–12 wide
def inf06():
    ground("g", -10, 10, -6, 6)
    box("base", -1.2, 1.2, -1, 1, 0, 1.2, M["graphite"])
    box("post", -0.4, 0.4, -0.3, 0.3, 1.2, 6, M["steel"])
    box("frame", -6, 6, -0.4, 0.4, 6, 12, M["graphite"])
    box("screen", -5.5, 5.5, -0.45, -0.38, 6.4, 11.6, M["cyan_soft"])
    box("emit", -5.5, 5.5, -0.6, -0.4, 5.9, 6.1, M["cyan_e"])
    cbox("holo", 0, -2.0, 9, 9, 0.05, 5, M["holo"])
    text("ad", "CIRCUIT MARKET", 0, -2.1, 9.2, 1.2, M["amber_e"])
    for s in (-1, 1):
        box(f"trim{s}", s * 6 - 0.3, s * 6 + 0.3, -0.45, 0.45, 6, 12, M["orange"])
    note("holo", (3, -2.0, 10.5), "Projected holo layer (animated texture)"); note("frame", (6, 0, 12), "12-wide frame (4/8/12 variants)")
    note("emit", (0, -0.6, 6), "Projector bar"); note("base", (1.2, 0, 1.2), "Ballast base")
    robot("v", "Patch", 3, -4, 0.3)

# ------------------------------------------------------------------ INF-07 Industrial Ventilation Unit 8×8×6
def inf07():
    ground("g", -8, 8, -8, 8)
    box("box", -4, 4, -4, 4, 0, 5, M["steel"])
    box("trim", -4.05, 4.05, -4.05, 4.05, 0, 0.6, M["yellow"])
    cyl("fan_ring", 0, 0, 5, 0.6, 3.3, M["graphite"], 32)
    cyl("fan_hub", 0, 0, 5.3, 0.5, 0.8, M["orange"], 16)
    for k in range(6):
        cbox(f"blade{k}", 1.6 * math.cos(k), 1.6 * math.sin(k), 5.4, 2.6, 0.6, 0.08, M["panel"], rot=(0.3, 0, k))
    for k in range(5):
        box(f"louver{k}", -3.5, 3.5, -4.05, -3.95, 1 + k * 0.8, 1.4 + k * 0.8, M["graphite"])
    box("status", 2.5, 3.5, -4.1, -4.05, 3.8, 4.4, M["cyan_e"])
    note("fan_hub", (0, 0, 5.8), "Top exhaust fan (spins; stops when Offline)"); note("louver2", (0, -4, 3), "Intake louvres")
    note("status", (3, -4, 4.4), "Status LED"); note("trim", (4, -4, 0.6), "Factory-yellow base trim")
    robot("t", "Patch", 6, -4, 0.6)

# ------------------------------------------------------------------ INF-08 Cooling System 16×8×10
def inf08():
    ground("g", -14, 14, -10, 10)
    box("skid", -8, 8, -4, 4, 0, 0.8, M["graphite"])
    for k, x in enumerate((-5, 0, 5)):
        box(f"cell{k}", x - 2.3, x + 2.3, -3.6, 3.6, 0.8, 7.5, M["steel"])
        cyl(f"fan{k}", x, 0, 7.5, 0.5, 1.9, M["graphite"], 24); cyl(f"hub{k}", x, 0, 7.8, 0.4, 0.5, M["blue"], 12)
        for j in range(6):
            box(f"fin{k}{j}", x - 2.2, x + 2.2, -3.65, -3.6, 1.5 + j, 1.8 + j, M["graphite"])
    tank("tank", 0, 6.5, 0.8, 0, 1.4, horizontal=True) if False else None
    cyl("pipe_in", -8, -2, 3, 16, 0.5, M["blue"], 12, rot=(0, math.radians(90), 0)).location = (0, -4.4, 3)
    cyl("pipe_out", -8, 2, 3, 16, 0.5, M["orange"], 12, rot=(0, math.radians(90), 0)).location = (0, 4.4, 3)
    box("gauge", 7.5, 8.1, -2, 0, 3, 5, M["panel"]); box("gauge_l", 8.1, 8.15, -1.8, -0.2, 3.4, 4.6, M["cyan_e"])
    note("fan1", (0, 0, 8), "Fan cells ×3 (steam VFX at Warning)"); note("pipe_in", (0, -4.4, 3.5), "Coolant supply (blue)")
    note("pipe_out", (0, 4.4, 3.5), "Return (orange)"); note("gauge_l", (8.1, -1, 4.6), "State gauge Normal / Warning / Critical")
    robot("t", "Sentinel", -11, -4, 0.4)

# ------------------------------------------------------------------ INF-09 Water Recycling System 24×16×12
def inf09():
    ground("g", -18, 18, -14, 14)
    box("slab", -12, 12, -8, 8, 0, 0.5, X["concrete2"])
    for k, x in enumerate((-8, 0)):
        tank(f"tank{k}", x, 2, 0.5, 9, 3.2, M["white"])
    cyl("basin", 8, -2, 0.5, 2, 4, M["graphite"], 32); cyl("water", 8, -2, 2.4, 0.1, 3.7, M["blue"], 32)
    box("plant", 5, 11, 4, 8, 0.5, 6, M["panel"]); box("plant_s", 5.5, 10.5, 3.9, 4, 3, 5, M["cyan_soft"])
    cyl("pipe", -12, -5, 2, 24, 0.4, M["blue"], 12, rot=(0, math.radians(90), 0)).location = (0, -5, 2)
    box("walk", -12, 12, -8, -6.5, 4, 4.3, M["grate"]); box("walk_rail", -12, 12, -8.05, -7.9, 4.3, 5.4, M["orange"])
    note("tank0", (-8, 2, 11), "Filtration tanks"); note("water", (8, -2, 2.5), "Settling basin")
    note("walk", (-6, -7, 4.3), "Maintenance catwalk"); note("plant_s", (8, 4, 5), "Pump control")
    robot("t", "Patch", -2, -10, 0.2)

# ------------------------------------------------------------------ INF-10 Maintenance Tunnel module 12 wide × 16 long
def inf10():
    CUT_H[0] = 7
    ground("g", -12, 12, -12, 12)
    box("floor", -6, 6, -8, 8, 0, 0.4, M["floor"]); box("floor_grate", -2, 2, -8, 8, 0.4, 0.45, M["grate"])
    vault("tube", 0, 6, 4, 6, -8, 8, 0.6, M["graphite"])
    for s in (-1, 1):
        box(f"wall{s}", s * 6 - 0.3 if s > 0 else -6.6, s * 6 + 0.3 if s > 0 else -6, -8, 8, 0, 6, M["graphite"])
        box(f"strip{s}", s * 5.6 - 0.1, s * 5.6 + 0.1, -8, 8, 0.6, 0.9, M["amber_e"])
        for k, z in enumerate((2.5, 3.6, 4.7)):
            cyl(f"pipe{s}{k}", s * 5.2, -8, z, 16, 0.3, [M["blue"], M["orange"], M["steel"]][k], 10, rot=(math.radians(-90), 0, 0))
    for y in (-8, 0, 8):
        vault(f"rib{y}", 0, 6.2, 4.2, 6, y - 0.4, y + 0.4, 0.8, M["steel"])
    cyl("lamp", 0, 0, 9.4, 0.3, 0.8, M["cyan_e"], 16)
    note("rib0", (4.4, 0, 9.4), "Ribbed tunnel module (16 long, 8-stud ribs)"); note("pipe-11", (-5.2, -6, 3.6), "Service pipes (blue / orange / steel)")
    note("strip1", (5.6, -6, 0.9), "Amber floor guide strips"); note("floor_grate", (0, -6, 0.45), "Centre grate (Ghost Train access)")
    robot("w", "Cypher", 0, 2, 0.0, z=0.4)

# ------------------------------------------------------------------ INF-11 Elevated Pedestrian Bridge 8 wide × 16 module
def inf11():
    ground("g", -12, 12, -14, 14)
    for y in (-8, 8):
        box(f"pier{y}", -1, 1, y - 1, y + 1, 0, 16, M["graphite"])
    box("deck", -4, 4, -12, 12, 16, 17, M["steel"])
    box("walk", -3.6, 3.6, -12, 12, 17, 17.1, M["floor"])
    for s in (-1, 1):
        box(f"rail{s}", s * 4 - 0.15, s * 4 + 0.15, -12, 12, 17, 20, M["glass"])
        box(f"railtop{s}", s * 4 - 0.25, s * 4 + 0.25, -12, 12, 20, 20.3, M["orange"])
        box(f"edge{s}", s * 3.5 - 0.1, s * 3.5 + 0.1, -12, 12, 17.1, 17.2, M["cyan_e"])
    box("canopy", -4.4, 4.4, -12, 12, 24, 24.5, M["panel"]) if False else None
    note("deck", (4, 0, 16.5), "8-wide deck at +16 (16-stud repeat)"); note("rail1", (4, -6, 20), "Glass balustrade, orange cap rail")
    note("edge1", (3.5, 6, 17.2), "Cyan edge lighting"); note("pier-8", (1, -8, 8), "Piers every 16")
    robot("w1", "Cypher", -1.5, -3, 0.0, z=17.1); robot("w2", "Patch", 1.5, 4, 3.0, z=17.1)

# ------------------------------------------------------------------ INF-12 Monorail Track Module 16 long, 10 rail
def inf12():
    ground("g", -12, 12, -14, 14)
    box("pier", -1.5, 1.5, -1.5, 1.5, 0, 14, M["graphite"])
    box("cap", -5, 5, -2, 2, 14, 15.5, M["graphite"])
    box("beam", -2, 2, -8, 8, 15.5, 19.5, M["graphite"])
    for s in (-1, 1):
        box(f"route{s}", s * 2 - 0.05, s * 2 + 0.05, -8, 8, 17.5, 18.2, M["blue"])
        box(f"power{s}", s * 2.05 - 0.1, s * 2.05 + 0.1, -8, 8, 16, 16.4, M["orange"])
    box("joint", -2.1, 2.1, 7.8, 8, 15.5, 19.5, M["steel"])
    box("walkway", 2, 4.5, -8, 8, 15.5, 15.8, M["grate"]); box("walkrail", 4.4, 4.6, -8, 8, 15.8, 17, M["orange"])
    note("beam", (-2, -6, 19.5), "Straddle beam 4 × 4 (16-stud module)"); note("route1", (2, 0, 18.2), "Blue route light strip")
    note("power1", (2.05, 4, 16.4), "Power rail (orange)"); note("walkway", (4, -6, 15.8), "Service walkway")
    robot("t", "Patch", 3.2, 2, 1.6, z=15.8)

REG = {f"INF-{n:02d}": ("INF", f, {}) for n, f in
       ((1, inf01), (2, inf02), (3, inf03), (4, inf04), (5, inf05), (6, inf06), (7, inf07), (8, inf08),
        (9, inf09), (10, inf10), (11, inf11), (12, inf12))}
