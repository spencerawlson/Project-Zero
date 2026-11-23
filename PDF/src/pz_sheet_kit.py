"""Shared sheet frame, styling and drawing helpers for the Production Bible.
Sheets are 17 x 11 in landscape (tabloid) rendered at 160 dpi."""
import os, sys, json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib.lines import Line2D
from PIL import Image

ROOT = r"D:\Project Zero_Roblox\Project_Zero_Production_Bible"
sys.path.append(os.path.join(ROOT, "Blender", "scripts"))
import pz_layout as L

W_IN, H_IN, DPI = 17.0, 11.0, 160
C = dict(bg="#0B1220", panel="#101A2B", panel2="#0E1626", line="#2A3A55", cyan="#22D3EE",
         orange="#E8731A", amber="#FFB020", text="#DCE6F2", muted="#8FA3BF", red="#E5383B",
         green="#35D07F", violet="#8B5CF6", white="#FFFFFF")
REV = "REV C  ·  2026-11-19"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": C["text"], "axes.edgecolor": C["line"]})

def new_sheet():
    fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI, facecolor=C["bg"])
    return fig

def frame(fig, sheet_id, title, subtitle, page, total, status="FOR REVIEW", asset="BLD-01  ·  PZ_AWK_StasisFacility",
          note="Dimensions are DESIGN ASSUMPTIONS in Roblox studs — not measurements taken from concept art."):
    # header band
    fig.patches.append(mp.Rectangle((0, 0.925), 1, 0.075, transform=fig.transFigure, color="#0F1E33", zorder=0))
    fig.patches.append(mp.Rectangle((0, 0.922), 1, 0.003, transform=fig.transFigure, color=C["orange"], zorder=1))
    fig.text(0.018, 0.962, sheet_id, fontsize=22, weight="bold", color=C["orange"], va="center")
    fig.text(0.115, 0.968, title, fontsize=19, weight="bold", color=C["white"], va="center")
    fig.text(0.115, 0.938, subtitle, fontsize=10.5, color=C["cyan"], va="center")
    fig.text(0.982, 0.968, "PROJECT ZERO  ·  NEXUS-01", fontsize=11, weight="bold", color=C["text"], ha="right", va="center")
    fig.text(0.982, 0.940, "ASSET & ARCHITECTURE PRODUCTION BIBLE", fontsize=8.5, color=C["muted"], ha="right", va="center")
    # footer title block
    fig.patches.append(mp.Rectangle((0, 0), 1, 0.038, transform=fig.transFigure, color="#0F1E33", zorder=0))
    fig.patches.append(mp.Rectangle((0, 0.038), 1, 0.002, transform=fig.transFigure, color=C["line"], zorder=1))
    cells = [("ASSET", asset), ("SHEET", f"{sheet_id}  ({page}/{total})"),
             ("STATUS", status), ("REVISION", REV)]
    for (k, v), x in zip(cells, (0.018, 0.25, 0.37, 0.47)):
        fig.text(x, 0.026, k, fontsize=6.5, color=C["muted"], va="center")
        fig.text(x, 0.012, v, fontsize=8.5 if len(v) < 34 else 7.4, color=C["text"], weight="bold", va="center")
    fig.text(0.982, 0.019, note, fontsize=7.5, color=C["amber"], ha="right", va="center", style="italic")

def panel(fig, rect, label=None, sub=None):
    x, y, w, h = rect
    fig.patches.append(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.004",
                                         transform=fig.transFigure, facecolor=C["panel"], edgecolor=C["line"], lw=0.8, zorder=0))
    if label:
        fig.text(x + 0.008, y + h - 0.016, label, fontsize=9.5, weight="bold", color=C["cyan"], va="center")
    if sub:
        fig.text(x + w - 0.008, y + h - 0.016, sub, fontsize=7.5, color=C["muted"], ha="right", va="center")

def image_axes(fig, rect, path, crop=None, pad_top=0.03, pad=0.006):
    """Place an image inside a panel rect, preserving aspect. Returns (ax, (x0,y0) crop offset)."""
    im = Image.open(path).convert("RGBA")
    ox, oy = 0, 0
    if crop:
        im = im.crop(crop); ox, oy = crop[0], crop[1]
    x, y, w, h = rect
    x += pad; y += pad; w -= 2 * pad; h -= pad + pad_top
    fw, fh = fig.get_size_inches()
    iw, ih = im.size
    box_aspect = (w * fw) / (h * fh)
    img_aspect = iw / ih
    if img_aspect > box_aspect:
        nh = w * fw / img_aspect / fh
        y += (h - nh) / 2; h = nh
    else:
        nw = h * fh * img_aspect / fw
        x += (w - nw) / 2; w = nw
    ax = fig.add_axes([x, y, w, h]); ax.set_zorder(3)
    ax.imshow(im, interpolation="lanczos")
    ax.set_xlim(0, iw); ax.set_ylim(ih, 0); ax.axis("off")
    ax._pz_off = (ox, oy)
    return ax

def callout(ax, xy, text, dxy=(60, -60), color=None, fs=7.5, ha=None):
    """xy in original image pixels (crop offset applied)."""
    color = color or C["cyan"]
    ox, oy = getattr(ax, "_pz_off", (0, 0))
    x, y = xy[0] - ox, xy[1] - oy
    tx, ty = x + dxy[0], y + dxy[1]
    ax.plot([x], [y], "o", ms=3.5, color=color, mec="#000000", mew=0.4, zorder=6)
    ax.annotate(text, (x, y), (tx, ty), fontsize=fs, color=C["white"], zorder=7,
                ha=ha or ("left" if dxy[0] >= 0 else "right"), va="center",
                bbox=dict(boxstyle="round,pad=0.25", fc="#0B1220E0", ec=color, lw=0.7),
                arrowprops=dict(arrowstyle="-", color=color, lw=0.8))

def dim(ax, p0, p1, text, off=30, color=None, fs=7.5, vertical=False, ext=True):
    """Dimension line between two image-pixel points (crop offset applied)."""
    color = color or C["amber"]
    ox, oy = getattr(ax, "_pz_off", (0, 0))
    (x0, y0), (x1, y1) = (p0[0] - ox, p0[1] - oy), (p1[0] - ox, p1[1] - oy)
    if vertical:
        lx = x0 + off
        if ext:
            ax.plot([x0, lx + (6 if off > 0 else -6)], [y0, y0], color=color, lw=0.5)
            ax.plot([x1, lx + (6 if off > 0 else -6)], [y1, y1], color=color, lw=0.5)
        ax.annotate("", (lx, y0), (lx, y1), arrowprops=dict(arrowstyle="<|-|>", color=color, lw=0.8, mutation_scale=7))
        ax.text(lx + (8 if off > 0 else -8), (y0 + y1) / 2, text, fontsize=fs, color=color, rotation=90,
                ha="left" if off > 0 else "right", va="center", weight="bold")
    else:
        ly = y0 + off
        if ext:
            ax.plot([x0, x0], [y0, ly + (6 if off > 0 else -6)], color=color, lw=0.5)
            ax.plot([x1, x1], [y1, ly + (6 if off > 0 else -6)], color=color, lw=0.5)
        ax.annotate("", (x0, ly), (x1, ly), arrowprops=dict(arrowstyle="<|-|>", color=color, lw=0.8, mutation_scale=7))
        ax.text((x0 + x1) / 2, ly + (12 if off > 0 else -6), text, fontsize=fs, color=color,
                ha="center", va="top" if off > 0 else "bottom", weight="bold",
                bbox=dict(boxstyle="square,pad=0.1", fc=C["panel"], ec="none"))

def text_block(fig, x, y, lines, fs=8.2, lh=0.0185, color=None, width=None):
    """lines: list of str or (str, style) where style in {'h','b','m','o','c'}."""
    for ln in lines:
        st = None
        if isinstance(ln, tuple):
            ln, st = ln
        kw = dict(fontsize=fs, color=color or C["text"], va="top")
        if st == "h":
            kw.update(fontsize=fs + 1.5, weight="bold", color=C["cyan"]); y -= lh * 0.3
        elif st == "b":
            kw.update(weight="bold")
        elif st == "m":
            kw.update(color=C["muted"])
        elif st == "o":
            kw.update(color=C["orange"], weight="bold")
        elif st == "a":
            kw.update(color=C["amber"], style="italic")
        fig.text(x, y, ln, **kw)
        y -= lh * (1.25 if st == "h" else 1.0)
    return y

def table(fig, rect, cols, rows, widths, fs=7.4, head_color=None, row_h=None):
    x, y, w, h = rect
    n = len(rows) + 1
    rh = row_h or h / n
    head_color = head_color or "#173049"
    fig.patches.append(mp.Rectangle((x, y + h - rh), w, rh, transform=fig.transFigure, color=head_color, zorder=1))
    cx = x
    for c, cw in zip(cols, widths):
        fig.text(cx + 0.004, y + h - rh / 2, c, fontsize=fs, weight="bold", color=C["cyan"], va="center", zorder=2)
        cx += cw * w
    for i, r in enumerate(rows):
        yy = y + h - rh * (i + 2)
        if i % 2 == 0:
            fig.patches.append(mp.Rectangle((x, yy), w, rh, transform=fig.transFigure, color="#13203A", zorder=1))
        cx = x
        for j, (v, cw) in enumerate(zip(r, widths)):
            fig.text(cx + 0.004, yy + rh / 2, str(v), fontsize=fs, color=C["text"] if j else C["orange"],
                     weight="bold" if j == 0 else "normal", va="center", zorder=2)
            cx += cw * w
    return y + h - rh * (n)

def swatch_row(fig, x, y, items, sw=0.022, sh=0.03, gap=0.006, fs=6.8):
    for name, hexv in items:
        fig.patches.append(mp.Rectangle((x, y), sw, sh, transform=fig.transFigure, color=hexv, zorder=2, ec=C["line"]))
        fig.text(x + sw + 0.004, y + sh * 0.68, name, fontsize=fs, color=C["text"], va="center")
        fig.text(x + sw + 0.004, y + sh * 0.22, hexv, fontsize=fs - 0.6, color=C["muted"], va="center", family="DejaVu Sans Mono")
        x += sw + 0.085 + gap

def save(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=DPI, facecolor=C["bg"])
    plt.close(fig)
    print("SHEET", path)

def load_meta(render_dir, shot):
    with open(os.path.join(render_dir, shot + ".json")) as f:
        return json.load(f)
