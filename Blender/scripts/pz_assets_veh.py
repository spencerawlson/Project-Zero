"""VEH-01 … VEH-09 procedural blockouts. Length along Y, nose faces -Y (front view = nose).
Groups drive the exploded view: roof, body, interior, chassis, bogie.

Crew spaces follow the crew standard in pz_asset_lib.CREW (owner decision 2026-11-23: robots must be able to
get into the cab). Bodies that carry robots are hollow cabins with 5 x 8 doors and robot seats; every seat and
doorway is registered with crew_seat() / walk_check() and verified against the largest robot at render time."""
import math
from pz_asset_lib import *
from pz_build_stasis import M

def wheel(name, x, y, r, w, hub=None):
    """Wheel whose tyre spans x .. x + w (axis along X)."""
    grp("bogie")
    cyl(name, x, y, r, w, r, M["rubber"], 20, rot=(0, math.radians(90), 0)).location = (x, y, r)
    cyl(name + "_hub", x, y, r, w + 0.1, r * 0.55, hub or M["orange"], 16, rot=(0, math.radians(90), 0)).location = (x, y, r)

def side_band(name, x, a, b, z0, z1, gaps, m, t=0.15):
    """Strip on the outside face of a side wall at x (sign gives the side), skipping door gaps [(c, w)]."""
    spans, cur = [], a
    for c, w in sorted(gaps):
        if c - w / 2 > cur:
            spans.append((cur, c - w / 2))
        cur = max(cur, c + w / 2)
    if cur < b:
        spans.append((cur, b))
    s = 1 if x > 0 else -1
    for k, (s0, s1) in enumerate(spans):
        box(f"{name}{k}", x if s > 0 else x - t, x + t if s > 0 else x, s0, s1, z0, z1, m)

def windows(name, x, a, b, z0, z1, gaps, m, step=4.0, gap=0.8):
    """Repeated window panes on a side wall outside face, skipping door gaps."""
    k = 0
    for s0 in frange(a, b, step):
        s1 = min(s0 + step - gap, b)
        if any(s1 > c - w / 2 - 0.3 and s0 < c + w / 2 + 0.3 for c, w in gaps):
            continue
        side_band(f"{name}{k}", x, s0, s1, z0, z1, [], m, 0.12); k += 1

DOOR_W, DOOR_H = CREW["walk_w"], CREW["walk_h"]
CLEAR = DOOR_H + 0.4          # cabin clear height (floor to roof soffit)

def car_seats(prefix, c, half_inner, zf, xs=(-5.1, 5.1), occupants=None):
    """Four rows of 1+1 forward-facing robot seats around a mid-car door zone (c +/- 2.5)."""
    rows = [c - half_inner + 2.3, c - 4.3, c + 4.8, c + half_inner - 1.8]
    occupants = occupants or {}
    for r, y in enumerate(rows):
        for x in xs:
            key = (r, x)
            crew_seat(f"{prefix}_s{r}{'L' if x < 0 else 'R'}", x, y, zf, "-Y", occupants.get(key))
    return rows

# ------------------------------------------------------------------ VEH-01 Ghost Train 70×16×14
def veh01():
    CUT_H[0] = 7.5
    ZF = 2.8; ZR = ZF + CLEAR
    ground("g", -30, 30, -55, 55)
    grp("chassis")
    for x in (-3, 3):
        box(f"rail{x}", x - 0.3, x + 0.3, -50, 50, 0, 0.5, M["steel"])
    for k in range(25):
        box(f"tie{k}", -6, 6, -48 + k * 4, -47 + k * 4, 0, 0.25, M["rubber"])
    cars = [(-35, -13, "cab"), (-11.5, 10.5, "p1"), (12, 34, "p2")]
    for (y0, y1, kind) in cars:
        c = (y0 + y1) / 2
        grp("chassis"); box(f"{kind}_frame", -6.5, 6.5, y0 + 1, y1 - 1, 1.6, 2.4, M["graphite"])
        for yy in (y0 + 4, y1 - 4):
            grp("bogie"); box(f"{kind}_bogie{yy}", -4.5, 4.5, yy - 2, yy + 2, 0.5, 1.6, M["panel"])
            for xx in (-3.6, 3.0):
                for dy in (-1.2, 1.2):
                    wheel(f"{kind}_w{yy}{xx}{dy}", xx, yy + dy, 0.9, 0.6)
        grp("body")
        ops = [("W", c, DOOR_W, 0, DOOR_H), ("E", c, DOOR_W, 0, DOOR_H)]
        if kind != "cab":
            ops.append(("S", 0, DOOR_W, 0, DOOR_H))
        if kind != "p2":
            ops.append(("N", 0, DOOR_W, 0, DOOR_H))
        cabin(kind, -8, 8, y0, y1, ZF, ZR, t=0.5, wall_m=M["graphite"], openings=ops, roof=False)
        gaps = [(c, DOOR_W)]
        for side in (-1, 1):
            windows(f"{kind}_win{side}", side * 8, y0 + 1.5, y1 - 1.5, 6.4, 9.6, gaps, M["amber_e"])
            side_band(f"{kind}_stripe{side}", side * 8, y0, y1, 4.2, 4.8, gaps, M["orange"])
            # sliding door leaf, parked open beside the opening
            box(f"{kind}_door{side}", side * 8.15 - 0.1, side * 8.15 + 0.1, c + DOOR_W / 2, c + DOOR_W / 2 + DOOR_W, ZF, ZF + DOOR_H, M["steel"])
        grp("roof")
        vault(f"{kind}_roof", 0, 8, 2.2, ZR, y0, y1, 0.5, M["steel"])
        walk_check(f"{kind}_doorW", -7.75, c, ZF); walk_check(f"{kind}_doorE", 7.75, c, ZF)
        if kind != "cab":
            walk_check(f"{kind}_gangS", 0, y0 + 0.25, ZF)
        if kind != "p2":
            walk_check(f"{kind}_gangN", 0, y1 - 0.25, ZF)
        grp("interior")
        if kind != "cab":
            occ = {(1, -5.1): "Cypher"} if kind == "p1" else {}
            car_seats(kind, c, 10.5, ZF, occupants=occ)
            walk_check(f"{kind}_aisleF", 0, c - 6.5, ZF); walk_check(f"{kind}_aisleR", 0, c + 6.5, ZF)
            box(f"{kind}_aisle", -1.2, 1.2, y0 + 1, y1 - 1, ZF, ZF + 0.05, M["amber_e"])
    grp("body")
    cbox("nose", 0, -38.2, 6.8, 15, 4, 8, M["graphite"], rot=(math.radians(-25), 0, 0))
    box("windscreen", -6, 6, -35.3, -35.05, 7.6, 10.4, M["cyan_soft"])
    for x in (-5, 5):
        cyl(f"head{x}", x, -40.0, 3.6, 0.3, 1.0, M["cyan_e"], 16, rot=(math.radians(90), 0, 0)).location = (x, -40.1, 4.6)
    box("plow", -6.5, 6.5, -40.6, -39.1, 0.6, 2.2, M["orange"])
    note("nose", (0, -38, 9), "Cab nose, cyan headlights (tunnel silhouette)")
    note("p1_win-10", (-8, -6, 9), "Amber passenger windows (Ghost Train glow)")
    note("p1_bogie-7.5", (0, -7.5, 1.6), "Two-axle bogies (scripted motion, no physics)")
    note("p1_door-1", (-8.2, 1.5, 10.8), "Sliding doors 5 × 8 both sides (shown open)")
    grp("interior")
    box("cab_desk", -5, 5, -34.5, -32.5, ZF, ZF + 2.2, M["graphite"]); box("cab_scr", -4.5, 4.5, -34.6, -34.5, ZF + 2.2, ZF + 4.2, M["cyan_soft"])
    crew_seat("cab_driver", 0, -30.2, ZF, "-Y", "Patch")
    walk_check("cab_floor", 0, -24, ZF)
    note("cab_desk", (0, -33.5, 5), "Control cabin (INT-05): 1 robot seat")
    note("p2_s1L", (-5.1, 18.7, 6), "8 robot seats / car, 1+1 rows, 5.4 aisle (crew standard)")

# ------------------------------------------------------------------ VEH-02 NEXUS-01 Monorail 49×16×17
def veh02():
    CUT_H[0] = 11
    ZF = 5.4; ZR = ZF + CLEAR
    ground("g", -20, 20, -40, 40)
    grp("chassis")
    box("beam", -2, 2, -36, 36, 0, 4, M["graphite"]); box("beam_l", -2.05, -1.95, -36, 36, 2.4, 3.0, M["blue"])
    for y in (-30, 0, 30):
        box(f"pier{y}", -1.5, 1.5, y - 1.5, y + 1.5, -6, 0, M["graphite"])
    for k, (y0, y1) in enumerate(((-24, 0), (1, 25))):
        c = (y0 + y1) / 2
        grp("bogie")
        for yy in (y0 + 5, y1 - 5):
            box(f"straddle{k}{yy}", -3, 3, yy - 2.5, yy + 2.5, 3, 5, M["panel"])
        grp("body")
        ops = [("W", c, DOOR_W, 0, DOOR_H), ("E", c, DOOR_W, 0, DOOR_H), ("N" if k == 0 else "S", 0, DOOR_W, 0, DOOR_H)]
        cabin(f"car{k}", -8, 8, y0, y1, ZF, ZR, t=0.5, wall_m=X["white"], openings=ops, roof=False)
        gaps = [(c, DOOR_W)]
        for side in (-1, 1):
            windows(f"win{k}{side}", side * 8, y0 + 1.5, y1 - 1.5, 9.4, 12.8, gaps, M["cyan_soft"])
            side_band(f"stripe{k}{side}", side * 8, y0, y1, 7.2, 7.8, gaps, M["blue"])
        grp("roof")
        vault(f"roofc{k}", 0, 8, 1.5, ZR, y0, y1, 0.4, M["steel"])
        walk_check(f"car{k}_doorW", -7.75, c, ZF); walk_check(f"car{k}_doorE", 7.75, c, ZF)
        walk_check(f"car{k}_gang", 0, -0.25 if k == 0 else 1.25, ZF)
        walk_check(f"car{k}_aisleF", 0, c - 7, ZF); walk_check(f"car{k}_aisleR", 0, c + 7, ZF)
        grp("interior")
        occ = {(1, 5.1): "Cypher"} if k == 0 else {(2, -5.1): "Patch"}
        car_seats(f"car{k}", c, 11.5, ZF, occupants=occ)
    grp("body")
    cbox("nose", 0, -28.0, 10.0, 15, 4, 9, X["white"], rot=(math.radians(-35), 0, 0))
    box("screen", -4.5, 4.5, -29.6, -29.2, 11.0, 13.4, M["cyan_soft"])
    note("beam", (0, -33, 4), "Straddle guideway beam (INF-12)")
    note("win0-10", (-8, -12, 12), "Panoramic windows; blue route stripe")
    note("nose", (0, -28, 13), "Aerodynamic nose")
    note("car0_s1L", (-5.1, -12, 8), "8 robot seats / car, 1+1 rows (crew standard)")

# ------------------------------------------------------------------ VEH-03 Maintenance Train 40×12×12
def veh03():
    CUT_H[0] = 8
    ZF = 2.6; ZR = ZF + CLEAR
    ground("g", -20, 20, -30, 30)
    grp("chassis")
    for x in (-3, 3):
        box(f"rail{x}", x - 0.3, x + 0.3, -26, 26, 0, 0.5, M["steel"])
    box("frame", -5, 5, -20, 20, 1.6, 2.2, M["graphite"])
    for yy in (-15, 15):
        grp("bogie"); box(f"bog{yy}", -4.5, 4.5, yy - 2, yy + 2, 0.5, 1.6, M["panel"])
        for xx in (-3.6, 3.0):
            for dy in (-1.2, 1.2):
                wheel(f"w{yy}{xx}{dy}", xx, yy + dy, 0.9, 0.6)
    grp("body")
    dc = -11.5
    cabin("cab", -6, 6, -20, -8, ZF, ZR, t=0.4, wall_m=M["yellow"],
          openings=[("W", dc, DOOR_W, 0, DOOR_H), ("E", dc, DOOR_W, 0, DOOR_H)])
    box("cab_win", -5, 5, -20.2, -19.95, 7, 10.4, M["cyan_soft"])
    for k in range(7):
        box(f"haz{k}", -6 + k * 1.8, -5.1 + k * 1.8, -20.3, -20.1, ZF, ZF + 1.6, M["graphite"])
    box("flatbed", -5, 5, -8, 20, 2.2, 3.2, M["panel"])
    for k in range(3):
        box(f"crate{k}", -4, -0.5, -4 + k * 5, -0.5 + k * 5, 3.2, 6, [M["orange"], M["teal"], M["steel"]][k])
    grp("roof")
    cyl("crane_base", 2.5, 12, 3.2, 1.2, 1.8, M["graphite"], 16)
    cbox("crane_boom", 2.5, 7, 9, 1, 12, 1, M["yellow"], rot=(math.radians(55), 0, 0))
    box("beacon", -1, 1, -15, -13, ZR + 0.4, ZR + 1.4, M["amber_e"])
    grp("body")
    note("crane_boom", (2.5, 6, 12), "Hydraulic repair crane (animated)")
    note("cab", (0, -20, 9), "Hazard-yellow walk-in work cab, side doors 5 × 8")
    note("crate1", (-2, 3, 6), "Flatbed spares / rail modules")
    note("beacon", (0, -14, ZR + 1.4), "Amber work beacon")
    grp("interior"); box("cabdesk", -4, 4, -19.6, -18.2, ZF, ZF + 2.0, M["graphite"])
    crew_seat("cab_driver", 0, -15.9, ZF, "-Y", "Patch")
    walk_check("cab_doorW", -5.8, dc, ZF); walk_check("cab_doorE", 5.8, dc, ZF); walk_check("cab_floor", 0, dc, ZF)

# ------------------------------------------------------------------ VEH-04 Cargo Transport Vehicle — TITAN-R1 (26×13×12.8)
def veh04():
    CUT_H[0] = 6.5
    ZF = 2.6; ZR = ZF + CLEAR
    dc = -4.7                                  # side door centre (door zone between the two seat rows)
    ground("g", -16, 16, -20, 20)
    for y in (-10.5, 3.5, 9.0):                # axles kept clear of the door zone
        wheel(f"wR{y}", 5.5, y, 1.75, 1.0); wheel(f"wL{y}", -6.5, y, 1.75, 1.0)
    grp("chassis")
    box("frame", -3.6, 3.6, -12, 12, 1.4, 2.2, M["graphite"])
    box("winch", -2, 2, -13.6, -13, 1.4, 2.8, M["orange"])
    grp("body")
    cabin("cab", -5.4, 5.4, -13, 2.4, ZF, ZR, t=0.4, wall_m=X["white"],
          openings=[("W", dc, DOOR_W, 0, DOOR_H), ("E", dc, DOOR_W, 0, DOOR_H)])
    box("cab_glass", -4.6, 4.6, -13.15, -12.95, 6.2, 9.8, M["cyan_soft"])
    box("cargo", -5.4, 5.4, 2.4, 13, 2.2, ZR + 0.4, M["graphite"])
    gaps = [(dc, DOOR_W)]
    for side in (-1, 1):
        side_band(f"stripe{side}", side * 5.4, -13, 13, 4.2, 4.8, gaps, M["orange"])
        box(f"step{side}", 5.4 if side > 0 else -6.4, 6.4 if side > 0 else -5.4, dc - 2.3, dc + 2.3, 1.2, 1.6, M["steel"])
        text(f"logo{side}", "NEXUS-01", side * 5.5, 8, 7.0, 1.1, M["steel"], rz=math.radians(-90 if side < 0 else 90))
    for x in (-3.6, 3.6):
        box(f"headlight{x}", x - 1, x + 1, -13.2, -13.0, 4.0, 4.6, M["cyan_e"])
    box("bullbar", -5.2, 5.2, -13.8, -13.2, 2.0, 4.4, M["graphite"])
    box("pcore", -1.2, 1.2, 13, 14, 3.0, 5.6, M["cyan_e"])
    grp("roof")
    box("rack", -5, 5, -11, 12, ZR + 0.4, ZR + 0.8, M["steel"])
    for k in range(3):
        box(f"roofbox{k}", -4, 4, -6 + k * 6, -2 + k * 6, ZR + 0.8, ZR + 1.8, [M["orange"], M["graphite"], M["teal"]][k])
    box("lightbar", -4.5, 4.5, -12.6, -12, ZR + 0.4, ZR + 0.9, M["cyan_e"])
    grp("body")
    note("cab_glass", (0, -13, 9.8), "Walk-in cab: 2 driver seats + 2 crew seats (crew standard)")
    note("wR-10.5", (6, -10.5, 3.5), "6 × all-terrain wheels, axles clear of the door")
    note("rack", (0, 5, ZR + 0.8), "Roof module rail (cargo / drone / sensor)")
    note("winch", (0, -13.6, 2.8), "Recovery winch")
    note("step-1", (-6, dc, 1.6), "Side doors 5 × 8 with entry step (both sides)")
    note("pcore", (0, 13.5, 5.6), "Rear power core unit (mobile generator)")
    grp("interior")
    box("dash", -5, 5, -12.6, -11.2, ZF, ZF + 2.0, M["graphite"])
    crew_seat("drv_L", -2.5, -9.0, ZF, "-Y", "Cypher"); crew_seat("drv_R", 2.5, -9.0, ZF, "-Y")
    crew_seat("crew_L", -2.5, 0.0, ZF, "-Y"); crew_seat("crew_R", 2.5, 0.0, ZF, "-Y", "Sentinel")
    walk_check("doorW", -5.2, dc, ZF); walk_check("doorE", 5.2, dc, ZF); walk_check("cab_floor", 0, dc, ZF)

# ------------------------------------------------------------------ VEH-05 Autonomous Robot Shuttle 16×10.4×10.8
def veh05():
    CUT_H[0] = 5.5
    ZF = 1.4; ZR = ZF + CLEAR
    ground("g", -11, 11, -12, 12)
    for y in (-5, 5):
        wheel(f"wR{y}", 5.3, y, 1.1, 0.6, M["cyan_e"]); wheel(f"wL{y}", -5.9, y, 1.1, 0.6, M["cyan_e"])
    grp("body")
    cabin("tub", -5.2, 5.2, -8, 8, ZF, ZR, t=0.4, wall_m=X["white"], openings=[("E", 0, DOOR_W, 0, DOOR_H)], roof_m=X["white"])
    gaps = [(0, DOOR_W)]
    side_band("stripeW", -5.2, -8, 8, 3.0, 3.4, [], M["teal"]); side_band("stripeE", 5.2, -8, 8, 3.0, 3.4, gaps, M["teal"])
    side_band("canopyW", -5.2, -7.4, 7.4, 4.6, 8.8, [], M["glass"], 0.12)
    side_band("canopyE", 5.2, -7.4, 7.4, 4.6, 8.8, gaps, M["glass"], 0.12)
    box("canopyN", -4.4, 4.4, 8.0, 8.12, 4.6, 8.8, M["glass"])
    box("doorleaf", 5.25, 5.4, DOOR_W / 2, DOOR_W / 2 + DOOR_W, ZF, ZF + DOOR_H, M["cyan_soft"])
    for y in (-8.2, 8.2):
        box(f"bump{y}", -4.8, 4.8, y - 0.2, y + 0.2, 1.4, 2.4, M["graphite"])
    box("visor", -3.6, 3.6, -8.15, -7.95, 5.0, 7.6, M["graphite"])
    for x in (-1.8, 1.8):
        sphere(f"eye{x}", x, -8.1, 6.3, 0.55, M["cyan_e"])
    grp("roof")
    box("sensor", -1, 1, -6, -4, ZR + 0.4, ZR + 1.0, M["cyan_e"])
    grp("body")
    note("eye-1.8", (-1.8, -8, 6.3), "Family screen-face front (friendly cyan eyes)")
    note("doorleaf", (5.3, 5, ZF + DOOR_H), "Sliding glass door 5 × 8, curb side (shown open)")
    note("sensor", (0, -5, ZR + 1.0), "Roof lidar (no driver)")
    grp("interior")
    crew_seat("s_FL", -2.4, -5.0, ZF, "+Y"); crew_seat("s_FR", 2.4, -5.0, ZF, "+Y")
    crew_seat("s_RL", -2.4, 5.0, ZF, "-Y"); crew_seat("s_RR", 2.4, 5.0, ZF, "-Y", "Patch")
    note("s_FL", (-2.4, -5, 3), "4 robot seats, facing pairs (crew standard)")
    walk_check("door", 5.0, 0, ZF); walk_check("cabin", 2.2, 0, ZF)

# ------------------------------------------------------------------ VEH-06 Industrial Transport Drone 8×8×3
def veh06():
    CUT_H[0] = 1.6
    ground("g", -8, 8, -8, 8)
    grp("body")
    box("hub", -1.6, 1.6, -1.6, 1.6, 1.4, 2.6, M["graphite"])
    box("hub_l", -1.65, 1.65, -1.65, -1.55, 1.8, 2.1, M["cyan_e"])
    for k, (x, y) in enumerate(((-3, -3), (3, -3), (-3, 3), (3, 3))):
        cbox(f"arm{k}", x / 2, y / 2, 2.1, abs(x) * 1.414, 0.5, 0.4, M["steel"], rot=(0, 0, math.atan2(y, x)))
        grp("roof")
        tube(f"duct{k}", x, y, 1.8, 0.7, 1.5, 0.18, M["orange"])
        cyl(f"rotor{k}", x, y, 2.2, 0.08, 1.25, M["panel"], 24)
        grp("body")
    grp("chassis")
    for x in (-1.2, 1.2):
        box(f"skid{x}", x - 0.15, x + 0.15, -2, 2, 0, 0.3, M["graphite"]); box(f"strut{x}", x - 0.1, x + 0.1, -0.1, 0.1, 0.3, 1.4, M["graphite"])
    grp("interior")
    box("crate", -1.2, 1.2, -1.2, 1.2, 0.4, 1.35, M["orange"])
    note("duct0", (-3, -3, 2.5), "Ducted rotors ×4 (orange guards)")
    note("hub_l", (0, -1.6, 2), "Cyan status band (family accent)")
    note("crate", (0, -1.2, 1.3), "Clamp-on cargo crate (uncrewed)")

# ------------------------------------------------------------------ VEH-07 Freight Elevator 16×16 platform
def veh07():
    CUT_H[0] = 9.5   # above the 5.5 platform deck + crates
    ground("g", -14, 14, -14, 14)
    grp("chassis")
    for (x, y) in ((-9, -9), (9, -9), (-9, 9), (9, 9)):
        box(f"post{x}{y}", x - 0.8, x + 0.8, y - 0.8, y + 0.8, 0, 32, M["yellow"])
    box("head", -9.8, 9.8, -9.8, 9.8, 32, 33.5, M["graphite"])
    box("motor", -3, 3, 4, 9, 33.5, 36, M["steel"])
    for x in (-9, 9):
        cyl(f"cable{x}", x * 0.6, 0, 6, 26, 0.12, M["steel"], 8)
    box("counter", 8.4, 9.6, -2, 2, 14, 20, M["graphite"])
    grp("body")
    box("platform", -8, 8, -8, 8, 5.5, 6.2, M["grate"])
    box("edge", -8, 8, -8.1, -7.9, 6.2, 6.4, M["yellow"])
    for side in ((-8, 8, 7.8, 8), (-8, -7.8, -8, 8), (7.8, 8, -8, 8)):
        box(f"cage{side}", side[0], side[1], side[2], side[3], 6.2, 10, M["steel"])
    box("gate", -8, 8, -8.2, -8.0, 6.2, 7.0, M["orange"])
    box("panel", 6, 7.5, 6.6, 7.6, 6.2, 9, M["graphite"]); box("panel_l", 6.1, 7.4, 6.5, 6.6, 7.6, 8.6, M["cyan_e"])
    grp("interior")
    for k in range(2):
        box(f"crate{k}", -6 + k * 5, -2 + k * 5, -5, -1, 6.2, 9.2, M["orange"])
    note("platform", (0, -8, 6.4), "16 × 16 grated platform (server-owned position)")
    note("motor", (0, 6.5, 36), "Winch head")
    note("gate", (0, -8, 7), "Drop gate (hazard orange)")
    note("counter", (9, 0, 20), "Counterweight")
    robot("r", "Sentinel", 3, 2, 0.4, z=6.2)
    walk_check("platform", -4, 4, 6.2)        # open deck beside the crates

# ------------------------------------------------------------------ VEH-08 Passenger Elevator 8×8 car
def veh08():
    CUT_H[0] = 12.5  # inside the car (floor 8.5, ceiling 16.5)
    ground("g", -8, 8, -8, 8)
    grp("chassis")
    for (x, y) in ((-5, -5), (5, -5), (-5, 5), (5, 5)):
        box(f"post{x}{y}", x - 0.4, x + 0.4, y - 0.4, y + 0.4, 0, 30, M["graphite"])
        box(f"postl{x}{y}", x - 0.45, x + 0.45, y - 0.45, y - 0.35, 0, 30, M["cyan_e"]) if y < 0 else None
    box("head", -5.4, 5.4, -5.4, 5.4, 30, 31, M["graphite"])
    grp("body")
    box("floor", -4, 4, -4, 4, 8, 8.5, M["steel"])
    box("ceiling", -4, 4, -4, 4, 16.6, 17.1, M["steel"])
    for (a0, a1, b0, b1) in ((-4, 4, 3.8, 4), (-4, -3.8, -4, 4), (3.8, 4, -4, 4)):
        box(f"glass{a0}{b0}", a0, a1, b0, b1, 8.5, 16.6, M["glass"])
    box("doorL", -4, -0.05, -4.1, -3.9, 8.5, 16.6, M["cyan_soft"]); box("doorR", 0.05, 4, -4.1, -3.9, 8.5, 16.6, M["cyan_soft"])
    tube("ring", 0, 0, 16.4, 0.2, 3.5, 0.3, M["cyan_e"])
    grp("interior"); box("rail", -3.8, 3.8, 3.6, 3.8, 11, 11.3, M["orange"])
    note("glass-43.8", (0, 4, 13), "Glass car 8 × 8 × 8.1 (district vistas)")
    note("doorL", (-2, -4, 16), "Bi-parting doors (full car width)")
    note("head", (0, 0, 31), "Guide frame + head")
    robot("r", "Cypher", 0, 0, 0.0, z=8.5)
    walk_check("car", 0, 0, 8.5)

# ------------------------------------------------------------------ VEH-09 NX-A17 RAVEN VTOL (56×15.6×18)
def veh09():
    CUT_H[0] = 8
    ZF = 4.3; ZR = ZF + CLEAR
    ground("g", -32, 32, -34, 34)
    grp("chassis")
    for (x, y) in ((-6, -16), (6, -16), (-6.5, 12), (6.5, 12)):
        box(f"gear{x}{y}", x - 0.4, x + 0.4, y - 0.4, y + 0.4, 0.8, 3.9, M["graphite"])
        cyl(f"tyre{x}{y}", x, y, 0, 1.6, 0.8, M["rubber"], 16, rot=(0, math.radians(90), 0)).location = (x, y, 0.8)
    grp("body")
    cabin("fuse", -7.8, 7.8, -20, 18, ZF, ZR, t=0.4, wall_m=M["graphite"], openings=[("N", 0, 9, 0, DOOR_H)])
    cbox("nose", 0, -23.4, 8.4, 14, 6, 8, M["graphite"], rot=(math.radians(-20), 0, 0))
    box("canopy", -5, 5, -26, -20.2, 10.2, 13.2, M["cyan_soft"])
    for side in (-1, 1):
        side_band(f"stripe{side}", side * 7.8, -20, 18, 7.2, 8.0, [], M["orange"])
        text(f"tag{side}", "NX-A17", side * 7.95, 2, 10.5, 1.4, X["white"], rz=math.radians(-90 if side < 0 else 90))
        windows(f"win{side}", side * 7.8, -14, 6, 9.0, 11.2, [], M["cyan_soft"])
    box("ramp", -4.5, 4.5, 18, 22, 3.5, 4.2, M["steel"])
    grp("roof")
    box("wing", -20, 20, -6, 2, ZR + 0.4, ZR + 1.4, M["graphite"])
    for side in (-1, 1):
        x = side * 20
        tube(f"duct{side}", x, -2, ZR - 0.6, 3, 7, 1.2, M["graphite"])
        tube(f"ductring{side}", x, -2, ZR + 2.5, 0.3, 7.1, 0.5, M["orange"])
        cyl(f"rotor{side}", x, -2, ZR + 0.7, 0.2, 5.8, M["panel"], 32)
        cyl(f"rotorhub{side}", x, -2, ZR + 0.5, 0.8, 1.2, M["cyan_e"], 16)
    for side in (-1, 1):
        cbox(f"fin{side}", side * 3.5, 17, ZR + 4.0, 0.6, 6, 7, M["graphite"], rot=(0, math.radians(side * 18), 0))
        box(f"fintip{side}", side * 3.5 - 0.35, side * 3.5 + 0.35, 18.5, 20, ZR + 5.5, ZR + 7.5, M["orange"])
    grp("body")
    note("duct1", (20, -2, ZR + 2.8), "Tilt-ducted VTOL rotors ×2 (Ø 14)")
    note("canopy", (0, -23, 13.2), "Cockpit canopy (pilot + systems bay)")
    note("ramp", (0, 20, 4.2), "Rear loading ramp, 9 × 8 opening (walk-in)")
    note("fin1", (3.5, 18, ZR + 6.5), "Twin tail fins, orange tips")
    note("gear-6-16", (-6, -16, 3), "Retractable landing gear")
    grp("interior")
    box("cockpit_desk", -7, 2.8, -19.6, -18.0, ZF, ZF + 2.3, M["graphite"])
    box("cockpit_scr", -6.5, 2.3, -19.6, -19.5, ZF + 2.3, ZF + 3.8, M["cyan_e"])
    box("systems", 3.6, 7.4, -19.6, -14.6, ZF, ZF + 5.0, M["panel"])
    crew_seat("pilot", -4.2, -15.9, ZF, "-Y", "Cypher")
    for r, y in enumerate((-12.0, -8.1, -4.2, -0.3)):
        for x in (-5.0, 5.0):
            crew_seat(f"cabin_s{r}{'L' if x < 0 else 'R'}", x, y, ZF, "-Y", "Sentinel" if (r, x) == (2, 5.0) else None)
    note("cabin_s0L", (-5, -12, 6), "Personnel config: 8 robot seats, 1+1 rows (crew standard)")
    walk_check("ramp", 0, 17.8, ZF); walk_check("aisleR", 0, 8, ZF); walk_check("aisleF", 0, -6, ZF)
    walk_check("cockpit", 0.5, -15.6, ZF)

REG = {f"VEH-{n:02d}": ("VEH", f, {"hero_dir": (-0.95, -1.0, 0.5)}) for n, f in
       ((1, veh01), (2, veh02), (3, veh03), (4, veh04), (5, veh05), (6, veh06), (7, veh07), (8, veh08), (9, veh09))}
