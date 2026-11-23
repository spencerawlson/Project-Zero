"""Generic per-asset sheet composer for BLD-02…15, VEH-01…09, EQP-01…12, INF-01…12, INT-02…10.
Reads <Category>/<ID>/renders/*.png + *.json (camera mapping, anchors, notes, bbox)."""
from pz_sheet_kit import *
import matplotlib.patches as mp
import pz_inventory as INV
from pz_asset_specs import SPECS, CAT_TEMPLATES

CATDIR = {"BLD": "Buildings", "VEH": "Vehicles", "EQP": "Equipment", "INF": "Infrastructure", "INT": "Interiors"}
CATNAME = {"BLD": "BUILDING", "VEH": "VEHICLE", "EQP": "EQUIPMENT", "INF": "INFRASTRUCTURE", "INT": "INTERIOR"}
INVD = {a[0]: a for a in INV.ASSETS}

SUBDIR = ["renders"]
def rd(aid):
    return os.path.join(ROOT, CATDIR[aid[:3]], aid, SUBDIR[0])

def meta(aid, shot):
    p = os.path.join(rd(aid), shot + ".json")
    return json.load(open(p)) if os.path.exists(p) else None

# ---------------------------------------------------------------- world → pixel for ortho views
def mapper(m):
    W, H = m["res"]; k = W / m["ortho"] if W >= H else H / m["ortho"]
    cx, cy, cz = m["center"]; v = m["view"]
    if v == "front":   return lambda x, y, z: (W / 2 + (x - cx) * k, H / 2 - (z - cz) * k)
    if v == "rear":    return lambda x, y, z: (W / 2 - (x - cx) * k, H / 2 - (z - cz) * k)
    if v == "left":    return lambda x, y, z: (W / 2 - (y - cy) * k, H / 2 - (z - cz) * k)
    if v == "right":   return lambda x, y, z: (W / 2 + (y - cy) * k, H / 2 - (z - cz) * k)
    if v in ("top", "plan"): return lambda x, y, z: (W / 2 + (x - cx) * k, H / 2 - (y - cy) * k)
    if v == "section": return lambda x, y, z: (W / 2 + (x - cx) * k, H / 2 - (z - cz) * k)
    if v == "scale":   return lambda x, y, z: (W / 2 - (y - cy) * k, H / 2 - (z - cz) * k)
    return None

def bbox(m):
    b = m["bbox"] if m.get("view") == "scale" else (m.get("bbox_obj") or m["bbox"])
    return b[0], b[1]

def fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")

def crop_for(m, f, pad=60):
    mn, mx = bbox(m)
    xs, ys = [], []
    for x in (mn[0], mx[0]):
        for y in (mn[1], mx[1]):
            for z in (mn[2], mx[2]):
                px, py = f(x, y, z); xs.append(px); ys.append(py)
    W, H = m["res"]
    return (max(0, int(min(xs) - pad * 2.2)), max(0, int(min(ys) - pad)), min(W, int(max(xs) + pad * 2.2)), min(H, int(max(ys) + pad * 1.6)))

def ortho_panel(fig, rect, aid, shot, title, dims=True):
    m = meta(aid, shot)
    path = os.path.join(rd(aid), shot + ".png")
    if not m or not os.path.exists(path):
        panel(fig, rect, title, "MISSING RENDER"); return None
    f = mapper(m)
    crop = crop_for(m, f) if f and "res" in m else None
    panel(fig, rect, title, None)
    ax = image_axes(fig, rect, path, crop=crop)
    if f and dims:
        mn, mx = bbox(m)
        v = shot
        if v == "scale":
            dim(ax, f(0, mx[1], mn[2]), f(0, mx[1], mx[2]), fmt(mx[2] - mn[2]), off=40, vertical=True, fs=6.8)
        elif v in ("front", "rear", "section"):
            dim(ax, f(mn[0], 0, mn[2]), f(mx[0], 0, mn[2]), fmt(mx[0] - mn[0]), off=28, fs=6.8)
            dim(ax, f(mn[0] if v != "rear" else mx[0], 0, mn[2]), f(mn[0] if v != "rear" else mx[0], 0, mx[2]), fmt(mx[2] - mn[2]), off=-34, vertical=True, fs=6.8)
        elif v in ("left", "right"):
            dim(ax, f(0, mn[1], mn[2]), f(0, mx[1], mn[2]), fmt(mx[1] - mn[1]), off=28, fs=6.8)
        elif v in ("top", "plan"):
            dim(ax, f(mn[0], mn[1], 0), f(mx[0], mn[1], 0), fmt(mx[0] - mn[0]), off=30, fs=6.8)
            dim(ax, f(mx[0], mn[1], 0), f(mx[0], mx[1], 0), fmt(mx[1] - mn[1]), off=34, vertical=True, fs=6.8)
    return ax

def _is_interior(m, xyz):
    mn, mx = bbox(m)
    return (mn[0] + 3 < xyz[0] < mx[0] - 3 and mn[1] + 3 < xyz[1] < mx[1] - 3 and xyz[2] < mn[2] + (mx[2] - mn[2]) * 0.6)

def hero_panel(fig, rect, aid, shot="hero", title="THREE-QUARTER RENDER", sub="Cycles · procedural blockout (concept intent)",
               notes=True, maxn=7, which="ext"):
    m = meta(aid, shot); path = os.path.join(rd(aid), shot + ".png")
    if not m or not os.path.exists(path):
        panel(fig, rect, title, "MISSING RENDER"); return None
    panel(fig, rect, title, sub)
    ax = image_axes(fig, rect, path)
    if notes:
        W, H = m["res"]; an = m["anchors"]
        items = []
        for k, v in m.get("notes", {}).items():
            if k not in an or an[k][2] <= 0:
                continue
            px, py = an[k][0], an[k][1]
            if not (20 < px < W - 20 and 20 < py < H - 20):
                continue
            if len(v) > 2:
                inside = (v[2] == "interior") if aid[:3] == "BLD" else False
            else:
                inside = _is_interior(m, v[0]) if aid[:3] == "BLD" else False
            if (which == "ext" and inside) or (which == "int" and not inside):
                continue
            items.append((px, py, v[1]))
        items = items[:maxn]
        for side in ("L", "R"):
            col = sorted([it for it in items if (it[0] < W / 2) == (side == "L")], key=lambda t: t[1])
            n = len(col)
            if not n:
                continue
            gap = min(70, (H - 120) / max(n, 1))
            y = max(60, min(H - 60 - gap * (n - 1), col[0][1] - gap))
            for px, py, label in col:
                lx = 24 if side == "L" else W - 24
                callout(ax, (px, py), label, (lx - px, y - py), C["cyan"], fs=6.4, ha="left" if side == "L" else "right")
                y += gap
    return ax

def spec_panels(fig, aid, y0=0.05, h=0.37, x0=0.012, w=0.976, split=0.55):
    a = INVD.get(aid); s = SPECS.get(aid); t = CAT_TEMPLATES[aid[:3]]
    w1 = w * split
    panel(fig, (x0, y0, w1 - 0.004, h), "SPECIFICATION", "Phase 5 fields · design assumptions")
    rows = [("Asset ID / name", f"{aid} · {a[1] if a else ''}  ({INV.roblox_name(a) if a else ''})"),
            ("Purpose", s[0] if s else "—"), ("Visual description", s[1] if s else "—"),
            ("Proposed dimensions", ("To be set at blockout — concept only, nothing measured" if a and "concept" in a[5] and "≈" not in a[5]
                                     else f"{a[5] if a else '—'} studs (model bbox on views)")),
            ("Interaction points", s[2] if s else "—"), ("Animation", s[3] if s else "—"),
            ("Modular construction", t["modular"]), ("Collision", t["collision"]),
            ("LOD strategy", t["lod"]),
            ("Complexity · priority · deps", f"{a[4]} · {a[3]} · {a[6]}" if a else "—")]
    compact = h < 0.3
    if compact:
        rows = [r for r in rows if r[0] not in ("Modular construction", "LOD strategy", "Visual description")]
    yy = y0 + h - 0.036
    lh = (h - 0.045) / len(rows)
    for k, v in rows:
        fig.text(x0 + 0.008, yy, k, fontsize=6.6, weight="bold", color=C["orange"], va="top")
        fig.text(x0 + 0.115, yy, _wrap(v, int((w1 - 0.13) * (300 if compact else 230))), fontsize=6.0 if compact else 6.5, color=C["text"], va="top", linespacing=1.1)
        yy -= lh
    x1 = x0 + w1
    if w - w1 < 0.05:
        return
    panel(fig, (x1 + 0.004, y0, w - w1 - 0.004, h), "PRODUCTION HANDOFF", "Meshy → Blender → Roblox")
    ww = max(40, int((w - w1) * 215))
    lines = [("Meshy prompt", "o"), _wrap(f"{s[4] if s else ''}, futuristic industrial sci-fi, graphite brushed metal, orange accents, cyan emissive strips, game-ready, no text", ww)]
    if not compact:
        lines += [("Negative", "o"), "organic, cartoon toy, chrome, humans, text, watermark"]
    lines += [("Blender refinement", "o"), _wrap(t["blender"], ww), ("Roblox implementation", "o"), _wrap(t["roblox"], ww)]
    yy = y0 + h - 0.034
    for ln in lines:
        st = None
        if isinstance(ln, tuple):
            ln, st = ln
        fs_ = (6.4 if st else 5.9) if compact else (6.9 if st else 6.4)
        fig.text(x1 + 0.012, yy, ln, fontsize=fs_, color=C["orange"] if st else C["text"], weight="bold" if st else "normal", va="top", linespacing=1.1)
        yy -= (0.0145 if compact else 0.0185) * (ln.count("\n") + 1) + (0.001 if st else 0.003)
    sw = [] if compact else [("graphite", "#2B2F36"), ("steel", "#8A9099"), ("orange", "#E8731A"), ("cyan", "#22D3EE"), ("amber", "#FFB020")]
    for i, (n, hx) in enumerate(sw):
        fig.patches.append(mp.Rectangle((x1 + 0.012 + i * min(0.07, (w - w1 - 0.02) / 5), y0 + 0.012), 0.016, 0.022, transform=fig.transFigure, fc=hx, ec=C["line"], zorder=2))
        fig.text(x1 + 0.031 + i * min(0.07, (w - w1 - 0.02) / 5), y0 + 0.023, f"{n}\n{hx}", fontsize=5.6, color=C["muted"], va="center", linespacing=1.1)

def _wrap(s, n):
    import textwrap
    return "\n".join(textwrap.wrap(str(s), n)) if s else "—"

_UM = {}            # aid -> 1 when an extra user-model page follows the procedural pages

def head(fig, aid, sub, page, total):
    a = INVD.get(aid)
    if _UM.get(aid) and SUBDIR[0] != "user_model":
        total += 1
    frame(fig, aid, f"{a[1].upper() if a else aid} — {CATNAME[aid[:3]]} SHEET", sub, page, total,
          asset=f"{aid}  ·  {INV.roblox_name(a) if a else ''}")

# ---------------------------------------------------------------- layouts
def sheet_bld_veh(aid):
    cat = aid[:3]; out = []
    fig = new_sheet()
    head(fig, aid, "Exterior · three-quarter render · elevations · top view — all views from one procedural model", 1, 2)
    hero_panel(fig, (0.012, 0.43, 0.6, 0.482), aid)
    ortho_panel(fig, (0.62, 0.43, 0.368, 0.482), aid, "top", "TOP / ROOF VIEW")
    for i, (shot, t) in enumerate((("front", "FRONT"), ("rear", "REAR"), ("left", "LEFT"), ("right", "RIGHT"))):
        ortho_panel(fig, (0.012 + i * 0.246, 0.05, 0.238, 0.372), aid, shot, t)
    p1 = os.path.join(ROOT, CATDIR[cat], aid, f"{aid}_1_Exterior.png"); save(fig, p1); out.append(p1)
    fig = new_sheet()
    head(fig, aid, ("Floor plan (cut at +%s) · interior cutaway · specification" if cat == "BLD" else "Interior layout (cut at +%s) · exploded view · specification") % fmt(meta(aid, "plan")["cut"] if meta(aid, "plan") else 0), 2, 2)
    ortho_panel(fig, (0.012, 0.43, 0.4, 0.482), aid, "plan", "FLOOR PLAN" if cat == "BLD" else "INTERIOR LAYOUT (PLAN CUT)")
    hero_panel(fig, (0.42, 0.43, 0.568, 0.482), aid, "cutaway" if cat == "BLD" else "exploded",
               "INTERIOR CUTAWAY (walls cut, roof removed)" if cat == "BLD" else "EXPLODED VIEW (roof / body / chassis / running gear)",
               "Workbench axonometric", notes=(cat == "BLD"), which="int")
    spec_panels(fig, aid)
    p2 = os.path.join(ROOT, CATDIR[cat], aid, f"{aid}_2_Plan_Spec.png"); save(fig, p2); out.append(p2)
    return out

def sheet_eqp(aid):
    fig = new_sheet()
    head(fig, aid, "Three-quarter · detail close-up · scale vs Cypher (6.0 studs) · five orthographic views", 1, 1)
    hero_panel(fig, (0.012, 0.5, 0.4, 0.412), aid, maxn=5)
    cc = os.path.join(ROOT, CATDIR["EQP"], aid, "concept_crop.png")
    if os.path.exists(cc):
        panel(fig, (0.42, 0.5, 0.26, 0.412), "USER CONCEPT (design sheet)", "reference")
        image_axes(fig, (0.42, 0.5, 0.26, 0.412), cc)
    else:
        hero_panel(fig, (0.42, 0.5, 0.26, 0.412), aid, "detail", "DETAIL CLOSE-UP", "Cycles", notes=False)
    ortho_panel(fig, (0.688, 0.5, 0.3, 0.412), aid, "scale", "SCALE vs CYPHER (6.0)", dims=True)
    for i, (shot, t) in enumerate((("front", "FRONT"), ("rear", "BACK"), ("left", "LEFT"), ("right", "RIGHT"), ("top", "TOP"))):
        ortho_panel(fig, (0.012 + i * 0.1956, 0.27, 0.1896, 0.222), aid, shot, t)
    spec_panels(fig, aid, y0=0.05, h=0.212)
    p = os.path.join(ROOT, CATDIR["EQP"], aid, f"{aid}_Sheet.png"); save(fig, p); return [p]

def sheet_inf(aid):
    fig = new_sheet()
    head(fig, aid, "Three-quarter render · four elevations · top view · family robot for scale", 1, 1)
    hero_panel(fig, (0.012, 0.45, 0.44, 0.462), aid)
    for i, (shot, t) in enumerate((("front", "FRONT"), ("rear", "REAR"), ("left", "LEFT"), ("right", "RIGHT"))):
        ortho_panel(fig, (0.46 + (i % 2) * 0.266, 0.45 + (1 - i // 2) * 0.233, 0.26, 0.229), aid, shot, t)
    ortho_panel(fig, (0.012, 0.05, 0.25, 0.392), aid, "top", "TOP VIEW")
    spec_panels(fig, aid, x0=0.27, w=0.718, h=0.392, split=0.56)
    p = os.path.join(ROOT, CATDIR["INF"], aid, f"{aid}_Sheet.png"); save(fig, p); return [p]

def sheet_int(aid):
    fig = new_sheet()
    m = meta(aid, "plan")
    head(fig, aid, "Interior view · floor plan (cut at +%s) · cutaway · section — one procedural model" % fmt(m["cut"] if m else 0), 1, 1)
    hero_panel(fig, (0.012, 0.45, 0.55, 0.462), aid, title="INTERIOR VIEW")
    ortho_panel(fig, (0.57, 0.45, 0.418, 0.462), aid, "plan", "FLOOR PLAN")
    hero_panel(fig, (0.012, 0.05, 0.3, 0.392), aid, "cutaway", "CUTAWAY AXONOMETRIC", "Workbench", notes=False)
    ortho_panel(fig, (0.318, 0.05, 0.25, 0.392), aid, "section", "SECTION (centre line)")
    spec_panels(fig, aid, x0=0.574, w=0.414, h=0.392, split=0.999)
    # handoff for interiors lives in Meshy_Prompts/ and Roblox/ (panel too narrow here)
    p = os.path.join(ROOT, CATDIR["INT"], aid, f"{aid}_Sheet.png"); save(fig, p); return [p]

USER_VEH = {"VEH-10": ("Meshy_AI_Industrial Freight Train Concept.png", "Meshy textured GLB (zip 231005)"),
            "VEH-11": ("Meshy_AI_Armored Security Carrier Concept.png", "Armored_Security_Carr.glb"),
            "VEH-12": ("Meshy_AI_Armored VTOL Security Aircraft Concept.png", "Meshy textured GLB (zip 231458)"),
            "VEH-13": ("Meshy_AI_Industrial Cargo Hauler Concept.png", None)}

def sheet_user_veh(aid):
    concept, model = USER_VEH[aid]
    fig = new_sheet()
    head(fig, aid, "User-supplied concept + Meshy model · turnaround rendered from the model file (unmodified, scaled)" if model
         else "User-supplied concept (no 3D model yet) · production specification", 1, 1)
    if model and meta(aid, "front"):
        m = meta(aid, "front")
        hero_panel(fig, (0.012, 0.45, 0.44, 0.462), aid, title="USER MODEL · RENDER", sub=f"{model} · {m['tris']:,} tris", notes=False)
        panel(fig, (0.46, 0.45, 0.27, 0.462), "CONCEPT", "user-supplied reference")
        image_axes(fig, (0.46, 0.45, 0.27, 0.462), os.path.join(r"D:\Project Zero_Roblox", concept))
        ortho_panel(fig, (0.738, 0.45, 0.25, 0.462), aid, "top", "TOP")
        for i, (shot, t) in enumerate((("front", "FRONT"), ("rear", "REAR"), ("left", "LEFT"))):
            ortho_panel(fig, (0.012 + i * 0.13, 0.05, 0.126, 0.392), aid, shot, t)
        spec_panels(fig, aid, x0=0.405, w=0.583, h=0.392, split=0.55)
    else:
        panel(fig, (0.012, 0.45, 0.6, 0.462), "CONCEPT", "user-supplied reference · not measured")
        image_axes(fig, (0.012, 0.45, 0.6, 0.462), os.path.join(r"D:\Project Zero_Roblox", concept))
        panel(fig, (0.62, 0.45, 0.368, 0.462), "STATUS", None)
        text_block(fig, 0.63, 0.88, [("No 3D model supplied yet", "o"), "Next: Meshy image-to-3D from this concept,",
                                      "then the standard turnaround is rendered from it.", ("Design assumptions", "o"),
                                      "Length ≈ 36 studs (≈ 10 m at 0.28 m/stud).", "Family vehicle palette: graphite, white,",
                                      "orange hazard, cyan lights (matches VEH-10…12)."], fs=8, lh=0.026)
        spec_panels(fig, aid, h=0.392)
    os.makedirs(os.path.join(ROOT, CATDIR["VEH"], aid), exist_ok=True)
    p = os.path.join(ROOT, CATDIR["VEH"], aid, f"{aid}_Sheet.png"); save(fig, p); return [p]

def sheet_weapon_concept(aid):
    from pz_weapons import BY_ID
    w = BY_ID[aid]
    _, name, cls, box, size, cell, role, sig, meshy = w
    fig = new_sheet()
    head(fig, aid, f"{cls} · user-supplied concept (Weapons & Combat Equipment sheet) + harmonised production spec", 1, 1)
    panel(fig, (0.012, 0.33, 0.6, 0.582), "USER CONCEPT · DESIGN SHEET PANEL", "reference only · not measured")
    image_axes(fig, (0.012, 0.33, 0.6, 0.582), os.path.join(ROOT, CATDIR["EQP"], aid, "concept_crop.png"))
    panel(fig, (0.62, 0.33, 0.368, 0.582), "HARMONISED SPEC", "design assumptions")
    rows = [("Class", cls), ("Role", role), ("Signature", sig), ("Proposed size", f"{size} studs"),
            ("vs Cypher (6.0)", "held two-handed" if "long" in size and float(size.split()[0].split("–")[0]) > 3.5 else "one-handed / deployable"),
            ("Energy cell", cell), ("Roblox", "Tool + Handle; client VFX, server validates"),
            ("Palette", "graphite #1A1D22 · brushed #7A7F86 · white #E6E8EB · orange #FF7A00 · cyan #00D4FF"),
            ("3D model", "none supplied: Meshy image-to-3D from the panel views")]
    table(fig, (0.626, 0.36, 0.356, 0.52), ["FIELD", "VALUE"], rows, [0.27, 0.73], fs=6.6)
    spec_panels(fig, aid, y0=0.05, h=0.27)
    p = os.path.join(ROOT, CATDIR["EQP"], aid, f"{aid}_Sheet.png"); save(fig, p); return [p]

CONCEPT_IMG = {"BLD-19": r"D:\\Project Zero_Roblox\\Meshy_AI_futuristic_monorail_station.png"}
USER_SRC = {}

def _concept_for(aid):
    if aid in CONCEPT_IMG and os.path.exists(CONCEPT_IMG[aid]):
        return CONCEPT_IMG[aid]
    for d in (os.path.join(ROOT, CATDIR[aid[:3]], aid),):
        p = os.path.join(d, "concept_crop.png")
        if os.path.exists(p):
            return p
    return None

def sheet_user_model(aid, sub, fname, page, total):
    """Page built from a user-supplied model's audit renders (read-only)."""
    SUBDIR[0] = sub
    try:
        m = meta(aid, "front")
        fig = new_sheet()
        head(fig, aid, "User-supplied Meshy model · turnaround rendered from the model file (unmodified, uniformly scaled)", page, total)
        hero_panel(fig, (0.012, 0.45, 0.44, 0.462), aid, title="USER MODEL · RENDER", sub=f"{m['source'][:40]} · {m['tris']:,} tris", notes=False)
        cp = _concept_for(aid)
        if cp:
            panel(fig, (0.46, 0.45, 0.27, 0.462), "CONCEPT", "user-supplied reference")
            image_axes(fig, (0.46, 0.45, 0.27, 0.462), cp)
            ortho_panel(fig, (0.738, 0.45, 0.25, 0.462), aid, "top", "TOP")
        else:
            ortho_panel(fig, (0.46, 0.45, 0.528, 0.462), aid, "top", "TOP")
        for i, (shot, t) in enumerate((("front", "FRONT"), ("rear", "REAR"), ("left", "LEFT"))):
            ortho_panel(fig, (0.012 + i * 0.13, 0.05, 0.126, 0.392), aid, shot, t)
        spec_panels(fig, aid, x0=0.405, w=0.583, h=0.392, split=0.55)
        p = os.path.join(ROOT, CATDIR[aid[:3]], aid, fname); save(fig, p); return [p]
    finally:
        SUBDIR[0] = "renders"

def sheet_concept_bld(aid):
    fig = new_sheet()
    head(fig, aid, "Metropolis concept district · no model yet · production specification", 1, 1)
    panel(fig, (0.012, 0.45, 0.6, 0.462), "CONCEPT · NEXUS-01 ROBOTIC METROPOLIS (crop)", "user-supplied reference · not measured")
    image_axes(fig, (0.012, 0.45, 0.6, 0.462), _concept_for(aid))
    panel(fig, (0.62, 0.45, 0.368, 0.462), "STATUS", None)
    text_block(fig, 0.63, 0.88, [("Concept only", "o"), "District shown in the metropolis concept image.",
                                  "Next: blockout or Meshy model, then the standard",
                                  "turnaround and plan views.", ("Priority", "o"), "P3: after the launch hub (NEXUS-01 bible §13)."], fs=8, lh=0.026)
    spec_panels(fig, aid, h=0.392)
    p = os.path.join(ROOT, CATDIR["BLD"], aid, f"{aid}_Sheet.png"); save(fig, p); return [p]

def user_model_pages(aid):
    """Extra page for existing assets that also have a user model."""
    d = os.path.join(ROOT, CATDIR[aid[:3]], aid, "user_model")
    if not os.path.exists(os.path.join(d, "front.json")):
        return []
    fname = f"{aid}_3_UserModel.png" if aid[:3] in ("BLD", "VEH") else f"{aid}_UserModel.png"
    n = 3 if aid[:3] in ("BLD", "VEH") else 2
    return sheet_user_model(aid, "user_model", fname, n, n)

def compose(aid):
    if not (meta(aid, "front") or meta(aid, "hero") or _concept_for(aid) or aid in USER_VEH):
        return []          # nothing rendered yet: no placeholder sheet
    _UM[aid] = int(os.path.exists(os.path.join(ROOT, CATDIR[aid[:3]], aid, "user_model", "front.json")))
    if aid in ("BLD-21", "BLD-22", "BLD-23", "BLD-24"):
        return sheet_concept_bld(aid)
    m0 = meta(aid, "front")
    if m0 and m0.get("cat") == "USER" and aid not in USER_VEH:
        return sheet_user_model(aid, "renders", f"{aid}_Sheet.png", 1, 1) + user_model_pages(aid)
    if aid in [f"EQP-{n}" for n in range(13, 26)] and not meta(aid, "front"):
        return sheet_weapon_concept(aid)
    if aid in USER_VEH:
        return sheet_user_veh(aid)
    extra = user_model_pages(aid)
    c = aid[:3]
    return {"BLD": sheet_bld_veh, "VEH": sheet_bld_veh, "EQP": sheet_eqp, "INF": sheet_inf, "INT": sheet_int}[c](aid) + extra

if __name__ == "__main__":
    for a in sys.argv[1:]:
        compose(a)
