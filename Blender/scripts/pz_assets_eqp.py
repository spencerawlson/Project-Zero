"""EQP-01 … EQP-12 hand-held / module equipment. Long axis along Y, business end toward -Y.
Items rest on the ground (z = 0). A Cypher instance (6.0 studs) stands at +X for the scale view only."""
import math
from pz_asset_lib import *
from pz_build_stasis import M

def scale_ref(x):
    robot("scale_cypher", "Cypher", 0, x + 1.0, -math.pi / 2)   # beside the item along +Y, facing the side camera

def grip(name, x, y, z, h=1.0, w=0.35):
    cbox(name, x, y, z - h / 2, w, w * 1.2, h, M["rubber"], rot=(math.radians(-12), 0, 0))

# ------------------------------------------------------------------ EQP-01 Repair Tool (~3 studs)
def eqp01():
    grp("body")
    cbox("body", 0, 0, 1.0, 0.7, 2.2, 0.8, M["white"])
    cbox("shell_o", 0, 0.6, 1.0, 0.75, 0.8, 0.85, M["orange"])
    grip("grip", 0, 0.5, 0.7, 1.0)
    cyl("emitter", 0, -1.1, 1.0, 0.6, 0.25, M["cyan_e"], 16, rot=(math.radians(90), 0, 0)).location = (0, -1.25, 1.0)
    for s in (-1, 1):
        cbox(f"jaw{s}", s * 0.35, -1.7, 1.0, 0.18, 0.9, 0.3, M["orange"], rot=(0, 0, math.radians(s * 15)))
    cbox("battery", 0, 1.0, 1.55, 0.5, 0.6, 0.3, M["graphite"]); cbox("battery_led", 0, 1.0, 1.72, 0.4, 0.4, 0.05, M["cyan_e"])
    note("emitter", (0, -1.4, 1.0), "Repair beam emitter (cyan)"); note("jaw1", (0.4, -1.9, 1.0), "Wrench jaws (orange)")
    note("battery_led", (0, 1.0, 1.75), "Swappable power cell + charge LED"); note("grip", (0, 0.5, 0.3), "Rubber grip (R15 RightHand attach)")
    scale_ref(4)

# ------------------------------------------------------------------ EQP-02 Energy Blade (~4 studs)
def eqp02():
    grp("body")
    cyl("hilt", 0, 1.2, 0.3, 1.2, 0.18, M["graphite"], 16, rot=(math.radians(90), 0, 0)).location = (0, 1.4, 0.3)
    cbox("guard", 0, 0.75, 0.3, 0.9, 0.18, 0.35, M["orange"])
    cbox("emit", 0, 0.6, 0.3, 0.3, 0.2, 0.25, M["cyan_e"])
    cbox("blade", 0, -1.0, 0.3, 0.1, 3.2, 0.32, M["cyan_e"])
    cbox("blade_core", 0, -1.0, 0.3, 0.12, 3.0, 0.08, M["white"])
    cyl("pommel", 0, 2.05, 0.3, 0.2, 0.22, M["orange"], 16, rot=(math.radians(90), 0, 0)).location = (0, 2.1, 0.3)
    note("blade", (0, -1.8, 0.45), "Hard-light blade 3.2 (cyan, emissive)"); note("guard", (0.45, 0.75, 0.3), "Orange cross-guard")
    note("hilt", (0, 1.4, 0.48), "Graphite hilt with grip rings"); note("pommel", (0, 2.1, 0.3), "Energy-cell pommel")
    scale_ref(3)

# ------------------------------------------------------------------ EQP-03 Pulse Rifle (~4 studs)
def eqp03():
    grp("body")
    cbox("receiver", 0, 0.2, 1.2, 0.5, 2.0, 0.7, M["graphite"])
    cbox("shroud", 0, -1.2, 1.25, 0.45, 1.2, 0.5, M["white"])
    for k in range(3):
        cyl(f"coil{k}", 0, -1.0 - k * 0.35, 1.25, 0.12, 0.3, M["cyan_e"], 16, rot=(math.radians(90), 0, 0)).location = (0, -0.9 - k * 0.35, 1.25)
    cyl("barrel", 0, -2.0, 1.25, 0.9, 0.12, M["steel"], 12, rot=(math.radians(90), 0, 0)).location = (0, -2.2, 1.25)
    cbox("stock", 0, 1.6, 1.0, 0.4, 1.0, 0.6, M["orange"])
    grip("grip", 0, 0.5, 0.8, 0.8)
    cbox("mag", 0, -0.2, 0.75, 0.3, 0.4, 0.5, M["cyan_e"])
    cbox("scope", 0, 0.1, 1.75, 0.25, 0.9, 0.25, M["panel"]); cbox("scope_l", 0, -0.36, 1.75, 0.2, 0.02, 0.2, M["cyan_e"])
    note("coil1", (0, -1.35, 1.5), "Pulse accelerator coils"); note("mag", (0, -0.2, 0.5), "Energy cell magazine")
    note("stock", (0, 1.6, 1.3), "Orange stock (Resistance colour)"); note("scope", (0, 0.1, 1.9), "Holo sight")
    scale_ref(3)

# ------------------------------------------------------------------ EQP-04 Scanner (~2 studs)
def eqp04():
    grp("body")
    cbox("body", 0, 0.2, 0.9, 0.6, 1.2, 0.5, M["white"])
    tube("ring", 0, 0, -0.1, 0.2, 0.55, 0.12, M["cyan_e"]).rotation_euler = (math.radians(90), 0, 0)
    bpy_set_loc("ring", (0, -0.55, 1.0))
    cyl("lens", 0, -0.5, 1.0, 0.1, 0.4, M["glass"], 24, rot=(math.radians(90), 0, 0)).location = (0, -0.5, 1.0)
    grip("grip", 0, 0.5, 0.65, 0.7)
    cbox("screen", 0, 0.45, 1.16, 0.45, 0.6, 0.03, M["cyan_soft"])
    note("ring", (0, -0.6, 1.55), "Scan ring emitter (Pulse Scan)"); note("screen", (0, 0.45, 1.2), "Top readout screen")
    note("grip", (0, 0.5, 0.3), "Pistol grip")
    scale_ref(2.5)

def bpy_set_loc(name, loc):
    import bpy
    bpy.data.objects[name].location = loc

# ------------------------------------------------------------------ EQP-05 Hacking Terminal (tablet 2 × 1.4)
def eqp05():
    grp("body")
    cbox("slab", 0, 0, 0.1, 2.0, 1.4, 0.16, M["graphite"])
    cbox("screen", 0, -0.02, 0.19, 1.7, 1.1, 0.02, M["cyan_soft"])
    for s in (-1, 1):
        cbox(f"handle{s}", s * 1.05, 0, 0.12, 0.2, 1.0, 0.24, M["orange"])
    cyl("antenna", 0.8, 0.6, 0.2, 0.6, 0.04, M["steel"], 8); sphere("ant_tip", 0.8, 0.6, 0.82, 0.07, M["red_e"])
    cbox("port", 0, 0.72, 0.1, 0.4, 0.06, 0.08, M["cyan_e"])
    note("screen", (0, 0, 0.22), "Hack UI screen (System Override)"); note("handle1", (1.05, 0, 0.24), "Orange grip rails")
    note("antenna", (0.8, 0.6, 0.8), "Uplink antenna"); note("port", (0, 0.75, 0.15), "Data spike port")
    scale_ref(2.5)

# ------------------------------------------------------------------ EQP-06 Shield Generator (module 2)
def eqp06():
    grp("body")
    cyl("base", 0, 0, 0, 0.4, 0.9, M["graphite"], 6)
    cyl("core", 0, 0, 0.4, 0.5, 0.5, M["cyan_e"], 6)
    cyl("cap", 0, 0, 0.9, 0.25, 0.75, M["orange"], 6)
    for k in range(3):
        a = 2 * math.pi * k / 3
        cbox(f"fin{k}", 0.75 * math.cos(a), 0.75 * math.sin(a), 0.5, 0.15, 0.4, 0.8, M["steel"], rot=(0, 0, a))
    grp("roof")
    sphere("field", 0, 0, 2.3, 2.25, M["glass"])
    note("core", (0.5, 0, 0.6), "Hex energy core"); note("field", (0, -1.7, 3.2), "Projected shield bubble (r 2.25)")
    note("cap", (0, 0, 1.15), "Orange emitter cap")
    scale_ref(4)

# ------------------------------------------------------------------ EQP-07 Power Core (module 1.5)
def eqp07():
    grp("body")
    cyl("bot", 0, 0, 0, 0.3, 0.55, M["graphite"], 16)
    cyl("glow", 0, 0, 0.3, 0.9, 0.35, M["cyan_e"], 16)
    tube("cage", 0, 0, 0.3, 0.9, 0.5, 0.06, M["glass"])
    for k in range(4):
        a = math.pi / 2 * k + math.pi / 4
        cbox(f"bar{k}", 0.5 * math.cos(a), 0.5 * math.sin(a), 0.75, 0.1, 0.1, 0.9, M["orange"])
    cyl("top", 0, 0, 1.2, 0.3, 0.55, M["graphite"], 16)
    cyl("handle", 0, 0, 1.5, 0.12, 0.25, M["steel"], 12)
    note("glow", (0.35, 0, 0.8), "Cyan energy column (charge level)"); note("bar0", (0.4, 0.4, 1.1), "Orange guard bars")
    note("handle", (0, 0, 1.62), "Carry handle / socket key")
    scale_ref(2)

# ------------------------------------------------------------------ EQP-08 Grappling Device (~3 studs)
def eqp08():
    grp("body")
    cbox("body", 0, 0.3, 0.9, 0.55, 1.6, 0.6, M["graphite"])
    cyl("drum", 0, 0.6, 0.9, 0.5, 0.35, M["orange"], 20, rot=(0, math.radians(90), 0)).location = (0, 0.6, 0.9)
    grip("grip", 0, 0.7, 0.6, 0.7)
    cyl("barrel", 0, -0.7, 0.9, 0.6, 0.18, M["steel"], 12, rot=(math.radians(90), 0, 0)).location = (0, -0.75, 0.9)
    for k in range(3):
        a = 2 * math.pi * k / 3
        cbox(f"claw{k}", 0.22 * math.cos(a), -1.25, 0.9 + 0.22 * math.sin(a), 0.08, 0.45, 0.08, M["cyan_e"], rot=(math.radians(25) * math.sin(a), 0, 0))
    note("claw0", (0.22, -1.3, 0.9), "3-prong magnetic claw"); note("drum", (0.3, 0.6, 0.9), "Cable drum (orange)")
    note("grip", (0, 0.7, 0.25), "Wrist/hand grip")
    scale_ref(3)

# ------------------------------------------------------------------ EQP-09 Medical Repair Drone (2 × 2 × 1) — family screen face
def eqp09():
    grp("body")
    sphere("shell", 0, 0, 0.9, 0.7, M["white"])
    cbox("visor", 0, -0.55, 0.95, 0.8, 0.2, 0.45, M["graphite"])
    for x in (-0.18, 0.18):
        sphere(f"eye{x}", x, -0.66, 0.98, 0.07, M["cyan_e"])
    cbox("cross_v", 0, 0.68, 1.0, 0.1, 0.05, 0.36, M["orange_e"]); cbox("cross_h", 0, 0.68, 1.0, 0.36, 0.05, 0.1, M["orange_e"])
    for s in (-1, 1):
        cbox(f"arm{s}", s * 0.8, 0, 1.0, 0.5, 0.15, 0.1, M["graphite"])
        tube(f"duct{s}", s * 1.15, 0, 0.95, 0.2, 0.38, 0.06, M["orange"])
        cyl(f"rotor{s}", s * 1.15, 0, 1.05, 0.03, 0.32, M["panel"], 16)
    cyl("injector", 0, 0, 0.1, 0.25, 0.07, M["cyan_e"], 8)
    note("eye0.18", (0.18, -0.7, 1.0), "Family screen-face (cyan eyes = friendly)"); note("cross_v", (0, 0.7, 1.2), "Medical cross (orange)")
    note("duct1", (1.15, 0, 1.15), "Twin ducted rotors"); note("injector", (0, 0, 0.25), "Repair injector")
    scale_ref(3)

# ------------------------------------------------------------------ EQP-10 Portable Charging Unit (2 × 1.5 × 2)
def eqp10():
    grp("body")
    box("case", -1.0, 1.0, -0.75, 0.75, 0, 1.6, M["graphite"])
    box("corners", -1.05, 1.05, -0.8, 0.8, 0, 0.2, M["orange"])
    box("meter", -0.6, 0.6, -0.78, -0.75, 0.5, 1.2, M["panel"])
    for k in range(5):
        box(f"bar{k}", -0.5 + k * 0.21, -0.35 + k * 0.21, -0.8, -0.78, 0.6, 1.1, M["cyan_e"] if k < 4 else M["panel"])
    cyl("handle", 0, 0, 1.6, 0.35, 0.08, M["steel"], 8).scale = (6, 1, 1)
    cyl("reel", 1.05, 0, 0.8, 0.3, 0.45, M["orange"], 20, rot=(0, math.radians(90), 0)).location = (1.15, 0, 0.8)
    note("bar2", (0, -0.8, 1.1), "Charge meter (4/5 bars)"); note("reel", (1.3, 0, 0.8), "Retractable charge cable")
    note("handle", (0, 0, 1.95), "Carry handle")
    scale_ref(3)

# ------------------------------------------------------------------ EQP-11 Memory Storage Module (0.6 × 0.4 × 1)
def eqp11():
    grp("body")
    box("body", -0.3, 0.3, -0.2, 0.2, 0, 1.0, M["graphite"])
    box("window", -0.22, 0.22, -0.21, -0.19, 0.25, 0.8, M["violet_e"])
    box("contacts", -0.25, 0.25, -0.15, 0.15, -0.05, 0.0, M["amber_e"])
    box("cap", -0.32, 0.32, -0.22, 0.22, 0.9, 1.05, M["orange"])
    text("label", "MEM", 0, -0.215, 0.13, 0.12, M["cyan_e"])
    note("window", (0, -0.22, 0.6), "Violet memory crystal window"); note("cap", (0, 0, 1.05), "Orange eject cap")
    note("contacts", (0, 0, -0.05), "Gold contacts (archive slots)")
    scale_ref(1.5)

# ------------------------------------------------------------------ EQP-12 Industrial Welding Tool (~3 studs)
def eqp12():
    grp("body")
    cbox("body", 0, 0.3, 1.0, 0.5, 1.6, 0.55, M["yellow"])
    cyl("tank", 0, 0.7, 1.45, 0.7, 0.25, M["steel"], 16, rot=(math.radians(90), 0, 0)).location = (0, 0.7, 1.55)
    grip("grip", 0, 0.6, 0.7, 0.7)
    cyl("nozzle", 0, -0.7, 1.0, 0.8, 0.12, M["graphite"], 12, r2=0.07, rot=(math.radians(90), 0, 0)).location = (0, -0.85, 1.0)
    sphere("flame", 0, -1.35, 1.0, 0.12, M["orange_e"])
    cbox("guard", 0, -0.45, 1.0, 0.7, 0.05, 0.7, M["graphite"])
    note("flame", (0, -1.4, 1.0), "Arc tip (orange glow)"); note("tank", (0, 0.7, 1.85), "Gas cartridge")
    note("guard", (0.35, -0.45, 1.3), "Spark guard"); note("body", (0.25, 0.3, 1.3), "Factory-yellow housing")
    scale_ref(3)

REG = {f"EQP-{n:02d}": ("EQP", f, {"hero_dir": (-0.9, -1.0, 0.55), "lens": 50}) for n, f in
       ((1, eqp01), (2, eqp02), (3, eqp03), (4, eqp04), (5, eqp05), (6, eqp06), (7, eqp07), (8, eqp08),
        (9, eqp09), (10, eqp10), (11, eqp11), (12, eqp12))}
