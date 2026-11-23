"""INT-02 … INT-10 interior architecture (INT-01 lives in the BLD-01 package).
Rooms are closed shells (ceiling kept for the interior hero; plan / cutaway / section from the same model)."""
import math
from pz_asset_lib import *
from pz_build_stasis import M

def room(w, d, h, wall=None, openings=None, floor_m=None):
    shell("room", -w / 2, w / 2, -d / 2, d / 2, h, wall_m=wall, openings=openings or [("S", 0, 6, 10)], parapet=0, floor_m=floor_m)
    for k, y in enumerate(range(int(-d / 2) + 4, int(d / 2), 8)):
        grp("roof"); box(f"ceil_l{k}", -w / 2 + 2, w / 2 - 2, y - 0.3, y + 0.3, h - 0.15, h, M["cyan_e"]); grp("interior")

# ------------------------------------------------------------------ INT-02 Robot Residential Apartment 24×16×12
def int02():
    CUT_H[0] = 7
    grp("interior")
    room(24, 16, 12)
    box("dock", 6, 11, 2, 7, 0, 9, M["graphite"]); box("dock_glow", 6.5, 10.5, 1.9, 2.0, 1, 8, M["cyan_e"])
    box("dock_pad", 6, 11, -1, 2, 0, 0.3, M["cyan_soft"])
    note("dock_glow", (8.5, 2, 8), "Dock bay: charging pod (rest / save point)")
    box("alcove", -11.5, -10.5, -3, 3, 2, 8, M["panel"])
    for k in range(4):
        box(f"mem{k}", -10.5, -10.4, -2.5 + k * 1.4, -1.5 + k * 1.4, 4, 5.5, M["violet_e"])
    note("alcove", (-10.5, 0, 8), "Memory alcove (collectible display)")
    box("rack", -6, 2, 6.5, 7.5, 0, 9, M["steel"])
    for k in range(3):
        box(f"shelf{k}", -6, 2, 5.8, 7.5, 2 + k * 2.6, 2.3 + k * 2.6, M["graphite"])
        box(f"part{k}", -5 + k * 2.5, -3.8 + k * 2.5, 6, 7, 2.3 + k * 2.6, 3.4 + k * 2.6, [M["orange"], M["teal"], M["white"]][k])
    note("rack", (-2, 7, 9), "Storage rack (cosmetics / equipment)")
    box("niche", 9, 11.5, -7.5, -3, 0, 6, M["panel"]); cbox("niche_arm", 10, -5, 5, 0.6, 0.6, 3, M["orange"], rot=(0.6, 0, 0))
    note("niche", (10, -5, 6), "Repair niche (ambient animation)")
    box("window", -11.9, -11.85, -6, -3.5, 4, 9, M["amber_e"]) if False else None
    win_band("win", "N", -10, -4, 5, 9, -12, 12, -8, 8, m=M["amberwin"])
    box("rug", -6, 2, -5, 1, 0.1, 0.15, M["teal"])
    robot("res", "Cypher", -2, -2, 0.5, z=0.1)

# ------------------------------------------------------------------ INT-03 Workshop Repair Bay 24×24×16
def int03():
    CUT_H[0] = 9
    grp("interior")
    room(24, 24, 16, openings=[("S", 0, 12, 12)])
    box("lift", -5, 5, -3, 7, 0, 1.2, M["graphite"]); box("lift_ring", -5.1, 5.1, -3.1, 7.1, 1.2, 1.35, M["yellow"])
    note("lift", (5, 2, 1.3), "Hydraulic service lift 10 × 10")
    for s in (-1, 1):
        cyl(f"arm_base{s}", s * 8, 4, 0, 1.5, 1.2, M["graphite"], 16)
        cbox(f"arm1{s}", s * 7.2, 4, 4.5, 1, 1, 6, M["orange"], rot=(0, math.radians(-s * 25), 0))
        cbox(f"arm2{s}", s * 4.8, 4, 8, 0.8, 0.8, 4, M["orange"], rot=(0, math.radians(s * 60), 0))
        sphere(f"arm_tool{s}", s * 3.4, 4, 7, 0.5, M["cyan_e"])
    note("arm11", (7.2, 4, 7.5), "Twin repair arms (scripted)")
    box("toolwall", -11.5, -10.5, -8, 8, 2, 11, M["panel"])
    for k in range(5):
        box(f"tool{k}", -10.5, -10.3, -7 + k * 3, -5.5 + k * 3, 4, 8, [M["orange"], M["steel"], M["cyan_e"]][k % 3])
    note("toolwall", (-10.5, 0, 11), "Tool wall (crafting recipes)")
    box("bench", 6, 11.5, -10, -6, 0, 3.5, M["graphite"]); box("bench_s", 6.5, 11, -10.1, -10, 3.5, 6, M["cyan_soft"])
    note("bench", (9, -8, 6), "Diagnostics bench")
    grp("roof"); box("crane_rail", -11, 11, 3, 5, 14.5, 15.5, M["yellow"]); box("crane_hoist", -2, 2, 2.5, 5.5, 12, 14.5, M["graphite"]); grp("interior")
    note("crane_rail", (-8, 4, 15.5), "Overhead hoist rail")
    robot("patient", "Sentinel", 0, 2, 0.0, z=1.2)
    robot("mech", "Patch", -4, -5, 0.6)

# ------------------------------------------------------------------ INT-04 Train Passenger Compartment 17 × 23 × 8.6
# Interior of a VEH-01 passenger car, built to the crew standard: inner 15 × 21 × 8.5, 1+1 robot seats (4.8 wide),
# 5.4 aisle, 5 × 8 doors on both sides and both gangway ends.
def int04():
    CUT_H[0] = 5.5
    ZF = 0.1
    grp("interior")
    room(17, 23, 8.6, openings=[("S", 0, 5, 8.1), ("N", 0, 5, 8.1), ("W", 0, 5, 8.1), ("E", 0, 5, 8.1)], floor_m=M["panel"])
    for r, y in enumerate((-8.2, -4.3, 4.8, 8.7)):
        for x in (-5.1, 5.1):
            occ = {(1, -5.1): "Cypher", (2, 5.1): "Patch"}.get((r, x))
            crew_seat(f"seat{r}{'L' if x < 0 else 'R'}", x, y, ZF, "-Y", occ)
    for s in (-1, 1):
        for k, (a, b) in enumerate(((-10, -3), (3, 10))):
            win_band(f"win{s}{k}", "W" if s < 0 else "E", a, b, 3.6, 6.6, -8.5, 8.5, -11.5, 11.5, m=M["amber_e"], step=3.5, gap=0.7)
        box(f"rail{s}", s * 2.7 - 0.08, s * 2.7 + 0.08, -10, 10, 7.6, 7.75, M["steel"])
    box("aisle", -1, 1, -10.5, 10.5, ZF, ZF + 0.05, M["amber_e"])
    for k, x in enumerate((-2.5, 2.5)):
        box(f"door_frame{k}", x - 0.15, x + 0.15, 10.4, 10.6, 0, 8.1, M["cyan_soft"])
    walk_check("aisleF", 0, -6.5, ZF); walk_check("aisleR", 0, 6.5, ZF)
    walk_check("doorW", -8.0, 0, ZF); walk_check("doorE", 8.0, 0, ZF)
    walk_check("gangS", 0, -11.0, ZF); walk_check("gangN", 0, 11.0, ZF)
    note("seat1L", (-5.1, -4.3, 3.2), "1+1 robot seats (4.8 wide), orange upholstery"); note("win00", (-8.5, -6, 6.6), "Amber window glow (Ghost Train)")
    note("aisle", (0, 9, 0.2), "Lit aisle guide, 5.4 clear"); note("rail1", (2.7, 4, 7.75), "Grab rails over the seat edge (clear of the aisle)")

# ------------------------------------------------------------------ INT-05 Train Control Cabin 17 × 12 × 8.6
# Driver cabin of the VEH-01 cab car, built to the crew standard: robot seat, 5 × 8 rear door.
def int05():
    CUT_H[0] = 5.5
    ZF = 0.1
    grp("interior")
    room(17, 12, 8.6, openings=[("N", 0, 5, 8.1)], floor_m=M["panel"])
    box("windscreen", -6.5, 6.5, -6.1, -5.9, 3.6, 7.4, M["cyan_soft"])
    cbox("console", 0, -4.3, 2.2, 13, 1.4, 1.2, M["graphite"], rot=(math.radians(-15), 0, 0))
    for k, x in enumerate((-4, 0, 4)):
        cbox(f"disp{k}", x, -4.6, 3.2, 2.8, 0.1, 1.2, M["cyan_e"] if k != 1 else M["amber_e"], rot=(math.radians(-25), 0, 0))
    crew_seat("seat", 0, -1.2, ZF, "-Y", "Patch")
    box("lever", 3.0, 3.4, -3.4, -3.0, 2.2, 3.6, M["red_e"])
    box("panel_side", 6.6, 7.4, -3, 3, 1, 6, M["panel"])
    for k in range(4):
        box(f"sw{k}", 6.55, 6.6, -2.4 + k * 1.4, -1.6 + k * 1.4, 3, 4, M["cyan_e"])
    walk_check("door", 0, 5.5, ZF); walk_check("behind_seat", 0, 2.8, ZF)
    note("windscreen", (0, -6, 7.4), "Wrap windscreen (tunnel view)"); note("disp1", (0, -4.6, 3.8), "Route / speed displays")
    note("lever", (3.2, -3.2, 3.6), "Emergency stop (mission event)"); note("seat", (0, -1.2, 1.7), "Driver seat sized for the largest robot")

# ------------------------------------------------------------------ INT-06 Research Laboratory Interior 48×32×16
def int06():
    CUT_H[0] = 9
    grp("interior")
    room(48, 32, 16, wall=M["white"])
    cyl("holotable", 0, 0, 0, 3, 4, M["white"], 32); cyl("holo", 0, 0, 3, 0.2, 3.6, M["cyan_e"], 32)
    sphere("holo_globe", 0, 0, 6, 2, M["glass"])
    note("holo_globe", (0, 0, 8), "Holo analysis table (memory playback)")
    for k, x in enumerate((-18, -10, 10, 18)):
        box(f"bench{k}", x - 3, x + 3, -10, -6, 0, 3.2, M["white"]); box(f"scr{k}", x - 2.5, x + 2.5, -6.1, -6, 3.2, 6, M["violet_e"])
    note("scr1", (-10, -6, 6), "Lab benches, violet terminals")
    box("partition", -23, 23, 6, 6.3, 0, 10, M["glass"]); box("partition_top", -23, 23, 6, 6.3, 10, 10.4, M["cyan_e"])
    note("partition", (12, 6, 10), "Glass partition to sealed vault")
    for k, x in enumerate((-18, -9, 0, 9, 18)):
        box(f"vault{k}", x - 3, x + 3, 10, 14, 0, 11, M["graphite"]); box(f"vaultl{k}", x - 2.5, x + 2.5, 9.9, 10, 1, 10, M["cyan_soft"])
    note("vault2", (0, 10, 11), "Evidence vault racks (access levels)")
    robot("r1", "Cypher", -6, -2, 0.4); robot("r2", "Patch", 6, -14, -0.3)

# ------------------------------------------------------------------ INT-07 Factory Assembly Floor 96×64×28
def int07():
    CUT_H[0] = 12
    grp("interior")
    room(96, 64, 28, openings=[("S", -20, 16, 16)])
    for k, y in enumerate((-18, 0, 18)):
        box(f"conv{k}", -42, 42, y - 2, y + 2, 0, 2.5, M["graphite"]); box(f"belt{k}", -42, 42, y - 1.6, y + 1.6, 2.5, 2.7, M["rubber"])
        for x in (-28, -8, 12, 32):
            cyl(f"armb{k}{x}", x, y + 4.5, 0, 2, 1.3, M["graphite"], 16)
            cbox(f"arm{k}{x}", x, y + 3, 4.8, 1, 1, 6, M["yellow"], rot=(math.radians(35), 0, 0))
            box(f"cage{k}{x}", x - 5, x + 5, y + 2.5, y + 7, 0, 0.15, M["yellow"])
    note("belt1", (-36, 0, 2.7), "Conveyor lines ×3"); note("arm1-8", (-8, 3, 8), "Assembly arms ×12 (timing hazards)")
    grp("roof")
    for s in (-1, 1):
        box(f"crane_rail{s}", -47, 47, s * 28 - 1, s * 28 + 1, 24, 25.5, M["graphite"])
    box("crane_bridge", -2, 2, -29, 29, 22, 24, M["yellow"])
    grp("interior")
    note("crane_bridge", (0, -20, 24), "Overhead bridge crane")
    box("walk", -47, 47, 26, 30, 10, 10.6, M["steel"]); box("walk_r", -47, 47, 25.9, 26.1, 10.6, 12, M["yellow"])
    note("walk", (30, 28, 10.6), "Safety walkway +10")
    box("ctrl", 36, 46, -30, -22, 0, 8, M["panel"]); box("ctrl_w", 35.9, 36, -29, -23, 3, 7, M["cyan_soft"])
    note("ctrl", (41, -26, 8), "Line control booth")
    for k in range(24):
        box(f"haz{k}", -46 + k * 4, -44 + k * 4, -24, -23.6, 0.1, 0.2, M["yellow"])
    robot("w1", "Patch", -20, -12, 0.3); robot("w2", "Sentinel", 18, -26, -0.4)

# ------------------------------------------------------------------ INT-08 Security Control Room 24×20×12
def int08():
    CUT_H[0] = 7
    grp("interior")
    room(24, 20, 12)
    box("monwall", -11, 11, 8.5, 9.5, 2, 10, M["panel"])
    for r in range(2):
        for c in range(5):
            box(f"mon{r}{c}", -10 + c * 4.2, -6.5 + c * 4.2, 8.4, 8.5, 2.6 + r * 3.6, 5.6 + r * 3.6, M["red_e"] if (r + c) == 3 else M["cyan_soft"])
    note("mon12", (-1.5, 8.4, 9), "Surveillance wall 10 feeds (one alert)")
    for k, x in enumerate((-6, 0, 6)):
        cbox(f"desk{k}", x, 3, 1.6, 4.5, 2.2, 3.2, M["graphite"]); cbox(f"deskscr{k}", x, 3.9, 3.6, 3.5, 0.1, 1.4, M["cyan_e"], rot=(math.radians(-15), 0, 0))
    note("desk1", (0, 3, 3.6), "Operator desks ×3")
    cyl("holo", 0, -4, 0, 2.4, 3, M["graphite"], 24); cyl("holomap", 0, -4, 2.4, 0.1, 2.8, M["red_e"], 24)
    note("holomap", (0, -4, 2.5), "District holo-map (Security state)")
    box("lockdown", 10.5, 11.5, -6, -2, 3, 6, M["red"]); box("lockdown_btn", 10.4, 10.5, -4.5, -3.5, 4, 5, M["red_e"])
    note("lockdown_btn", (10.4, -4, 5), "Lockdown control (bypass puzzle)")
    robot("g1", "Sentinel", -6, 0, math.pi); robot("g2", "Sentinel", 7, -7, 0.6)

# ------------------------------------------------------------------ INT-09 Underground Market Stall 8×8×10
def int09():
    CUT_H[0] = 5
    grp("interior")
    box("floor", -4, 4, -4, 4, 0, 0.2, M["floor"])
    box("back", -4, 4, 3.4, 4, 0.2, 9, M["graphite"])
    for s in (-1, 1):
        box(f"side{s}", s * 4 - 0.3 if s > 0 else -4, s * 4 if s > 0 else -3.7, -1, 4, 0.2, 9, M["graphite"])
    box("counter", -3.7, 3.7, -2.8, -1.6, 0.2, 3.4, M["graphite"]); box("counter_top", -3.9, 3.9, -3, -1.4, 3.4, 3.7, M["steel"])
    box("counter_l", -3.6, 3.6, -2.85, -2.8, 2.2, 2.6, M["amber_e"])
    for k in range(3):
        box(f"shelf{k}", -3.6, 3.6, 2.6, 3.4, 2 + k * 2, 2.3 + k * 2, M["steel"])
        for j in range(4):
            box(f"item{k}{j}", -3 + j * 1.7, -2.2 + j * 1.7, 2.7, 3.3, 2.3 + k * 2, 3.1 + k * 2, [M["orange"], M["teal"], M["violet_e"], M["cyan_e"]][(k + j) % 4])
    grp("roof")
    box("canopy", -4.6, 4.6, -4.5, 4, 9, 9.4, M["orange"])
    box("sign", -3.5, 3.5, -4.6, -4.4, 6.5, 8.5, M["cyan_e"])
    grp("interior")
    text("signtxt", "PARTS", 0, -4.7, 7.1, 1.0, M["graphite"])
    note("canopy", (0, -4.5, 9.4), "Orange canopy (market identity)"); note("sign", (2.5, -4.5, 8.5), "Holo sign (INF-06 small)")
    note("counter_l", (3, -2.85, 2.6), "Service counter, amber underglow"); note("item12", (0, 3, 5.1), "Product shelves (preview items)")
    robot("vendor", "Patch", 0, 0.6, 0.0)

# ------------------------------------------------------------------ INT-10 Energy Reactor Control Room 32×24×16
def int10():
    CUT_H[0] = 9
    grp("interior")
    room(32, 24, 16)
    cyl("core_base", 0, 3, 0, 1.5, 5, M["graphite"], 32); cyl("core", 0, 3, 1.5, 12, 2.4, M["cyan_e"], 32)
    tube("core_glass", 0, 3, 1.5, 12, 4, 0.2, M["glass"]); cyl("core_cap", 0, 3, 13.5, 1.5, 4.5, M["graphite"], 32)
    for k in range(4):
        a = math.pi / 2 * k + math.pi / 4
        box(f"strut{k}", 4.2 * math.cos(a) - 0.3, 4.2 * math.cos(a) + 0.3, 3 + 4.2 * math.sin(a) - 0.3, 3 + 4.2 * math.sin(a) + 0.3, 1.5, 13.5, M["orange"])
    note("core", (2.4, 3, 10), "Reactor column (colour = Power state)")
    for k in range(5):
        a = math.pi + math.pi * (k + 0.5) / 5
        x, y = 9 * math.cos(a), 3 + 9 * math.sin(a)
        cbox(f"con{k}", x, y, 1.6, 3.4, 1.6, 3.2, M["graphite"], rot=(0, 0, a + math.pi / 2))
        cbox(f"conscr{k}", x * 0.93, 3 + (y - 3) * 0.93, 3.6, 2.8, 0.1, 1.4, M["cyan_e"] if k != 2 else M["amber_e"], rot=(math.radians(-20), 0, a + math.pi / 2))
    note("con2", (0, -6, 3.6), "Console arc ×5 (rerouting puzzle)")
    for k in range(6):
        box(f"cab{k}", -15.5, -14.5, -10 + k * 4, -7 + k * 4, 0, 9, M["panel"]); box(f"cabl{k}", -14.5, -14.4, -9.5 + k * 4, -7.5 + k * 4, 6, 6.5, M["amber_e"])
    note("cab2", (-14.5, -1.5, 9), "Breaker cabinets")
    robot("op", "Cypher", -3, -6, 0.2)

REG = {f"INT-{n:02d}": ("INT", f, {"outside_hero": n == 9}) for n, f in
       ((2, int02), (3, int03), (4, int04), (5, int05), (6, int06), (7, int07), (8, int08), (9, int09), (10, int10))}
