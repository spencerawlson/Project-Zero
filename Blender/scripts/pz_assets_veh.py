"""VEH-01 … VEH-09 procedural blockouts. Length along Y, nose faces -Y (front view = nose).
Groups drive the exploded view: roof, body, interior, chassis, bogie."""
import math
from pz_asset_lib import *
from pz_build_stasis import M

def wheel(name, x, y, r, w, hub=None):
    grp("bogie")
    cyl(name, x, y, r, w, r, M["rubber"], 20, rot=(0, math.radians(90), 0)).location = (x, y, r)
    cyl(name + "_hub", x, y, r, w + 0.1, r * 0.55, hub or M["orange"], 16, rot=(0, math.radians(90), 0)).location = (x, y, r)

def seat_row(prefix, x0, x1, y, z, n, m=None):
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        box(f"{prefix}{k}", x - 0.9, x + 0.9, y - 0.9, y + 0.9, z, z + 1.4, m or M["orange"])
        box(f"{prefix}{k}b", x - 0.9, x + 0.9, y + 0.7, y + 1.0, z + 1.4, z + 3.2, m or M["orange"])

# ------------------------------------------------------------------ VEH-01 Ghost Train 70×12×14 (Asset Bible target)
def veh01():
    CUT_H[0] = 7.5
    ground("g", -30, 30, -55, 55)
    grp("chassis")
    for x in (-3, 3):
        box(f"rail{x}", x - 0.3, x + 0.3, -50, 50, 0, 0.5, M["steel"])
    for k in range(25):
        box(f"tie{k}", -5, 5, -48 + k * 4, -47 + k * 4, 0, 0.25, M["rubber"])
    cars = [(-35, -13, "cab"), (-11.5, 10.5, "p1"), (12, 34, "p2")]
    for (y0, y1, kind) in cars:
        grp("chassis"); box(f"{kind}_frame", -5, 5, y0 + 1, y1 - 1, 1.6, 2.4, M["graphite"])
        for yy in (y0 + 4, y1 - 4):
            grp("bogie"); box(f"{kind}_bogie{yy}", -4.5, 4.5, yy - 2, yy + 2, 0.5, 1.6, M["panel"])
            for xx in (-3.3, 3.3):
                for dy in (-1.2, 1.2):
                    wheel(f"{kind}_w{yy}{xx}{dy}", xx - 0.3 if xx < 0 else xx - 0.3, yy + dy, 0.9, 0.6)
        grp("body")
        box(f"{kind}_floor", -5.5, 5.5, y0, y1, 2.4, 2.8, M["panel"])
        for side in (-1, 1):
            box(f"{kind}_side{side}", side * 5.5 - 0.4, side * 5.5 + 0.4, y0, y1, 2.8, 11, M["graphite"])
            win_band(f"{kind}_win{side}", "W" if side < 0 else "E", y0 + 2, y1 - 2, 6, 9, side * 5.5 - 0.4, side * 5.5 + 0.4, y0, y1, m=M["amber_e"], step=4, gap=0.8)
            box(f"{kind}_stripe{side}", side * 5.6 - 0.25, side * 5.6 + 0.25, y0, y1, 4.2, 4.8, M["orange"])
            box(f"{kind}_door{side}", side * 5.6 - 0.2, side * 5.6 + 0.2, (y0 + y1) / 2 - 1.8, (y0 + y1) / 2 + 1.8, 2.8, 10, M["steel"])
        box(f"{kind}_endS", -5.5, 5.5, y0, y0 + 0.4, 2.8, 11, M["graphite"]); box(f"{kind}_endN", -5.5, 5.5, y1 - 0.4, y1, 2.8, 11, M["graphite"])
        grp("roof")
        vault(f"{kind}_roof", 0, 5.5, 2.2, 11, y0, y1, 0.5, M["steel"])
        grp("interior")
        if kind != "cab":
            seat_row(f"{kind}_sL", -5, -1.5, (y0 + y1) / 2 - 6, 2.8, 2); seat_row(f"{kind}_sR", 1.5, 5, (y0 + y1) / 2 - 6, 2.8, 2)
            seat_row(f"{kind}_sL2", -5, -1.5, (y0 + y1) / 2 + 4, 2.8, 2); seat_row(f"{kind}_sR2", 1.5, 5, (y0 + y1) / 2 + 4, 2.8, 2)
            box(f"{kind}_aisle", -1.2, 1.2, y0 + 1, y1 - 1, 2.8, 2.85, M["amber_e"])
    grp("body")
    cbox("nose", 0, -36.5, 6.5, 11, 4, 8, M["graphite"], rot=(math.radians(-25), 0, 0))
    box("windscreen", -4, 4, -36.3, -35.9, 7.5, 10, M["cyan_soft"])
    for x in (-3.5, 3.5):
        cyl(f"head{x}", x, -38.3, 3.6, 0.3, 1.0, M["cyan_e"], 16, rot=(math.radians(90), 0, 0)).location = (x, -38.4, 4.6)
    box("plow", -5, 5, -39, -37.5, 0.6, 2.2, M["orange"])
    note("nose", (0, -37, 9), "Cab nose, cyan headlights (tunnel silhouette)")
    note("p1_win-1", (-5.5, -6, 9), "Amber passenger windows (Ghost Train glow)")
    note("p1_bogie-7.5", (0, -7.5, 1.6), "Two-axle bogies (scripted motion, no physics)")
    note("p1_door-1", (-5.6, -0.5, 10), "Sliding doors both sides")
    grp("interior")
    box("cab_desk", -4, 4, -32, -29, 2.8, 5, M["graphite"]); box("cab_scr", -3.5, 3.5, -32.1, -32, 5, 7, M["cyan_soft"])
    note("cab_desk", (0, -30.5, 5), "Control cabin (INT-05)")
    note("p2_sL0", (-3, 17, 4), "Passenger compartment (INT-04)")
    robot("driver", "Patch", 0, -27, math.pi, z=2.8)
    robot("pass1", "Cypher", -3, 0, 0.0, z=2.8)

# ------------------------------------------------------------------ VEH-02 NEXUS-01 Monorail 48×10×12
def veh02():
    CUT_H[0] = 11
    ground("g", -20, 20, -40, 40)
    grp("chassis")
    box("beam", -2, 2, -36, 36, 0, 4, M["graphite"]); box("beam_l", -2.05, -1.95, -36, 36, 2.4, 3.0, M["blue"])
    for y in (-30, 0, 30):
        box(f"pier{y}", -1.5, 1.5, y - 1.5, y + 1.5, -6, 0, M["graphite"])
    for k, (y0, y1) in enumerate(((-24, 0), (1, 25))):
        grp("bogie")
        for yy in (y0 + 5, y1 - 5):
            box(f"straddle{k}{yy}", -3, 3, yy - 2.5, yy + 2.5, 3, 5, M["panel"])
        grp("body")
        box(f"car{k}", -5, 5, y0, y1, 5, 14, M["white"])
        for side in (-1, 1):
            win_band(f"win{k}{side}", "W" if side < 0 else "E", y0 + 2, y1 - 2, 9, 12, -5, 5, y0, y1, m=M["cyan_soft"])
            box(f"stripe{k}{side}", side * 5 - 0.12, side * 5 + 0.12, y0, y1, 6.8, 7.4, M["blue"])
        grp("roof")
        vault(f"roofc{k}", 0, 5, 1.5, 14, y0, y1, 0.4, M["steel"])
    grp("body")
    cbox("nose", 0, -25.5, 9.5, 10, 4, 9, M["white"], rot=(math.radians(-35), 0, 0))
    box("screen", -3.5, 3.5, -25.7, -25.3, 10.5, 13, M["cyan_soft"])
    note("beam", (0, -33, 4), "Straddle guideway beam (INF-12)")
    note("win0-1", (-5, -12, 12), "Panoramic windows; blue route stripe")
    note("nose", (0, -26, 13), "Aerodynamic nose")
    grp("interior")
    seat_row("s1", -4, 4, -14, 5, 3); seat_row("s2", -4, 4, 8, 5, 3)
    note("s10", (-3, -14, 7), "Bench seating 6 robots / car")
    robot("p1", "Cypher", 2, -4, 0.0, z=5); robot("p2", "Patch", -2, 14, 0.0, z=5)

# ------------------------------------------------------------------ VEH-03 Maintenance Train 40×10×12
def veh03():
    CUT_H[0] = 8
    ground("g", -20, 20, -30, 30)
    grp("chassis")
    for x in (-3, 3):
        box(f"rail{x}", x - 0.3, x + 0.3, -26, 26, 0, 0.5, M["steel"])
    box("frame", -5, 5, -20, 20, 1.6, 2.6, M["graphite"])
    for yy in (-15, 15):
        grp("bogie"); box(f"bog{yy}", -4.5, 4.5, yy - 2, yy + 2, 0.5, 1.6, M["panel"])
        for xx in (-3.6, 3.0):
            for dy in (-1.2, 1.2):
                wheel(f"w{yy}{xx}{dy}", xx, yy + dy, 0.9, 0.6)
    grp("body")
    box("cab", -5, 5, -20, -8, 2.6, 11, M["yellow"]); box("cab_win", -4, 4, -20.2, -19.9, 7, 10, M["cyan_soft"])
    for k in range(6):
        box(f"haz{k}", -5 + k * 1.7, -4.2 + k * 1.7, -20.3, -20.1, 2.6, 4.2, M["graphite"])
    box("flatbed", -5, 5, -8, 20, 2.6, 3.2, M["panel"])
    for k in range(3):
        box(f"crate{k}", -4, -0.5, -4 + k * 5, -0.5 + k * 5, 3.2, 6, [M["orange"], M["teal"], M["steel"]][k])
    grp("roof")
    cyl("crane_base", 2.5, 12, 3.2, 1.2, 1.8, M["graphite"], 16)
    cbox("crane_boom", 2.5, 7, 9, 1, 12, 1, M["yellow"], rot=(math.radians(55), 0, 0))
    box("beacon", -1, 1, -15, -13, 11, 12, M["amber_e"])
    grp("body")
    note("crane_boom", (2.5, 6, 12), "Hydraulic repair crane (animated)")
    note("cab", (0, -20, 9), "Hazard-yellow work cab")
    note("crate1", (-2, 3, 6), "Flatbed spares / rail modules")
    note("beacon", (0, -14, 12), "Amber work beacon")
    grp("interior"); box("cabdesk", -3, 3, -18, -16, 2.6, 4.5, M["graphite"])
    robot("op", "Patch", 0, -12, math.pi, z=2.6)

# ------------------------------------------------------------------ VEH-04 Cargo Transport Vehicle — TITAN-R1 (24×9.5×9.6)
def veh04():
    CUT_H[0] = 6.5
    ground("g", -15, 15, -20, 20)
    grp("bogie")
    for y in (-8, 0, 8):
        for x in (-4.4, 4.4):
            wheel(f"w{y}{x}", x - (0.9 if x > 0 else 0.1), y, 1.75, 1.0)
    grp("chassis")
    box("frame", -3.6, 3.6, -11, 11, 1.4, 2.6, M["graphite"])
    box("winch", -2, 2, -12.6, -11, 1.4, 2.8, M["orange"])
    grp("body")
    box("cab", -4.7, 4.7, -12, -4, 2.6, 8.4, X["white"])
    box("cab_glass", -4.2, 4.2, -12.15, -11.9, 5.6, 8, M["cyan_soft"])
    box("cargo", -4.7, 4.7, -4, 12, 2.6, 8.8, M["graphite"])
    for side in (-1, 1):
        box(f"stripe{side}", side * 4.75 - 0.08, side * 4.75 + 0.08, -12, 12, 4.2, 4.8, M["orange"])
        box(f"door{side}", side * 4.75 - 0.08, side * 4.75 + 0.08, -3, 1, 2.8, 8, M["steel"])
        text(f"logo{side}", "NEXUS-01", side * 4.85, 6, 6.2, 0.9, M["graphite"], rz=math.radians(-90 if side < 0 else 90))
    for x in (-3.3, 3.3):
        box(f"headlight{x}", x - 1, x + 1, -12.2, -12.0, 4.0, 4.6, M["cyan_e"])
    box("bullbar", -4.5, 4.5, -12.8, -12.2, 2.0, 4.4, M["graphite"])
    gear("gear", 0, -12.25, 7.0, 0.9) if False else None
    grp("roof")
    box("rack", -4.2, 4.2, -9, 11, 8.8, 9.2, M["steel"])
    for k in range(3):
        box(f"roofbox{k}", -3.5, 3.5, -6 + k * 5.5, -2 + k * 5.5, 9.2, 10.2, [M["orange"], M["graphite"], M["teal"]][k])
    box("lightbar", -3.5, 3.5, -11.6, -11, 8.4, 8.9, M["cyan_e"])
    grp("body")
    note("cab_glass", (0, -12, 8), "Driver cab, panoramic glass (2 seats)")
    note("w-8-4.4", (-4.4, -8, 3.5), "6 × all-terrain wheels, orange hubs")
    note("rack", (0, 5, 10.2), "Roof module rail (cargo / drone / sensor)")
    note("winch", (0, -12.6, 2.8), "Recovery winch")
    note("door-1", (-4.8, -1, 8), "Side entry doors (both sides)")
    grp("interior")
    box("dash", -4, 4, -11.5, -10, 2.6, 4.4, M["graphite"])
    seat_row("crew", -3.8, 3.8, -2, 2.6, 3)
    box("cargo_floor", -4.2, 4.2, 3, 11.6, 2.6, 2.8, M["grate"])
    for k in range(2):
        box(f"crate{k}", -3.8 + k * 4, -0.6 + k * 4, 6, 10.5, 2.8, 5.4, M["orange"])
    box("pcore", -1, 1, 0.5, 2.5, 2.6, 5, M["cyan_e"])
    note("crew0", (-2.5, -2, 4), "Crew cabin (4 seats)")
    note("crate0", (-2, 8, 5.4), "Cargo bay ≈ 8 m³")
    note("pcore", (0, 1.5, 5), "Power core unit (mobile generator)")
    robot("drv", "Cypher", -2, -8.5, 0.0, z=2.6)

# ------------------------------------------------------------------ VEH-05 Autonomous Robot Shuttle 16×8×8
def veh05():
    CUT_H[0] = 5.5
    ground("g", -10, 10, -12, 12)
    grp("bogie")
    for y in (-5, 5):
        for x in (-3.6, 3.6):
            wheel(f"w{y}{x}", x - (0.6 if x > 0 else 0), y, 1.1, 0.6, M["cyan_e"])
    grp("body")
    box("tub", -4, 4, -8, 8, 1.2, 4.4, X["white"])
    box("stripe", -4.05, 4.05, -8.05, 8.05, 3.0, 3.4, M["teal"])
    box("door", 3.95, 4.1, -2.5, 2.5, 1.4, 7.6, M["cyan_soft"])
    for y in (-7.9, 7.9):
        box(f"bump{y}", -3.8, 3.8, y - 0.2, y + 0.2, 1.4, 2.4, M["graphite"])
    box("visor", -3.2, 3.2, -8.1, -7.9, 4.6, 6.6, M["graphite"])
    for x in (-1.6, 1.6):
        sphere(f"eye{x}", x, -8.05, 5.6, 0.45, M["cyan_e"])
    grp("roof")
    box("canopy", -4, 4, -8, 8, 4.4, 7.4, M["glass"])
    box("roof", -3.8, 3.8, -7.6, 7.6, 7.4, 8.0, X["white"])
    box("sensor", -1, 1, -6, -4, 8.0, 8.6, M["cyan_e"])
    grp("body")
    note("eye-1.6", (-1.6, -8, 5.6), "Family screen-face front (friendly cyan eyes)")
    note("door", (4, 0, 7.6), "Sliding glass door (curb side)")
    note("sensor", (0, -5, 8.6), "Roof lidar (no driver)")
    grp("interior")
    seat_row("s", -3.4, 3.4, -4, 1.4, 2); seat_row("s2", -3.4, 3.4, 3, 1.4, 2)
    note("s0", (-1.7, -4, 3), "4 robot seats, facing pairs")
    robot("p", "Patch", -1.5, 0, 0.0, z=1.4)

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
    note("crate", (0, -1.2, 1.3), "Clamp-on cargo crate")

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
    box("ceiling", -4, 4, -4, 4, 16.5, 17, M["steel"])
    for (a0, a1, b0, b1) in ((-4, 4, 3.8, 4), (-4, -3.8, -4, 4), (3.8, 4, -4, 4)):
        box(f"glass{a0}{b0}", a0, a1, b0, b1, 8.5, 16.5, M["glass"])
    box("doorL", -4, -0.05, -4.1, -3.9, 8.5, 16.5, M["cyan_soft"]); box("doorR", 0.05, 4, -4.1, -3.9, 8.5, 16.5, M["cyan_soft"])
    tube("ring", 0, 0, 16.3, 0.2, 3.5, 0.3, M["cyan_e"])
    grp("interior"); box("rail", -3.8, 3.8, 3.6, 3.8, 11, 11.3, M["orange"])
    note("glass-43.8", (0, 4, 13), "Glass car 8 × 8 × 8 (district vistas)")
    note("doorL", (-2, -4, 16), "Bi-parting doors")
    note("head", (0, 0, 31), "Guide frame + head")
    robot("r", "Cypher", 0, 0, 0.0, z=8.5)

# ------------------------------------------------------------------ VEH-09 NX-A17 RAVEN VTOL (56×40×16)
def veh09():
    CUT_H[0] = 8
    ground("g", -32, 32, -34, 34)
    grp("chassis")
    for (x, y) in ((-5, -16), (5, -16), (-6, 12), (6, 12)):
        box(f"gear{x}{y}", x - 0.4, x + 0.4, y - 0.4, y + 0.4, 0.8, 4, M["graphite"])
        cyl(f"tyre{x}{y}", x, y, 0, 1.6, 0.8, M["rubber"], 16, rot=(0, math.radians(90), 0)).location = (x, y, 0.8)
    grp("body")
    box("fuse", -5.5, 5.5, -20, 18, 4, 13, M["graphite"])
    cbox("nose", 0, -22, 8, 9, 6, 8, M["graphite"], rot=(math.radians(-20), 0, 0))
    box("canopy", -4, 4, -25, -19, 9.5, 12.5, M["cyan_soft"])
    for side in (-1, 1):
        box(f"stripe{side}", side * 5.55 - 0.08, side * 5.55 + 0.08, -20, 18, 7, 7.8, M["orange"])
        text(f"tag{side}", "NX-A17", side * 5.65, 0, 9, 1.4, X["white"], rz=math.radians(-90 if side < 0 else 90))
        win_band(f"win{side}", "W" if side < 0 else "E", -14, 6, 9, 11, -5.5, 5.5, -20, 18, m=M["cyan_soft"], step=4, gap=1)
    box("ramp", -4.5, 4.5, 18, 22, 3.5, 4.2, M["steel"])
    grp("roof")
    box("wing", -20, 20, -6, 2, 11.5, 12.5, M["graphite"])
    for side in (-1, 1):
        x = side * 20
        tube(f"duct{side}", x, -2, 10.5, 3, 7, 1.2, M["graphite"])
        tube(f"ductring{side}", x, -2, 13.6, 0.3, 7.1, 0.5, M["orange"])
        cyl(f"rotor{side}", x, -2, 11.8, 0.2, 5.8, M["panel"], 32)
        cyl(f"rotorhub{side}", x, -2, 11.6, 0.8, 1.2, M["cyan_e"], 16)
    for side in (-1, 1):
        cbox(f"fin{side}", side * 3.5, 17, 15.5, 0.6, 6, 7, M["graphite"], rot=(0, math.radians(side * 18), 0))
        box(f"fintip{side}", side * 3.5 - 0.35, side * 3.5 + 0.35, 18.5, 20, 17, 19, M["orange"])
    grp("body")
    note("duct1", (20, -2, 14), "Tilt-ducted VTOL rotors ×2 (Ø 14)")
    note("canopy", (0, -22, 12.5), "Cockpit canopy (pilot + systems)")
    note("ramp", (0, 20, 4.2), "Rear loading ramp (extraction)")
    note("fin1", (3.5, 18, 18), "Twin tail fins, orange tips")
    note("gear-5-16", (-5, -16, 3), "Retractable landing gear")
    grp("interior")
    box("cabin_floor", -5, 5, -18, 17, 4, 4.3, M["grate"])
    seat_row("sL", -5, -2, -8, 4.3, 3); seat_row("sR", 2, 5, -8, 4.3, 3)
    seat_row("sL2", -5, -2, 2, 4.3, 3); seat_row("sR2", 2, 5, 2, 4.3, 3)
    box("cockpit_desk", -4, 4, -21, -18.5, 4.3, 7, M["graphite"]); box("cockpit_scr", -3.5, 3.5, -21.1, -21, 7, 8.5, M["cyan_e"])
    note("sL0", (-4, -8, 6), "Personnel config: 8 seats")
    robot("pilot", "Cypher", -1.5, -16.5, math.pi, z=4.3)

REG = {f"VEH-{n:02d}": ("VEH", f, {"hero_dir": (-0.95, -1.0, 0.5)}) for n, f in
       ((1, veh01), (2, veh02), (3, veh03), (4, veh04), (5, veh05), (6, veh06), (7, veh07), (8, veh08), (9, veh09))}
