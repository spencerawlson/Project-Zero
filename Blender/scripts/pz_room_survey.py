"""Survey a supplied room/interior model before preparing it for Roblox (read-only on the source).

blender -b --factory-startup -P pz_room_survey.py -- <model.glb> <out_prefix>

- Finds the yaw that makes the footprint's bounding rectangle smallest (rooms are often exported at an angle)
  and reports the aligned size, triangle count and textures.
- Writes <out_prefix>_survey.json and orthographic renders of the aligned model: top, and the four sides
  (side_south = looking north from -Y, etc.), each with a 1-unit grid scale in the json so sizes can be read.
- Height scan: a grid of downward rays gives the floor height map; for each column the clear height between the
  first upward hit above the floor and the floor ("headroom") is recorded on a coarse grid, which locates pods
  and their interior clearance."""
import bpy, bmesh, sys, math, json
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index("--") + 1:]
SRC, PREFIX = a[0], a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
for o in list(bpy.context.scene.objects):
    if o.type != "MESH":
        o.select_set(False)
bpy.ops.object.select_all(action="DESELECT")
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = obj.data
pts = [v.co.copy() for v in me.vertices]

def rect(angle):
    c, s = math.cos(angle), math.sin(angle)
    xs = [p.x * c - p.y * s for p in pts]; ys = [p.x * s + p.y * c for p in pts]
    return (max(xs) - min(xs)) * (max(ys) - min(ys)), max(xs) - min(xs), max(ys) - min(ys)

best = min((rect(math.radians(d / 2)) + (d / 2,) for d in range(0, 180)), key=lambda r: r[0])
yaw = best[3]
# make the long side run along X
if best[2] > best[1]:
    yaw += 90
obj.matrix_world = Matrix.Rotation(math.radians(yaw), 4, "Z") @ obj.matrix_world
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
pts = [v.co.copy() for v in me.vertices]
mn = Vector([min(p[i] for p in pts) for i in range(3)]); mx = Vector([max(p[i] for p in pts) for i in range(3)])
for v in me.vertices:
    v.co -= Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z))
me.update()
size = mx - mn
tris = sum(len(p.vertices) - 2 for p in me.polygons)
imgs = [(im.name, list(im.size)) for im in bpy.data.images]

# height scan on a grid (units of the model)
bm = bmesh.new(); bm.from_mesh(me); bvh = BVHTree.FromBMesh(bm)
N = 48
cells = []
for i in range(N):
    for j in range(int(N * size.y / size.x) + 1):
        x = -size.x / 2 + (i + 0.5) * size.x / N
        y = -size.y / 2 + (j + 0.5) * size.x / N
        if y > size.y / 2:
            continue
        # floor: lowest upward-facing surface reached from below
        hit = bvh.ray_cast(Vector((x, y, -0.01)), Vector((0, 0, 1)))
        if hit[0] is None:
            continue
        floor = hit[0].z
        up = bvh.ray_cast(Vector((x, y, floor + 0.02 * size.z)), Vector((0, 0, 1)))
        head = (up[0].z - floor) if up[0] is not None else None
        cells.append([round(x, 3), round(y, 3), round(floor, 3), None if head is None else round(head, 3)])

out = {"source": SRC, "yaw_applied_deg": yaw, "size": [round(size.x, 3), round(size.y, 3), round(size.z, 3)],
       "triangles": tris, "vertices": len(me.vertices), "images": imgs, "scan_cells": cells, "scan_N": N}
json.dump(out, open(PREFIX + "_survey.json", "w"), indent=1)

sc = bpy.context.scene
engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in engines else "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = 1200, 700
sc.render.film_transparent = True
sc.view_settings.view_transform = "Standard"
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.7, 0.72, 0.76, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 1.2
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sun.data.energy = 2.5
sun.rotation_euler = (math.radians(40), 0, math.radians(30)); sc.collection.objects.link(sun)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = "ORTHO"
c = Vector((0, 0, size.z / 2))
views = {"top": Vector((0.0001, 0, 1)), "side_south": Vector((0, -1, 0)), "side_north": Vector((0, 1, 0)),
         "end_west": Vector((-1, 0, 0)), "end_east": Vector((1, 0, 0)), "q34_south": Vector((-0.8, -1, 0.6))}
for name, d in views.items():
    d = d.normalized(); cam.location = c + d * (3 * max(size))
    cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.ortho_scale = max(size.x, size.y if name in ("top",) else size.z, size.y) * 1.08
    sc.render.filepath = f"{PREFIX}_{name}.png"
    bpy.ops.render.render(write_still=True)
print("SURVEY", json.dumps({k: out[k] for k in ("yaw_applied_deg", "size", "triangles", "vertices", "images")}))
