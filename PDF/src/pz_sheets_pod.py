"""SF-04 Stasis Pod sheets."""
from pz_sheet_kit import *
import matplotlib.patches as mp
import math
import numpy as np

RD = os.path.join(ROOT, "Stasis_Facility", "renders")
SD = os.path.join(ROOT, "Stasis_Facility", "sheets")
R = lambda n: os.path.join(RD, n + ".png")

K = 1400 / 22.0
def pf(x, z):  return (700 + (x - 2) * K, 700 - (z - 7.5) * K)      # front / section
def pr(x, z):  return (700 - (x - 2) * K, 700 - (z - 7.5) * K)      # rear
def pl(y, z):  return (700 - y * K, 700 - (z - 7.5) * K)            # left
def prt(y, z): return (700 + y * K, 700 - (z - 7.5) * K)            # right
def pt(x, y):  return (700 + (x - 2) * K, 700 - y * K)              # top / plan cut

def glass_overlay(ax, closed):
    """Exact glass half-shell positions (r = 3.2) drawn over the plan cut."""
    ox, oy = ax._pz_off
    def arc(a0, a1, r):
        ts = np.linspace(math.radians(a0), math.radians(a1), 60)
        pts = [pt(r * math.cos(t), r * math.sin(t)) for t in ts]
        return [p[0] - ox for p in pts], [p[1] - oy for p in pts]
    ax.plot(*arc(0, 180, 3.25), color=C["cyan"], lw=2.4, zorder=6)                 # rear half (fixed)
    if closed:
        ax.plot(*arc(180, 360, 3.25), color=C["cyan"], lw=2.4, zorder=6)           # front half (closed)
        ax.text(*[v - o for v, o in zip(pt(0, -4.0), (ox, oy))], "front half closed", fontsize=6, color=C["cyan"], ha="center", va="top")
    else:
        ax.plot(*arc(165 + 180, 165 + 360, 3.0), color=C["amber"], lw=2.4, ls=(0, (3, 2)), zorder=6)  # parked front half
        ax.plot(*arc(180, 360, 3.25), color=C["green"], lw=0.8, ls=(0, (2, 3)), zorder=6)
        ax.text(*[v - o for v, o in zip(pt(0, -4.0), (ox, oy))], "OPEN: exit ↓", fontsize=6.4, color=C["green"], ha="center", va="top", weight="bold")
        ax.text(*[v - o for v, o in zip(pt(0, 3.7), (ox, oy))], "front half parked", fontsize=6, color=C["amber"], ha="center", va="bottom")

def pod_view(fig, rect, shot, title, crop, sub=None):
    panel(fig, rect, title, sub)
    return image_axes(fig, rect, R(shot), crop=crop)

def sf04a():
    fig = new_sheet()
    frame(fig, "SF-04", "STASIS POD — ORTHOGRAPHIC SET (CLOSED)",
          "Asset BLD-01-M01 · PZ_AWK_StasisPod_A · all views rendered from one Blender model at one scale", 1, 2)
    w, g, x0 = 0.238, 0.008, 0.012
    ax = pod_view(fig, (x0, 0.47, w, 0.442), "pod_closed_front", "FRONT", (60, 120, 1340, 1260), "63.6 px / stud")
    dim(ax, pf(-6.3, 0), pf(-6.3, 14.5), "14.5 overall", off=-40, vertical=True)
    for (z0, z1, t) in ((0, 2.5, "2.5"), (2.5, 11, "8.5 glass"), (11, 13.5, "2.5"), (13.5, 14.5, "1.0")):
        dim(ax, pf(5.6, z0), pf(5.6, z1), t, off=20, vertical=True, ext=False, fs=6.6)
    dim(ax, pf(-4.0, 13.5), pf(4.0, 13.5), "Ø 8.0 cap", off=-130, fs=6.8)
    dim(ax, pf(-6.3, 0), pf(4.7, 0), "11.0 overall width", off=55, fs=6.8)
    dim(ax, pf(9.5, 0), pf(9.5, 6.0), "6.0", off=95, vertical=True, fs=6.6)
    ax.text(*pf(9.2, -0.6), "SCALE REF.: CYPHER\n6.0 studs (CHR-01)", fontsize=6, color=C["amber"], ha="center", va="top")
    ax = pod_view(fig, (x0 + w + g, 0.47, w, 0.442), "pod_closed_left", "LEFT", (300, 120, 1180, 1260))
    dim(ax, pl(4.9, 0), pl(-4.4, 0), "9.3 overall depth", off=55, fs=6.8)
    dim(ax, pl(4.5, 2.5), pl(-4.5, 2.5), "Ø 9.0 plinth", off=-25, fs=6.6)
    callout(ax, pl(4.55, 9), "coolant risers ×2", (40, -80), fs=6.6)
    callout(ax, pl(-4.4, 1.45), "status strip", (-40, 60), C["orange"], fs=6.6)
    ax = pod_view(fig, (x0 + 2 * (w + g), 0.47, w, 0.442), "pod_closed_rear", "REAR", (60, 120, 1340, 1260))
    callout(ax, pr(0, 1.6), "power conduit (orange)", (120, 70), C["orange"], fs=6.6)
    callout(ax, pr(0, 8), "service spine 1.8 × 1.0", (160, -60), fs=6.6)
    ax = pod_view(fig, (x0 + 3 * (w + g), 0.47, w, 0.442), "pod_closed_right", "RIGHT", (220, 120, 1100, 1260))
    callout(ax, prt(-4.2, 3.8), "front console, screen 20° tilt", (-20, -140), fs=6.6, ha="center")
    ax = pod_view(fig, (x0, 0.05, w, 0.41), "pod_closed_top", "TOP", (120, 260, 1000, 1140))
    dim(ax, pt(-6.3, -4.4), pt(4.7, -4.4), "11.0", off=70, fs=6.8)
    dim(ax, pt(4.7, -4.4), pt(4.7, 5.3), "9.7", off=60, vertical=True, fs=6.8)
    fig.text(x0 + 0.01, 0.062, "▼ FRONT — faces centre aisle", fontsize=7, color=C["cyan"], weight="bold")
    panel(fig, (x0 + w + g, 0.05, 0.36, 0.41), "SPECIFICATION", "design assumptions")
    tx = x0 + w + g + 0.01
    text_block(fig, tx, 0.425, [
        ("Function", "o"),
        "Cryogenic stasis pod for one robot (or human, Chapter 4).",
        "Each player wakes in own pod (P02–04, P06); Cypher first in P01.",
        ("Envelope", "o"),
        "11.0 W × 9.7 D × 14.5 H studs  ·  pod bay module 14 × 18",
        "Clear interior Ø 6.0 × 8.5 H  →  occupant ≤ 7.5 studs tall",
        ("Construction stack (bottom → top)", "o"),
        "Step ring Ø10 · 0.4  |  octagonal plinth Ø9 · 2.1",
        "Deck + cyan deck light Ø6  |  glass cylinder Ø6.4 · 8.5",
        "Cap Ø8 · 2.5 with cyan light band  |  crown housing Ø5.2 · 1.0",
        ("Glazing", "o"),
        "Two half-shells. Rear half fixed; front half rotates 165°",
        "about the pod axis to park behind the rear half (sheet 2/2).",
        ("Peripherals", "o"),
        "Power/diagnostic unit (L) 2.6×3.2×3.5 · console (R) 1.6×1.3×3.8",
        ("Scale reference", "o"),
        "Cypher (6.0 studs) stands beside the pod and sleeps inside it —",
        "canonical model, unmodified (see CHR-00 / CHR-01).",
    ], fs=7.3, lh=0.0192)
    x2 = x0 + w + g + 0.36 + g
    panel(fig, (x2, 0.05, 0.988 - x2, 0.41), "MATERIALS & COLOUR", "HEX = sRGB")
    rows = [("MAT-01", "Graphite metal", "#2B2F36", "plinth, cap, posts, units · metal 0.8 / rough 0.45"),
            ("MAT-02", "Brushed steel", "#8A9099", "crown, deck, coolant lines · metal 0.9 / rough 0.3"),
            ("MAT-03", "Cryo glass", "#4FCFE6", "glass shells · Roblox Glass, transparency 0.35"),
            ("MAT-04", "Cyan emissive", "#22D3EE", "cap band, deck ring, screens · Neon"),
            ("MAT-05", "Orange industrial", "#E8731A", "power conduit, status strip"),
            ("MAT-06", "Amber emissive", "#FFB020", "unit status strip · Neon"),
            ("MAT-07", "Coolant blue", "#1E88E5", "coolant line bands"),
            ("MAT-08", "Panel dark", "#1C1F24", "step ring, service spine")]
    yy = 0.405
    for mid, name, hx, use in rows:
        yy -= 0.043
        fig.patches.append(mp.Rectangle((x2 + 0.01, yy), 0.03, 0.033, transform=fig.transFigure, fc=hx, ec=C["line"], zorder=2))
        fig.text(x2 + 0.046, yy + 0.024, f"{mid}  {name}", fontsize=7.2, weight="bold", color=C["text"], va="center")
        fig.text(x2 + 0.046, yy + 0.008, f"{hx}  ·  {use}", fontsize=6.4, color=C["muted"], va="center")
    save(fig, os.path.join(SD, "SF-04_StasisPod_1_Ortho.png"))

def sf04b():
    fig = new_sheet()
    frame(fig, "SF-04", "STASIS POD — STATES, INTERNALS & CONNECTIONS", "Closed / open states · section · services · wake animation", 2, 2)
    panel(fig, (0.012, 0.42, 0.24, 0.492), "CLOSED  ·  STASIS", "Cycles render")
    image_axes(fig, (0.012, 0.42, 0.24, 0.492), R("pod_closed_hero"), crop=(100, 60, 1100, 1140))
    panel(fig, (0.26, 0.42, 0.24, 0.492), "OPEN  ·  WAKE COMPLETE", "Cycles render")
    image_axes(fig, (0.26, 0.42, 0.24, 0.492), R("pod_open_hero"), crop=(100, 60, 1100, 1140))
    panel(fig, (0.508, 0.42, 0.25, 0.492), "SECTION A–A  (cut at Y = 0, looking rear)", None)
    ax = image_axes(fig, (0.508, 0.42, 0.25, 0.492), R("pod_closed_section"), crop=(130, 200, 1000, 1220))
    callout(ax, pf(0, 13.0), "1 cap: cryo manifold", (200, -60), fs=6.4)
    callout(ax, pf(3.4, 12.0), "2 cyan band Ø8.1", (120, 40), fs=6.4)
    callout(ax, pf(0.6, 8.4), "3 Cypher 6.0 (limit 7.5)", (200, 10), fs=6.4)
    callout(ax, pf(-2.9, 6.0), "4 rear glass (fixed)", (-60, -90), fs=6.4)
    callout(ax, pf(2.6, 2.85), "5 deck + light ring", (170, -40), fs=6.4)
    callout(ax, pf(0.0, 1.3), "6 power riser", (200, 50), C["orange"], fs=6.4)
    callout(ax, pf(-5.0, 2.0), "7 power / diag. unit", (-10, 120), C["amber"], fs=6.4)
    panel(fig, (0.766, 0.668, 0.222, 0.244), "PLAN CUT +7 · CLOSED", "glass overlay")
    ax = image_axes(fig, (0.766, 0.668, 0.222, 0.244), R("pod_closed_plancut"), crop=(150, 240, 1050, 1060))
    glass_overlay(ax, closed=True)
    panel(fig, (0.766, 0.42, 0.222, 0.24), "PLAN CUT +7 · OPEN", "front half → 165°")
    ax = image_axes(fig, (0.766, 0.42, 0.222, 0.24), R("pod_open_plancut"), crop=(150, 240, 1050, 1060))
    glass_overlay(ax, closed=False)
    panel(fig, (0.012, 0.05, 0.47, 0.36), "POWER & COOLING CONNECTIONS", "all services enter from rear / floor")
    rows = [("SVC-1", "Power feed", "Ø0.9 orange conduit", "Rear floor box → plinth", "R10 Energy / Power state"),
            ("SVC-2", "Coolant supply", "Ø0.64 steel, blue band", "Floor → cap manifold", "R06 Cryo / Cooling state"),
            ("SVC-3", "Coolant return", "Ø0.64 steel, blue band", "Cap manifold → floor", "R06 Cryo plant"),
            ("SVC-4", "Data / vitals", "inside service spine", "Spine → console", "R09 Medical monitoring"),
            ("SVC-5", "Service hatch", "4 × 6 wall panel", "Pod rear ↔ corridor R05", "Repair objectives")]
    table(fig, (0.018, 0.06, 0.458, 0.31), ["ID", "SERVICE", "SPEC", "ROUTING", "SOURCE / GAME STATE"], rows,
          [0.09, 0.17, 0.24, 0.25, 0.25], fs=6.6)
    panel(fig, (0.49, 0.05, 0.498, 0.36), "WAKE SEQUENCE · ANIMATION (server-triggered, client-rendered)", None)
    steps = [("0.0 s", "STASIS", "cyan band steady, status strip amber (dim)", C["cyan"]),
             ("0.0–1.2", "THAW", "band pulses cyan → white; frost decal fades; hiss SFX", C["white"]),
             ("1.2–1.6", "UNLOCK", "status strip → orange; crown lamp blinks twice", C["orange"]),
             ("1.6–3.2", "OPEN", "front glass half: TweenService rotate 165° (Quad, Out)", C["amber"]),
             ("3.2–4.0", "RELEASE", "deck ring fades; occupant ProximityPrompt enabled", C["green"]),
             ("—", "FAULT", "Power Offline: band dark, red status, manual-crank prompt", C["red"])]
    y = 0.36
    for t, n, d, col in steps:
        fig.patches.append(mp.Rectangle((0.5, y - 0.03), 0.005, 0.036, transform=fig.transFigure, color=col))
        fig.text(0.512, y - 0.012, t, fontsize=7.2, color=C["muted"], va="center", family="DejaVu Sans Mono")
        fig.text(0.575, y - 0.012, n, fontsize=7.6, color=col, weight="bold", va="center")
        fig.text(0.64, y - 0.012, d, fontsize=7.2, color=C["text"], va="center")
        y -= 0.047
    text_block(fig, 0.5, 0.078, [("Runs once per player pod (P01 Cypher plays it first as the cue). Hinge model only; glass collision off while open; server owns state.", "a")], fs=6.8)
    save(fig, os.path.join(SD, "SF-04_StasisPod_2_States.png"))
