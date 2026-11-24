"""Prepare a supplied room module with stasis pods (the owner's Robot Containment Chamber) for Roblox.

blender -b --factory-startup -P pz_room_prep.py -- <in.glb> <out.glb> <yaw_deg> <length_studs> <room_pieces> <tris_per_piece> <report.json>

1. Import (the source is never modified), join, rotate by <yaw_deg> about Z so the long side runs along X
   (pz_room_survey.py finds it), centre on the origin, floor at Z = 0, scale to <length_studs>.
2. Pods: the glass of each pod is a cylinder textured pale blue. Pale-blue faces between 15 % and 65 % of the
   room height are clustered along X; each roughly round cluster inside the room is one pod. Its centre and
   radius come from the cluster; every face of the glass shell (distance 0.55-1.2 radius, glass height band) is
   separated so it can be a see-through MeshPart in Roblox and fade out when the pod opens.
   The platform top is found by a ray straight down the pod axis.
3. Weld, decimate the room to <room_pieces> x <tris_per_piece> and each glass shell to at most 3000 triangles.
4. Bake (same method as pz_vehicle_prep.py bake mode): fresh UVs per piece, colour / tangent normal / roughness
   from the full-detail original at 1024 px, metalness written into the texture's blue channel.
5. Export GLB (+Y up). Objects: <base>_Room1..n (split along X) and <base>_GlassP1..P4 (pods ordered by X).
Report JSON: pods (centre x/y, radius, platform top z, glass z range, interior clearance check), sizes, triangles.
All dimensions are studs and are design choices: <length_studs> is set so the pods hold the largest robot."""
import bpy, bmesh, sys, os, json, math
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT, YAW, LENGTH, ROOM_PIECES, PER, REPORT = a[0], a[1], float(a[2]), float(a[3]), int(a[4]), int(a[5]), a[6]
GLASS_TRIS = 3000
BAKE_RES = 1024
base = os.path.splitext(os.path.basename(OUT))[0]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
bpy.ops.object.select_all(action="DESELECT")
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
ob = bpy.context.view_layer.objects.active
ob.parent = None
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = ob.data
me.transform(Matrix.Rotation(math.radians(YAW), 4, "Z"))
n = len(me.vertices)
co = np.empty(n * 3, np.float32); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
mn, mx = co.min(0), co.max(0)
f = LENGTH / (mx[0] - mn[0])
me.transform(Matrix.Scale(f, 4) @ Matrix.Translation(-Vector(((mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, mn[2]))))
me.update()
co = np.empty(n * 3, np.float32); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
size = co.max(0) - co.min(0)
H = float(size[2])
src_tris = len(me.polygons)
print("ROOM size", np.round(size, 2), "scale", round(f, 3), "tris", src_tris, flush=True)

# ---- pods: pale-blue glass faces ------------------------------------------------------------------------
nl = len(me.loops)
uv = np.empty(nl * 2, np.float32); me.uv_layers.active.data.foreach_get("uv", uv); uv = uv.reshape(-1, 2)
lv = np.empty(nl, np.int32); me.loops.foreach_get("vertex_index", lv)
ls = np.empty(len(me.polygons), np.int32); me.polygons.foreach_get("loop_start", ls)
lt = np.empty(len(me.polygons), np.int32); me.polygons.foreach_get("loop_total", lt)
assert (lt == 3).all(), "expected a triangulated mesh"
mat = me.materials[0]
tex = next(nd.image for nd in mat.node_tree.nodes if nd.type == "TEX_IMAGE" and nd.outputs["Color"].links
           and any(l.to_socket.name == "Base Color" for l in nd.outputs["Color"].links))
W, Hh = tex.size
px = np.array(tex.pixels[:], np.float32).reshape(Hh, W, 4)
fuv = (uv[ls] + uv[ls + 1] + uv[ls + 2]) / 3
col = px[np.clip((fuv[:, 1] % 1) * Hh, 0, Hh - 1).astype(int), np.clip((fuv[:, 0] % 1) * W, 0, W - 1).astype(int), :3]
fc = (co[lv[ls]] + co[lv[ls + 1]] + co[lv[ls + 2]]) / 3
r, g, b = col[:, 0], col[:, 1], col[:, 2]
isglass = (b > r + 0.12) & (b > 0.45) & (g > r)
# mid-height band of the glass (well above platforms, below the pod caps) and away from the end-wall screens
band = isglass & (fc[:, 2] > 0.33 * H) & (fc[:, 2] < 0.55 * H) & (np.abs(fc[:, 0]) < 0.45 * size[0])
cand = np.where(band)[0]
# pods are peaks in where the glass faces sit along X (0.5-stud bins, smoothed); at most 8, at least 4 studs apart
hist, edges = np.histogram(fc[cand, 0], bins=np.arange(-size[0] / 2, size[0] / 2 + 0.5, 0.5))
sm = np.convolve(hist, np.ones(5) / 5, mode="same")
peaks = []
for i in np.argsort(-sm):
    x = (edges[i] + edges[i + 1]) / 2
    if sm[i] < 0.25 * sm.max() or len(peaks) >= 8:
        break
    if all(abs(x - p_) >= 4.0 for p_ in peaks):
        peaks.append(float(x))

def circle_fit(xy):
    """Kasa least-squares circle: returns cx, cy, r."""
    A = np.c_[2 * xy[:, 0], 2 * xy[:, 1], np.ones(len(xy))]
    bb = (xy ** 2).sum(1)
    sol, *_ = np.linalg.lstsq(A, bb, rcond=None)
    cx_, cy_ = sol[0], sol[1]
    return float(cx_), float(cy_), float(math.sqrt(max(1e-9, sol[2] + cx_ ** 2 + cy_ ** 2)))

def hough_ring(pts, seed, span=1.5, rmin=1.5, rmax=3.2, tol=0.12):
    """Best circle through pale-blue faces near `seed`: the (centre, radius) on a 0.1-stud grid with the most
    faces within `tol` of the ring. Robust to stray frame/screen faces, unlike a least-squares fit."""
    near = pts[np.hypot(pts[:, 0] - seed[0], pts[:, 1] - seed[1]) < span + rmax + 0.5]
    best = (0, None)
    for cxg in np.arange(seed[0] - span, seed[0] + span + 1e-6, 0.1):
        for cyg in np.arange(seed[1] - span, seed[1] + span + 1e-6, 0.1):
            d = np.hypot(near[:, 0] - cxg, near[:, 1] - cyg)
            hist_r, _ = np.histogram(d, bins=np.arange(rmin - tol, rmax + tol + 1e-6, 0.05))
            win = int(round(2 * tol / 0.05))
            votes = np.convolve(hist_r, np.ones(win, int), mode="valid")
            k = int(np.argmax(votes))
            if votes[k] > best[0]:
                best = (int(votes[k]), (float(cxg), float(cyg), float(rmin - tol + 0.05 * k + tol)))
    return best

# Seeds (studs, at this scale) measured on a horizontal cut through the pods at 42 % height, 2026-11-23;
# scaled with the model so they stay valid if LENGTH changes.
SEEDS = [(x * LENGTH / 49.5, -0.2 * LENGTH / 49.5) for x in (-13.7, -5.2, 4.45, 13.4)]
pts_band = fc[cand, :2].astype(np.float64)
pods = []
for seed in SEEDS:
    votes, fit = hough_ring(pts_band, seed)
    cx_, cy_, rad = fit
    ring = np.where(isglass & (np.abs(np.hypot(fc[:, 0] - cx_, fc[:, 1] - cy_) - rad) < 0.35))[0]
    if len(ring) < 100:
        print("SKIP seed", seed, "fit", np.round(fit, 2), "votes", votes, "ring faces", len(ring))
        continue
    z0, z1 = float(np.percentile(fc[ring, 2], 1)), float(np.percentile(fc[ring, 2], 99))
    pods.append(dict(cx=cx_, cy=cy_, r=rad, z0=z0, z1=z1, faces=int(len(ring)), votes=votes))
pods.sort(key=lambda q: q["cx"])
# The pods are identical: use the median depth (y) and radius for all, which removes single-pod fit outliers.
if len(pods) >= 3:
    cy_med = float(np.median([q["cy"] for q in pods])); r_med = float(np.median([q["r"] for q in pods]))
    for q in pods:
        q["fit_cy"], q["fit_r"] = q["cy"], q["r"]
        q["cy"], q["r"] = cy_med, r_med
print("PODS", json.dumps([{k: round(v, 2) if isinstance(v, float) else v for k, v in q.items()} for q in pods]), flush=True)
assert len(pods) >= 1, "no pods found"

# glass shell faces for each pod (any colour: frame clamps sit on the shell too)
pod_of_face = np.full(len(me.polygons), -1, np.int32)
for i, q in enumerate(pods):
    d = np.hypot(fc[:, 0] - q["cx"], fc[:, 1] - q["cy"])
    # only the glass itself (pale blue); frame clamps on the shell stay with the room
    sel = isglass & (d > q["r"] - 0.8) & (d < q["r"] + 0.7) & (fc[:, 2] > q["z0"] - 0.2) & (fc[:, 2] < q["z1"] + 0.2)
    pod_of_face[sel & (pod_of_face < 0)] = i

# platform top and interior clearance on the full-detail mesh (glass shell excluded)
bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
keep_idx = np.where(pod_of_face < 0)[0]
verts_np = co
tris_np = np.stack([lv[ls], lv[ls + 1], lv[ls + 2]], 1)
bvh_room = BVHTree.FromPolygons([Vector(v) for v in verts_np], [tuple(t) for t in tris_np[keep_idx]])
for q in pods:
    mid = Vector((q["cx"], q["cy"], (q["z0"] + q["z1"]) / 2))
    hit = bvh_room.ray_cast(mid, Vector((0, 0, -1)))
    q["platform_z"] = float(hit[0].z) if hit[0] else q["z0"]
    up = bvh_room.ray_cast(Vector((q["cx"], q["cy"], q["platform_z"] + 0.05)), Vector((0, 0, 1)))
    q["ceiling_z"] = float(up[0].z) if up[0] else q["z1"]
    # clearance: a 0.45 r cylinder from the platform to 7.5 studs above it must be free of room geometry
    blocked = 0
    for ang in range(0, 360, 30):
        for hz in (1.0, 3.0, 5.0, 7.0):
            o = Vector((q["cx"], q["cy"], q["platform_z"] + hz))
            dirv = Vector((math.cos(math.radians(ang)), math.sin(math.radians(ang)), 0))
            h = bvh_room.ray_cast(o, dirv, 0.45 * q["r"])
            blocked += h[0] is not None
    q["blocked_probe_rays"] = blocked
    q["clear_height"] = round(q["ceiling_z"] - q["platform_z"], 2)
bm.free()
print("PODS_MEASURED", json.dumps([{k: round(v, 2) if isinstance(v, float) else v for k, v in q.items()} for q in pods]), flush=True)
if "detect" in a[7:]:                               # quick check of pod detection only
    print("DETECT_ONLY_DONE", flush=True)
    sys.exit(0)

# ---- split: room vs glass shells, keep a full-detail reference for baking ---------------------------------
high = ob.copy(); high.data = me.copy(); high.name = "HIGH_REF"
bpy.context.scene.collection.objects.link(high)
glass_all = ob.copy(); glass_all.data = me.copy(); glass_all.name = "GLASS"
bpy.context.scene.collection.objects.link(glass_all)
room = ob

def delete_faces(obj, mask):
    """Delete the faces where mask is True (bmesh, no selection state involved)."""
    bm_ = bmesh.new(); bm_.from_mesh(obj.data); bm_.faces.ensure_lookup_table()
    bmesh.ops.delete(bm_, geom=[bm_.faces[i] for i in np.where(mask)[0]], context="FACES")
    bm_.to_mesh(obj.data); bm_.free(); obj.data.update()

delete_faces(room, pod_of_face >= 0)
delete_faces(glass_all, pod_of_face < 0)
print("SPLIT room faces", len(room.data.polygons), "glass faces", len(glass_all.data.polygons), flush=True)
assert len(room.data.polygons) > 0 and len(glass_all.data.polygons) > 0

def weld_and_decimate(o, target):
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles(threshold=LENGTH * 2e-5); bpy.ops.object.mode_set(mode="OBJECT")
    t0 = len(o.data.polygons)
    if t0 > target:
        m = o.modifiers.new("dec", "DECIMATE"); m.ratio = target / t0; m.use_collapse_triangulate = True
        bpy.ops.object.modifier_apply(modifier="dec")
    return t0, len(o.data.polygons)

print("ROOM_DECIMATE", weld_and_decimate(room, ROOM_PIECES * PER), flush=True)
print("GLASS_DECIMATE", weld_and_decimate(glass_all, GLASS_TRIS * len(pods)), flush=True)

# ---- one joined low mesh; material index = piece (room pieces by X, then one per pod) ----------------------
def metallic_of(obj):
    m = obj.data.materials[0]
    bsdf = next(nd for nd in m.node_tree.nodes if nd.type == "BSDF_PRINCIPLED")
    inp = bsdf.inputs["Metallic"]; node = inp.links[0].from_node if inp.links else None
    while node is not None and node.type != "TEX_IMAGE":
        ins = [i for i in node.inputs if i.links]
        node = ins[0].links[0].from_node if ins else None
    if node is None:
        return inp.default_value
    im = node.image.copy(); im.scale(64, 64)
    v = float(np.array(im.pixels[:]).reshape(-1, 4)[:, 2].mean()); bpy.data.images.remove(im)
    return v
metallic = metallic_of(high)

names = [f"Room{k + 1}" for k in range(ROOM_PIECES)] + [f"GlassP{i + 1}" for i in range(len(pods))]
for o in (room, glass_all):
    o.data.materials.clear()
bpy.ops.object.select_all(action="DESELECT"); room.select_set(True); glass_all.select_set(True)
bpy.context.view_layer.objects.active = room
GLASS_FLAG = "pz_is_glass"
for o, flag in ((room, 0), (glass_all, 1)):
    attr = o.data.attributes.new(GLASS_FLAG, "INT", "FACE")
    attr.data.foreach_set("value", [flag] * len(o.data.polygons))
bpy.ops.object.join()
low = bpy.context.view_layer.objects.active
low.name = "LOW"
while low.data.uv_layers:
    low.data.uv_layers.remove(low.data.uv_layers[0])
low.data.uv_layers.new(name="UVMap")
mats = []
for nm in names:
    m = bpy.data.materials.new(f"{base}_{nm}"); m.use_nodes = True
    nt = m.node_tree; bsdf = next(nd for nd in nt.nodes if nd.type == "BSDF_PRINCIPLED")
    ims = {}
    for kind, cs in (("color", "sRGB"), ("normal", "Non-Color"), ("rough", "Non-Color")):
        im = bpy.data.images.new(f"{base}_{nm}_{kind}", BAKE_RES, BAKE_RES, alpha=False)
        im.colorspace_settings.name = cs
        node = nt.nodes.new("ShaderNodeTexImage"); node.image = im; node.name = kind
        ims[kind] = node
    low.data.materials.append(m); mats.append((m, ims, bsdf))
flags = np.empty(len(low.data.polygons), np.int32); low.data.attributes[GLASS_FLAG].data.foreach_get("value", flags)
cen = np.empty(len(low.data.polygons) * 3, np.float32); low.data.polygons.foreach_get("center", cen); cen = cen.reshape(-1, 3)
room_idx = np.where(flags == 0)[0]
xs = np.sort(cen[room_idx, 0])
cuts = [xs[len(xs) * k // ROOM_PIECES] for k in range(1, ROOM_PIECES)]
midx = np.zeros(len(low.data.polygons), np.int32)
midx[room_idx] = np.searchsorted(np.array(cuts), cen[room_idx, 0], side="right")
gidx = np.where(flags == 1)[0]
pc = np.array([[q["cx"], q["cy"]] for q in pods])
nearest = np.argmin(((cen[gidx, None, :2] - pc[None, :, :]) ** 2).sum(-1), axis=1)
midx[gidx] = ROOM_PIECES + nearest
low.data.polygons.foreach_set("material_index", midx)
low.data.update()
bpy.ops.object.select_all(action="DESELECT"); low.select_set(True); bpy.context.view_layer.objects.active = low
bpy.context.tool_settings.mesh_select_mode = (False, False, True)
for k in range(len(names)):
    sel = (midx == k)
    low.data.polygons.foreach_set("select", sel)
    low.data.update()
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.003, scale_to_bounds=False)
    bpy.ops.object.mode_set(mode="OBJECT")

sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 4
bk = sc.render.bake
bk.use_selected_to_active = True; bk.cage_extrusion = 0.004 * LENGTH; bk.max_ray_distance = 0.03 * LENGTH; bk.margin = 8
bpy.ops.object.select_all(action="DESELECT"); high.select_set(True); low.select_set(True)
bpy.context.view_layer.objects.active = low
for kind, btype in (("color", "DIFFUSE"), ("normal", "NORMAL"), ("rough", "ROUGHNESS")):
    for m, ims, _ in mats:
        m.node_tree.nodes.active = ims[kind]
    if btype == "DIFFUSE":
        bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"})
    elif btype == "NORMAL":
        bpy.ops.object.bake(type="NORMAL", normal_space="TANGENT")
    else:
        bpy.ops.object.bake(type="ROUGHNESS")
    print("ROOM_BAKED", kind, flush=True)
for m, ims, bsdf in mats:
    nt = m.node_tree
    nt.links.new(ims["color"].outputs["Color"], bsdf.inputs["Base Color"])
    rim = ims["rough"].image
    pxr = np.array(rim.pixels[:], dtype=np.float32).reshape(-1, 4); pxr[:, 2] = metallic
    rim.pixels.foreach_set(pxr.ravel()); rim.update()
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(ims["rough"].outputs["Color"], sep.inputs["Color"])
    nt.links.new(sep.outputs["Green"], bsdf.inputs["Roughness"]); nt.links.new(sep.outputs["Blue"], bsdf.inputs["Metallic"])
    nm_ = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(ims["normal"].outputs["Color"], nm_.inputs["Color"]); nt.links.new(nm_.outputs["Normal"], bsdf.inputs["Normal"])
    for node in ims.values():
        node.image.pack()
bpy.data.objects.remove(high)
bpy.ops.object.select_all(action="DESELECT"); low.select_set(True); bpy.context.view_layer.objects.active = low
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.mesh.separate(type="MATERIAL"); bpy.ops.object.mode_set(mode="OBJECT")
parts = {}
for o in [o for o in bpy.context.scene.objects if o.type == "MESH"]:
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.material_slot_remove_unused()
    nm = o.data.materials[0].name.replace(base + "_", "")
    o.name = f"{base}_{nm}"; o.data.name = o.name
    if GLASS_FLAG in o.data.attributes:
        o.data.attributes.remove(o.data.attributes[GLASS_FLAG])
    parts[o.name] = len(o.data.polygons)
print("ROOM_PARTS", json.dumps(parts), flush=True)
assert max(parts.values()) <= 20000, "a piece is over Roblox's 20,000-triangle limit"
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_yup=True, export_image_format="JPEG",
                          export_jpeg_quality=92, export_materials="EXPORT")
rep = dict(source=SRC, yaw=YAW, length=LENGTH, scale=round(f, 4), size=[round(float(v), 2) for v in size],
           source_triangles=src_tris, parts=parts, metallic=round(metallic, 3),
           pods=[{k: (round(v, 3) if isinstance(v, float) else v) for k, v in q.items()} for q in pods],
           frame="Blender: X = length, Y = depth, Z = up, origin at floor centre; exported +Y up")
json.dump(rep, open(REPORT, "w"), indent=1, default=float)  # numpy float32 values
print("ROOM_DONE", OUT, round(os.path.getsize(OUT) / 1e6, 2), "MB", flush=True)
