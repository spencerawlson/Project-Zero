"""Weapons & combat equipment blockouts matched to the user's design-sheet panels (19 Nov 2026).
EQP-13 … EQP-25 plus rebuilt EQP-06 (AEGIS-S1) and EQP-07 (energy cell set).
Long axis along Y, business end toward -Y; items rest on z = 0. Cypher (6.0) beside at +Y for the scale view."""
import math
from pz_asset_lib import *
from pz_build_stasis import M

R90X = (math.radians(90), 0, 0)      # cylinder axis → Y

def scale_ref(y):
    robot("scale_cypher", "Cypher", 0, y + 1.0, -math.pi / 2)

def ycyl(name, y0, length, r, m, z=1.0, x=0.0, seg=24, r2=None):
    """Cylinder along Y from y0 toward -Y by `length` (business end at more negative Y)."""
    o = cyl(name, x, y0, z, length, r, m, seg, r2=r2, rot=(math.radians(90), 0, 0))
    return o

def ring_y(name, y, r, t, m, z=1.0, depth=0.25, x=0.0):
    o = tube(name, 0, 0, -depth / 2, depth, r, t, m)
    o.rotation_euler = R90X; o.location = (x, y, z)
    return o

def grip(name, y, z, h=0.9, w=0.32):
    cbox(name, 0, y, z - h / 2, w, w * 1.3, h, M["rubber"], rot=(math.radians(-14), 0, 0))

def gun_body(prefix, y0, y1, z, w, h, m=None):
    """Receiver block between y0 (front) and y1 (rear)."""
    box(prefix, -w / 2, w / 2, y0, y1, z - h / 2, z + h / 2, m or M["white"])

# ------------------------------------------------------------------ EQP-13 VOLT-X Energy Carbine (3.8)
def eqp13():
    grp("body"); Z = 1.1
    gun_body("recv", -0.6, 0.9, Z, 0.45, 0.55)
    box("recv_g", -0.24, 0.24, -0.4, 0.7, Z - 0.3, Z - 0.05, M["graphite"])
    box("cellwin", -0.235, -0.225, -0.2, 0.45, Z - 0.05, Z + 0.12, M["cyan_e"]); box("cellwin2", 0.225, 0.235, -0.2, 0.45, Z - 0.05, Z + 0.12, M["cyan_e"])
    ycyl("barrel", -0.6, 1.0, 0.11, M["graphite"], Z + 0.08); ring_y("muzzle", -1.55, 0.16, 0.06, M["orange"], Z + 0.08)
    box("shroud", -0.2, 0.2, -1.1, -0.6, Z - 0.12, Z + 0.25, M["orange"])
    ycyl("scope", 0.6, 1.0, 0.11, M["graphite"], Z + 0.45); ring_y("scope_lens", -0.42, 0.1, 0.02, M["cyan_e"], Z + 0.45)
    box("scope_mount", -0.06, 0.06, 0.0, 0.3, Z + 0.27, Z + 0.36, M["steel"])
    grip("grip", 0.55, Z - 0.3); grip("fgrip", -0.4, Z - 0.3, 0.6, 0.26)
    box("stock_top", -0.12, 0.12, 0.9, 1.9, Z + 0.05, Z + 0.2, M["orange"]); box("stock_bot", -0.12, 0.12, 1.2, 1.9, Z - 0.5, Z - 0.35, M["orange"])
    box("stock_butt", -0.18, 0.18, 1.8, 1.95, Z - 0.5, Z + 0.2, M["graphite"])
    note("cellwin", (-0.24, 0.1, Z + 0.1), "E-20 cell window (cyan)"); note("scope", (0, 0.1, Z + 0.56), "Long holo scope")
    note("stock_top", (0, 1.4, Z + 0.2), "Skeletal orange stock"); note("muzzle", (0, -1.55, Z + 0.24), "Orange muzzle ring")
    scale_ref(2.0)

# ------------------------------------------------------------------ EQP-14 THUNDER-9 Heavy Ion Cannon (5.8)
def eqp14():
    grp("body"); Z = 1.6
    ycyl("chamber_glass", -0.6, 2.0, 0.62, M["glass"], Z, seg=32)
    ycyl("chamber_core", -0.7, 1.8, 0.34, M["cyan_e"], Z, seg=24)
    for k, y in enumerate((-0.7, -1.6, -2.55)):
        ring_y(f"band{k}", y, 0.7, 0.12, M["orange"] if k != 1 else M["white"], Z, 0.3)
    ring_y("muzzle_ring", -2.9, 0.75, 0.25, M["graphite"], Z, 0.4); ring_y("muzzle_glow", -3.0, 0.5, 0.08, M["cyan_e"], Z, 0.1)
    gun_body("recv", -0.6, 1.6, Z, 0.9, 0.9)
    box("recv_side", -0.47, -0.45, -0.3, 1.2, Z - 0.2, Z + 0.25, M["orange"]); box("recv_side2", 0.45, 0.47, -0.3, 1.2, Z - 0.2, Z + 0.25, M["orange"])
    gear("gear", 0, 0, 0, 0.18, M["orange_e"]) if False else None
    box("handle", -0.08, 0.08, -0.2, 0.9, Z + 0.55, Z + 0.7, M["graphite"]); box("handle_p", -0.08, 0.08, -0.2, -0.05, Z + 0.4, Z + 0.55, M["graphite"])
    grip("grip", 1.0, Z - 0.45, 0.9, 0.36)
    box("stock", -0.35, 0.35, 1.6, 2.6, Z - 0.6, Z + 0.3, M["white"]); box("stock_pad", -0.38, 0.38, 2.55, 2.75, Z - 0.6, Z + 0.3, M["graphite"])
    note("chamber_core", (0.34, -1.6, Z + 0.3), "Ion chamber (cyan core in glass)"); note("muzzle_ring", (0, -2.9, Z + 0.75), "Ring muzzle Ø1.5")
    note("handle", (0, 0.4, Z + 0.7), "Carry handle"); note("stock", (0.35, 2.1, Z), "Heavy white stock")
    scale_ref(2.8)

# ------------------------------------------------------------------ EQP-15 NOVA-3 Precision Energy Rifle (6.0)
def eqp15():
    grp("body"); Z = 1.1
    gun_body("recv", -0.7, 1.0, Z, 0.4, 0.5)
    box("recv_o", -0.21, 0.21, -0.3, 0.6, Z - 0.1, Z + 0.1, M["orange"])
    ycyl("barrel", -0.7, 2.4, 0.1, M["graphite"], Z + 0.05)
    ycyl("shroud", -0.7, 1.0, 0.17, M["white"], Z + 0.05)
    ring_y("lens", -3.15, 0.14, 0.05, M["cyan_e"], Z + 0.05, 0.1)
    ycyl("scope", 0.7, 1.6, 0.2, M["graphite"], Z + 0.55, seg=24); ring_y("scope_lens", -0.92, 0.18, 0.04, M["cyan_e"], Z + 0.55)
    for y in (-0.4, 0.4):
        box(f"mount{y}", -0.06, 0.06, y - 0.06, y + 0.06, Z + 0.25, Z + 0.38, M["steel"])
    grip("grip", 0.75, Z - 0.3)
    box("cell", -0.15, 0.15, -0.2, 0.2, Z - 0.6, Z - 0.25, M["cyan_e"])
    box("stock", -0.15, 0.15, 1.0, 2.8, Z - 0.35, Z + 0.15, M["white"]); box("cheek", -0.16, 0.16, 1.6, 2.4, Z + 0.15, Z + 0.3, M["orange"])
    for s in (-1, 1):
        cbox(f"bipod{s}", s * 0.25, -1.6, Z - 0.45, 0.06, 0.06, 0.9, M["graphite"], rot=(0, math.radians(s * 20), 0))
    note("scope", (0, 0, Z + 0.75), "Long-range scope (large objective)"); note("lens", (0, -3.15, Z + 0.2), "Cyan muzzle lens")
    note("cell", (0.15, 0, Z - 0.45), "E-60 cell"); note("bipod1", (0.25, -1.6, Z - 0.6), "Folding bipod")
    scale_ref(2.9)

# ------------------------------------------------------------------ EQP-16 TITAN BREAKER Heavy Hammer (5.6)
def eqp16():
    grp("body"); Z = 0.9
    ycyl("haft", 2.4, 4.4, 0.12, M["graphite"], Z, seg=16)
    for k, y in enumerate((1.6, 0.4, -0.9)):
        ring_y(f"band{k}", y, 0.16, 0.06, M["orange"], Z, 0.35)
    ycyl("pommel", 2.75, 0.4, 0.22, M["white"], Z, seg=8)
    head = cyl("head", 0, -2.6, Z - 0.95, 1.9, 0.75, M["white"], 8)
    cyl("head_core", 0, -2.6, Z - 0.6, 1.2, 0.79, M["cyan_e"], 8).scale = (1, 0.55, 1)
    for s in (-1, 1):
        cyl(f"face{s}", 0, -2.6, Z + s * 0.95 - (0.2 if s > 0 else 0), 0.2, 0.62, M["graphite"], 8)
    cbox("head_o", 0, -2.6, Z, 0.4, 1.62, 0.5, M["orange"])
    note("head_core", (0.4, -2.6, Z + 0.3), "Armoured head with cyan impact core"); note("band1", (0, 0.4, Z + 0.25), "Orange grip bands")
    note("haft", (0, 1.0, Z + 0.15), "Graphite haft 4.4"); note("pommel", (0, 2.9, Z + 0.25), "E-50 cell pommel")
    scale_ref(3.0)

# ------------------------------------------------------------------ EQP-17 ARC CLAWS (pair, 1.8 long)
def eqp17():
    grp("body")
    for s, xo in ((-1, -0.8), (1, 0.8)):
        ycyl(f"gaunt{s}", 0.7, 1.0, 0.32, M["white"], 0.45, x=xo, seg=8)
        ycyl(f"cuff{s}", 0.9, 0.25, 0.35, M["orange"], 0.45, x=xo, seg=8)
        box(f"plate{s}", xo - 0.2, xo + 0.2, -0.3, 0.6, 0.72, 0.82, M["graphite"])
        box(f"led{s}", xo - 0.12, xo + 0.12, -0.1, 0.4, 0.82, 0.86, M["cyan_e"])
        for k, dx in enumerate((-0.18, 0, 0.18)):
            cbox(f"blade{s}{k}", xo + dx, -0.85, 0.45 + (0.05 if k == 1 else 0), 0.05, 1.2, 0.16, M["cyan_e"], rot=(math.radians(-12), 0, math.radians(dx * 25)))
    note("blade10", (0.8, -1.3, 0.55), "3 retractable hard-light blades"); note("led1", (0.8, 0.1, 0.86), "Charge LED (E-15)")
    note("cuff-1", (-0.8, 0.8, 0.8), "Wrist cuff (orange)"); note("gaunt1", (1.1, 0.3, 0.45), "Gauntlet shell")
    scale_ref(1.4)

# ------------------------------------------------------------------ EQP-18 SHOCK STAFF (7.0)
def eqp18():
    grp("body"); Z = 0.6
    ycyl("shaft", 2.9, 5.8, 0.1, M["graphite"], Z, seg=16)
    for k, y in enumerate((1.6, 0.6, -0.6, -1.6)):
        ring_y(f"seg{k}", y, 0.14, 0.05, M["white"] if k % 2 else M["orange"], Z, 0.25)
    for s in (-1, 1):
        y = s * 3.1
        ycyl(f"emit{s}", y + 0.35 if s < 0 else y + 0.35, 0.7, 0.28, M["glass"], Z, seg=20)
        ycyl(f"emitc{s}", y + 0.3, 0.6, 0.16, M["cyan_e"], Z, seg=16)
        ring_y(f"emitr{s}", y + 0.4 * (1 if s < 0 else -1), 0.32, 0.08, M["orange"], Z, 0.12)
        ring_y(f"emitr2{s}", y - 0.4 * (1 if s < 0 else -1), 0.32, 0.08, M["orange"], Z, 0.12)
    note("emitc-1", (0, -3.1, Z + 0.3), "Electro emitter (stun)"); note("emitc1", (0, 3.1, Z + 0.3), "Twin emitter")
    note("seg1", (0, 0.6, Z + 0.15), "Segmented shaft (grip zones)")
    scale_ref(3.6)

# ------------------------------------------------------------------ EQP-19 BASTION-X Heavy Riot Shield (4.5 tall)
def eqp19():
    grp("body")
    box("slab", -1.4, 1.4, -0.15, 0.15, 0, 4.5, M["white"])
    for (x0, x1, z0, z1) in ((-1.55, -1.3, 0, 4.5), (1.3, 1.55, 0, 4.5), (-1.55, 1.55, 4.3, 4.55), (-1.55, 1.55, -0.05, 0.25)):
        box(f"rim{x0}{z0}", x0, x1, -0.22, 0.22, z0, z1, M["graphite"])
    box("visor", -0.9, 0.9, -0.2, -0.15, 3.3, 3.75, M["cyan_e"])
    gear("gear", 0, -0.2, 1.9, 0.5, M["orange_e"])
    box("band", -1.4, 1.4, -0.18, -0.15, 0.7, 0.95, M["orange"])
    box("handle", -0.4, 0.4, 0.2, 0.45, 2.0, 2.3, M["rubber"])
    note("visor", (0, -0.2, 3.75), "Cyan visor slot"); note("gear", (0.5, -0.2, 1.9), "Resistance gear emblem")
    note("rim1.3-0.05", (1.5, 0, 0.2), "Graphite impact rim"); note("handle", (0, 0.4, 2.3), "Rear handle")
    scale_ref(1.0)

# ------------------------------------------------------------------ EQP-20 DOME-4 Portable Shield Projector (2.5)
def eqp20():
    grp("body")
    cyl("puck", 0, 0, 0.6, 0.6, 1.1, M["white"], 8)
    cyl("puck_o", 0, 0, 0.9, 0.18, 1.14, M["orange"], 8)
    cyl("top", 0, 0, 1.2, 0.2, 0.75, M["graphite"], 24); tube("ring", 0, 0, 1.4, 0.12, 0.7, 0.18, M["cyan_e"])
    cyl("emit", 0, 0, 1.3, 0.25, 0.35, M["cyan_e"], 24)
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        cbox(f"leg{k}", 1.05 * math.cos(a), 1.05 * math.sin(a), 0.45, 0.22, 0.22, 1.0, M["graphite"], rot=(0, math.radians(35), a))
        box(f"foot{k}", 1.45 * math.cos(a) - 0.18, 1.45 * math.cos(a) + 0.18, 1.45 * math.sin(a) - 0.18, 1.45 * math.sin(a) + 0.18, 0, 0.1, M["orange"])
    note("ring", (0.7, 0, 1.55), "Dome emitter ring (projects r 8)"); note("puck_o", (1.14, 0, 1.0), "Orange body band")
    note("leg0", (0.8, 0.8, 0.5), "Four deploy legs"); note("emit", (0, 0, 1.55), "E-80 core")
    scale_ref(1.8)

# ------------------------------------------------------------------ EQP-21 EMP-6 Disruption Launcher (4.0)
def eqp21():
    grp("body"); Z = 1.2
    ycyl("barrel", -0.2, 1.7, 0.42, M["graphite"], Z, seg=24)
    ring_y("muzzle", -1.95, 0.48, 0.14, M["orange"], Z, 0.3); ring_y("glow", -2.0, 0.3, 0.07, M["cyan_e"], Z, 0.08)
    cyl("lens", 0, -1.9, Z, 0.05, 0.3, M["glass"], 24, rot=R90X).location = (0, -1.95, Z)
    ring_y("band", -1.0, 0.45, 0.06, M["white"], Z, 0.3)
    gun_body("body", -0.2, 1.4, Z, 0.7, 0.7)
    box("body_o", -0.36, 0.36, 0.0, 0.5, Z + 0.1, Z + 0.36, M["orange"])
    grip("grip", 0.9, Z - 0.35); box("cell", -0.18, 0.18, 0.2, 0.6, Z - 0.65, Z - 0.35, M["cyan_e"])
    box("stock", -0.2, 0.2, 1.4, 2.0, Z - 0.35, Z + 0.2, M["white"])
    note("muzzle", (0, -1.95, Z + 0.62), "Wide EMP ring muzzle"); note("cell", (0.18, 0.4, Z - 0.5), "E-40 cell")
    note("band", (0.45, -1.0, Z), "White barrel band"); note("body_o", (0, 0.25, Z + 0.36), "Orange receiver panel")
    scale_ref(2.1)

# ------------------------------------------------------------------ EQP-22 GRAVITY-8 Gravity Manipulator (4.0)
def eqp22():
    grp("body"); Z = 1.4
    ring_y("ring", -1.4, 0.95, 0.18, M["graphite"], Z, 0.3)
    ring_y("halo", -1.4, 1.1, 0.08, M["orange"], Z, 0.12)
    sphere("core", 0, -1.4, Z, 0.32, M["cyan_e"])
    for k in range(3):
        a = math.pi / 2 + k * 2 * math.pi / 3
        cbox(f"spoke{k}", 0.6 * math.cos(a), -1.4, Z + 0.6 * math.sin(a), 0.55, 0.12, 0.1, M["steel"], rot=(0, -a, 0))
    gun_body("body", -1.1, 0.9, Z, 0.55, 0.6)
    box("body_o", -0.29, 0.29, -0.8, 0.3, Z + 0.05, Z + 0.3, M["orange"])
    ycyl("scope", 0.4, 0.8, 0.1, M["graphite"], Z + 0.45)
    grip("grip", 0.5, Z - 0.3); box("stock", -0.15, 0.15, 0.9, 1.8, Z - 0.35, Z + 0.15, M["white"])
    note("core", (0, -1.4, Z + 0.35), "Graviton core"); note("halo", (1.1, -1.4, Z), "Orange halo ring (lift field)")
    note("scope", (0, 0, Z + 0.56), "Targeting optic"); note("stock", (0, 1.4, Z + 0.15), "White stock")
    scale_ref(1.9)

# ------------------------------------------------------------------ EQP-23 PULSE-MINE (1.5 wide)
def eqp23():
    grp("body")
    cyl("body", 0, 0, 0.15, 0.3, 0.55, M["white"], 6)
    cyl("top", 0, 0, 0.45, 0.1, 0.4, M["graphite"], 6); cyl("eye", 0, 0, 0.55, 0.06, 0.22, M["cyan_e"], 20)
    for k in range(6):
        a = k * math.pi / 3
        cbox(f"leg{k}", 0.62 * math.cos(a), 0.62 * math.sin(a), 0.12, 0.42, 0.14, 0.1, M["graphite"], rot=(0, math.radians(-15), a))
        box(f"tip{k}", 0.82 * math.cos(a) - 0.07, 0.82 * math.cos(a) + 0.07, 0.82 * math.sin(a) - 0.07, 0.82 * math.sin(a) + 0.07, 0, 0.1, M["orange"])
    note("eye", (0, 0, 0.61), "Proximity sensor (cyan)"); note("leg0", (0.62, 0, 0.17), "Six clamp legs")
    note("body", (0.55, 0, 0.3), "Low-profile hex body")
    scale_ref(1.0)

# ------------------------------------------------------------------ EQP-24 OVERDRIVE CORE (1.2 tall)
def eqp24():
    grp("body")
    cyl("base", 0, 0, 0, 0.18, 0.42, M["graphite"], 16); cyl("cap", 0, 0, 1.0, 0.2, 0.42, M["graphite"], 16)
    cyl("glow", 0, 0, 0.18, 0.82, 0.26, M["cyan_e"], 16); tube("glass", 0, 0, 0.18, 0.82, 0.36, 0.04, M["glass"])
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        box(f"bar{k}", 0.37 * math.cos(a) - 0.05, 0.37 * math.cos(a) + 0.05, 0.37 * math.sin(a) - 0.05, 0.37 * math.sin(a) + 0.05, 0.18, 1.0, M["orange"])
    cyl("plug", 0, 0, 1.2, 0.12, 0.15, M["steel"], 12)
    note("glow", (0.26, 0, 0.6), "Overdrive column"); note("bar0", (0.26, 0.26, 0.9), "Orange cage"); note("plug", (0, 0, 1.32), "Plug-in socket")
    scale_ref(0.8)

# ------------------------------------------------------------------ EQP-25 SENTINEL DRONE (3.0 wide)
def eqp25():
    grp("body")
    sphere("shell", 0, 0, 1.6, 0.6, M["white"])
    cyl("eye_ring", 0, -0.55, 1.6, 0.12, 0.38, M["graphite"], 24, rot=R90X).location = (0, -0.58, 1.6)
    cyl("eye", 0, -0.62, 1.6, 0.06, 0.24, M["cyan_e"], 24, rot=R90X).location = (0, -0.66, 1.6)
    cbox("band", 0, 0, 1.6, 1.25, 1.25, 0.18, M["orange"])
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        x, y = 1.05 * math.cos(a), 1.05 * math.sin(a)
        cbox(f"arm{k}", x * 0.55, y * 0.55, 1.6, 0.9, 0.12, 0.1, M["graphite"], rot=(0, 0, a))
        tube(f"duct{k}", x, y, 1.45, 0.3, 0.38, 0.08, M["white"]); tube(f"ductb{k}", x, y, 1.6, 0.06, 0.39, 0.06, M["orange"])
        cyl(f"rotor{k}", x, y, 1.58, 0.03, 0.3, M["panel"], 16)
    for s in (-1, 1):
        cbox(f"fin{s}", s * 0.25, 0.2, 2.25, 0.08, 0.3, 0.6, M["graphite"], rot=(0, math.radians(s * 15), 0))
    cbox("chin", 0, -0.1, 0.95, 0.15, 0.15, 0.3, M["orange"])
    note("eye", (0, -0.66, 1.85), "Cyan sensor eye (family face)"); note("duct0", (0.74, 0.74, 1.8), "Quad ducted rotors")
    note("fin1", (0.25, 0.2, 2.5), "Antenna fins"); note("band", (0.62, 0, 1.6), "Mini-shield band (orange)")
    scale_ref(1.6)

# ------------------------------------------------------------------ EQP-06 AEGIS-S1 Deployable Energy Shield (rebuilt)
def eqp06b():
    grp("body")
    for k in range(3):
        a = math.pi / 2 + k * 2 * math.pi / 3
        cbox(f"leg{k}", 0.5 * math.cos(a), 0.6 + 0.5 * math.sin(a), 0.6, 0.15, 0.15, 1.3, M["graphite"], rot=(math.radians(-25) * math.sin(a), math.radians(25) * math.cos(a), 0))
    box("emitter", -0.35, 0.35, 0.2, 1.0, 1.1, 1.9, M["white"]); box("emitter_o", -0.36, 0.36, 0.2, 0.4, 1.2, 1.8, M["orange"])
    box("emit_lens", -0.25, 0.25, 0.16, 0.2, 1.35, 1.65, M["cyan_e"])
    wall = cyl("wall", 0, 0, 0, 0.12, 1.9, M["glass"], 6)
    wall.rotation_euler = (math.radians(90), 0, math.radians(0)); wall.location = (0, -0.6, 3.0)
    edge = tube("wall_edge", 0, 0, -0.08, 0.16, 1.95, 0.1, M["cyan_e"]); edge.rotation_euler = (math.radians(90), 0, 0)
    edge.location = (0, -0.6, 3.0)
    note("wall", (1.2, -0.6, 3.6), "Hex hard-light wall (absorbs energy fire)"); note("emitter_o", (0.36, 0.3, 1.8), "Emitter head")
    note("leg0", (0, 1.1, 0.6), "Tripod deploy legs"); note("emit_lens", (0, 0.16, 1.5), "E-25 cell emitter")
    scale_ref(1.4)

# ------------------------------------------------------------------ EQP-07 Energy Cell System E-10 … E-100 (rebuilt)
def eqp07b():
    grp("body")
    sizes = [("E-10", 0.6), ("E-20", 0.7), ("E-40", 0.85), ("E-60", 1.0), ("E-80", 1.2), ("E-100", 1.45)]
    x = -2.6
    for k, (lab, h) in enumerate(sizes):
        r = 0.18 + k * 0.03
        cyl(f"c{k}_base", x, 0, 0, 0.12, r + 0.04, M["graphite"], 16)
        cyl(f"c{k}_glow", x, 0, 0.12, h - 0.24, r * 0.7, M["cyan_e"], 16)
        tube(f"c{k}_glass", x, 0, 0.12, h - 0.24, r, 0.03, M["glass"])
        cyl(f"c{k}_cap", x, 0, h - 0.12, 0.12, r + 0.04, M["orange"], 16)
        note(f"c{k}_cap", (x, 0, h), lab)
        x += 0.5 + r * 2
    scale_ref(0.6)

REG = {f"EQP-{n}": ("EQP", f, {"hero_dir": (-0.9, -1.0, 0.55), "lens": 50}) for n, f in
       ((13, eqp13), (14, eqp14), (15, eqp15), (16, eqp16), (17, eqp17), (18, eqp18), (19, eqp19),
        (20, eqp20), (21, eqp21), (22, eqp22), (23, eqp23), (24, eqp24), (25, eqp25))}
REG["EQP-06"] = ("EQP", eqp06b, {"hero_dir": (-0.9, -1.0, 0.55), "lens": 50})
REG["EQP-07"] = ("EQP", eqp07b, {"hero_dir": (-0.3, -1.0, 0.45), "lens": 50})
