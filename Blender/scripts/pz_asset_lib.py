"""Generic asset build + render library for the remaining NEXUS-01 assets.
Re-uses the approved Stasis Facility toolkit (pz_build_stasis) so materials, lighting and robots match.

blender -b --factory-startup -P pz_build_asset.py -- <ASSET_ID> <outdir> [quick]
All dimensions are DESIGN ASSUMPTIONS in studs (1 BU = 1 stud).
"""
import bpy, math, os, json
from mathutils import Vector
import pz_build_stasis as K
from pz_build_stasis import M, mat

# ------------------------------------------------------------------ extra materials
X = dict(
    amberwin=mat("amber_window", "#FFB020", 0, 0.4, emit=3.5),
    violet_e=mat("violet_emit", "#8B5CF6", 0, 0.4, emit=6),
    teal=mat("teal", "#1FB5A8", 0.3, 0.45),
    yellow=mat("factory_yellow", "#EBAB2E", 0.3, 0.45),
    red=mat("warning_red", "#A22625", 0.3, 0.5),
    white=mat("white_metal", "#D6D6DA", 0.4, 0.4),
    rubber=mat("rubber", "#121314", 0.0, 0.9),
    glassdome=mat("glass_dome", "#7FD6F0", 0.0, 0.05, emit=0.3, trans=1.0),
    concrete2=mat("aged_concrete", "#5A5E63", 0.0, 0.9),
    holo=mat("holo", "#22D3EE", 0, 0.2, emit=4),
    green_e=M["green_e"],
)

for _k, _v in X.items():          # make extra materials reachable through M as well
    M.setdefault(_k, _v)

GROUP = ["body"]
NOTES = {}           # key -> (xyz, label)
CUT_H = [10.0]       # cutaway height for this asset

def grp(name):
    GROUP[0] = name

def _tag(o):
    if o is not None:
        o["grp"] = GROUP[0]
    return o

def note(key, xyz, text):
    NOTES[key] = (tuple(xyz), text, GROUP[0])
    K.anchor(key, xyz)

# wrappers that tag explode groups
def box(name, x0, x1, y0, y1, z0, z1, m): return _tag(K.box(name, x0, x1, y0, y1, z0, z1, m))
def cbox(name, cx, cy, cz, sx, sy, sz, m, rot=(0, 0, 0)): return _tag(K.cbox(name, cx, cy, cz, sx, sy, sz, m, rot))
def cyl(name, x, y, z0, h, r, m, seg=32, r2=None, rot=None): return _tag(K.cyl(name, x, y, z0, h, r, m, seg, r2, rot))
def sphere(name, x, y, z, r, m): return _tag(K.sphere(name, x, y, z, r, m))
def tube(name, x, y, z0, h, r, t, m, a0=0.0, a1=2 * math.pi, seg=40): return _tag(K.tube_shell(name, x, y, z0, h, r, t, m, a0, a1, seg))

def hollow_prism(name, h, r, seg, t, m, cut):
    """Polygonal volume (aligned with cyl(seg)) built hollow so cutaway / plan can see inside:
    floor, wall ring split at the cut height (upper part tagged), roof cap in the roof group."""
    a0 = math.pi / 2
    cyl(name + "_floor", 0, 0, 0, 0.4, r, m, seg)
    tube(name, 0, 0, 0, cut, r, t, m, a0, a0 + 2 * math.pi, seg)
    up = tube(name + "_up", 0, 0, cut, h - cut, r, t, m, a0, a0 + 2 * math.pi, seg); up["upper"] = 1
    prev = GROUP[0]; grp("roof")
    cyl(name + "_roof", 0, 0, h - 0.6, 0.6, r, m, seg)
    grp(prev)
def vault(name, cx, a, b, spring, y0, y1, t, m): return _tag(K.arch_shell(name, cx, a, b, spring, y0, y1, t, m))

def dome(name, x, y, z, r, m, flat=1.0):
    o = sphere(name, x, y, z, r, m); o.scale = (1, 1, flat)
    return o

# Blockout scenes use neutral grey stand-in figures, not the finished robot models: mixing finished
# characters into box blockouts read as "two different games" (user review 2026-11-23). The figure keeps the
# robot's design height so scale stays honest. Real robots appear on character and supplied-model sheets only.
STANDIN_M = mat("standin_grey", "#A3A9B2", 0.0, 0.65)
FIGURES = []         # (pivot, frame name, height)

def robot(name, frame, x, y, rz=0.0, z=0.0):
    h = K.L.ROBOTS[frame]["height"]
    piv = K.mannequin(name, x, y, z, h, STANDIN_M, rz)   # parts are built at z; pivot stays at floor level
    piv["grp"] = "robots"; piv["robot"] = 1; piv["frame"] = frame; piv["z0"] = z
    for c in piv.children:
        c["robot"] = 1; c["grp"] = "robots"
    FIGURES.append((piv, frame, h))
    return piv

def _figure_proxy(x, y, z0, h, r):
    from mathutils.bvhtree import BVHTree
    zs, ze = z0 + 0.35, z0 + h * 0.95
    v = [Vector((x + sx * r, y + sy * r, zz)) for zz in (zs, ze) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    f = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return BVHTree.FromPolygons(v, f), Vector((x - r, y - r, zs)), Vector((x + r, y + r, ze))

def resolve_figure_clashes():
    """Move any stand-in figure that intersects scenery to the nearest clear floor spot (searching outward
    up to 8 studs). Uses real mesh surfaces (BVH), not bounding boxes, so hollow shells and vaults don't count."""
    from mathutils.bvhtree import BVHTree
    if not FIGURES:
        return
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    obs = []
    for o in bpy.context.scene.objects:
        if o.type not in ("MESH", "FONT") or o.get("robot") or o.get("ground") or o.hide_render:
            continue
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        mn = Vector([min(p[i] for p in bb) for i in range(3)]); mx = Vector([max(p[i] for p in bb) for i in range(3)])
        if mx.z <= 0.36:                     # floor slabs, painted strips
            continue
        obs.append((o, mn, mx, None))
    def tree(i):
        o, mn, mx, t = obs[i]
        if t is None:
            t = BVHTree.FromObject(o, dg); obs[i] = (o, mn, mx, t)
        return t
    def clear(x, y, z0, h, r):
        prox, pmn, pmx = _figure_proxy(x, y, z0, h, r)
        for i, (o, mn, mx, _) in enumerate(obs):
            if mx.x < pmn.x or mn.x > pmx.x or mx.y < pmn.y or mn.y > pmx.y or mx.z < pmn.z or mn.z > pmx.z:
                continue
            if tree(i).overlap(prox):
                return False
            if mn.x <= pmn.x and mx.x >= pmx.x and mn.y <= pmn.y and mx.y >= pmx.y and mn.z <= pmn.z and mx.z >= pmx.z \
                    and o.type == "MESH" and len(o.data.polygons) <= 12:
                return False                  # figure buried inside a solid box (no surface crossing)
        return True
    for piv, frame, h in FIGURES:
        x, y, z0 = piv.location.x, piv.location.y, piv.get("z0", 0.0)
        r = 1.25 * h / 7.0 + 0.15
        if clear(x, y, z0, h, r):
            continue
        spot = None
        for ring in range(1, 17):
            d = ring * 0.5
            for k in range(16):
                a = 2 * math.pi * k / 16
                nx, ny = x + d * math.cos(a), y + d * math.sin(a)
                if clear(nx, ny, z0, h, r):
                    spot = (nx, ny); break
            if spot:
                break
        if spot:
            piv.location.x, piv.location.y = spot
            print(f"STANDIN_MOVED {piv.name} ({frame}) from ({x:.1f},{y:.1f}) to ({spot[0]:.1f},{spot[1]:.1f})")
        else:
            print(f"STANDIN_REMOVED {piv.name} ({frame}) at ({x:.1f},{y:.1f}): no clear spot within 8 studs")
            for c in list(piv.children):
                bpy.data.objects.remove(c)
            bpy.data.objects.remove(piv)
    bpy.context.view_layer.update()

def _wb(w, h):
    """Workbench ortho setup for asset sheets: light steel object outlines so dark parts read on the dark sheets."""
    K.setup_workbench(w, h)
    bpy.context.scene.display.shading.object_outline_color = (0.42, 0.46, 0.52)

def text(name, body, x, y, z, size, m, rz=0.0, facing="-Y"):
    t = bpy.data.curves.new(name, "FONT"); t.body = body; t.size = size; t.extrude = 0.08; t.align_x = "CENTER"
    o = K._obj(name, t, m); o.location = (x, y, z)
    o.rotation_euler = (math.radians(90), 0, rz)
    return _tag(o)

# ------------------------------------------------------------------ architecture DSL
def shell(name, x0, x1, y0, y1, h, wall_m=None, openings=None, t=1.0, roof=True, parapet=1.0, floor_m=None):
    """Rectangular building volume: floor, 4 walls with openings, roof slab + parapet.
    openings: list of (side, centre, width, height) with side in S N W E (S = -Y front)."""
    wall_m = wall_m or M["graphite"]
    openings = openings or []
    box(name + "_floor", x0, x1, y0, y1, 0, 0.1, floor_m or M["floor"])
    for side in "SNWE":
        if side in "SN":
            yy = y0 if side == "S" else y1 - t; a, b = x0, x1
            seg = lambda s0, s1, z0, z1, k: box(f"{name}_w{side}{k}", s0, s1, yy, yy + t, z0, z1, wall_m)
        else:
            xx = x0 if side == "W" else x1 - t; a, b = y0, y1
            seg = lambda s0, s1, z0, z1, k: box(f"{name}_w{side}{k}", xx, xx + t, s0, s1, z0, z1, wall_m)
        ops = sorted([(c - w / 2, c + w / 2, oh) for (sd, c, w, oh) in openings if sd == side])
        cur, k = a, 0
        for o0, o1, oh in ops:
            _wall_split(seg, cur, o0, 0, h, k); k += 2
            if oh < h:
                _wall_split(seg, o0, o1, oh, h, k); k += 2
            cur = o1
        _wall_split(seg, cur, b, 0, h, k)
    if roof:
        grp_prev = GROUP[0]; grp("roof")
        box(name + "_roof", x0, x1, y0, y1, h, h + 0.8, M["panel"])
        if parapet:
            for (a0, a1, b0, b1) in ((x0, x1, y0, y0 + 0.6), (x0, x1, y1 - 0.6, y1), (x0, x0 + 0.6, y0, y1), (x1 - 0.6, x1, y0, y1)):
                box(f"{name}_par{a0}{b0}", a0, a1, b0, b1, h + 0.8, h + 0.8 + parapet, wall_m)
            box(name + "_cap1", x0, x0 + 0.6, y0, y0 + 0.6, h + 0.8 + parapet, h + 1.1 + parapet, M["orange"])
            box(name + "_cap2", x1 - 0.6, x1, y0, y0 + 0.6, h + 0.8 + parapet, h + 1.1 + parapet, M["orange"])
        grp(grp_prev)

def _wall_split(seg, s0, s1, z0, z1, k):
    """Split wall pieces at the cutaway height so the upper part can be hidden."""
    if s1 - s0 <= 0.01 or z1 - z0 <= 0.01:
        return
    c = CUT_H[0]
    if z0 < c < z1:
        seg(s0, s1, z0, c, k); o = seg(s0, s1, c, z1, f"{k}u")
        if o is not None:
            o["upper"] = 1
    else:
        o = seg(s0, s1, z0, z1, k)
        if o is not None and z0 >= c:
            o["upper"] = 1

def win_band(name, side, a, b, z0, z1, x0, x1, y0, y1, m=None, step=None, gap=0.6):
    """Emissive window strip(s) on a facade. step -> repeated windows."""
    m = m or M["cyan_soft"]
    spans = [(a, b)] if not step else [(s, min(s + step - gap, b)) for s in frange(a, b, step)]
    for k, (s0, s1) in enumerate(spans):
        if side == "S": box(f"{name}{k}", s0, s1, y0 - 0.12, y0 + 0.02, z0, z1, m)
        if side == "N": box(f"{name}{k}", s0, s1, y1 - 0.02, y1 + 0.12, z0, z1, m)
        if side == "W": box(f"{name}{k}", x0 - 0.12, x0 + 0.02, s0, s1, z0, z1, m)
        if side == "E": box(f"{name}{k}", x1 - 0.02, x1 + 0.12, s0, s1, z0, z1, m)

def frange(a, b, s):
    v = a
    while v < b - 1e-6:
        yield v; v += s

def pilasters(name, side, a, b, h, x0, x1, y0, y1, step=8, m=None):
    m = m or M["steel"]
    for k, s in enumerate(frange(a + step, b, step)):
        if side == "S": box(f"{name}{k}", s - 0.5, s + 0.5, y0 - 0.5, y0, 0, h, m)
        if side == "N": box(f"{name}{k}", s - 0.5, s + 0.5, y1, y1 + 0.5, 0, h, m)
        if side == "W": box(f"{name}{k}", x0 - 0.5, x0, s - 0.5, s + 0.5, 0, h, m)
        if side == "E": box(f"{name}{k}", x1, x1 + 0.5, s - 0.5, s + 0.5, 0, h, m)

def door(name, side, c, w, h, x0, x1, y0, y1, kind="std"):
    """Visible door leaf + frame placed in an opening made by shell()."""
    fm = M["orange"] if kind in ("std", "egress") else M["graphite"]
    leaf = {"std": M["panel"], "main": M["graphite"], "egress": M["graphite"], "rollup": M["steel"]}[kind]
    seam = {"std": M["cyan_e"], "main": M["cyan_e"], "egress": M["green_e"], "rollup": M["amber_e"]}[kind]
    if side in "SN":
        yy = y0 if side == "S" else y1
        d = -1 if side == "S" else 1
        box(name + "_leaf", c - w / 2, c + w / 2, yy - 0.15, yy + 0.15, 0, h, leaf)
        box(name + "_seam", c - 0.1, c + 0.1, yy + d * 0.2 - 0.05, yy + d * 0.2 + 0.05, 0.4, h - 0.4, seam)
        box(name + "_fr", c - w / 2 - 0.5, c + w / 2 + 0.5, yy + d * 0.3 - 0.25, yy + d * 0.3 + 0.25, h, h + 0.6, fm)
    else:
        xx = x0 if side == "W" else x1
        d = -1 if side == "W" else 1
        box(name + "_leaf", xx - 0.15, xx + 0.15, c - w / 2, c + w / 2, 0, h, leaf)
        box(name + "_seam", xx + d * 0.2 - 0.05, xx + d * 0.2 + 0.05, c - 0.1, c + 0.1, 0.4, h - 0.4, seam)
        box(name + "_fr", xx + d * 0.3 - 0.25, xx + d * 0.3 + 0.25, c - w / 2 - 0.5, c + w / 2 + 0.5, h, h + 0.6, fm)

def stack(name, x, y, z0, h, r, band=True):
    cyl(name, x, y, z0, h, r, M["graphite"], 20)
    cyl(name + "_cap", x, y, z0 + h, 0.5, r * 1.25, M["steel"], 20)
    if band:
        cyl(name + "_band", x, y, z0 + h * 0.7, 0.8, r * 1.05, M["orange"], 20)

def tank(name, x, y, z0, h, r, m=None, horizontal=False):
    m = m or M["steel"]
    if horizontal:
        cyl(name, x, y, z0 + r, h, r, m, 24, rot=(math.radians(-90), 0, 0))
        cyl(name + "_b", x, y + h * 0.5, z0 + r, 0.8, r * 1.04, M["blue"], 24, rot=(math.radians(-90), 0, 0))
    else:
        cyl(name, x, y, z0, h, r, m, 24)
        dome(name + "_top", x, y, z0 + h, r, m, 0.45)
        cyl(name + "_b", x, y, z0 + h * 0.65, 0.8, r * 1.04, M["blue"], 24)

def emblem(name, x, y, z, s, m=None, rz=0.0):
    """Diamond emblem (Design Bible banner motif)."""
    return cbox(name, x, y, z, s, 0.2, s, m or M["amber_e"], rot=(0, math.radians(45), rz))

def gear(name, x, y, z, r, m=None, rz=0.0, teeth=8):
    """Gear emblem (Workshop / Foundry motif) facing -Y."""
    m = m or M["orange_e"]
    ring = tube(name, 0, 0, -0.125, 0.25, r, r * 0.35, m)
    ring.rotation_euler = (math.radians(90), 0, rz); ring.location = (x, y, z)
    for k in range(teeth):
        a = 2 * math.pi * k / teeth
        cbox(f"{name}_t{k}", x + math.cos(a) * r * 1.08, y - 0.12, z + math.sin(a) * r * 1.08, r * 0.28, 0.25, r * 0.28, m, rot=(0, -a, 0))

def ground(name, x0, x1, y0, y1, m=None):
    o = K.box(name, x0, x1, y0, y1, -0.08, 0.0, m or M["ground"]); o["ground"] = 1
    return o

# ------------------------------------------------------------------ framing + shots
def scene_bbox(robots=True):
    pts = []
    for o in bpy.context.scene.objects:
        if o.get("ground") or o.hide_render:
            continue
        if o.get("robot") and not robots:
            continue
        if o.type == "MESH" or (o.type == "FONT"):
            pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
        elif o.get("robot"):
            pts += [o.location, o.location + Vector((0, 0, 6))]
    mn = Vector([min(p[i] for p in pts) for i in range(3)]); mx = Vector([max(p[i] for p in pts) for i in range(3)])
    return mn, mx

def _views(mn, mx):
    c = (mn + mx) / 2
    return c, (mx - mn)

def hide_upper(flag):
    c = CUT_H[0]
    for o in bpy.context.scene.objects:
        if o.get("ground"):
            continue
        if o.get("grp") == "roof" or o.get("upper"):
            o.hide_render = flag; continue
        if o.type in ("MESH", "FONT"):
            zmin = min((o.matrix_world @ Vector(v)).z for v in o.bound_box)
            if zmin >= c - 0.01:
                o.hide_render = flag

def explode(flag, mn, mx):
    H = mx.z - mn.z
    off = {"roof": 1.25, "upper": 0.8, "body": 0.55, "interior": 0.15, "robots": 0.15, "chassis": 0.0, "bogie": -0.3}
    for o in bpy.context.scene.objects:
        g = o.get("grp")
        if g in off and o.parent is None:
            if flag:
                o["z0"] = o.location.z; o.location.z += off[g] * H * 1.2
            elif "z0" in o:
                o.location.z = o["z0"]
    bpy.context.view_layer.update()   # refresh matrix_world so framing sees the exploded positions

def _fit_ortho(cam, w, h, pad=1.08):
    """Recentre an ortho camera and set its scale from the projected extent of every visible object,
    so tall exploded stacks are not clipped by the shorter image axis."""
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    pts = []
    for o in bpy.context.scene.objects:
        if o.get("ground") or o.hide_render:
            continue
        if o.type in ("MESH", "FONT"):
            pts += [inv @ (o.matrix_world @ Vector(c)) for c in o.bound_box]
        elif o.get("robot"):
            pts += [inv @ o.location, inv @ (o.location + Vector((0, 0, 6)))]
    if not pts:
        return
    xs = [p.x for p in pts]; ys = [p.y for p in pts]
    cam.location = cam.matrix_world @ Vector(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, 0))
    cam.data.ortho_scale = max(max(xs) - min(xs), (max(ys) - min(ys)) * w / h) * pad
    bpy.context.view_layer.update()

def run_shots(cat, outdir, quick=False, hero_dir=(-0.75, -1.0, 0.42), lens=32, robots_in_ortho=True, outside_hero=False):
    os.makedirs(outdir, exist_ok=True)
    resolve_figure_clashes()
    SC = bpy.context.scene
    mn, mx = scene_bbox(robots=(cat != "EQP")); c, s = _views(mn, mx)
    mo, xo = scene_bbox(robots=False)
    meta_base = dict(bbox=[list(mn), list(mx)], bbox_obj=[list(mo), list(xo)],
                     notes={k: [list(v[0]), v[1], v[2]] for k, v in NOTES.items()}, cut=CUT_H[0], cat=cat)
    shots = {"BLD": ["hero", "front", "rear", "left", "right", "top", "plan", "cutaway"],
             "VEH": ["hero", "front", "rear", "left", "right", "top", "plan", "exploded"],
             "EQP": ["hero", "front", "rear", "left", "right", "top", "detail", "scale"],
             "INF": ["hero", "front", "rear", "left", "right", "top"],
             "INT": ["hero", "plan", "cutaway", "section"]}[cat]
    only = os.environ.get("PZ_SHOTS")
    if only:
        shots = [x for x in shots if x in only.split(",")]
    for shot in shots:
        for o in list(K.LIGHTS):
            bpy.data.objects.remove(o)
        K.LIGHTS.clear()
        meta = dict(meta_base, view=shot)
        rob = [o for o in SC.objects if o.get("robot")]
        if cat == "EQP":
            for o in rob:
                o.hide_render = (shot != "scale")
        if shot == "scale":
            mn2, mx2 = scene_bbox(robots=True); c2, s2 = _views(mn2, mx2)
            scale = max(s2.y, s2.z * 2.0) * 1.2
            _wb(2000, 1000)
            cam = K.camera("cam", ortho=scale); K.look(cam, Vector((c2.x - 200, c2.y, c2.z)), (c2.x, c2.y, c2.z))
            meta.update(ortho=scale, center=list(c2), res=[2000, 1000], bbox=[list(mn2), list(mx2)])
            K.render(shot, cam, meta)
            continue
        if shot in ("hero", "detail"):
            w, h = (1440, 900) if shot == "hero" else (1100, 900)
            K.setup_cycles(8 if quick else (16 if cat != "INT" else 24), w, h)
            K.world((0.016, 0.024, 0.04), 1.4)
            R = max(s.length / 2, 3)
            d = Vector(hero_dir).normalized()
            if cat == "INT" and shot == "hero" and not outside_hero:
                cam = K.camera("cam", lens=18)
                eye = Vector((mn.x + s.x * 0.12, mn.y + s.y * 0.1, mn.z + min(6.5, s.z * 0.45)))
                K.look(cam, eye, (c.x + s.x * 0.15, mx.y, mn.z + s.z * 0.35))
                K.light("AREA", (c.x, c.y, mx.z - 1), 900 + 6 * s.x * s.y, (0.6, 0.85, 1.0), size=max(s.x, s.y) * 0.6, rot=(0, 0, 0))
            else:
                zoom = 1.0 if shot == "hero" else 0.55
                cam = K.camera("cam", lens=lens if shot == "hero" else 55)
                tgt = c + Vector((0, 0, -s.z * 0.08))
                K.look(cam, tgt + d * R * ((3.1 if cat == "EQP" else 2.15) if shot == "hero" else 3.2) * zoom, tgt)
                K.light("SUN", (0, 0, 100), 1.6, (0.8, 0.88, 1.0), rot=(math.radians(55), 0, math.radians(-38)))
                K.light("AREA", tuple(c + Vector((-R * 2, -R * 1.5, R * 1.8))), 160 * R * R, (0.55, 0.75, 1.0), size=R * 1.5, target=tuple(c))
                K.light("AREA", tuple(c + Vector((R * 1.6, R * 2.0, R * 1.2))), 260 * R * R, (0.25, 0.75, 1.0), size=R * 1.5, target=tuple(c))
                K.light("AREA", tuple(c + Vector((R * 0.8, -R * 1.8, R * 0.2))), 60 * R * R, (1.0, 0.55, 0.25), size=R, target=tuple(c))
            K.render(shot, cam, meta)
            hide_upper(False)
            continue
        # orthographic (Workbench)
        for o in rob:
            o.hide_render = (not robots_in_ortho) or cat == "EQP"
        if shot == "section":
            scale = max(s.x, s.z * 2.0) * 1.14
            _wb(2000, 1000)
            cam = K.camera("cam", ortho=scale); cam.data.clip_start = 0.001
            cam.location = (c.x, c.y, c.z); cam.rotation_euler = (math.radians(90), 0, 0)
            meta.update(ortho=scale, center=list(c), res=[2000, 1000], cut_y=c.y)
        elif shot in ("front", "rear", "left", "right"):
            horiz = s.x if shot in ("front", "rear") else s.y
            scale = max(horiz, s.z * 2.0) * 1.14
            _wb(2000, 1000)
            cam = K.camera("cam", ortho=scale)
            D = max(s.length, 10) * 3
            dirs = {"front": (0, -1), "rear": (0, 1), "left": (-1, 0), "right": (1, 0)}[shot]
            loc = Vector((c.x + dirs[0] * D, c.y + dirs[1] * D, c.z))
            K.look(cam, loc, (c.x, c.y, c.z))
            meta.update(ortho=scale, center=list(c), res=[2000, 1000])
        elif shot in ("top", "plan"):
            scale = max(s.x, s.y) * 1.12
            _wb(1600, 1600)
            cam = K.camera("cam", ortho=scale)
            z = mx.z + 50 if shot == "top" else CUT_H[0]
            cam.location = (c.x, c.y, z); cam.rotation_euler = (0, 0, 0)
            if shot == "plan":
                cam.data.clip_start = 0.001
            meta.update(ortho=scale, center=list(c), res=[1600, 1600])
        elif shot in ("cutaway", "exploded"):
            _wb(2000, 1400)
            if shot == "cutaway":
                hide_upper(True)
            else:
                explode(True, mn, mx)
                for o in SC.objects:
                    if o.get("ground"):
                        o.hide_render = True
            mn2, mx2 = scene_bbox(); c2, s2 = _views(mn2, mx2)
            scale = max(s2.x, s2.y, s2.z) * 1.35
            cam = K.camera("cam", ortho=scale)
            K.look(cam, c2 + Vector((1.0, -1.15, 0.95)).normalized() * max(s2.length, 10) * 3, c2)
            if shot == "exploded":
                _fit_ortho(cam, 2000, 1400)
        K.render(shot, cam, meta)
        if shot == "cutaway":
            hide_upper(False)
        if shot == "exploded":
            explode(False, mn, mx)
        for o in rob:
            o.hide_render = (cat == "EQP")
