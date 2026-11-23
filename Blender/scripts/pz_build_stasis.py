"""Procedural build + render of PZ_STA_StasisFacility (Blender 5.x, headless).

Usage:
  blender -b --factory-startup -P pz_build_stasis.py -- <mode> <outdir> <shot> [<shot> ...]
  mode : facility | cutaway | pod | kit
Every render also writes <shot>.json with camera mapping + projected anchor points,
used by the sheet composer for callouts and dimension lines.
All dimensions are DESIGN ASSUMPTIONS in studs (1 BU = 1 stud).
"""
import bpy, bmesh, sys, os, math, json
from mathutils import Vector, Euler
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pz_layout as L

argv = sys.argv[sys.argv.index("--") + 1:]
MODE, OUT, SHOTS = argv[0], argv[1], argv[2:]
os.makedirs(OUT, exist_ok=True)
CUT = 12.0 if MODE == "cutaway" else None
ANCHORS = {}

bpy.ops.wm.read_factory_settings(use_empty=True)
SC = bpy.context.scene

# ------------------------------------------------------------------ materials
def srgb2lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def hexrgb(h):
    h = h.lstrip("#")
    return tuple(srgb2lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))

MATS = {}
def mat(name, hexcol, metal=0.0, rough=0.5, emit=0.0, trans=0.0, alpha=1.0):
    if name in MATS:
        return MATS[name]
    m = bpy.data.materials.new(name)
    rgb = hexrgb(hexcol)
    m.diffuse_color = (*rgb, 1.0)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1)
        b.inputs["Emission Strength"].default_value = emit
    if trans:
        b.inputs["Transmission Weight"].default_value = trans
        b.inputs["IOR"].default_value = 1.2
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    MATS[name] = m
    return m

P = L.PALETTE
M = dict(
    graphite=mat("graphite", P["graphite"], 0.8, 0.45),
    panel=mat("panel_dark", P["panel_dark"], 0.7, 0.55),
    steel=mat("steel", P["steel"], 0.9, 0.3),
    concrete=mat("concrete", P["concrete"], 0.0, 0.85),
    floor=mat("floor", P["floor"], 0.5, 0.6),
    orange=mat("orange", P["orange"], 0.3, 0.4),
    orange_e=mat("orange_emit", P["orange"], 0, 0.4, emit=6),
    amber_e=mat("amber_emit", P["amber"], 0, 0.4, emit=8),
    cyan_e=mat("cyan_emit", P["cyan"], 0, 0.3, emit=10),
    cyan_soft=mat("cyan_soft", P["cyan"], 0, 0.3, emit=2.5),
    blue=mat("blue", P["blue"], 0.4, 0.4),
    red_e=mat("red_emit", P["red"], 0, 0.4, emit=6),
    green_e=mat("green_emit", "#35D07F", 0, 0.4, emit=6),
    glass=mat("glass", "#4FCFE6", 0.0, 0.08, emit=0.02, trans=1.0),
    grate=mat("grate", "#15181C", 0.8, 0.6),
    figure=mat("figure", "#C9CED6", 0.2, 0.5),
    human=mat("human_ref", "#E9A23B", 0.0, 0.6),
    ground=mat("ground", "#24282E", 0.2, 0.8),
    banner=mat("banner", "#C2561A", 0.0, 0.7),
)

# ------------------------------------------------------------------ primitives
COLL = SC.collection

def _obj(name, me, m):
    o = bpy.data.objects.new(name, me)
    COLL.objects.link(o)
    if m is not None:
        o.data.materials.append(m)
    return o

def box(name, x0, x1, y0, y1, z0, z1, m):
    if x1 - x0 <= 0 or y1 - y0 <= 0 or z1 - z0 <= 0:
        return None
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update()
    return _obj(name, me, m)

def cbox(name, cx, cy, cz, sx, sy, sz, m, rot=(0, 0, 0)):
    o = box(name, -sx / 2, sx / 2, -sy / 2, sy / 2, -sz / 2, sz / 2, m)
    o.location = (cx, cy, cz); o.rotation_euler = rot
    return o

def cyl(name, x, y, z0, h, r, m, seg=32, r2=None, rot=None):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg,
                          radius1=r, radius2=r if r2 is None else r2, depth=h)
    bm.to_mesh(me); bm.free()
    o = _obj(name, me, m)
    if rot is None:
        o.location = (x, y, z0 + h / 2)
    else:
        o.rotation_euler = rot
        d = Euler(rot).to_matrix() @ Vector((0, 0, 1))
        o.location = Vector((x, y, z0)) + d * (h / 2)
    for p in me.polygons:
        p.use_smooth = True
    return o

def sphere(name, x, y, z, r, m):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=r)
    bm.to_mesh(me); bm.free()
    o = _obj(name, me, m); o.location = (x, y, z)
    for p in me.polygons:
        p.use_smooth = True
    return o

def tube_shell(name, x, y, z0, h, r, thick, m, a0=0.0, a1=2 * math.pi, seg=40):
    """Cylindrical shell segment from angle a0..a1 (0 = +X, CCW)."""
    n = seg
    full = abs(a1 - a0 - 2 * math.pi) < 1e-6
    cnt = n if full else n + 1
    angs = [a0 + (a1 - a0) * i / n for i in range(cnt)]
    v = []
    for zz in (z0, z0 + h):
        for rr in (r, r - thick):
            for a in angs:
                v.append((x + rr * math.cos(a), y + rr * math.sin(a), zz))
    def idx(zi, ri, i):
        return zi * 2 * cnt + ri * cnt + (i % cnt)
    f = []
    rng = range(cnt) if full else range(cnt - 1)
    for i in rng:
        f.append((idx(0, 0, i), idx(0, 0, i + 1), idx(1, 0, i + 1), idx(1, 0, i)))   # outer
        f.append((idx(0, 1, i + 1), idx(0, 1, i), idx(1, 1, i), idx(1, 1, i + 1)))   # inner
        f.append((idx(0, 0, i + 1), idx(0, 0, i), idx(0, 1, i), idx(0, 1, i + 1)))   # bottom
        f.append((idx(1, 0, i), idx(1, 0, i + 1), idx(1, 1, i + 1), idx(1, 1, i)))   # top
    if not full:
        for i, s in ((0, 1), (cnt - 1, -1)):
            f.append((idx(0, 0, i), idx(1, 0, i), idx(1, 1, i), idx(0, 1, i))[::s])
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update()
    for p in me.polygons:
        p.use_smooth = True
    return _obj(name, me, m)

def ellipse_pts(a, b, seg, cx=0.0, cz=0.0):
    return [(cx + a * math.cos(math.pi * i / seg), cz + b * math.sin(math.pi * i / seg)) for i in range(seg + 1)]

def arch_shell(name, cx, a, b, spring, y0, y1, thick, m, seg=28):
    """Elliptical barrel-vault shell along Y. a = half span, b = rise."""
    outer = ellipse_pts(a + thick, b + thick, seg)
    inner = ellipse_pts(a, b, seg)
    v, f = [], []
    for yy in (y0, y1):
        for (u, w) in outer + inner:
            v.append((cx + u, yy, spring + w))
    n = seg + 1
    def i(yi, ring, k):
        return yi * 2 * n + ring * n + k
    for k in range(seg):
        f.append((i(0, 0, k), i(0, 0, k + 1), i(1, 0, k + 1), i(1, 0, k)))
        f.append((i(0, 1, k + 1), i(0, 1, k), i(1, 1, k), i(1, 1, k + 1)))
        f.append((i(0, 0, k + 1), i(0, 0, k), i(0, 1, k), i(0, 1, k + 1)))
        f.append((i(1, 0, k), i(1, 0, k + 1), i(1, 1, k + 1), i(1, 1, k)))
    for k in (0, seg):
        f.append((i(0, 0, k), i(1, 0, k), i(1, 1, k), i(0, 1, k)))
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update()
    return _obj(name, me, m)

def gable(name, cx, a, b, spring, y, thick, m, seg=28):
    """Flat elliptical infill (vault end wall above spring line)."""
    pts = ellipse_pts(a, b, seg)
    v = [(cx + u, y, spring + w) for u, w in pts] + [(cx + u, y + thick, spring + w) for u, w in pts]
    n = len(pts)
    f = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))]
    for k in range(n - 1):
        f.append((k + 1, k, n + k, n + k + 1))
    f.append((0, n - 1, 2 * n - 1, n))
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update()
    return _obj(name, me, m)

def plate_with_octagon(name, w, h, ow, oh, depth, m, chamfer=0.28):
    """Frame plate (outer rect ow x oh) with octagonal opening w x h, in local XZ, centred x=0, z from 0.
    Built as triangle fan between outer rect and inner octagon."""
    c = min(w, h) * chamfer
    inner = [(-w / 2 + c, 0), (w / 2 - c, 0), (w / 2, c), (w / 2, h - c), (w / 2 - c, h),
             (-w / 2 + c, h), (-w / 2, h - c), (-w / 2, c)]
    z0 = -(oh - h) * 0.25
    outer = [(-ow / 2, z0), (ow / 2, z0), (ow / 2, z0), (ow / 2, z0 + oh), (ow / 2, z0 + oh),
             (-ow / 2, z0 + oh), (-ow / 2, z0 + oh), (-ow / 2, z0)]
    # pair inner vertex k with outer vertex k (outer duplicated corners keep quads valid)
    v = []
    for yy in (-depth / 2, depth / 2):
        for (u, w2) in outer + inner:
            v.append((u, yy, w2))
    n = 8
    def i(side, ring, k):
        return side * 16 + ring * 8 + (k % 8)
    f = []
    for k in range(n):
        for side in (0, 1):
            q = (i(side, 0, k), i(side, 0, k + 1), i(side, 1, k + 1), i(side, 1, k))
            f.append(q if side else q[::-1])
        f.append((i(0, 1, k), i(0, 1, k + 1), i(1, 1, k + 1), i(1, 1, k)))
        f.append((i(0, 0, k + 1), i(0, 0, k), i(1, 0, k), i(1, 0, k + 1)))
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f)
    me.validate(); me.update()
    return _obj(name, me, m)

def place(o, x, y, z=0.0, rz=0.0):
    o.location = (x, y, z); o.rotation_euler = (0, 0, rz); return o

def anchor(name, xyz):
    ANCHORS[name] = tuple(xyz)

# ------------------------------------------------------------------ figures
def mannequin(prefix, x, y, z0, height, m, face_rz=0.0):
    """Neutral proportion figure (NOT a canonical character). Height in studs."""
    s = height / 7.0
    parts = []
    parts.append(cyl(prefix + "_legL", -0.35 * s, 0, z0, 3.2 * s, 0.32 * s, m, 12))
    parts.append(cyl(prefix + "_legR", 0.35 * s, 0, z0, 3.2 * s, 0.32 * s, m, 12))
    parts.append(cbox(prefix + "_pelvis", 0, 0, z0 + 3.35 * s, 1.2 * s, 0.7 * s, 0.5 * s, m))
    parts.append(cbox(prefix + "_torso", 0, 0, z0 + 4.55 * s, 1.5 * s, 0.85 * s, 1.9 * s, m))
    parts.append(cyl(prefix + "_armL", -0.98 * s, 0, z0 + 3.0 * s, 2.5 * s, 0.22 * s, m, 10))
    parts.append(cyl(prefix + "_armR", 0.98 * s, 0, z0 + 3.0 * s, 2.5 * s, 0.22 * s, m, 10))
    parts.append(cyl(prefix + "_neck", 0, 0, z0 + 5.5 * s, 0.35 * s, 0.18 * s, m, 10))
    parts.append(sphere(prefix + "_head", 0, 0, z0 + 6.3 * s, 0.62 * s, m))
    pivot = bpy.data.objects.new(prefix, None); COLL.objects.link(pivot)
    for p in parts:
        p.parent = pivot
    pivot.location = (x, y, 0); pivot.rotation_euler = (0, 0, face_rz)
    return pivot

# ------------------------------------------------------------------ canonical robots
_BOTS = {}
def robot_collection(name):
    """Import a canonical robot once into an unlinked collection (rest pose, stray helper removed, uniform scale)."""
    if name in _BOTS:
        return _BOTS[name]
    spec = L.ROBOTS[name]
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(L.ROBOT_SRC_DIR, spec["file"]))
    new = [o for o in bpy.data.objects if o not in before]
    for o in list(new):
        if o.type == "MESH" and o.name.startswith("Icosphere") and o.parent is None:
            new.remove(o); bpy.data.objects.remove(o)
    for o in new:
        if o.type == "ARMATURE":
            if o.animation_data:
                o.animation_data.action = None
            o.data.pose_position = "REST"
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in new:
        if o.type == "MESH":
            ev = o.evaluated_get(dg); me = ev.to_mesh()
            pts += [ev.matrix_world @ v.co for v in me.vertices]
            ev.to_mesh_clear()
    mn = Vector([min(p[k] for p in pts) for k in range(3)]); mx = Vector([max(p[k] for p in pts) for k in range(3)])
    sc = spec["height"] / (mx.z - mn.z)
    coll = bpy.data.collections.new("BOT_" + name)
    piv = bpy.data.objects.new("BOTROOT_" + name, None); coll.objects.link(piv)
    for o in new:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)
        if o.parent is None:
            o.parent = piv
    piv.scale = (sc, sc, sc)
    piv.location = (-sc * (mn.x + mx.x) / 2, -sc * (mn.y + mx.y) / 2, -sc * mn.z)
    _BOTS[name] = coll
    return coll

def robot_instance(objname, name, x, y, z=0.0, rz=0.0):
    e = bpy.data.objects.new(objname, None)
    e.instance_type = "COLLECTION"; e.instance_collection = robot_collection(name)
    COLL.objects.link(e); e.location = (x, y, z); e.rotation_euler = (0, 0, rz)
    return e

# ------------------------------------------------------------------ stasis pod
def build_pod(prefix, state="closed", occupant=True, detail=True):
    """Stasis pod, local origin at floor centre, front faces -Y. Returns pivot empty."""
    D = L.POD
    objs = []
    pz, gh, ch = D["plinth_h"], D["glass_h"], D["cap_h"]
    gr = D["glass_d"] / 2
    objs.append(cyl(prefix + "_step", 0, 0, 0, 0.4, 5.0, M["panel"], 8))
    objs.append(cyl(prefix + "_plinth", 0, 0, 0.4, pz - 0.4, D["plinth_d"] / 2, M["graphite"], 8))
    objs.append(cyl(prefix + "_plinth_ring", 0, 0, pz - 0.35, 0.35, D["plinth_d"] / 2 + 0.1, M["steel"], 8))
    objs.append(cbox(prefix + "_status", 0, -4.25, 1.45, 3.0, 0.3, 0.45, M["orange_e"]))
    objs.append(cyl(prefix + "_deck", 0, 0, pz, 0.3, gr - 0.15, M["steel"], 32))
    objs.append(tube_shell(prefix + "_deck_light", 0, 0, pz + 0.3, 0.12, gr - 0.3, 0.35, M["cyan_e"]))
    # glass: back half fixed; front half rotates around behind when open
    objs.append(tube_shell(prefix + "_glass_back", 0, 0, pz, gh, gr, 0.15, M["glass"], 0, math.pi))
    front = tube_shell(prefix + "_glass_front", 0, 0, pz, gh, gr - 0.2, 0.15, M["glass"], math.pi, 2 * math.pi)
    if state == "open":
        front.rotation_euler = (0, 0, math.radians(165))
    objs.append(front)
    # vertical frame posts
    for a in (math.pi * 0.0, math.pi * 1.0):
        objs.append(cbox(prefix + f"_post{int(a*10)}", (gr + 0.15) * math.cos(a), 0, pz + gh / 2, 0.5, 0.6, gh, M["graphite"]))
    cz = pz + gh
    objs.append(cyl(prefix + "_cap", 0, 0, cz, ch, D["cap_d"] / 2, M["graphite"], 32))
    objs.append(tube_shell(prefix + "_cap_light", 0, 0, cz + 0.7, 0.5, D["cap_d"] / 2 + 0.08, 0.2, M["cyan_e"]))
    objs.append(cyl(prefix + "_cap_inner_light", 0, 0, cz - 0.12, 0.12, gr - 0.4, M["cyan_e"], 32))
    objs.append(cyl(prefix + "_crown", 0, 0, cz + ch, 1.0, 2.6, M["steel"], 24))
    objs.append(cbox(prefix + "_crown_lamp", 0, -2.65, cz + ch + 0.5, 1.6, 0.2, 0.35, M["cyan_e"]))
    # rear service spine + coolant/power connections
    objs.append(cbox(prefix + "_spine", 0, gr + 0.55, pz + gh / 2, 1.8, 1.0, gh, M["panel"]))
    for i, xx in enumerate((-0.55, 0.55)):
        objs.append(cyl(prefix + f"_cool{i}", xx, gr + 1.35, 0, cz + 1.6, 0.32, M["steel"], 14))
        objs.append(cyl(prefix + f"_coolband{i}", xx, gr + 1.35, 6.0, 0.4, 0.36, M["blue"], 14))
    objs.append(cyl(prefix + "_power", 0, gr + 1.35, 0, pz + 1.2, 0.45, M["orange"], 14))
    objs.append(cbox(prefix + "_floor_box", 0, gr + 1.4, 0.15, 2.6, 1.4, 0.3, M["grate"]))
    if detail:
        # front console (right) and power/diagnostic unit (left) - per page-10 reference
        objs.append(cbox(prefix + "_console", 3.9, -3.6, 1.9, 1.6, 1.3, 3.8, M["graphite"]))
        objs.append(cbox(prefix + "_screen", 3.9, -4.15, 3.6, 1.3, 0.15, 1.0, M["cyan_e"],
                         rot=(math.radians(-20), 0, 0)))
        objs.append(cbox(prefix + "_unit", -5.0, -0.6, 1.75, 2.6, 3.2, 3.5, M["graphite"]))
        objs.append(cbox(prefix + "_unit_strip", -5.0, -2.25, 1.0, 1.8, 0.12, 0.35, M["amber_e"]))
        objs.append(cbox(prefix + "_unit_scr", -5.0, -2.25, 2.7, 1.6, 0.12, 0.9, M["cyan_soft"]))
    ld = bpy.data.lights.new(prefix + "_glow", "POINT"); ld.energy = 260; ld.color = (0.35, 0.85, 1.0); ld.shadow_soft_size = 2.0
    lo = bpy.data.objects.new(prefix + "_glow", ld); COLL.objects.link(lo); lo.location = (0, -1.2, pz + gh * 0.55); objs.append(lo)
    lo.visible_camera = False; lo.visible_glossy = False; lo.visible_transmission = False
    if occupant in L.ROBOTS:
        objs.append(robot_instance(prefix + "_occ", occupant, 0, 0, pz + 0.3))
    elif occupant:
        mannequin(prefix + "_occ", 0, 0, pz + 0.3, 6.8, M["figure"])
        objs.append(bpy.data.objects[prefix + "_occ"])
    pivot = bpy.data.objects.new(prefix, None); COLL.objects.link(pivot)
    for o in objs:
        o.parent = pivot
    return pivot

# ------------------------------------------------------------------ walls
def door_list(axis, fixed):
    return [d for d in L.DOORS if d[2] == axis and abs(d[4] - fixed) < 0.6]

def wall(name, axis, fixed, a, b, h, thick, m, offset=0.0):
    """Wall along axis ('x' wall runs along X at y=fixed). offset shifts wall body perpendicular."""
    if CUT is not None:
        h = min(h, CUT)
    ops = sorted([(d[3] - d[5] / 2, d[3] + d[5] / 2, d[6]) for d in door_list(axis, fixed)
                  if a <= d[3] <= b])
    segs, cur = [], a
    for (o0, o1, dh) in ops:
        segs.append((cur, o0, 0, h))
        if dh < h:
            segs.append((o0, o1, dh, h))
        cur = o1
    segs.append((cur, b, 0, h))
    t0, t1 = fixed - thick / 2 + offset, fixed + thick / 2 + offset
    for k, (s0, s1, z0, z1) in enumerate(segs):
        if axis == "x":
            box(f"{name}_{k}", s0, s1, t0, t1, z0, z1, m)
        else:
            box(f"{name}_{k}", t0, t1, s0, s1, z0, z1, m)

def merged_room_edges():
    edges = {}
    for (_, _, x0, x1, y0, y1, _) in L.ROOMS:
        for key, iv in ((("x", y0), (x0, x1)), (("x", y1), (x0, x1)), (("y", x0), (y0, y1)), (("y", x1), (y0, y1))):
            edges.setdefault(key, []).append(iv)
    out = []
    for (axis, fixed), ivs in edges.items():
        ivs.sort()
        cur = list(ivs[0])
        for s, e in ivs[1:]:
            if s <= cur[1]:
                cur[1] = max(cur[1], e)
            else:
                out.append((axis, fixed, *cur)); cur = [s, e]
        out.append((axis, fixed, *cur))
    split = []
    for (axis, fixed, a, b) in out:
        cuts = [c for c in ((24, 104) if axis == "y" else (-24, 24)) if a < c < b]
        pts = [a] + cuts + [b]
        split += [(axis, fixed, pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    return split

def volume_height_at(x, y):
    for (_, x0, x1, y0, y1, h) in L.VOLUMES:
        if x0 <= x <= x1 and y0 <= y <= y1:
            return h
    return 18

def door_leaf(d):
    did, label, axis, pos, fixed, w, h, kind = d
    if kind == "main":
        lm, seam = M["graphite"], M["cyan_e"]
    elif kind == "blast":
        lm, seam = M["panel"], M["cyan_e"]
    elif kind == "rollup":
        lm, seam = M["steel"], M["amber_e"]
    elif kind == "egress":
        lm, seam = M["graphite"], M["green_e"]
    else:
        return
    if CUT is not None:
        return
    objs = []
    if kind in ("main", "blast"):
        objs.append(box(f"{did}_leafL", -w / 2, -0.15, -0.3, 0.3, 0, h, lm))
        objs.append(box(f"{did}_leafR", 0.15, w / 2, -0.3, 0.3, 0, h, lm))
        objs.append(box(f"{did}_seam", -0.15, 0.15, -0.35, 0.35, 0.5, h - 0.5, seam))
        objs.append(box(f"{did}_band", -w / 2, w / 2, -0.36, 0.36, h * 0.55, h * 0.55 + 0.35, M["orange"]))
        fr = plate_with_octagon(f"{did}_frame", w, h, w + 5, h + 3, 2.6, M["graphite"])
        objs.append(fr)
        objs.append(box(f"{did}_frame_light", -w / 2 - 0.2, w / 2 + 0.2, -1.4, -1.3, h + 0.4, h + 0.7, seam))
    elif kind == "rollup":
        objs.append(box(f"{did}_shutter", -w / 2, w / 2, -0.25, 0.25, 0, h, lm))
        for k in range(1, int(h)):
            objs.append(box(f"{did}_slat{k}", -w / 2, w / 2, -0.3, -0.25, k - 0.05, k + 0.05, M["graphite"]))
        for s in (-1, 1):
            objs.append(box(f"{did}_haz{s}", s * w / 2 - 0.6, s * w / 2 + 0.6, -0.5, 0.5, 0, h + 1, M["orange"]))
        objs.append(box(f"{did}_lamp", -2, 2, -0.6, -0.4, h + 1.2, h + 1.6, seam))
    elif kind == "egress":
        objs.append(box(f"{did}_leaf", -w / 2, w / 2, -0.2, 0.2, 0, h, lm))
        objs.append(box(f"{did}_frame_t", -w / 2 - 0.6, w / 2 + 0.6, -0.5, 0.5, h, h + 0.6, M["orange"]))
        objs.append(box(f"{did}_frame_l", -w / 2 - 0.6, -w / 2, -0.5, 0.5, 0, h, M["orange"]))
        objs.append(box(f"{did}_frame_r", w / 2, w / 2 + 0.6, -0.5, 0.5, 0, h, M["orange"]))
        objs.append(box(f"{did}_exit", -1.2, 1.2, -0.7, -0.5, h + 1.0, h + 1.8, seam))
    piv = bpy.data.objects.new(did, None); COLL.objects.link(piv)
    for o in objs:
        o.parent = piv
    # local -Y must face outward / toward the viewer side of the wall
    if axis == "x":
        rz = math.pi if fixed >= 100 and kind == "rollup" else 0.0
        if kind == "blast" and fixed == 104:
            rz = 0.0
        place(piv, pos, fixed, 0, rz)
    else:
        rz = -math.pi / 2 if fixed < 0 else math.pi / 2
        place(piv, fixed, pos, 0, rz)
    anchor(did, (pos, fixed, h + 1) if axis == "x" else (fixed, pos, h + 1))

# ------------------------------------------------------------------ facility
def build_facility():
    C = L.CHAMBER
    # ground + slab
    if MODE != "cutaway":
        box("ground", -260, 260, -200, 320, -0.6, -0.5, M["ground"])
    box("slab", L.X0 - 1, L.X1 + 1, L.Y0 - 1, L.Y1 + 1, -0.5, 0, M["concrete"])
    # room floors (tinted by function so cutaway reads)
    for (rid, label, x0, x1, y0, y1, ck) in L.ROOMS:
        fm = M["floor"] if ck != "chamber" else M["panel"]
        box(f"floor_{rid}", x0, x1, y0, y1, 0, 0.05, fm)
        anchor(rid, ((x0 + x1) / 2, (y0 + y1) / 2, 0.5))
    # exterior walls
    T = L.EXT_WALL
    wall("ext_S", "x", 0, -44, 44, 20, T, M["graphite"], offset=T / 2)
    wall("ext_N", "x", 120, -44, 44, 22, T, M["graphite"], offset=-T / 2)
    for side, xf, off in (("W", -44, T / 2), ("E", 44, -T / 2)):
        wall(f"ext_{side}a", "y", xf, 0, 24, 20, T, M["graphite"], offset=off)
        wall(f"ext_{side}b", "y", xf, 24, 104, 18, T, M["graphite"], offset=off)
        wall(f"ext_{side}c", "y", xf, 104, 120, 22, T, M["graphite"], offset=off)
    # interior walls from merged room edges
    for k, (axis, fixed, a, b) in enumerate(merged_room_edges()):
        if (axis == "x" and fixed in (0, 120)) or (axis == "y" and fixed in (-44, 44)):
            continue
        if axis == "y" and abs(fixed) == 24 and a >= 24 and b <= 104:
            h = C["spring"]
        elif axis == "x" and fixed in (24, 104) and a >= -24 and b <= 24:
            h = C["spring"]
        else:
            mx = (a + b) / 2
            h = volume_height_at(fixed, mx) - 1 if axis == "y" else volume_height_at(mx, fixed) - 1
        # chamber side walls carry the medical observation window
        if axis == "y" and fixed == 24 and a <= 34 and b >= 56 and a >= 24:
            ow = L.OBS_WINDOW
            hh = min(h, CUT) if CUT else h
            wall(f"iw{k}a", "y", fixed, a, ow["y0"], h, L.WALL, M["graphite"])
            wall(f"iw{k}b", "y", fixed, ow["y1"], b, h, L.WALL, M["graphite"])
            box(f"iw{k}c", fixed - .5, fixed + .5, ow["y0"], ow["y1"], 0, ow["z0"], M["graphite"])
            box(f"iw{k}d", fixed - .5, fixed + .5, ow["y0"], ow["y1"], ow["z1"], hh, M["graphite"])
            box(f"iw{k}g", fixed - .1, fixed + .1, ow["y0"], ow["y1"], ow["z0"], ow["z1"], M["glass"])
            continue
        wall(f"iw{k}", axis, fixed, a, b, h, L.WALL, M["graphite"] if CUT is None else M["steel"])
    for d in L.DOORS:
        door_leaf(d)

    if CUT is None:
        # roofs + parapets
        for (name, x0, x1, y0, y1, h) in L.VOLUMES:
            box(f"roof_{name}", x0, x1, y0, y1, h - 1, h, M["panel"])
            for (a0, a1, b0, b1) in ((x0, x1, y0, y0 + 0.8), (x0, x1, y1 - 0.8, y1), (x0, x0 + 0.8, y0, y1), (x1 - 0.8, x1, y0, y1)):
                box(f"par_{name}_{a0}_{b0}", a0, a1, b0, b1, h, h + 1.2, M["graphite"])
            box(f"parcap_{name}", x0, x0 + 0.8, y0, y0 + 0.8, h + 1.2, h + 1.5, M["orange"])
            box(f"parcap2_{name}", x1 - 0.8, x1, y0, y0 + 0.8, h + 1.2, h + 1.5, M["orange"])
        for (x0, x1, y, z0, z1) in ((-44, -24, 24, 18, 20), (24, 44, 24, 18, 20), (-44, -24, 104, 18, 22), (24, 44, 104, 18, 22)):
            box(f"skirt_{x0}_{y}", x0, x1, y - 0.5, y + 0.5, z0, z1, M["graphite"])
        # barrel vault, gables, ribs, ridge light
        a, b = (C["x1"] - C["x0"]) / 2, C["crown"] - C["spring"] - 1
        arch_shell("vault", 0, a, b, C["spring"], C["y0"], C["y1"], 1.0, M["panel"])
        gable("gable_S", 0, a, b, C["spring"], C["y0"] - 0.5, 1.0, M["graphite"])
        gable("gable_N", 0, a, b, C["spring"], C["y1"] - 0.5, 1.0, M["graphite"])
        for y in range(C["y0"], C["y1"] + 1, L.RIB_STEP):
            arch_shell(f"rib_{y}", 0, a + 0.9, b + 0.9, C["spring"], y - 0.6, y + 0.6, 1.2, M["graphite"], seg=28)
            arch_shell(f"rib_in_{y}", 0, a - 1.2, b - 1.2, C["spring"], y - 0.4, y + 0.4, 1.2, M["graphite"], seg=28)
            for s in (-1, 1):
                box(f"pil_{y}_{s}", s * 24 - 1.0 if s > 0 else -24.0, s * 24 if s > 0 else -23.0,
                    y - 0.5, y + 0.5, 0, C["spring"], M["graphite"])
                box(f"buttress_{y}_{s}", s * 24 + (0.5 if s > 0 else -2.5), s * 24 + (2.5 if s > 0 else -0.5),
                    y - 0.7, y + 0.7, 17, 19.5, M["graphite"])
        box("ridge_light", -0.8, 0.8, C["y0"], C["y1"], C["crown"] - 0.05, C["crown"] + 0.35, M["cyan_e"])
        box("ridge_cap", -1.6, 1.6, C["y0"], C["y1"], C["crown"] + 0.35, C["crown"] + 0.6, M["graphite"])
        for y in range(C["y0"] + 4, C["y1"], 16):
            cyl(f"ceil_lamp_{y}", 0, y, C["crown"] - 2.0, 0.6, 1.8, M["cyan_e"], 24)
        anchor("vault", (0, 64, C["crown"]))
        anchor("ribs", (-12, 40, C["spring"] + 12))
        # roof equipment
        for i, y in enumerate((32, 46, 60)):
            box(f"cool_{i}", 28, 40, y, y + 10, 18, 22, M["steel"])
            cyl(f"fan_{i}", 34, y + 5, 22, 0.4, 3.6, M["panel"], 24)
            cyl(f"fanhub_{i}", 34, y + 5, 22.4, 0.3, 0.9, M["orange"], 16)
        anchor("cooling_units", (34, 46, 22.5))
        for i, x in enumerate((-40, -33)):
            cyl(f"cryo_tank_{i}", x + 2.5, 30, 20.5, 26, 2.4, M["steel"], 24, rot=(math.radians(-90), 0, 0))
            for yy in (34, 48):
                box(f"tank_saddle_{i}_{yy}", x, x + 5, yy - 1, yy, 18, 20, M["graphite"])
            cyl(f"cryo_band_{i}", x + 2.5, 42, 20.5, 1.0, 2.5, M["blue"], 24, rot=(math.radians(-90), 0, 0))
        anchor("cryo_tanks", (-33, 45, 23))
        cyl("roof_pipe_run_w", -27, 26, 18.6, 72, 0.6, M["steel"], 12, rot=(math.radians(-90), 0, 0))
        cyl("roof_pipe_run_e", 26.5, 26, 18.6, 72, 0.6, M["orange"], 12, rot=(math.radians(-90), 0, 0))
        for i, x in enumerate((-36, -30, 30, 36)):
            cyl(f"vent_{i}", x, 8, 19, 5, 1.2, M["graphite"], 16)
            cyl(f"vent_cap_{i}", x, 8, 24, 0.5, 1.6, M["steel"], 16)
        anchor("vents", (36, 8, 24))
        cyl("antenna", -34, 112, 22, 16, 0.4, M["steel"], 12)
        cyl("antenna_dish", -34, 112, 30, 0.6, 2.2, M["graphite"], 24)
        sphere("antenna_beacon", -34, 112, 38.3, 0.5, M["red_e"])
        anchor("antenna", (-34, 112, 38))
        box("hvac_rear", 10, 30, 108, 116, 22, 25, M["steel"])
        # facade details: window strips, signage, banners, light bands
        for x0, x1 in ((-40, -18), (18, 40)):
            box(f"win_S_{x0}", x0, x1, -0.15, 0.05, 12, 14, M["cyan_soft"])
        for y0_, y1_ in ((30, 50), (58, 78), (84, 100)):
            box(f"win_W_{y0_}", -44.15, -43.95, y0_, y1_, 10, 11.5, M["cyan_soft"])
            box(f"win_E_{y0_}", 43.95, 44.15, y0_, y1_, 10, 11.5, M["cyan_soft"])
        # facade pilasters every 8 studs + mid band (panel rhythm on the 8-stud grid)
        for x in range(-40, 41, 8):
            if abs(x) <= 20:
                continue
            box(f"pilS_{x}", x - 0.6, x + 0.6, -0.6, 0, 0, 19, M["steel"])
        for y in range(8, 120, 8):
            hh = 20 if y < 24 else (18 if y < 104 else 22)
            if y in (80, 112):
                continue
            for s in (-1, 1):
                box(f"pil{s}_{y}", (s * 44 - 0.6) if s < 0 else 44, (s * 44) if s < 0 else 44.6, y - 0.6, y + 0.6, 0, hh - 1, M["steel"])
        for s in (-1, 1):
            box(f"band_{s}", (s * 44 - 0.4) if s < 0 else 44, (s * 44) if s < 0 else 44.4, 0, 120, 6, 6.6, M["graphite"])
        box("band_S", -44, 44, -0.4, 0, 6, 6.6, M["graphite"])
        box("base_band_S", -44, 44, -0.25, 0.0, 0, 1.2, M["orange"])
        box("top_band_S", -44, 44, -0.25, 0.0, 18.2, 18.6, M["cyan_e"])
        for s in (-1, 1):
            box(f"banner_{s}", s * 13 - 2, s * 13 + 2, -0.8, -0.3, 6, 16, M["banner"])
            cbox(f"banner_emblem_{s}", s * 13, -0.9, 12.5, 2.0, 0.2, 2.0, M["amber_e"], rot=(0, math.radians(45), 0))
            box(f"pylon_{s}", s * 19 - 1.5, s * 19 + 1.5, -3, 0, 0, 20.5, M["graphite"])
            box(f"pylon_light_{s}", s * 19 - 0.3, s * 19 + 0.3, -3.1, -2.9, 1, 19, M["cyan_e"])
        anchor("banners", (13, -1, 16))
        txt = bpy.data.curves.new("sign", "FONT"); txt.body = "NX-01  STASIS FACILITY"
        txt.size = 1.7; txt.extrude = 0.1; txt.align_x = "CENTER"
        so = _obj("sign", txt, M["cyan_e"]); so.location = (0, -0.6, 16.6); so.rotation_euler = (math.radians(90), 0, 0)
        anchor("signage", (0, -1, 17.5))
        # entrance apron + guide lights
        box("apron", -16, 16, -26, 0, 0, 0.08, M["floor"])
        for s in (-1, 1):
            box(f"apron_light_{s}", s * 6.5 - 0.3, s * 6.5 + 0.3, -26, -3, 0.08, 0.16, M["amber_e"])
            box(f"apron_haz_{s}", s * 16 - 0.6, s * 16, -26, 0, 0.08, 0.14, M["orange"])
        box("service_apron", -14, 14, 120, 138, 0, 0.08, M["floor"])
        box("dock_haz", -9, 9, 121, 123, 0.08, 0.14, M["orange"])
        anchor("apron", (0, -16, 0))

    # ---- chamber interior
    C2 = L.CHAMBER
    box("aisle", -L.AISLE_HALF, L.AISLE_HALF, 24, 104, 0.05, 0.12, M["grate"])
    for s in (-1, 1):
        box(f"aisle_strip_{s}", s * L.AISLE_HALF - 0.3, s * L.AISLE_HALF + 0.3, 26, 102, 0.12, 0.2, M["amber_e"])
    for y in range(28, 104, 4):
        box(f"aisle_slat_{y}", -L.AISLE_HALF + 0.6, L.AISLE_HALF - 0.6, y, y + 0.35, 0.12, 0.17, M["steel"])
    for y in L.POD_YS:
        for s in (-1, 1):
            box(f"trench_{y}_{s}", s * 6.3 if s > 0 else -11.5, 11.5 if s > 0 else -6.3, y - 0.8, y + 0.8, 0.05, 0.14, M["cyan_soft"])
    anchor("aisle", (0, 30, 0.2))
    for (pid, x, y, face) in L.PODS:
        p = build_pod(pid, "closed", occupant=L.POD_OCCUPANTS.get(pid, True))
        place(p, x, y, 0, math.pi / 2 if x < 0 else -math.pi / 2)
        anchor(pid, (x, y, 14.5))
    # pod service hatches on maintenance-corridor side
    for y in L.POD_YS:
        box(f"hatch_{y}", -24.7, -24.4, y - 2, y + 2, 1, 7, M["orange"])
    # mezzanine + stair + rail
    mz = L.MEZZANINE
    box("mezz_slab", -23.5, 23.5, mz["y0"], mz["y1"], mz["z"] - 0.8, mz["z"], M["graphite"])
    box("mezz_rail", -23.5, 23.5, mz["y1"] - 0.2, mz["y1"], mz["z"], mz["z"] + 3.2, M["steel"])
    box("mezz_rail_light", -23.5, 23.5, mz["y1"] - 0.25, mz["y1"] - 0.15, mz["z"] + 3.2, mz["z"] + 3.4, M["cyan_e"])
    for k in range(12):
        box(f"mstair_{k}", -23.5, -19.5, 44 - k * 1.0, 45 - k * 1.0, 0, (k + 1) * 1.0, M["steel"])
    anchor("mezzanine", (10, 32, 12.5))
    if CUT is None:
        cr = L.CRANE
        for s in (-1, 1):
            box(f"crane_rail_{s}", s * cr["rail_x"] - 0.6, s * cr["rail_x"] + 0.6, 26, 102, cr["z"], cr["z"] + 1.2, M["graphite"])
        by = cr["bridge_y"]
        box("crane_bridge", -15, 15, by - 1.2, by + 1.2, cr["z"] - 1.8, cr["z"], M["orange"])
        box("crane_trolley", -2.2, 2.2, by - 1.8, by + 1.8, cr["z"] - 3.2, cr["z"] - 1.8, M["graphite"])
        # orange manipulator arm (ref. page 10)
        cyl("arm_base", 0, by, cr["z"] - 4.4, 1.2, 1.0, M["graphite"], 16)
        cbox("arm_seg1", -2.2, by, cr["z"] - 6.6, 1.2, 1.2, 5.5, M["orange"], rot=(0, math.radians(-40), 0))
        sphere("arm_j1", -4.1, by, cr["z"] - 8.7, 0.9, M["graphite"])
        cbox("arm_seg2", -6.3, by, cr["z"] - 8.5, 1.0, 1.0, 4.6, M["orange"], rot=(0, math.radians(80), 0))
        sphere("arm_j2", -8.5, by, cr["z"] - 8.2, 0.7, M["graphite"])
        cbox("arm_grip_a", -9.3, by - 0.5, cr["z"] - 9.2, 0.4, 0.3, 2.2, M["steel"], rot=(0, math.radians(20), 0))
        cbox("arm_grip_b", -9.3, by + 0.5, cr["z"] - 9.2, 0.4, 0.3, 2.2, M["steel"], rot=(0, math.radians(20), 0))
        anchor("crane", (0, by, cr["z"]))
        anchor("arm", (-6, by, cr["z"] - 8.5))
        # banners at containment door (inside chamber)
        for s in (-1, 1):
            box(f"in_banner_{s}", s * 13 - 2, s * 13 + 2, 102.6, 103.0, 7, 16, M["banner"])
            cbox(f"in_emblem_{s}", s * 13, 102.5, 12.5, 2.0, 0.2, 2.0, M["amber_e"], rot=(0, math.radians(45), 0))
    # ---- room props
    # reception
    box("rec_desk", -8, 8, 12, 14.5, 0, 3.2, M["graphite"])
    box("rec_desk_top", -8.2, 8.2, 11.8, 14.7, 3.2, 3.5, M["steel"])
    box("rec_desk_scr", -6, 6, 11.7, 11.8, 2.0, 3.0, M["cyan_soft"])
    for s in (-1, 1):
        box(f"scan_post_{s}", s * 5 - 0.6, s * 5 + 0.6, 18.5, 20, 0, 10, M["graphite"])
        box(f"scan_glow_{s}", s * 5 - 0.65 * s * 0 - 0.1, s * 5 + 0.1, 18.4, 20.1, 1, 9, M["cyan_e"])
    box("scan_head", -5.6, 5.6, 18.5, 20, 10, 11.2, M["graphite"])
    anchor("scanner_arch", (0, 19, 11))
    # security office
    box("sec_monitor_wall", -43, -41.5, 4, 20, 3, 9, M["panel"])
    for k in range(4):
        box(f"sec_scr_{k}", -41.5, -41.4, 5 + k * 3.8, 8 + k * 3.8, 4, 8, M["red_e"] if k == 1 else M["cyan_soft"])
    box("sec_desk", -38, -30, 8, 11, 0, 3, M["graphite"])
    # lockers
    for k in range(6):
        box(f"locker_{k}", 26 + k * 3, 28.6 + k * 3, 21, 23, 0, 7, M["steel"])
    box("decon_pad", 30, 38, 6, 14, 0.05, 0.2, M["orange"])
    # maintenance corridor pipe runs
    for k, (xx, zz, mm) in enumerate(((-31.2, 2.5, "steel"), (-31.2, 4.0, "blue"), (-31.2, 14, "steel"), (-25.6, 13, "orange"))):
        cyl(f"mc_pipe_{k}", xx, 24.5, zz, 79, 0.45, M[mm], 12, rot=(math.radians(-90), 0, 0))
    box("mc_tray", -31.6, -27, 24.5, 103.5, 15.5, 15.8, M["graphite"])
    anchor("maint_corridor_pipes", (-30, 64, 4))
    # cryogenic plant
    for k, y in enumerate((30, 40, 50, 62)):
        cyl(f"cryo_vtank_{k}", -38, y, 0, 13, 3.2, M["steel"], 24)
        cyl(f"cryo_vband_{k}", -38, y, 9, 0.8, 3.3, M["blue"], 24)
        cyl(f"cryo_vcap_{k}", -38, y, 13, 0.6, 2.0, M["graphite"], 16)
    anchor("cryo_plant", (-38, 48, 14))
    # spares store crates
    for k in range(4):
        box(f"crate_{k}", -43, -39, 90 + k * 3.4, 93 + k * 3.4, 0, 3 + (k % 2), M["graphite"])
        box(f"crate_strip_{k}", -39.05, -38.95, 90.5 + k * 3.4, 92.5 + k * 3.4, 1, 1.4, M["orange_e"])
    # medical monitoring
    for k, y in enumerate((36, 46)):
        box(f"med_desk_{k}", 26, 30, y, y + 7, 0, 3, M["graphite"])
        box(f"med_scr_{k}", 25.8, 26, y + 0.5, y + 6.5, 3.4, 6.5, M["cyan_soft"])
    box("med_bed", 36, 42, 30, 34, 0, 2.6, M["steel"])
    box("med_bed_glow", 36.2, 41.8, 30.2, 33.8, 2.6, 2.7, M["cyan_e"])
    box("med_wall_scr", 43.3, 43.5, 38, 54, 4, 10, M["cyan_soft"])
    anchor("medical_consoles", (28, 42, 6))
    # energy control: power core + cabinets
    cyl("core_base", 34, 76, 0, 1.5, 4.2, M["graphite"], 32)
    cyl("core_glow", 34, 76, 1.5, 11, 2.2, M["cyan_e"], 32)
    tube_shell("core_cage", 34, 76, 1.5, 11, 3.4, 0.3, M["glass"])
    cyl("core_cap", 34, 76, 12.5, 1.5, 3.8, M["graphite"], 32)
    for k in range(5):
        box(f"cab_{k}", 42, 43.5, 62 + k * 6, 67 + k * 6, 0, 9, M["panel"])
        box(f"cab_led_{k}", 41.9, 42, 63 + k * 6, 66 + k * 6, 6, 6.6, M["amber_e"] if k % 2 else M["cyan_e"])
    box("energy_console", 26, 29, 70, 82, 0, 3, M["graphite"])
    box("energy_console_scr", 28.9, 29.0, 71, 81, 2.2, 3.0, M["cyan_soft"])
    anchor("power_core", (34, 76, 14))
    # emergency exits marking
    box("egressE_floor", 26, 42, 104, 118, 0.05, 0.12, M["floor"])
    for k in range(5):
        box(f"egress_chev_{k}", 30 + k * 2.5, 31 + k * 2.5, 110, 114, 0.12, 0.18, M["green_e"])
    for k in range(4):
        box(f"egressW_chev_{k}", -42 + k * 2.4, -41 + k * 2.4, 78, 82, 0.12, 0.18, M["green_e"])
    # service bay
    box("cargo_pad", -6, 6, 108, 116, 0.05, 0.15, M["orange"])
    box("cargo_pad_in", -5, 5, 109, 115, 0.15, 0.2, M["grate"])
    for k in range(3):
        box(f"bay_crate_{k}", 14 + 0, 21, 106 + k * 4.4, 110 + k * 4.4, 0, 3.5, M["graphite"])
    # service stair
    for k in range(14):
        box(f"sstair_{k}", -42, -36, 105 + k * 1.0, 106 + k * 1.0, 0, (k + 1) * 0.9, M["steel"])
    anchor("service_stair", (-39, 112, 12))

# ------------------------------------------------------------------ kit layout (SF-05)
def build_kit():
    """SF-05 modular kit laid out on a grid (no ground; transparent render)."""
    # row A (y = 0)
    box("K01", 0, 8, 0, 8, 0, 0.5, M["floor"]); box("K01_seam", 0, 8, 3.9, 4.1, 0.5, 0.55, M["steel"]); anchor("K01", (4, 4, 0.6))
    box("K02", 16, 24, 3.5, 4.5, 0, 18, M["graphite"]); box("K02_strip", 16, 24, 3.4, 3.5, 10, 11.5, M["cyan_soft"])
    box("K02_pil", 23.4, 24.6, 3.0, 5.0, 0, 18, M["steel"]); anchor("K02", (20, 4, 18.5))
    box("K05", 32, 44, 0, 8, 0, 0.2, M["grate"])
    for s_ in (32.3, 43.1):
        box(f"K05_l{s_}", s_, s_ + 0.6, 0, 8, 0.2, 0.28, M["amber_e"])
    for yy in range(1, 8, 2):
        box(f"K05_s{yy}", 33, 43, yy, yy + 0.35, 0.2, 0.25, M["steel"])
    anchor("K05", (38, 4, 0.4))
    box("K10", 51, 53, 3, 5, 0, 3.8, M["graphite"])
    cbox("K10_scr", 52, 2.85, 3.4, 1.6, 0.15, 1.1, M["cyan_e"], rot=(math.radians(-20), 0, 0)); anchor("K10", (52, 4, 4.6))
    p = build_pod("K06", "closed", occupant=False); place(p, 66, 4, 0, 0); anchor("K06", (66, 4, 14.6))
    robot_instance("K_cypher", "Cypher", 78, 4); anchor("K_human", (78, 4, 6.4))
    # row B (y = 30)
    box("K07_l", 4, 9.85, 29.7, 30.3, 0, 14, M["panel"]); box("K07_r", 10.15, 16, 29.7, 30.3, 0, 14, M["panel"])
    box("K07_seam", 9.85, 10.15, 29.65, 30.35, 0.5, 13.5, M["cyan_e"])
    box("K07_band", 4, 16, 29.6, 30.4, 7.7, 8.05, M["orange"])
    fr = plate_with_octagon("K07_frame", 12, 14, 17, 17, 2.6, M["graphite"]); fr.location = (10, 30, 0)
    anchor("K07", (10, 30, 16.6))
    box("K08", 28, 36, 26, 34, 11.2, 12, M["graphite"])
    for xx in (28.3, 35.7):
        for yy in (26.6, 33.4):
            box(f"K08_c{xx}_{yy}", xx - 0.3, xx + 0.3, yy - 0.3, yy + 0.3, 0, 11.2, M["steel"])
    box("K08_rail", 28, 36, 25.8, 26, 12, 15.2, M["steel"]); box("K08_led", 28, 36, 25.75, 25.85, 15.2, 15.4, M["cyan_e"])
    anchor("K08", (32, 30, 15.6))
    box("K09", 46, 62, 29.4, 30.6, 8, 9.2, M["graphite"])
    for xx in (47, 61):
        box(f"K09_h{xx}", xx - 0.4, xx + 0.4, 29.6, 30.4, 9.2, 11, M["steel"])
    box("K09_b", 53, 55, 29, 31, 6.5, 8, M["orange"]); anchor("K09", (54, 30, 11.2))
    # row C (y = 56): vault panel + rib, scaled to real 48-stud span
    arch_shell("K03", 40, 23.5, 13, 0, 52, 60, 1.0, M["panel"]); anchor("K03", (40, 56, 14))
    arch_shell("K04", 40, 24.5, 14, 0, 63, 64.2, 1.2, M["graphite"])
    for s_ in (-1, 1):
        box(f"K04_p{s_}", 40 + s_ * 24.5 - 0.6, 40 + s_ * 24.5 + 0.6, 63, 64.2, -18, 0, M["graphite"]) if False else None
    anchor("K04", (40, 63.6, 15.2))

# ------------------------------------------------------------------ pod scene
def build_pod_scene(state):
    box("pod_ground", -30, 30, -30, 30, -0.05, 0, M["ground"])
    p = build_pod("POD", "closed" if state in ("closed", "ortho") else "open", occupant="Cypher")
    robot_instance("SCALEREF", "Cypher", 9.5, -1.5)   # scale reference: Cypher 6.0 studs (no faceless figure)
    anchor("cap_light", (4.05, 0, 11.95)); anchor("glass", (-3.2, -0.5, 7)); anchor("plinth", (-4.5, -1.5, 1.5))
    anchor("status", (0, -4.4, 1.45)); anchor("console", (3.9, -4.2, 3.8)); anchor("unit", (-5, -2.3, 3.3))
    anchor("crown", (0, -2.6, 14.5)); anchor("coolant", (0.55, 4.55, 9)); anchor("power", (0, 4.55, 3.2))
    anchor("occupant", (0, 0, 9.4)); anchor("deck", (0, 0, 2.9)); anchor("human", (9.5, -1.5, 6.4))
    anchor("spine", (0, 3.75, 7))

# ------------------------------------------------------------------ family lineup scene
FAMILY_X = {"Cypher": -9.0, "Sentinel": -2.0, "Patch": 4.5}
def build_family_scene():
    box("fam_ground", -40, 40, -30, 30, -0.05, 0, M["ground"])
    for n, x in FAMILY_X.items():
        robot_instance("FAM_" + n, n, x, 0)
        anchor(n, (x, 0, L.ROBOTS[n]["height"] + 0.4))
    p = build_pod("FAMPOD", "open", occupant=None, detail=True); place(p, 15, 0, 0, 0)
    anchor("pod", (15, 0, 14.6))

# ------------------------------------------------------------------ cameras / render
def look(cam, loc, target):
    cam.location = loc
    d = Vector(target) - Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

def camera(name, ortho=None, lens=35):
    c = bpy.data.cameras.new(name)
    if ortho:
        c.type = "ORTHO"; c.ortho_scale = ortho
    else:
        c.lens = lens
    c.clip_start = 0.1; c.clip_end = 2000
    o = bpy.data.objects.new(name, c); COLL.objects.link(o); SC.camera = o
    return o

def world(col=(0.012, 0.016, 0.024), strength=1.0):
    w = bpy.data.worlds.new("W"); SC.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (*col, 1); bg.inputs[1].default_value = strength

LIGHTS = []
def light(kind, loc, energy, color=(1, 1, 1), size=10, rot=None, target=None):
    ld = bpy.data.lights.new(f"L{len(LIGHTS)}", kind); ld.energy = energy; ld.color = color
    if kind == "AREA":
        ld.size = size
    if kind == "SUN":
        ld.angle = math.radians(3)
    o = bpy.data.objects.new(ld.name, ld); COLL.objects.link(o); o.location = loc
    if target:
        look(o, loc, target)
    elif rot:
        o.rotation_euler = rot
    LIGHTS.append(o)
    return o

def setup_cycles(samples, w, h):
    SC.render.engine = "CYCLES"; SC.cycles.device = "CPU"
    SC.cycles.samples = samples; SC.cycles.use_denoising = True
    SC.cycles.max_bounces = 6; SC.cycles.transmission_bounces = 6
    SC.cycles.glossy_bounces = 3; SC.cycles.diffuse_bounces = 3
    SC.cycles.caustics_reflective = False; SC.cycles.caustics_refractive = False
    SC.cycles.use_adaptive_sampling = True
    SC.render.resolution_x = w; SC.render.resolution_y = h; SC.render.film_transparent = False
    pct = int(os.environ.get("PZ_PCT", "100"))
    SC.render.resolution_percentage = pct
    if pct < 100:
        SC.cycles.samples = 8
    SC.view_settings.view_transform = "AgX"
    try:
        SC.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass

def setup_workbench(w, h, transparent=True):
    SC.render.engine = "BLENDER_WORKBENCH"
    s = SC.display.shading
    s.light = "STUDIO"; s.color_type = "TEXTURE"
    s.show_cavity = True; s.cavity_type = "BOTH"; s.cavity_ridge_factor = 1.2; s.cavity_valley_factor = 1.4
    s.show_object_outline = True; s.object_outline_color = (0.02, 0.02, 0.03)
    s.show_shadows = True; s.shadow_intensity = 0.35
    SC.display.light_direction = (0.45, -0.55, 0.7)
    SC.render.resolution_x = w; SC.render.resolution_y = h
    SC.render.film_transparent = transparent
    SC.view_settings.view_transform = "Standard"
    for m in MATS.values():
        b = m.node_tree.nodes["Principled BSDF"]
        base = b.inputs["Base Color"].default_value
        if b.inputs["Emission Strength"].default_value > 0:
            m.diffuse_color = (*b.inputs["Emission Color"].default_value[:3], 1)
        else:
            m.diffuse_color = tuple(min(1.0, c * 2.4 + 0.035) for c in base[:3]) + (1,)

def render(shot, cam, meta=None):
    from bpy_extras.object_utils import world_to_camera_view
    SC.render.filepath = os.path.join(OUT, shot + ".png")
    bpy.ops.render.render(write_still=True)
    bpy.context.view_layer.update()
    W_, H_ = SC.render.resolution_x, SC.render.resolution_y
    pts = {}
    for k, v in ANCHORS.items():
        c = world_to_camera_view(SC, cam, Vector(v))
        pts[k] = [c.x * W_, (1 - c.y) * H_, c.z]
    info = dict(shot=shot, res=[W_, H_], cam_loc=list(cam.location), anchors=pts,
                ortho_scale=cam.data.ortho_scale if cam.data.type == "ORTHO" else None)
    info.update(meta or {})
    with open(os.path.join(OUT, shot + ".json"), "w") as f:
        json.dump(info, f, indent=1)
    print("RENDERED", shot)

def set_emit(name, hexcol, strength=None):
    m = MATS[name]; b = m.node_tree.nodes["Principled BSDF"]
    rgb = hexrgb(hexcol)
    b.inputs["Emission Color"].default_value = (*rgb, 1); m.diffuse_color = (*rgb, 1)
    if strength is not None:
        b.inputs["Emission Strength"].default_value = strength

# ------------------------------------------------------------------ shots
ELEV_SCALE = 160  # studs across 2400 px -> 15 px/stud, shared by all elevations

def run():
    if MODE in ("facility", "cutaway"):
        build_facility()
    elif MODE == "kit":
        build_kit()
    elif MODE == "family":
        build_family_scene()
    elif MODE == "pod":
        build_pod_scene(SHOTS[0].split("_")[1] if "_" in SHOTS[0] else "closed")

    for shot in SHOTS:
        for o in list(LIGHTS):
            bpy.data.objects.remove(o)
        LIGHTS.clear()
        if shot == "ext_hero":
            setup_cycles(28, 1920, 1080); world((0.02, 0.032, 0.05), 1.6)
            cam = camera("cam", lens=24); look(cam, (-70, -62, 19), (4, 44, 12))
            light("SUN", (0, 0, 100), 2.6, (0.8, 0.88, 1.0), rot=(math.radians(58), 0, math.radians(-40)))
            light("AREA", (-90, -40, 50), 220000, (0.55, 0.75, 1.0), size=80, target=(0, 40, 10))
            light("AREA", (60, 160, 60), 250000, (0.2, 0.75, 1.0), size=80, target=(0, 60, 20))
            light("AREA", (10, -45, 3), 9000, (1.0, 0.55, 0.25), size=20, target=(0, 0, 8))
            render(shot, cam)
        elif shot in ("elev_front", "elev_rear", "elev_left", "elev_right"):
            setup_workbench(2400, 1000)
            cam = camera("cam", ortho=ELEV_SCALE)
            cz = 22
            pos = {"elev_front": ((0, -400, cz), (0, 0, cz)), "elev_rear": ((0, 520, cz), (0, 120, cz)),
                   "elev_left": ((-440, 60, cz), (0, 60, cz)), "elev_right": ((440, 60, cz), (0, 60, cz))}[shot]
            look(cam, *pos)
            render(shot, cam, dict(px_per_stud=2400 / ELEV_SCALE, center_z=cz))
        elif shot == "roof_plan":
            setup_workbench(1500, 2000)
            bpy.data.objects["ground"].hide_render = True
            cam = camera("cam", ortho=150)
            cam.location = (0, 60, 300); cam.rotation_euler = (0, 0, 0)
            render(shot, cam, dict(px_per_stud=2000 / 150, center=[0, 60]))
            bpy.data.objects["ground"].hide_render = False
        elif shot == "section_chamber":
            setup_workbench(2400, 1200)
            cam = camera("cam", ortho=110); cam.data.clip_start = 0.01
            cam.location = (0, 61, 20); cam.rotation_euler = (math.radians(90), 0, 0)
            render(shot, cam, dict(px_per_stud=2400 / 110, center=[0, 20], cut_y=61))
        elif shot == "int_chamber":
            setup_cycles(36, 1920, 1080); world((0.004, 0.006, 0.01), 1.0)
            for nm in ("ground",):
                if nm in bpy.data.objects:
                    pass
            cam = camera("cam", lens=20); look(cam, (-7.5, 27.5, 6.5), (1.5, 100, 9.5))
            for y in (40, 64, 88):
                light("AREA", (0, y, 28), 9000, (0.55, 0.85, 1.0), size=14, rot=(0, 0, 0))
            light("AREA", (0, 100, 12), 3000, (1.0, 0.55, 0.25), size=10, target=(0, 104, 6))
            render(shot, cam)
        elif shot.startswith("light_"):
            state = shot.split("_")[1]
            setup_cycles(16, 960, 540); world((0.004, 0.006, 0.01), 1.0)
            cam = camera("cam", lens=20); look(cam, (-7.5, 27.5, 6.5), (1.5, 100, 9.5))
            cols = {"normal": ("#22D3EE", 10, (0.55, 0.85, 1.0), 9000),
                    "wake": ("#FFB020", 12, (1.0, 0.75, 0.4), 7000),
                    "lockdown": ("#E5383B", 12, (1.0, 0.25, 0.2), 4000),
                    "offline": ("#1E88E5", 1.2, (0.4, 0.5, 0.7), 600)}[state]
            set_emit("cyan_emit", cols[0], cols[1]); set_emit("cyan_soft", cols[0], cols[1] / 4)
            if state == "offline":
                set_emit("amber_emit", "#FFB020", 0.5); set_emit("orange_emit", "#E8731A", 0.5)
            for y in (40, 64, 88):
                light("AREA", (0, y, 28), cols[3], cols[2], size=14, rot=(0, 0, 0))
            render(shot, cam)
            set_emit("cyan_emit", "#22D3EE", 10); set_emit("cyan_soft", "#22D3EE", 2.5)
            set_emit("amber_emit", "#FFB020", 8); set_emit("orange_emit", "#E8731A", 6)
        elif shot == "cutaway_axo":
            setup_cycles(24, 2000, 1400); world((0.02, 0.025, 0.035), 1.0)
            cam = camera("cam", ortho=175); look(cam, (180, -150, 190), (0, 60, 0))
            light("SUN", (0, 0, 100), 3.0, (1.0, 0.97, 0.92), rot=(math.radians(35), 0, math.radians(30)))
            light("AREA", (0, 60, 80), 40000, (0.7, 0.85, 1.0), size=120, rot=(0, 0, 0))
            render(shot, cam)
        elif shot == "plan_cut":
            setup_workbench(1500, 2000)
            cam = camera("cam", ortho=150); cam.location = (0, 60, 300); cam.rotation_euler = (0, 0, 0)
            render(shot, cam, dict(px_per_stud=2000 / 150, center=[0, 60]))
        elif shot.startswith("pod_"):
            # pod_<state>_<view>
            _, state, view = shot.split("_")
            bpy.data.objects["pod_ground"].hide_render = (view != "hero")
            bpy.data.objects["SCALEREF"].hide_render = (view in ("right", "plancut"))
            if view == "hero":
                setup_cycles(32, 1200, 1200); world((0.01, 0.014, 0.022), 1.0)
                cam = camera("cam", lens=60); look(cam, (-24, -31, 13), (2.2, 0, 6.6))
                light("AREA", (-12, -16, 22), 3500, (0.75, 0.88, 1.0), size=10, target=(0, 0, 6))
                light("AREA", (14, 8, 10), 1800, (1.0, 0.6, 0.3), size=8, target=(0, 0, 6))
                render(shot, cam)
            else:
                setup_workbench(1400, 1400)
                cam = camera("cam", ortho=22 if view != "top" else 22)
                cz = 7.5
                v = {"front": ((0, -100, cz), (0, 0, cz)), "rear": ((0, 100, cz), (0, 0, cz)),
                     "left": ((-100, 0, cz), (0, 0, cz)), "right": ((100, 0, cz), (0, 0, cz))}
                XC = 2.0
                if view == "top":
                    cam.location = (XC, 0, 100); cam.rotation_euler = (0, 0, 0)
                elif view == "plancut":
                    cam.data.clip_start = 0.001; cam.location = (XC, 0, 7.0); cam.rotation_euler = (0, 0, 0)
                elif view == "section":
                    cam.data.clip_start = 0.001; cam.location = (XC, 0.0, cz); cam.rotation_euler = (math.radians(90), 0, 0)
                else:
                    loc, tgt = v[view]
                    xs = XC if view in ("front", "rear") else 0
                    look(cam, (loc[0] + xs, loc[1], loc[2]), (tgt[0] + xs, tgt[1], tgt[2]))
                render(shot, cam, dict(px_per_stud=1400 / 22))
        elif shot == "family_ortho":
            bpy.data.objects["fam_ground"].hide_render = True
            setup_workbench(2800, 1100)
            cam = camera("cam", ortho=38); cam.location = (3, -100, 7.2); cam.rotation_euler = (math.radians(90), 0, 0)
            render(shot, cam, dict(px_per_stud=2800 / 38.0, center=[3, 7.2]))
            bpy.data.objects["fam_ground"].hide_render = False
        elif shot == "family_hero":
            setup_cycles(40, 1920, 1080); world((0.012, 0.016, 0.026), 1.0)
            cam = camera("cam", lens=40); look(cam, (-1, -42, 9), (2.5, 0, 4.6))
            light("AREA", (-14, -20, 18), 6000, (0.8, 0.9, 1.0), size=14, target=(0, 0, 4))
            light("AREA", (16, -12, 8), 2500, (1.0, 0.6, 0.3), size=10, target=(0, 0, 4))
            light("AREA", (0, 18, 14), 5000, (0.3, 0.8, 1.0), size=16, target=(0, 0, 5))
            render(shot, cam)
        elif shot == "kit_axo":
            setup_workbench(2600, 1500)
            cam = camera("cam", ortho=112); look(cam, (40 + 160, 28 - 190, 150), (40, 28, 2))
            render(shot, cam)

if __name__ == "__main__":
    run()
    print("DONE", MODE)
