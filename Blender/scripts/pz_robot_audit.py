"""Audit renders of the canonical robots (read-only use of the user's GLBs).
blender -b --factory-startup -P pz_robot_audit.py -- <outdir>
Imports Cypher, Sentinel, Patch; normalises each to stand on Z=0 (no other changes);
renders a lineup + front/side/back/three-quarter per robot with Workbench (texture colours)."""
import bpy, sys, os, math, json
from mathutils import Vector
OUT = sys.argv[sys.argv.index("--") + 1:][0]
os.makedirs(OUT, exist_ok=True)
SRC = r"D:\Project Zero_Roblox"
import os as _os
_extra = _os.environ.get("PZ_BOTS")
BOTS = [tuple(x.split("=")) for x in _extra.split(";")] if _extra else [("Cypher", "Rigged_Cypher.glb"), ("Sentinel", "Rigged_Sentinel.glb"), ("Patch", "Patch_LowPoly.glb")]
bpy.ops.wm.read_factory_settings(use_empty=True)
SC = bpy.context.scene
info = {}
roots = {}
for i, (name, f) in enumerate(BOTS):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(SRC, f))
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        if o.type == "ARMATURE":
            if o.animation_data:
                o.animation_data.action = None      # no animation frame
            o.data.pose_position = "REST"           # bind/rest pose
    bpy.context.view_layer.update()
    strays = [o for o in new if o.type == "MESH" and o.name.startswith("Icosphere") and o.parent is None]
    for o in strays:                                # stray helper sphere shipped inside the GLB
        o.hide_render = True
    meshes = [o for o in new if o.type == "MESH" and o not in strays]
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in meshes:
        ev = o.evaluated_get(dg); me = ev.to_mesh()
        pts += [ev.matrix_world @ v.co for v in me.vertices]
        ev.to_mesh_clear()
    mn = Vector([min(p[k] for p in pts) for k in range(3)]); mx = Vector([max(p[k] for p in pts) for k in range(3)])
    top = [o for o in new if o.parent is None]
    piv = bpy.data.objects.new(name, None); SC.collection.objects.link(piv)
    for o in top:
        o.parent = piv
    piv.location = (-(mn.x + mx.x) / 2, -(mn.y + mx.y) / 2, -mn.z)
    roots[name] = piv
    info[name] = dict(file=f, size=[round(v, 3) for v in (mx - mn)], tris=sum(len(m.data.polygons) for m in meshes),
                      stray_objects=[o.name for o in strays])
s = SC.display.shading
SC.render.engine = "BLENDER_WORKBENCH"
s.light = "STUDIO"; s.color_type = "TEXTURE"; s.show_cavity = True; s.cavity_type = "BOTH"
s.show_object_outline = True; s.object_outline_color = (0.02, 0.02, 0.03)
SC.render.film_transparent = True; SC.view_settings.view_transform = "Standard"

def cam_ortho(scale, loc, rot, w, h):
    c = bpy.data.cameras.new("c"); c.type = "ORTHO"; c.ortho_scale = scale
    o = bpy.data.objects.new("c", c); SC.collection.objects.link(o); o.location = loc; o.rotation_euler = rot
    SC.camera = o; SC.render.resolution_x = w; SC.render.resolution_y = h
    return o

def shoot(path):
    SC.render.filepath = path; bpy.ops.render.render(write_still=True); print("RENDERED", os.path.basename(path))

# lineup at true imported scale, 1.4 apart
for i, name in enumerate(roots):
    roots[name].location.x += (i - (len(roots) - 1) / 2) * 1.4
cam_ortho(4.4, (0, -20, 1.0), (math.radians(90), 0, 0), 2400, 1400)
shoot(os.path.join(OUT, "robots_lineup_front.png"))
# per-robot turnarounds
for i, name in enumerate(roots):
    for other in roots.values():
        other.hide_render = True
        for ch in other.children_recursive:
            ch.hide_render = True
    r = roots[name]; r.hide_render = False
    for ch in r.children_recursive:
        ch.hide_render = ch.name.startswith("Icosphere")
    x = (i - (len(roots) - 1) / 2) * 1.4
    h = info[name]["size"][2]
    for view, ang in (("front", 0), ("side", 90), ("back", 180), ("q34", 35)):
        a = math.radians(ang)
        d = Vector((math.sin(a), -math.cos(a), 0.0))
        loc = Vector((x, 0, h / 2)) + d * 20
        rot = (math.radians(90), 0, a)
        cam_ortho(h * 1.15, loc, rot, 1000, 1150)
        shoot(os.path.join(OUT, f"{name}_{view}.png"))
_p = os.path.join(OUT, "robots_info.json")
_old = json.load(open(_p)) if os.path.exists(_p) else {}
_old.update(info)
json.dump(_old, open(_p, "w"), indent=1)          # merge, never overwrite other robots
print("INFO", json.dumps(info))
