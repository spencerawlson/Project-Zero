"""Fast triage thumbnail of a user GLB (read-only): Workbench texture, three-quarter, 900x700.
blender -b --factory-startup -P pz_thumb.py -- <glb> <out_png>"""
import bpy, sys, os, math
from mathutils import Vector
a = sys.argv[sys.argv.index("--") + 1:]
GLB, OUT = a[0], a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
for o in bpy.context.scene.objects:
    if o.type == "ARMATURE":
        if o.animation_data:
            o.animation_data.action = None
        o.data.pose_position = "REST"
    if o.type == "MESH" and o.name.startswith("Icosphere") and o.parent is None:
        o.hide_render = True
bpy.context.view_layer.update()
pts = [o.matrix_world @ Vector(c) for o in objs if not o.hide_render for c in o.bound_box]
mn = Vector([min(p[i] for p in pts) for i in range(3)]); mx = Vector([max(p[i] for p in pts) for i in range(3)])
c = (mn + mx) / 2; s = (mx - mn).length
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading; sh.light = "STUDIO"; sh.color_type = "TEXTURE"; sh.show_cavity = True
sc.render.resolution_x, sc.render.resolution_y = 900, 700
sc.render.film_transparent = False
w = bpy.data.worlds.new("w"); sc.world = w; w.color = (0.02, 0.03, 0.05)
cam = bpy.data.cameras.new("c"); cam.type = "ORTHO"; cam.ortho_scale = s * 1.05
co = bpy.data.objects.new("c", cam); sc.collection.objects.link(co); sc.camera = co
d = Vector((-0.8, -1.0, 0.55)).normalized(); co.location = c + d * s * 3
co.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
tris = sum(len(o.data.polygons) for o in objs)
print("THUMB_DONE", os.path.basename(GLB), "tris", tris, "anims", len(bpy.data.actions))
