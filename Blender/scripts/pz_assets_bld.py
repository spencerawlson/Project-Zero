"""BLD-02 … BLD-15 procedural blockouts. Footprints centred on origin; front (S) faces -Y.
Sizes follow the Asset Reference Bible targets where given; otherwise design assumptions (pz_inventory)."""
import math
from pz_asset_lib import *
from pz_build_stasis import M

def _robots(*items):
    for k, (f, x, y, rz) in enumerate(items):
        robot(f"bot{k}", f, x, y, rz)

# ------------------------------------------------------------------ BLD-02 Resistance Workshop 100×80×28
def bld02():
    CUT_H[0] = 10
    ground("g", -80, 80, -75, 70)
    shell("hall", -50, 50, -40, 40, 18, openings=[("S", 0, 36, 15), ("E", 20, 6, 10), ("W", -20, 6, 10)])
    vault("hall_vault", 0, 30, 10, 18.8, -40, 40, 1.0, M["panel"]); bpy_mark_roof("hall_vault")
    for y in range(-40, 41, 10):
        vault(f"rib{y}", 0, 31, 11, 18.8, y - 0.5, y + 0.5, 1.2, M["graphite"]); bpy_mark_roof(f"rib{y}")
    pilasters("pS", "S", -50, -18, 18, -50, 50, -40, 40); pilasters("pS2", "S", 18, 50, 18, -50, 50, -40, 40)
    win_band("wW", "W", -36, 36, 9, 11, -50, 50, -40, 40, step=8); win_band("wE", "E", -36, 36, 9, 11, -50, 50, -40, 40, step=8)
    box("canopy", -22, 22, -48, -40, 15.5, 16.3, M["orange"])
    for x in (-21, 21):
        box(f"canopy_post{x}", x - 0.5, x + 0.5, -48, -47, 0, 15.5, M["graphite"])
    box("canopy_light", -20, 20, -47.8, -47.4, 15.2, 15.5, M["amber_e"])
    gear("gear", 0, -40.6, 21.5, 3.2)
    text("sign", "RESISTANCE WORKSHOP", 0, -40.7, 16.8, 1.6, M["cyan_e"])
    note("bay", (0, -40, 8), "Open repair bay 36 × 15 (no door: always welcoming)")
    note("gear", (0, -40.6, 21.5), "Orange gear emblem — Resistance identity")
    # roof crane (Design Bible art)
    grp("roof")
    box("crane_tower", 30, 33, 20, 23, 18.8, 42, M["yellow"])
    box("crane_jib", 4, 46, 20.8, 22.2, 40, 41.6, M["yellow"])
    box("crane_hook", 8, 9, 21, 22, 30, 40, M["steel"])
    note("crane", (31.5, 21.5, 42), "Rooftop salvage crane (animated jib)")
    grp("body")
    # interior
    grp("interior")
    cyl("holo_base", 0, 0, 0, 0.8, 7, M["graphite"], 40)
    cyl("holo_ring", 0, 0, 0.8, 0.25, 6.5, M["cyan_e"], 40)
    for k in range(6):
        a = 2 * math.pi * k / 6
        cyl(f"holo_post{k}", 6.6 * math.cos(a), 6.6 * math.sin(a), 0.8, 8, 0.18, M["cyan_e"], 8)
    tube("holo_halo", 0, 0, 9.4, 0.3, 6.8, 0.4, M["cyan_e"])
    robot("holo_preview", "Cypher", 0, 0, 0.3, z=1.05)
    note("holo", (0, 0, 9.7), "Holo customization platform: previews the player's robot")
    for k, x in enumerate((-36, -24, 24, 36)):
        box(f"bench{k}", x - 4, x + 4, 22, 27, 0, 3.4, M["graphite"])
        box(f"bench_top{k}", x - 4.2, x + 4.2, 21.8, 27.2, 3.4, 3.7, M["steel"])
        box(f"arm{k}", x - 0.6, x + 0.6, 25, 26.2, 3.7, 9, M["orange"])
        cbox(f"arm2{k}", x, 24, 9.5, 1.0, 5.0, 1.0, M["orange"], rot=(math.radians(30), 0, 0))
    note("bench0", (-36, 24, 9), "Workbench + mechanical arm ×4 (crafting)")
    box("mission_term", 36, 42, -10, -4, 0, 4, M["graphite"]); box("mission_scr", 35.9, 36, -9.5, -4.5, 2.5, 6, M["cyan_soft"])
    note("mission_term", (36, -7, 6), "Mission terminal (party queue)")
    box("archive_wall", -49, -47.5, -16, 16, 1, 12, M["panel"]); win_band("arch", "E", -15, 15, 2, 11, -49, -47.5, -40, 40, m=X["violet_e"], step=3)
    note("archive_wall", (-47.5, 0, 12), "Archive wall (memory fragments)")
    box("test_bay", 10, 40, -36, -16, 0.1, 0.2, M["orange"]); box("test_bay_in", 11, 39, -35, -17, 0.2, 0.25, M["grate"])
    note("test_bay", (25, -26, 0.3), "Testing bay (non-reward sandbox)")
    grp("body")
    _robots(("Patch", -30, 18, 0.4), ("Cypher", -8, -12, 0.2), ("Sentinel", 8, -12, -0.2), ("Patch", 14, -52, 0.3))

def bpy_mark_roof(name):
    import bpy
    bpy.data.objects[name]["grp"] = "roof"

# ------------------------------------------------------------------ BLD-03 Residential Tower 48×48, 5 floors
def bld03():
    CUT_H[0] = 8
    ground("g", -45, 45, -50, 45)
    FH = 12
    shell("lobby", -24, 24, -24, 24, FH, openings=[("S", 0, 12, 10), ("E", 8, 6, 10)], roof=False)
    box("lobby_canopy", -10, 10, -30, -24, 10.5, 11.3, M["orange"])
    for f in range(1, 5):
        z = f * FH
        box(f"slab{f}", -24.5, 24.5, -24.5, 24.5, z, z + 0.8, M["panel"])["upper"] = 1
        sh = 1.5 if f % 2 else -1.0
        box(f"core{f}", -23, 23, -23, 23, z + 0.8, z + FH, M["graphite"])["upper"] = 1
        for side in "SNWE":
            win_band(f"win{f}{side}", side, -20, 20, z + 4, z + 9, -23, 23, -23, 23, m=X["amberwin"], step=6, gap=1.6)
        for x in (-16, 0, 16):
            b = box(f"balc{f}_{x}", x - 4 + sh, x + 4 + sh, -27, -23, z + 0.8, z + 1.4, M["steel"]); b["upper"] = 1
            r = box(f"rail{f}_{x}", x - 4 + sh, x + 4 + sh, -27.1, -26.8, z + 1.4, z + 3.4, M["teal"]); r["upper"] = 1
    grp("roof")
    box("roof", -24.5, 24.5, -24.5, 24.5, 5 * FH, 5 * FH + 1, M["panel"])
    box("liftcore_top", -5, 5, 5, 15, 5 * FH + 1, 5 * FH + 7, M["graphite"])
    cyl("antenna", 12, 12, 5 * FH + 1, 16, 0.4, M["steel"], 12); sphere("beacon", 12, 12, 5 * FH + 17.3, 0.6, M["red_e"])
    box("bridge_stub", 24, 34, -4, 4, 3 * FH, 3 * FH + 1, M["steel"])
    grp("body")
    text("sign", "HAB-7", 0, -24.2, 10.2, 1.5, M["cyan_e"])
    note("balc0_0", (0, -27, FH + 2), "Stacked balconies, offset per floor")
    note("antenna", (12, 12, 5 * FH + 17), "Rooftop antenna + red beacon")
    note("win1S", (-20, -23, FH + 6), "Warm amber windows (safe district)")
    note("bridge_stub", (29, 0, 3 * FH + 1), "Rooftop bridge connection (INF-11)")
    note("lobby_canopy", (0, -28, 11), "Lobby entrance 12 × 10")
    grp("interior")
    box("lift", -5, 5, 5, 15, 0.1, FH, M["steel"]); box("lift_door", -3, 3, 4.9, 5.0, 0.2, 9, M["cyan_soft"])
    for k, x in enumerate((-18, -12, 12, 18)):
        box(f"dock{k}", x - 2, x + 2, 17, 21, 0, 6, M["graphite"]); box(f"dock_l{k}", x - 1.5, x + 1.5, 16.9, 17, 2, 5, M["cyan_e"])
    note("dock0", (-18, 19, 6), "Shared charging docks (lobby)")
    note("lift", (0, 10, FH), "Lift core 10 × 10")
    box("mailwall", -23, -21.5, -15, 5, 1, 8, M["panel"]); win_band("mail", "E", -14, 4, 2, 7, -23, -21.5, -24, 24, m=X["amberwin"], step=2, gap=0.5)
    grp("body")
    _robots(("Cypher", -6, -34, 0.3), ("Patch", 6, -33, -0.4), ("Cypher", -15, 0, 1.0))

# ------------------------------------------------------------------ BLD-04 Circuit Market 100×70×20
def bld04():
    CUT_H[0] = 8
    ground("g", -70, 70, -60, 55)
    box("plaza", -50, 50, -35, 35, 0, 0.2, M["floor"])
    for k in range(12):
        a = 2 * math.pi * k / 12
        cyl(f"col{k}", 14 * math.cos(a), 14 * math.sin(a), 0, 12, 0.7, M["graphite"], 12)
    grp("roof")
    dome("dome", 0, 0, 12, 16, X["violet_e"], 0.55)
    tube("dome_ring", 0, 0, 11.5, 1.0, 16.4, 0.6, M["orange"])
    cyl("dome_top", 0, 0, 20.5, 2, 2, M["cyan_e"], 16)
    grp("body")
    note("dome", (0, 0, 20), "Central dome kiosk — violet glow landmark")
    cyl("kiosk", 0, 0, 0, 4, 6, M["graphite"], 32); tube("kiosk_light", 0, 0, 4, 0.4, 6.1, 0.3, M["amber_e"])
    note("kiosk", (0, -6, 4), "Central trade kiosk (vendor hub)")
    k = 0
    for side, xs in (("S", range(-44, 45, 11)), ("N", range(-44, 45, 11))):
        y = -30 if side == "S" else 24
        for x in xs:
            if abs(x) < 12:
                continue
            col = [M["orange"], X["violet_e"], M["cyan_soft"]][k % 3] if False else M["orange"]
            box(f"stall{k}", x - 4, x + 4, y, y + 6, 0, 3, M["graphite"])
            box(f"stall_top{k}", x - 4, x + 4, y, y + 6, 3, 3.3, M["steel"])
            for px in (x - 3.8, x + 3.6):
                box(f"stall_post{k}_{px}", px, px + 0.25, y + (0 if side == "S" else 5.7), y + (0.3 if side == "S" else 6), 0, 9, M["steel"])
            c = box(f"canopy{k}", x - 4.5, x + 4.5, y - 0.5, y + 6.5, 9, 9.5, [M["orange"], M["teal"], X["violet_e"]][k % 3]); c["grp"] = "roof"
            box(f"sign{k}", x - 3, x + 3, y - 0.2 if side == "S" else y + 6, y if side == "S" else y + 6.2, 6, 8, [M["cyan_e"], M["amber_e"], X["violet_e"]][k % 3])
            k += 1
    note("canopy0", (-44, -30, 9.5), "Stall module 8 × 6 (INT-09) with coloured canopy")
    note("sign1", (-33, -30, 8), "Animated holo signage (INF-06)")
    for x in (-50, 50):
        box(f"gate{x}", x - 1, x + 1, -8, 8, 0, 14, M["graphite"]); box(f"gatebar{x}", x - 1, x + 1, -8, 8, 14, 16, M["orange"])
        text(f"gtext{x}", "CIRCUIT MARKET", x - (1.2 if x < 0 else -1.2), 0, 14.4, 1.0, M["cyan_e"], rz=math.radians(-90 if x < 0 else 90))
    note("gate-50", (-50, 0, 16), "District gateway arches (E/W)")
    for x in (-35, -20, 20, 35):
        cyl(f"lamp{x}", x, -5, 0, 10, 0.3, M["steel"], 10); sphere(f"lampb{x}", x, -5, 10.3, 0.8, M["amber_e"])
    _robots(("Patch", -33, -23, 0.2), ("Cypher", -22, -24, 0.0), ("Sentinel", 0, -10, 0.3), ("Patch", 22, 17, 3.0), ("Cypher", 30, -14, -0.5))

# ------------------------------------------------------------------ BLD-05 Assembly Foundry 140×95×36
def bld05():
    CUT_H[0] = 10
    ground("g", -100, 100, -80, 75)
    shell("hall", -70, 50, -47, 48, 24, openings=[("S", -30, 20, 16), ("E", 0, 14, 14)], wall_m=M["graphite"])
    grp("roof")
    for k, y in enumerate(range(-47, 48, 12)):
        cbox(f"saw{k}", -10, y + 6, 27, 120, 12.4, 1.0, M["panel"], rot=(math.radians(-22), 0, 0))
        box(f"sawglass{k}", -70, 50, y + 11, y + 11.6, 24.6, 29, M["cyan_soft"])
    grp("body")
    note("saw3", (-10, -5, 29), "Sawtooth north-light roof")
    shell("power", 50, 70, -20, 20, 18, openings=[("W", 0, 6, 10)])
    note("power_roof", (60, 0, 19), "Power room annex (rerouting puzzle)")
    for k, (x, h) in enumerate(((-55, 20), (-45, 24), (60, 16))):
        stack(f"chim{k}", x, 38 if k < 2 else 12, 24 if k < 2 else 18.8, h, 2.4)
    note("chim1", (-45, 38, 48), "Smoke stacks ×3 (steam VFX = Cooling state)")
    for x in (-70, -30, 10, 50):
        box(f"gantry_leg{x}", x - 1, x + 1, -65, -63, 0, 30, M["yellow"])
    box("gantry_beam", -71, 51, -65.5, -62.5, 30, 32, M["yellow"])
    box("gantry_trolley", -12, -6, -66, -62, 27, 30, M["graphite"])
    note("gantry_beam", (-20, -64, 32), "External gantry crane over the loading yard")
    for k in range(10):
        box(f"haz{k}", -40 + k * 2, -39 + k * 2, -47.3, -47.0, 0, 1.4, M["yellow"] if k % 2 else M["graphite"])
    gear("gear", 20, -47.6, 17, 3.5, M["orange_e"])
    text("sign", "ASSEMBLY FOUNDRY 03", 20, -47.7, 12, 1.6, M["cyan_e"])
    grp("interior")
    for k, y in enumerate((-25, 0, 25)):
        box(f"conv{k}", -64, 40, y - 2, y + 2, 0, 2.5, M["graphite"])
        box(f"conv_belt{k}", -64, 40, y - 1.6, y + 1.6, 2.5, 2.7, M["rubber"])
        box(f"conv_led{k}", -64, 40, y - 2.05, y - 1.95, 1.2, 1.5, M["blue"])
        for x in (-40, -10, 20):
            cyl(f"arm_b{k}{x}", x, y + 4, 0, 2, 1.2, M["graphite"], 16)
            cbox(f"arm_s{k}{x}", x, y + 2.5, 4.5, 1.0, 1.0, 6, M["yellow"], rot=(math.radians(35), 0, 0))
    note("conv1", (-50, 0, 2.7), "Conveyor lines ×3 (timing puzzles)")
    note("arm_s1-10", (-10, 2.5, 7), "Robotic assembly arms (hazard timing)")
    box("bridge", -70, 50, 10, 13, 9, 9.6, M["steel"]); box("bridge_rail", -70, 50, 9.9, 10.1, 9.6, 11, M["yellow"])
    note("bridge", (-60, 11, 9.6), "Safety bridge +9")
    grp("body")
    _robots(("Sentinel", -30, -56, 0.2), ("Patch", -24, -55, -0.3), ("Patch", 0, -6, 1.2))

# ------------------------------------------------------------------ BLD-06 Research Laboratory 90×70×24
def bld06():
    CUT_H[0] = 8
    ground("g", -70, 70, -60, 55)
    shell("main", -25, 25, -20, 25, 12, wall_m=X["white"], openings=[("S", 0, 10, 10)], roof=True)
    shell("wingW", -45, -25, -35, 15, 10, wall_m=X["white"], openings=[("E", -25, 6, 9)])
    shell("wingE", 25, 45, -35, 15, 10, wall_m=X["white"], openings=[("W", -25, 6, 9)])
    grp("roof")
    cyl("dome_base", 0, 2, 12.8, 1.4, 18, M["graphite"], 48)
    dome("dome", 0, 2, 14.2, 17, X["glassdome"], 0.62)
    tube("dome_ring", 0, 2, 14.0, 0.6, 18.2, 0.4, M["cyan_e"])
    for k, rot in enumerate((0, 60, 120)):
        r = tube(f"atom{k}", 0, 0, -0.2, 0.4, 5, 0.35, M["cyan_e"])
        r.location = (0, 2, 20); r.rotation_euler = (math.radians(70), 0, math.radians(rot))
    sphere("atom_core", 0, 2, 20, 1.3, M["cyan_e"])
    grp("body")
    note("dome", (0, 2, 24), "Glass research dome — atom emblem landmark")
    win_band("wS", "S", -23, -7, 4, 9, -25, 25, -20, 25, m=X["violet_e"]); win_band("wS2", "S", 7, 23, 4, 9, -25, 25, -20, 25, m=X["violet_e"])
    for x0 in (-45, 25):
        win_band(f"wing{x0}", "S", x0 + 2, x0 + 18, 4, 7, x0, x0 + 20, -35, 15, m=M["cyan_soft"], step=4, gap=1)
    note("wS", (-15, -20, 9), "Violet data displays (research palette)")
    for k, x in enumerate((-40, 40)):
        tank(f"tank{k}", x, 25, 0, 14, 3, X["white"])
    note("tank0", (-40, 25, 14), "Coolant / gas tanks")
    text("sign", "RESEARCH LAB 2", 0, -20.3, 12.6, 1.4, M["cyan_e"])
    grp("interior")
    for k, x in enumerate((-15, -5, 5, 15)):
        box(f"labbench{k}", x - 3, x + 3, 0, 4, 0, 3.2, X["white"]); box(f"labscr{k}", x - 2, x + 2, 3.9, 4.0, 3.2, 5.5, X["violet_e"])
    box("partition", -24, 24, 8, 8.3, 0, 8, X["glassdome"])
    for k, x in enumerate((-20, -12, 12, 20)):
        box(f"rack{k}", x - 2, x + 2, 17, 23, 0, 9, M["graphite"]); box(f"rackl{k}", x - 1.5, x + 1.5, 16.9, 17, 1, 8, M["cyan_soft"])
    note("labbench1", (-5, 2, 5.5), "Lab benches with violet terminals")
    note("rack1", (-12, 20, 9), "Sealed evidence vault racks")
    grp("body")
    _robots(("Cypher", -4, -28, 0.1), ("Patch", 4, -27, -0.2))

# ------------------------------------------------------------------ BLD-07 Security Command Center 48×36 + tower
def bld07():
    CUT_H[0] = 8
    ground("g", -50, 50, -50, 45)
    shell("cmd", -24, 24, -18, 18, 14, openings=[("S", 0, 10, 10)], wall_m=M["graphite"])
    for x in (-24, 24):
        cbox(f"armour{x}", x * 1.02, -12, 7, 2, 14, 14, M["panel"], rot=(0, 0, math.radians(8 if x > 0 else -8)))
    box("tower", 12, 22, 4, 14, 14.8, 32, M["graphite"])
    box("tower_cab", 10, 24, 2, 16, 32, 37, M["panel"]); win_band("cab", "S", 11, 23, 33, 36, 10, 24, 2, 16, m=M["red_e"])
    cyl("beacon", 17, 9, 37, 2, 1.2, M["red_e"], 16)
    note("tower_cab", (17, 2, 36), "Watchtower cab — red surveillance strip")
    note("beacon", (17, 9, 39), "Alert beacon (Security state)")
    box("emblem_plate", -6, 6, -18.6, -18.2, 9, 13, M["red"])
    emblem("emblem", 0, -18.8, 11, 2.4, M["red_e"])
    text("sign", "SECURITY COMMAND", 0, -18.7, 14.5, 1.2, M["cyan_e"])
    note("emblem", (0, -18.8, 11), "ZERO security emblem (red)")
    for k in range(8):
        box(f"stripe{k}", -24 + k * 6, -21 + k * 6, -18.3, -18.1, 0, 1.2, M["orange"])
    box("gate_l", -40, -30, -30, -28, 0, 10, M["graphite"]); box("gate_r", 30, 40, -30, -28, 0, 10, M["graphite"])
    box("gate_bar", -30, 30, -29.5, -28.5, 9, 10, M["red"])
    note("gate_bar", (0, -29, 10), "Checkpoint barrier (INF-04 pattern)")
    grp("interior")
    box("monwall", -22, 2, 15, 16.5, 2, 9, M["panel"])
    for k in range(6):
        box(f"mon{k}", -21 + k * 4, -18 + k * 4, 14.9, 15, 3, 8, M["red_e"] if k == 2 else M["cyan_soft"])
    box("desk", -16, -4, 6, 9, 0, 3, M["graphite"])
    box("cells", 6, 22, -16, -6, 0, 8, M["panel"])
    for k in range(4):
        box(f"bars{k}", 7 + k * 4, 7.3 + k * 4, -6.2, -5.9, 0, 8, M["red_e"])
    note("monwall", (-10, 15, 9), "Surveillance wall")
    note("cells", (14, -11, 8), "Holding cells (bypass puzzle)")
    grp("body")
    _robots(("Sentinel", -8, -26, 0.0), ("Sentinel", 8, -26, 0.0))

# ------------------------------------------------------------------ BLD-08 Nexus Energy Spire 90×90×180
def bld08():
    CUT_H[0] = 10
    ground("g", -80, 80, -80, 80)
    hollow_prism("tier1", 14, 45, 8, 2.0, M["graphite"], 10)
    cyl("tier2", 0, 0, 14, 12, 32, M["panel"], 8)
    cyl("tier3", 0, 0, 26, 10, 22, M["graphite"], 8)
    for k in range(8):
        a = 2 * math.pi * k / 8 + math.pi / 8
        cbox(f"buttress{k}", 40 * math.cos(a), 40 * math.sin(a), 13, 8, 4, 26, M["steel"], rot=(0, 0, a))
        box(f"door{k}", 0, 0, 0, 0, 0, 0, M["steel"]) if False else None
    cyl("shaft", 0, 0, 36, 120, 8, M["graphite"], 24)
    cyl("core", 0, 0, 36, 120, 5, M["cyan_e"], 24)
    for k in range(14):
        z = 40 + k * 8.5
        cbox(f"strut{k}a", 0, 0, z, 17.5, 1.0, 1.0, M["steel"], rot=(0, 0, k * 0.4))
    for k, (z, r) in enumerate(((60, 20), (95, 16), (128, 12))):
        tube(f"ring{k}", 0, 0, z, 2.2, r, 1.6, M["cyan_e"] if k != 1 else M["orange"])
        box(f"platform{k}", -r * 0.7, r * 0.7, -2, 2, z - 1, z - 0.4, M["steel"])
    cyl("crown", 0, 0, 156, 8, 10, M["graphite"], 8, r2=4)
    cyl("crown_light", 0, 0, 164, 16, 1.2, M["cyan_e"], 12)
    note("ring0", (20, 0, 61), "Concentric energy rings (state colour)")
    note("core", (0, -8, 110), "Exposed cyan core — power state readable city-wide")
    note("tier1", (0, -45, 14), "Tiered octagonal reactor base 90 × 90")
    note("crown", (0, 0, 176), "Crown emitter (red in Lockdown)")
    note("platform1", (11, 0, 94), "Maintenance platforms")
    for k in range(4):
        a = math.pi / 2 * k
        box(f"entry{k}", 0, 0, 0, 0, 0, 0, M["steel"]) if False else None
    shell("ctrl", -12, 12, -45, -33, 8, openings=[("S", 0, 8, 7)], roof=True)
    note("ctrl_roof", (0, -39, 9), "Reactor control entry (INT-10)")
    grp("interior")
    tube("inner_ring", 0, 0, 0.1, 0.4, 30, 1.0, M["cyan_soft"])
    for k in range(6):
        a = 2 * math.pi * k / 6
        box(f"console{k}", 24 * math.cos(a) - 2, 24 * math.cos(a) + 2, 24 * math.sin(a) - 1, 24 * math.sin(a) + 1, 0, 3, M["graphite"])
    grp("body")
    _robots(("Cypher", -6, -52, 0.2), ("Sentinel", 6, -52, -0.2))

# ------------------------------------------------------------------ BLD-09 Robot Maintenance Hospital 80×64×24
def bld09():
    CUT_H[0] = 8
    ground("g", -60, 60, -55, 50)
    shell("main", -40, 40, -32, 32, 16, wall_m=X["white"], openings=[("S", 0, 14, 11), ("E", 16, 6, 10)])
    for x in (-40, 40):
        box(f"band{x}", x - (0.2 if x < 0 else -0.2) - 0.2, x + 0.2, -32, 32, 12, 13.5, M["teal"])
    box("bandS", -40, 40, -32.2, -32, 12, 13.5, M["teal"])
    box("cross_v", -1.2, 1.2, -32.6, -32.2, 4.5, 11, M["cyan_e"]); box("cross_h", -3.8, 3.8, -32.6, -32.2, 6.6, 8.9, M["cyan_e"])
    note("cross_v", (0, -32.6, 9), "Repair-cross beacon (cyan = open)")
    win_band("wS", "S", -36, -10, 5, 10, -40, 40, -32, 32, m=M["cyan_soft"], step=6); win_band("wS2", "S", 10, 36, 5, 10, -40, 40, -32, 32, m=M["cyan_soft"], step=6)
    box("canopy", -12, 12, -40, -32, 11.5, 12.2, M["teal"]); box("canopy_l", -11, 11, -39.8, -39.4, 11.2, 11.5, M["cyan_e"])
    note("canopy", (0, -38, 12), "Drop-off canopy 24 × 8")
    grp("roof")
    cyl("pad", 20, 10, 16.8, 0.5, 9, M["graphite"], 32); tube("pad_ring", 20, 10, 17.3, 0.15, 8.5, 0.6, M["teal"])
    text("padH", "H", 20, 10, 17.4, 6, M["cyan_e"]).rotation_euler = (0, 0, 0)
    note("pad", (20, 10, 17.5), "Medical drone pad (EQP-09)")
    grp("body")
    text("sign", "MAINTENANCE HOSPITAL", 0, -32.3, 14, 1.4, M["cyan_e"])
    grp("interior")
    for k, x in enumerate((-30, -18, 18, 30)):
        box(f"bay{k}", x - 4, x + 4, 14, 26, 0.1, 0.3, M["teal"])
        box(f"baybed{k}", x - 2, x + 2, 17, 23, 0.3, 3, X["white"])
        cbox(f"bayarm{k}", x, 25, 8, 1, 1, 7, M["orange"], rot=(math.radians(40), 0, 0))
        box(f"bayscr{k}", x - 2, x + 2, 25.9, 26, 4, 7, M["cyan_soft"])
    note("bay1", (-18, 20, 3), "Repair bays ×4 with overhead arms")
    box("triage", -8, 8, -4, 0, 0, 3.4, X["white"]); box("triage_s", -7, 7, -0.1, 0, 2, 3.2, M["cyan_soft"])
    note("triage", (0, -2, 3.4), "Triage desk")
    grp("body")
    _robots(("Patch", -6, -40, 0.0), ("Cypher", 6, -42, 0.3), ("Patch", -18, 20, 0.0))

# ------------------------------------------------------------------ BLD-10 Data Archive 64×48×28
def bld10():
    CUT_H[0] = 10   # racks are 8 tall: cut above them so the plan shows the rack grid
    ground("g", -50, 50, -45, 40)
    shell("base", -32, 32, -24, 24, 12, openings=[("S", 0, 8, 10)])
    shell("mid", -24, 24, -18, 18, 22, roof=True, parapet=0.6)
    for o in ("mid_floor",):
        pass
    box("top", -14, 14, -12, 12, 22.8, 28, M["graphite"])
    for k, x in enumerate(range(-22, 23, 4)):
        box(f"stripe{k}", x - 0.4, x + 0.4, -18.2, -18.0, 12.5, 21.5, M["cyan_e"] if k % 3 else X["violet_e"])
    for k, x in enumerate(range(-12, 13, 4)):
        box(f"tstripe{k}", x - 0.3, x + 0.3, -12.2, -12.0, 23, 27.5, X["violet_e"])
    note("stripe3", (-10, -18, 21), "Vertical data stripes (pulse when Data = Connected)")
    note("top", (0, -12, 28), "Stepped monolith crown")
    text("sign", "ARCHIVE", 0, -24.3, 9.8, 1.4, M["cyan_e"])
    cyl("dish", 0, 0, 28, 1.2, 4, M["steel"], 24); cyl("mast", 0, 0, 29.2, 7, 0.4, M["steel"], 12)
    note("dish", (0, 0, 30), "Uplink dish (Data relay)")
    grp("interior")
    for r in range(4):
        for c in range(5):
            x = -24 + c * 12; y = -14 + r * 9
            if abs(x) < 6 and y < -8:
                continue
            box(f"rack{r}{c}", x - 4, x + 4, y - 1.2, y + 1.2, 0, 8, M["graphite"])
            box(f"rackled{r}{c}", x - 3.6, x + 3.6, y - 1.25, y - 1.2, 1, 7, X["violet_e"] if (r + c) % 2 else M["cyan_soft"])
    note("rack11", (-12, -5, 8), "Server racks (memory fragment terminals)")
    grp("body")
    _robots(("Cypher", 0, -31, 0.0))

# ------------------------------------------------------------------ BLD-11 Underground Freight Depot 120×64×28
def bld11():
    CUT_H[0] = 8
    ground("g", -80, 80, -55, 55)
    shell("hall", -60, 60, -32, 32, 18, openings=[("W", 0, 16, 14), ("E", 0, 16, 14), ("S", -30, 12, 12)])
    grp("roof")
    box("berm", -62, 62, -10, 34, 19, 26, X["concrete2"])
    grp("body")
    for x in (-60, 60):
        k = "W" if x < 0 else "E"
        box(f"portal{k}", x - 1.5, x + 1.5, -11, 11, 0, 20, M["graphite"])
        box(f"portal_band{k}", x - 1.7, x + 1.7, -10, 10, 16, 17, M["orange"])
    note("portalW", (-60, 0, 20), "Tunnel portals E/W (freight line)")
    for y in (-4, 4):
        box(f"rail{y}", -80, 80, y - 0.3, y + 0.3, 0, 0.5, M["steel"])
    for k in range(40):
        box(f"tie{k}", -79 + k * 4, -78 + k * 4, -6, 6, 0, 0.25, M["rubber"])
    note("rail-4", (-70, -4, 0.5), "Freight track pair, 12-stud gauge zone")
    box("gantry_a", -20, -18, -28, 28, 0, 16, M["yellow"]); box("gantry_b", 18, 20, -28, 28, 0, 16, M["yellow"])
    box("gantry_beam", -20, 20, -2, 2, 15, 17, M["yellow"])
    note("gantry_beam", (0, 0, 17), "Container gantry (interior)")
    shell("lift", 30, 50, -50, -32, 14, openings=[("N", 40, 16, 12)], roof=True)
    box("lift_plat", 31, 49, -49, -33, 0.2, 0.8, M["orange"])
    note("lift_roof", (40, -41, 15), "Freight elevator VEH-07 (server platform)")
    text("sign", "FREIGHT DEPOT 1", -20, -32.3, 13, 1.5, M["cyan_e"])
    grp("interior")
    for k in range(6):
        x = -48 + k * 9
        box(f"crate{k}", x, x + 7, 14, 22, 0, 6, [M["orange"], M["teal"], M["graphite"]][k % 3])
    note("crate2", (-30, 18, 6), "Container stacks (cover + salvage)")
    grp("body")
    _robots(("Sentinel", -30, -40, 0.0), ("Patch", 36, -55, 0.2))

# ------------------------------------------------------------------ BLD-12 Robot Recycling Facility 96×72×30
def bld12():
    CUT_H[0] = 8
    ground("g", -70, 70, -60, 55)
    shell("hall", -48, 20, -36, 36, 18, openings=[("S", -14, 14, 12), ("E", 0, 10, 12)])
    box("hopper_base", 20, 44, -10, 14, 0, 14, M["graphite"])
    cyl("hopper", 32, 2, 14, 12, 10, M["yellow"], 8, r2=4)
    note("hopper", (32, 2, 26), "Intake hopper + shredder (hazard)")
    cbox("ramp", 32, -24, 9, 6, 32, 1.2, M["graphite"], rot=(math.radians(28), 0, 0))
    box("ramp_belt", 29.5, 34.5, -38, -10, 0, 0.1, M["rubber"])
    note("ramp", (32, -24, 10), "Inclined feed conveyor")
    for k, (x, y) in enumerate(((-38, 28), (-26, 28))):
        box(f"sorttower{k}", x - 4, x + 4, y - 4, y + 4, 18.8, 30, M["graphite"])
        box(f"sortled{k}", x - 3, x + 3, y - 4.1, y - 4, 22, 28, M["amber_e"])
    note("sorttower0", (-38, 24, 30), "Sorting towers")
    for k, (x, y, r) in enumerate(((-30, -50, 6), (-14, -52, 5), (40, 30, 7))):
        cyl(f"scrap{k}", x, y, 0, r * 0.6, r, M["rubber"], 7, r2=r * 0.2)
    note("scrap0", (-30, -50, 4), "Scrap heaps (salvage nodes)")
    for k in range(10):
        box(f"haz{k}", -48 + k * 4, -46 + k * 4, -36.3, -36.0, 0, 1.4, M["yellow"] if k % 2 else M["graphite"])
    text("sign", "RECYCLING 4", -14, -36.3, 14, 1.5, M["orange_e"])
    stack("stack", 10, 28, 18.8, 14, 2)
    grp("interior")
    box("conv", -44, 18, -2, 2, 0, 2.5, M["graphite"]); box("convb", -44, 18, -1.6, 1.6, 2.5, 2.7, M["rubber"])
    for k, x in enumerate((-36, -20, -4)):
        box(f"bin{k}", x - 4, x + 4, 8, 16, 0, 4, [M["orange"], M["teal"], M["steel"]][k])
        cbox(f"sorter{k}", x, 4, 6, 1, 1, 6, M["yellow"], rot=(math.radians(-30), 0, 0))
    note("bin1", (-20, 12, 4), "Sorting bins + pick arms")
    grp("body")
    _robots(("Patch", -10, -44, 0.2), ("Sentinel", 2, -46, -0.2))

# ------------------------------------------------------------------ BLD-13 Memory Restoration Laboratory 64×56×24
def bld13():
    CUT_H[0] = 8
    ground("g", -50, 50, -45, 45)
    R = 28
    hollow_prism("pavilion", 14, R, 6, 1.2, X["white"], 8)
    cyl("pavilion_band", 0, 0, 10, 1.4, R + 0.2, X["violet_e"], 6)
    grp("roof")
    cyl("crown", 0, 0, 14, 8, 16, X["glassdome"], 6, r2=8)
    cyl("crown_cap", 0, 0, 22, 1.5, 8.5, M["graphite"], 6)
    cyl("beam", 0, 0, 23.5, 6, 1, X["violet_e"], 12)
    grp("body")
    note("crown", (0, -12, 20), "Hexagonal violet glass crown")
    note("pavilion_band", (0, -R, 11), "Violet memory band (Research palette)")
    box("entry", -6, 6, -R - 4, -R + 1, 0, 10, M["graphite"]); box("entry_d", -4, 4, -R - 4.1, -R - 4, 0, 8, M["cyan_soft"])
    text("sign", "MEMORY RESTORATION", 0, -R - 4.2, 10.4, 1.1, M["cyan_e"])
    note("entry", (0, -R - 4, 10), "Entry vestibule")
    grp("interior")
    for k in range(6):
        a = 2 * math.pi * k / 6 + math.pi / 6
        x, y = 15 * math.cos(a), 15 * math.sin(a)
        cyl(f"mpod{k}", x, y, 0, 1.5, 3, M["graphite"], 8)
        tube(f"mpodg{k}", x, y, 1.5, 6, 2.4, 0.12, M["glass"])
        cyl(f"mpodc{k}", x, y, 7.5, 1, 2.8, X["violet_e"], 16)
    cyl("console_ring", 0, 0, 0, 3, 5, M["graphite"], 24); tube("console_l", 0, 0, 3, 0.3, 5.1, 0.3, X["violet_e"])
    note("mpod0", (13, 7.5, 8.5), "Memory restoration pods ×6")
    note("console_ring", (0, 0, 3.3), "Central replay console (memory playback)")
    grp("body")
    _robots(("Cypher", -3, -40, 0.0))

# ------------------------------------------------------------------ BLD-14 Automated Manufacturing Plant 128×96×32
def bld14():
    CUT_H[0] = 10
    ground("g", -90, 90, -70, 70)
    shell("hallA", -64, 64, -48, 0, 20, wall_m=X["white"], openings=[("S", -40, 16, 14)])
    shell("hallB", -64, 30, 0, 48, 24, wall_m=X["white"], openings=[])
    shell("port", 30, 64, 8, 48, 12, openings=[("S", 47, 12, 10)])
    note("hallA_roof", (-30, -24, 21), "Automated hall A (clean white shell)")
    grp("roof")
    for k in range(6):
        for j in range(3):
            cbox(f"solar{k}{j}", -50 + k * 18, -38 + j * 14, 22.5, 14, 10, 0.4, M["blue"], rot=(math.radians(-15), 0, 0))
    note("solar20", (-14, -38, 23), "Rooftop solar arrays")
    cyl("drone_pad", 47, 28, 12.8, 0.4, 12, M["graphite"], 40); tube("drone_ring", 47, 28, 13.2, 0.1, 11.5, 0.6, M["cyan_e"])
    note("drone_pad", (47, 28, 13.3), "Transport-drone port (VEH-06)")
    grp("body")
    for k in range(12):
        box(f"strip{k}", -62 + k * 10.5, -56 + k * 10.5, -48.2, -48.0, 15, 16.5, M["cyan_e"])
    text("sign", "AUTOMATED PLANT 9", 10, -48.3, 17.5, 1.6, M["cyan_e"])
    note("strip3", (-30, -48, 16), "Cyan status band (production running)")
    grp("interior")
    for r, y in enumerate((-36, -20)):
        for c in range(6):
            x = -54 + c * 18
            box(f"cell{r}{c}", x - 6, x + 6, y - 5, y + 5, 0.1, 0.3, M["yellow"])
            cyl(f"cella{r}{c}", x, y, 0.3, 2, 1.3, M["graphite"], 16)
            cbox(f"cellarm{r}{c}", x, y + 1.5, 5, 1, 1, 6, M["orange"], rot=(math.radians(30), 0, 0))
    note("cellarm03", (0, -34.5, 7), "Robotic cells (12) inside safety cages")
    box("agv_path", -60, 60, -10, -6, 0.1, 0.15, M["cyan_soft"])
    note("agv_path", (40, -8, 0.2), "AGV guide lane")
    grp("body")
    _robots(("Patch", -40, -58, 0.0), ("Cypher", -30, -57, 0.3))

# ------------------------------------------------------------------ BLD-15 Central Transit Terminal 90×24 platform
def bld15():
    CUT_H[0] = 8
    ground("g", -70, 70, -55, 50)
    shell("concourse", -45, 45, -40, 0, 14, openings=[("S", 0, 16, 11), ("S", -30, 8, 10), ("S", 30, 8, 10)], roof=False)
    vault("roof_vault", 0, 45, 8, 14, -40, 0, 0.8, M["panel"]); bpy_mark_roof("roof_vault")
    for y in range(-40, 1, 8):
        vault(f"roof_rib{y}", 0, 46, 9, 14, y - 0.4, y + 0.4, 1, M["graphite"]); bpy_mark_roof(f"roof_rib{y}")
    win_band("glazeS", "S", -42, -10, 3, 10, -45, 45, -40, 0, m=M["cyan_soft"], step=6); win_band("glazeS2", "S", 10, 42, 3, 10, -45, 45, -40, 0, m=M["cyan_soft"], step=6)
    note("roof_vault", (0, -20, 22), "Barrel-vault concourse roof (echoes Stasis hall)")
    # elevated platform + monorail beam
    for x in range(-44, 45, 11):
        box(f"pier{x}", x - 1, x + 1, 4, 6, 0, 16, M["graphite"])
    box("platform", -45, 45, 0, 24, 16, 17, M["steel"]); box("edge", -45, 45, 23.2, 24, 17, 17.2, M["orange"])
    box("canopy", -40, 40, 2, 20, 26, 26.8, M["panel"]); box("canopy_l", -38, 38, 10, 11, 25.7, 26, M["blue"])
    for x in (-38, -12, 12, 38):
        box(f"cpost{x}", x - 0.4, x + 0.4, 2, 2.8, 17, 26, M["steel"])
    box("guideway", -70, 70, 26, 32, 14, 16, M["graphite"]); box("guide_l", -70, 70, 25.9, 26, 14.5, 15.2, M["blue"])
    for x in range(-66, 67, 22):
        box(f"gpier{x}", x - 1.2, x + 1.2, 28, 30, 0, 14, M["graphite"])
    note("platform", (30, 12, 17), "Elevated platform 90 × 24 (+16)")
    note("guideway", (55, 29, 16), "Monorail guideway (INF-12, blue route light)")
    note("edge", (-30, 24, 17.2), "Orange safety edge")
    box("board", -8, 8, 1, 1.4, 20, 23, M["amber_e"])
    note("board", (0, 1, 23), "Departure board")
    text("sign", "CENTRAL TRANSIT", 0, -40.3, 11.3, 1.5, M["cyan_e"])
    grp("interior")
    for x in (-36, 36):
        for k in range(10):
            box(f"stair{x}{k}", x - 3, x + 3, -12 + k * 1.2, -10.8 + k * 1.2, 0, (k + 1) * 1.6, M["steel"])
    box("lift", -4, 4, -8, 0, 0, 16, M["steel"])
    for k, x in enumerate((-20, -10, 10, 20)):
        box(f"gateb{k}", x - 0.4, x + 0.4, -22, -18, 0, 4, M["graphite"]); box(f"gatel{k}", x - 0.45, x + 0.45, -22, -21.8, 2.5, 3.5, M["cyan_e"])
    note("gateb1", (-10, -20, 4), "Fare/route gates")
    note("lift", (0, -4, 16), "Platform lift (accessible route)")
    grp("body")
    robot("botp", "Cypher", -20, 12, 0.0, z=17); robot("botp2", "Patch", -14, 12, 0.3, z=17)
    _robots(("Sentinel", 0, -46, 0.0))

REG = {f"BLD-{n:02d}": ("BLD", f, {}) for n, f in
       ((2, bld02), (3, bld03), (4, bld04), (5, bld05), (6, bld06), (7, bld07), (8, bld08), (9, bld09),
        (10, bld10), (11, bld11), (12, bld12), (13, bld13), (14, bld14), (15, bld15))}
