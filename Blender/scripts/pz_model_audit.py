"""Render a USER-SUPPLIED model (read-only) for its sheet: hero (Cycles) + front/rear/left/right/top (Workbench texture).
blender -b --factory-startup -P pz_model_audit.py -- <glb> <outdir> <target_size> <size_axis: height|length> [front_axis: -Y|+Y|-X|+X]
Model is uniformly scaled to the target (studs, DESIGN ASSUMPTION), rest pose, stray helpers hidden. Files are never modified.
Writes json beside each render in the same format as pz_asset_lib (res, ortho, center, view, bbox_obj)."""
import bpy, sys, os, math, json
from mathutils import Vector
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
a = sys.argv[sys.argv.index("--") + 1:]
GLB, OUT, TARGET, AXIS = a[0], a[1], float(a[2]), a[3]
FRONT = a[4] if len(a) > 4 else "-Y"
sys.argv = [sys.argv[0], "--", "asset", OUT]
import pz_build_stasis as K
os.makedirs(OUT, exist_ok=True)

before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=GLB)
new = [o for o in bpy.data.objects if o not in before]
stray = []
for o in new:
    if o.type == "ARMATURE":
        if o.animation_data:
            o.animation_data.action = None
        o.data.pose_position = "REST"
    if o.type == "MESH" and o.name.startswith("Icosphere") and o.parent is None:
        o.hide_render = True; stray.append(o.name)
# render-time only: force opaque materials (Meshy textures can carry alpha → empty Workbench views)
for o in new:
    for slot in getattr(o, "material_slots", []):
        m = slot.material
        if not m or not m.use_nodes:
            continue
        for n in m.node_tree.nodes:
            if n.type == "BSDF_PRINCIPLED":
                for l in list(n.inputs["Alpha"].links):
                    m.node_tree.links.remove(l)
                n.inputs["Alpha"].default_value = 1.0
        try:
            m.blend_method = "OPAQUE"
        except Exception:
            pass
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
pts = []
for o in new:
    if o.type == "MESH" and not o.hide_render:
        ev = o.evaluated_get(dg); me = ev.to_mesh()
        mw = ev.matrix_world
        step = max(1, len(me.vertices) // 200000)
        pts += [mw @ me.vertices[i].co for i in range(0, len(me.vertices), step)]
        ev.to_mesh_clear()
mn = Vector([min(p[i] for p in pts) for i in range(3)]); mx = Vector([max(p[i] for p in pts) for i in range(3)])
size = mx - mn
cur = size.z if AXIS == "height" else max(size.x, size.y)
s = TARGET / cur
piv = bpy.data.objects.new("ROOT", None); K.COLL.objects.link(piv)
for o in new:
    if o.parent is None:
        o.parent = piv
rz = {"-Y": 0, "+Y": math.pi, "-X": math.pi / 2, "+X": -math.pi / 2}[FRONT]
piv.rotation_euler = (0, 0, rz); piv.scale = (s, s, s)
bpy.context.view_layer.update()
c0 = (mn + mx) / 2
off = Vector((c0.x, c0.y, mn.z)) * s
off.rotate(piv.rotation_euler)
piv.location = -off
bpy.context.view_layer.update()
# final bbox after transform
pts2 = [piv.matrix_world @ (p) for p in pts]
mn2 = Vector([min(p[i] for p in pts2) for i in range(3)]); mx2 = Vector([max(p[i] for p in pts2) for i in range(3)])
c = (mn2 + mx2) / 2; sz = mx2 - mn2
base = dict(bbox=[list(mn2), list(mx2)], bbox_obj=[list(mn2), list(mx2)], notes={}, cut=0, cat="USER",
            source=os.path.basename(GLB), scale_factor=s, stray=stray, tris=sum(len(o.data.polygons) for o in new if o.type == "MESH"))

def render(shot, cam, extra):
    meta = dict(base, view=shot); meta.update(extra)
    K.render(shot, cam, meta)

# hero  (memory: cap textures at 2048 px for rendering only)
K.setup_cycles(16, 1440, 900); K.world((0.016, 0.024, 0.04), 1.4)
K.SC.render.use_simplify = True
K.SC.cycles.texture_limit_render = "2048"
R = max(sz.length / 2, 3)
cam = K.camera("cam", lens=40)
d = Vector((-0.85, -1.0, 0.45)).normalized()
K.look(cam, c + d * max(R * 2.3, sz.z * 2.6), c)
K.light("SUN", (0, 0, 100), 1.6, (0.9, 0.93, 1.0), rot=(math.radians(55), 0, math.radians(-38)))
R = max(R, sz.z * 1.1)
K.light("AREA", tuple(c + Vector((-R * 2, -R * 1.5, R * 1.8))), 200 * R * R, (0.8, 0.88, 1.0), size=R * 1.5, target=tuple(c))
K.light("AREA", tuple(c + Vector((R * 1.6, R * 2.0, R * 1.2))), 220 * R * R, (0.3, 0.8, 1.0), size=R * 1.5, target=tuple(c))
gnd = K.box("gnd", c.x - R * 4, c.x + R * 4, c.y - R * 4, c.y + R * 4, mn2.z - 0.05, mn2.z, K.M["ground"])
render("hero", cam, {})
gnd.hide_render = True
for o in list(K.LIGHTS):
    bpy.data.objects.remove(o)
K.LIGHTS.clear()
# orthos (Workbench texture colours)
for shot in ("front", "rear", "left", "right", "top"):
    if shot == "top":
        sc = max(sz.x, sz.y) * 1.12; K.setup_workbench(1200, 1200); K.SC.display.render_aa = "5"; K.SC.display.shading.cavity_type = "SCREEN"
        cam = K.camera("cam", ortho=sc); cam.location = (c.x, c.y, mx2.z + 50); cam.rotation_euler = (0, 0, 0)
        render(shot, cam, dict(ortho=sc, center=list(c), res=[1200, 1200]))
        continue
    horiz = sz.x if shot in ("front", "rear") else sz.y
    sc = max(horiz, sz.z * 2.0) * 1.14; K.setup_workbench(1400, 700); K.SC.display.render_aa = "5"; K.SC.display.shading.cavity_type = "SCREEN"
    cam = K.camera("cam", ortho=sc)
    dirs = {"front": (0, -1), "rear": (0, 1), "left": (-1, 0), "right": (1, 0)}[shot]
    D = max(sz.length, 10) * 3
    K.look(cam, Vector((c.x + dirs[0] * D, c.y + dirs[1] * D, c.z)), (c.x, c.y, c.z))
    render(shot, cam, dict(ortho=sc, center=list(c), res=[1400, 700]))
print("AUDIT_DONE", os.path.basename(GLB), "scale", round(s, 3), "size", [round(v, 2) for v in sz])
