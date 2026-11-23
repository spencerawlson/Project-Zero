"""Compose Stasis Facility sheets SF-01 .. SF-05 from renders + layout data."""
import os, sys, math
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pz_sheet_kit import *
from pz_plan import draw_plan
import matplotlib.patches as mp

RD = os.path.join(ROOT, "Stasis_Facility", "renders")
SD = os.path.join(ROOT, "Stasis_Facility", "sheets")
R = lambda n: os.path.join(RD, n + ".png")

# elevation pixel mapping (see pz_build_stasis ELEV_SCALE: 15 px / stud, centre z = 22 at row 500)
PX = 15.0
def ez(z):
    return 500 - (z - 22) * PX
def ex_front(x):
    return 1200 + x * PX
def ex_rear(x):
    return 1200 - x * PX
def ey_left(y):
    return 1200 - (y - 60) * PX
def ey_right(y):
    return 1200 + (y - 60) * PX

# ============================================================== SF-02
def sf02():
    fig = new_sheet()
    frame(fig, "SF-02", "STASIS FACILITY — FLOOR PLAN", "Ground level (+0) · program, circulation, egress, service access · 8-stud grid", 1, 1)
    panel(fig, (0.012, 0.05, 0.585, 0.862), "GROUND FLOOR PLAN  ·  LEVEL +0", "Grid A–L / 1–16 at 8-stud centres")
    ax = fig.add_axes([0.016, 0.055, 0.577, 0.83])
    draw_plan(ax)
    x0 = 0.607
    panel(fig, (x0, 0.505, 0.381, 0.407), "ROOM SCHEDULE", "studs · clear heights are design targets")
    rows = []
    clear = {"R01": "19", "R02": "19", "R03": "19", "R04": "18 / 31 crown", "R05": "17", "R06": "17", "R07": "17",
             "R08": "17", "R09": "17", "R10": "17", "R11": "17–21", "R12": "21", "R13": "21"}
    func = {"R01": "Arrival, scanner arch, ZERO greeting", "R02": "Camera wall, lockdown control",
            "R03": "Decon pad, lockers (lore props)", "R04": "8 pods, aisle, mezzanine, crane",
            "R05": "Pod service hatches, pipe runs", "R06": "Coolant tanks (Cooling state)",
            "R07": "Fallback egress, always openable", "R08": "Salvage nodes, crates",
            "R09": "Vitals consoles, obs. window", "R10": "Power core, breaker puzzle",
            "R11": "Fallback egress, always openable", "R12": "Cargo pad, mission exit",
            "R13": "Roof access stair, riser"}
    for (rid, label, a, b, c, d, ck) in L.ROOMS:
        rows.append((rid, label.title()[:26], f"{b - a}×{d - c}", f"{(b - a) * (d - c):,}", clear[rid], func[rid]))
    table(fig, (x0 + 0.006, 0.512, 0.369, 0.372), ["ID", "SPACE", "SIZE", "AREA", "CLEAR H", "FUNCTION / INTERACTION"],
          rows, [0.07, 0.26, 0.08, 0.08, 0.13, 0.38], fs=6.6)
    panel(fig, (x0, 0.205, 0.381, 0.292), "DOOR SCHEDULE", "W × H studs")
    kinds = {"main": "Octagonal portal, slide", "blast": "Octagonal blast, slide", "rollup": "Roll-up shutter",
             "egress": "Emergency swing", "std": "Swing / slide"}
    beh = {"D01": "Locks in Lockdown", "D02": "Scanner-gated airlock", "D03": "Opens on power restore",
           "D04": "Server-owned state", "D05": "Never locks (failsafe)", "D06": "Never locks (failsafe)"}
    drows = [(d[0], d[1][:30], kinds[d[7]], f"{d[5]}×{d[6]}", beh.get(d[0], "Proximity open")) for d in L.DOORS]
    table(fig, (x0 + 0.006, 0.211, 0.369, 0.262), ["ID", "LOCATION", "TYPE", "W×H", "BEHAVIOUR"],
          drows, [0.08, 0.36, 0.25, 0.08, 0.23], fs=5.9)
    panel(fig, (x0, 0.05, 0.381, 0.147), "LEGEND & CIRCULATION", None)
    items = [("line", C["cyan"], "-", "Awakening route: Cypher (P01) leads players → D02 → D01"),
             ("line", C["red"], (0, (5, 2)), "Lockdown escape route via service bay (D03 → D04)"),
             ("line", C["green"], (0, (2, 2)), "Emergency egress (D05 / D06 never lock)"),
             ("line", C["text"], (0, (4, 3)), "Observation mezzanine above (+12)"),
             ("line", C["orange"], (0, (6, 4)), "Overhead crane rails above (+25)"),
             ("patch", "#0F151D", None, "Centre aisle grate, 12 wide, amber edge strips"),
             ("patch", C["cyan"], None, "Observation glazing R09 → R04"),
             ("patch", "#1E88E5", None, "Pod coolant / power spine (rear of pod)")]
    for i, (k, col, ls, t) in enumerate(items):
        cx = x0 + 0.012 + (i // 4) * 0.19
        cy = 0.168 - (i % 4) * 0.028
        if k == "line":
            fig.lines.append(Line2D([cx, cx + 0.022], [cy, cy], transform=fig.transFigure, color=col, ls=ls, lw=1.6))
        else:
            fig.patches.append(mp.Rectangle((cx, cy - 0.007), 0.022, 0.014, transform=fig.transFigure, fc=col,
                                            ec=C["amber"] if col == "#0F151D" else "none", lw=0.6, hatch="////" if col == "#0F151D" else None))
        fig.text(cx + 0.027, cy, t, fontsize=6.4, va="center", color=C["text"])
    save(fig, os.path.join(SD, "SF-02_FloorPlan.png"))

if __name__ == "__main__":
    which = sys.argv[1:] or ["sf02"]
    for w in which:
        globals()[w]()
