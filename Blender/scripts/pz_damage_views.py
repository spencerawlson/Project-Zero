"""Render a model from three fixed views for before/after damage scoring (read-only on the source file).

blender -b --factory-startup -P pz_damage_views.py -- <model.glb> <out_prefix>

The model is normalised exactly like pz_vehicle_prep.py does it (length along X, centred, resting on Z = 0), then
scaled to 10 units long, so an original and its prepared copy render with identical framing. Views: side (-Y),
three-quarter front-left, top. Eevee, transparent background, 640x420. Writes <out_prefix>_<view>.png.
Score the pair with PDF/src/pz_damage_score.py."""
import bpy, sys, math
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:]
GLB, PREFIX = a[0], a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
for o in list(bpy.context.scene.objects):
    if o.type == "MESH" and o.name.startswith("Icosphere") and o.parent is None:
        bpy.data.objects.remove(o)
    elif o.type == "ARMATURE":
        if o.animation_data:
            o.animation_data.action = None
        o.data.pose_position = "REST"
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
root = bpy.data.objects.new("ROOT", None); bpy.context.scene.collection.objects.link(root)
for o in bpy.context.scene.objects:
    if o.parent is None and o is not root:
        o.parent = root
bpy.context.view_layer.update()

def bounds():
    dg = bpy.context.evaluated_depsgraph_get(); pts = []
    for o in meshes:
        ev = o.evaluated_get(dg); me = ev.to_mesh()
        pts += [ev.matrix_world @ v.co for v in me.vertices]; ev.to_mesh_clear()
    return Vector([min(p[i] for p in pts) for i in range(3)]), Vector([max(p[i] for p in pts) for i in range(3)])

mn, mx = bounds()
if (mx - mn).y > (mx - mn).x:
    root.rotation_euler = (0, 0, math.pi / 2); bpy.context.view_layer.update(); mn, mx = bounds()
s = 10.0 / (mx - mn).x
root.scale = (s, s, s); bpy.context.view_layer.update(); mn, mx = bounds()
root.location -= Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z)); bpy.context.view_layer.update(); mn, mx = bounds()
size = mx - mn; c = (mn + mx) / 2

sc = bpy.context.scene
engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in engines else "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = 640, 420
sc.render.film_transparent = True
sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.6, 0.65, 0.72, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sun.data.energy = 3.0
sun.rotation_euler = (math.radians(50), 0, math.radians(30)); sc.collection.objects.link(sun)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = "ORTHO"
for name, d in (("side", Vector((0, -1, 0.12))), ("front34", Vector((-1, -0.8, 0.45))), ("top", Vector((0.001, -0.001, 1)))):
    d = d.normalized()
    cam.location = c + d * 40
    cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.ortho_scale = max(size.x, size.y, size.z) * 1.15
    sc.render.filepath = f"{PREFIX}_{name}.png"
    bpy.ops.render.render(write_still=True)
print("VIEWS_DONE", PREFIX)
