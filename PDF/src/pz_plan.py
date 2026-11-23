"""Architectural floor plan of PZ_AWK_StasisFacility drawn from pz_layout (same data as the Blender model)."""
import math
import matplotlib.patches as mp
from pz_sheet_kit import L, C

def merged_edges():
    edges = {}
    for (_, _, x0, x1, y0, y1, _) in L.ROOMS:
        for key, iv in ((("x", y0), (x0, x1)), (("x", y1), (x0, x1)), (("y", x0), (y0, y1)), (("y", x1), (y0, y1))):
            edges.setdefault(key, []).append(iv)
    out = []
    for (axis, fixed), ivs in edges.items():
        ivs.sort(); cur = list(ivs[0])
        for s, e in ivs[1:]:
            if s <= cur[1]:
                cur[1] = max(cur[1], e)
            else:
                out.append((axis, fixed, *cur)); cur = [s, e]
        out.append((axis, fixed, *cur))
    return out

def wall_rects(axis, fixed, a, b, thick, offset=0.0):
    ops = sorted([(d[3] - d[5] / 2, d[3] + d[5] / 2) for d in L.DOORS
                  if d[2] == axis and abs(d[4] - fixed) < 0.6 and a <= d[3] <= b])
    segs, cur = [], a
    for o0, o1 in ops:
        segs.append((cur, o0)); cur = o1
    segs.append((cur, b))
    t0 = fixed - thick / 2 + offset
    out = []
    for s0, s1 in segs:
        if s1 - s0 <= 0:
            continue
        out.append((s0, t0, s1 - s0, thick) if axis == "x" else (t0, s0, thick, s1 - s0))
    return out

def draw_plan(ax, labels=True, routes=True, dims=True, grid=True, fs=6.6):
    ax.set_facecolor(C["panel"])
    ax.set_zorder(3)
    ax.set_aspect("equal")
    ax.set_xlim(-66, 66); ax.set_ylim(-34, 142)
    ax.axis("off")
    # grid
    cols = "ABCDEFGHIJKL"
    if grid:
        for i, x in enumerate(range(-44, 45, 8)):
            ax.plot([x, x], [-6, 126], color="#1D2B44", lw=0.5, zorder=0)
            ax.add_patch(mp.Circle((x, 130), 2.6, fc=C["panel"], ec=C["muted"], lw=0.6, zorder=3))
            ax.text(x, 130, cols[i] if i < len(cols) else str(i), fontsize=fs - 0.8, ha="center", va="center", color=C["muted"], zorder=4)
        for j, y in enumerate(range(0, 121, 8)):
            ax.plot([-50, 50], [y, y], color="#1D2B44", lw=0.5, zorder=0)
            ax.add_patch(mp.Circle((54, y), 2.6, fc=C["panel"], ec=C["muted"], lw=0.6, zorder=3))
            ax.text(54, y, str(j + 1), fontsize=fs - 0.8, ha="center", va="center", color=C["muted"], zorder=4)
    # room fills
    for (rid, label, x0, x1, y0, y1, ck) in L.ROOMS:
        ax.add_patch(mp.Rectangle((x0, y0), x1 - x0, y1 - y0, fc=L.ROOM_COLOURS[ck], ec="none", zorder=1))
    # centre aisle + floor trenches
    ax.add_patch(mp.Rectangle((-L.AISLE_HALF, 24), 2 * L.AISLE_HALF, 80, fc="#0F151D", ec=C["amber"], lw=0.7, hatch="////", zorder=2))
    # mezzanine / crane above (dashed)
    mz = L.MEZZANINE
    ax.add_patch(mp.Rectangle((-23.5, mz["y0"]), 47, mz["y1"] - mz["y0"], fc="none", ec=C["text"], lw=0.6, ls=(0, (4, 3)), zorder=4))
    for s in (-1, 1):
        ax.plot([s * L.CRANE["rail_x"]] * 2, [26, 102], color=C["orange"], lw=0.6, ls=(0, (6, 4)), zorder=4)
    # mezzanine stair
    for k in range(12):
        ax.add_patch(mp.Rectangle((-23.5, 33 + k), 4, 1, fc="#3B4654", ec=C["muted"], lw=0.3, zorder=3))
    # pods
    for (pid, x, y, face) in L.PODS:
        sgn = 1 if x < 0 else -1          # +1: faces +X (aisle) for west pods
        ax.add_patch(mp.RegularPolygon((x, y), 8, radius=4.6, orientation=math.pi / 8, fc="#1F2A36", ec=C["steel"] if False else "#8A9099", lw=0.7, zorder=5))
        ax.add_patch(mp.Circle((x, y), 3.2, fc="#0E3A47", ec=C["cyan"], lw=1.0, zorder=6))
        # console (front-right) and unit (left) rotated with facing
        cx, cy = x + sgn * 3.6, y + sgn * 3.9
        ax.add_patch(mp.Rectangle((cx - 0.65, cy - 0.8), 1.3, 1.6, fc="#2B2F36", ec=C["cyan"], lw=0.5, zorder=6))
        ux, uy = x + sgn * 0.6, y - sgn * 5.0
        ax.add_patch(mp.Rectangle((ux - 1.6, uy - 1.3), 3.2, 2.6, fc="#2B2F36", ec=C["amber"], lw=0.5, zorder=6))
        # coolant/power spine behind pod (toward wall)
        ax.add_patch(mp.Rectangle((x - sgn * 4.6 - 0.7, y - 1.3), 1.4, 2.6, fc="#1E88E5", ec="none", zorder=6))
        if labels:
            ax.text(x, y, pid, fontsize=fs - 0.6, ha="center", va="center", color=C["white"], weight="bold", zorder=7)
    # props
    def r(x0, x1, y0, y1, fc="#2B2F36", ec="#8A9099", z=5, lw=0.4):
        ax.add_patch(mp.Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec=ec, lw=lw, zorder=z))
    r(-8, 8, 12, 14.5)                                         # reception desk
    for s in (-1, 1):
        r(s * 5 - 0.6, s * 5 + 0.6, 18.5, 20, fc=C["cyan"], ec="none")   # scanner arch posts
    ax.plot([-5, 5], [19.25, 19.25], color=C["cyan"], lw=0.8, ls=":", zorder=5)
    r(-43, -41.5, 4, 20); r(-38, -30, 8, 11)                  # security wall + desk
    for k in range(6):
        r(26 + k * 3, 28.6 + k * 3, 21, 23)                     # lockers
    r(30, 38, 6, 14, fc="#5A3418", ec=C["orange"])            # decon pad
    for k, y in enumerate((30, 40, 50, 62)):
        ax.add_patch(mp.Circle((-38, y), 3.2, fc="#3A4250", ec="#8A9099", lw=0.5, zorder=5))   # cryo tanks
    for k in range(4):
        r(-43, -39, 90 + k * 3.4, 93 + k * 3.4)                 # crates
    for y in (36, 46):
        r(26, 30, y, y + 7)                                     # medical desks
    r(36, 42, 30, 34)                                           # diagnostic bed
    ax.add_patch(mp.Circle((34, 76), 4.2, fc="#0E3A47", ec=C["cyan"], lw=1.0, zorder=5))   # power core
    ax.add_patch(mp.Circle((34, 76), 2.2, fc=C["cyan"], ec="none", zorder=6))
    for k in range(5):
        r(42, 43.5, 62 + k * 6, 67 + k * 6)                     # cabinets
    r(26, 29, 70, 82)                                           # energy console
    r(-6, 6, 108, 116, fc="#5A3418", ec=C["orange"])          # cargo pad
    for k in range(3):
        r(14, 21, 106 + k * 4.4, 110 + k * 4.4)
    for k in range(14):
        r(-42, -36, 105 + k, 106 + k, fc="#3B4654", ec=C["muted"], lw=0.25)  # service stair
    ax.plot([-31.2, -31.2], [24.5, 103.5], color="#1E88E5", lw=1.2, zorder=5)   # corridor pipes
    ax.plot([-25.6, -25.6], [24.5, 103.5], color=C["orange"], lw=1.0, zorder=5)
    # walls
    T = L.EXT_WALL
    ext = [("x", 0, -44, 44, T / 2), ("x", 120, -44, 44, -T / 2), ("y", -44, 0, 120, T / 2), ("y", 44, 0, 120, -T / 2)]
    for axis, fixed, a, b, off in ext:
        for (x, y, w, h) in wall_rects(axis, fixed, a, b, T, off):
            ax.add_patch(mp.Rectangle((x, y), w, h, fc="#C9D3E0", ec="none", zorder=8))
    for (axis, fixed, a, b) in merged_edges():
        if (axis == "x" and fixed in (0, 120)) or (axis == "y" and fixed in (-44, 44)):
            continue
        if axis == "y" and fixed == 24:
            ow = L.OBS_WINDOW
            for (x, y, w, h) in wall_rects(axis, fixed, a, ow["y0"], L.WALL) + wall_rects(axis, fixed, ow["y1"], b, L.WALL):
                ax.add_patch(mp.Rectangle((x, y), w, h, fc="#AEB8C6", ec="none", zorder=8))
            ax.add_patch(mp.Rectangle((23.6, ow["y0"]), 0.8, ow["y1"] - ow["y0"], fc=C["cyan"], ec="none", zorder=8))
            continue
        for (x, y, w, h) in wall_rects(axis, fixed, a, b, L.WALL):
            ax.add_patch(mp.Rectangle((x, y), w, h, fc="#AEB8C6", ec="none", zorder=8))
    # doors
    for (did, label, axis, pos, fixed, w, h, kind) in L.DOORS:
        if axis == "x":
            p0, p1 = (pos - w / 2, fixed), (pos + w / 2, fixed)
        else:
            p0, p1 = (fixed, pos - w / 2), (fixed, pos + w / 2)
        col = {"main": C["cyan"], "blast": C["cyan"], "rollup": C["amber"], "egress": C["green"], "std": C["text"]}[kind]
        if kind in ("main", "blast"):
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=col, lw=2.2, zorder=9, solid_capstyle="butt")
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            ax.plot([mx], [my], marker="8", ms=5, mfc="none", mec=col, mew=0.8, zorder=9)
        elif kind == "rollup":
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=col, lw=1.6, ls=(0, (2, 1.4)), zorder=9)
        else:
            # swing door arc
            if axis == "x":
                hinge = p0; ang0 = 0; leaf_end = (p0[0], p0[1] + (w if fixed < 60 else -w))
                theta = (0, 90) if fixed < 60 else (-90, 0)
            else:
                hinge = p0; leaf_end = (p0[0] + (w if fixed < 0 else -w), p0[1])
                theta = (0, 90) if fixed < 0 else (90, 180)
            ax.plot([hinge[0], leaf_end[0]], [hinge[1], leaf_end[1]], color=col, lw=0.8, zorder=9)
            ax.add_patch(mp.Arc(hinge, 2 * w, 2 * w, theta1=theta[0], theta2=theta[1], color=col, lw=0.5, ls=(0, (2, 1.5)), zorder=9))
        if labels:
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            dx, dy = (0, -2.6) if axis == "x" else (-2.8 if fixed <= 0 else 2.8, 0)
            if kind in ("main", "blast", "rollup"):
                dx, dy = 5.5, (-2.2 if fixed < 60 else 2.2)
            ax.text(mx + dx, my + dy, did, fontsize=fs - 1.6, color=col, ha="center", va="center", zorder=10,
                    bbox=dict(boxstyle="round,pad=0.12", fc=C["panel"], ec="none", alpha=0.85))
    # room labels
    if labels:
        for (rid, label, x0, x1, y0, y1, ck) in L.ROOMS:
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            if rid == "R04":
                cx, cy = -15, 97
            if rid == "R12":
                cx, cy = -13, 112
            if rid == "R05":
                ax.text(cx, 64, f"{rid}\n{label}", fontsize=fs - 1.3, ha="center", va="center", rotation=90, color=C["white"], zorder=10, weight="bold")
                continue
            if rid == "R01":
                cy = 6
            if rid == "R03":
                cy = 17
            if rid == "R09":
                cx, cy = 37, 52
            if rid == "R10":
                cx, cy = 34, 88
            if rid == "R06":
                cy = 69 - 0.5
                cx = -38
            area = (x1 - x0) * (y1 - y0)
            ax.text(cx, cy, f"{rid}  {label}\n{x1 - x0}×{y1 - y0} st · {area:,} st²", fontsize=fs - 1.4,
                    ha="center", va="center", color=C["white"], zorder=10, linespacing=1.25,
                    bbox=dict(boxstyle="round,pad=0.2", fc="#0B1220C8", ec="none"))
    # routes
    if routes:
        ax.plot([-11, -3, -3, 0, 0, 0], [40, 40, 30, 30, 24, -12], color=C["cyan"], lw=1.4, zorder=11,
                ls="-", marker=None)
        ax.annotate("", (0, -14), (0, -8), arrowprops=dict(arrowstyle="-|>", color=C["cyan"], lw=1.4), zorder=11)
        ax.plot([3, 3, 0, 0, 0], [86, 100, 100, 104, 126], color=C["red"], lw=1.2, ls=(0, (5, 2)), zorder=11)
        ax.annotate("", (0, 128), (0, 123), arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.2), zorder=11)
        ax.plot([4, 20, 24, 34, 34, 44, 49], [90, 90, 90, 90, 112, 112, 112], color=C["green"], lw=1.0, ls=(0, (2, 2)), zorder=11)
        ax.plot([-28, -28, -38, -38, -49], [100, 80, 80, 80, 80], color=C["green"], lw=1.0, ls=(0, (2, 2)), zorder=11)
        ax.text(-4.5, -12, "MAIN ENTRY", fontsize=fs - 1, color=C["cyan"], ha="right", va="center", weight="bold")
        ax.text(-4.5, 135.5, "SERVICE ACCESS", fontsize=fs - 1, color=C["amber"], ha="right", va="center", weight="bold")
        ax.text(48, 116, "EXIT E", fontsize=fs - 1, color=C["green"], ha="left", va="center", weight="bold")
        ax.text(-48, 84, "EXIT W", fontsize=fs - 1, color=C["green"], ha="right", va="center", weight="bold")
    # dimensions
    if dims:
        def hd(x0, x1, y, t):
            ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<|-|>", color=C["amber"], lw=0.7, mutation_scale=6), zorder=12)
            ax.text((x0 + x1) / 2, y - 1.3, t, fontsize=fs - 1, color=C["amber"], ha="center", va="top", weight="bold")
        def vd(y0, y1, x, t):
            ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<|-|>", color=C["amber"], lw=0.7, mutation_scale=6), zorder=12)
            ax.text(x - 1.2, (y0 + y1) / 2, t, fontsize=fs - 1, color=C["amber"], ha="right", va="center", rotation=90, weight="bold")
        hd(-44, 44, -24, "88")
        for a, b in ((-44, -32), (-32, -24), (-24, 24), (24, 44)):
            hd(a, b, -19, str(b - a))
        vd(0, 120, -60, "120")
        for a, b in ((0, 24), (24, 104), (104, 120)):
            vd(a, b, -55, str(b - a))
        for x in (-44, -32, -24, 24, 44):
            ax.plot([x, x], [-25, -2], color=C["amber"], lw=0.3, zorder=12)
        for y in (0, 24, 104, 120):
            ax.plot([-61, -46], [y, y], color=C["amber"], lw=0.3, zorder=12)
    # north arrow + scale bar
    ax.annotate("", (58, 141), (58, 133), arrowprops=dict(arrowstyle="-|>", color=C["text"], lw=1.0))
    ax.text(58, 131.5, "N", fontsize=fs, ha="center", va="top", color=C["text"], weight="bold")
    for k, (a, b) in enumerate(((22, 30), (30, 38), (38, 54))):
        ax.add_patch(mp.Rectangle((a, -31), b - a, 1.4, fc=C["text"] if k % 2 == 0 else C["panel"], ec=C["text"], lw=0.5))
    for v, t in ((22, "0"), (30, "8"), (38, "16"), (54, "32 studs")):
        ax.text(v, -28.8, t, fontsize=fs - 1.5, color=C["muted"], ha="center", va="bottom")
