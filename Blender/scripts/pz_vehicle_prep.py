"""Prepare a supplied (Meshy) vehicle model for Roblox and size it so robots fit inside.

blender -b --factory-startup -P pz_vehicle_prep.py -- <in.glb> <out.glb> <lengths> <tris_per_piece> <pieces> <report.json> [min_seats]

  lengths    comma list of candidate lengths in studs, e.g. 28,32,36,40 (longest horizontal side)
  min_seats  seats the vehicle must hold (default 1); the smallest candidate length that fits them is exported

1. Import (source file is never modified), join, rest on the ground, centre on the origin, length along X.
2. Decimate once to pieces * tris_per_piece triangles (scale-independent).
3. For each candidate length: crew-fit scan inside the hull shell for the largest robot (pz_asset_lib.CREW:
   4.4 wide, 7.5 tall), seated and standing, facing +X and -X; greedy non-overlapping seat layout.
4. Scale to the chosen length, split along X into <pieces> equal-triangle parts (each under Roblox's
   20,000-triangle limit), textures to 1024 px, export GLB (+Y up). Report JSON lists every length tried.
All dimensions are design assumptions in studs. Seats are chosen for one facing; which end is the front is set
by eye in Studio (the report keeps both facings)."""
import bpy, sys, os, json, math
from mathutils import Vector
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT, LENGTHS, PER, PIECES, REPORT = a[0], a[1], [float(v) for v in a[2].split(",")], int(a[3]), int(a[4]), a[5]
MIN_SEATS = int(a[6]) if len(a) > 6 else 1
# "nonormal": drop the normal map. The Titan Rover's baked normal map turned its whole SurfaceAppearance flat grey
# in Roblox (isolated map by map in Studio, 2026-11-23); colour + metalness + roughness alone render correctly.
NO_NORMAL = "nonormal" in a[7:]
CREW = dict(max_h=7.5, max_w=4.4, seat_w=4.8, seat_top=1.6, walk_h=8.0)   # mirrors pz_asset_lib.CREW
PITCH = 4.2                                                               # seat-to-seat spacing along the length

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
for o in list(bpy.context.scene.objects):        # importer bone-shape helpers are not part of the model
    if o.type == "MESH" and o.name.startswith("Icosphere") and o.parent is None:
        bpy.data.objects.remove(o)
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
for o in bpy.context.scene.objects:
    if o.type == "ARMATURE" and o.animation_data:
        o.animation_data.action = None
bpy.ops.object.select_all(action="DESELECT")
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
for o in meshes:
    for m in list(o.modifiers):
        if m.type == "ARMATURE":
            bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier=m.name)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
ob = bpy.context.view_layer.objects.active
ob.parent = None
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
src_tris = sum(len(p.vertices) - 2 for p in ob.data.polygons)

def bounds(o):
    vs = [o.matrix_world @ v.co for v in o.data.vertices]
    return Vector([min(v[i] for v in vs) for i in range(3)]), Vector([max(v[i] for v in vs) for i in range(3)])

mn, mx = bounds(ob)
if (mx - mn).y > (mx - mn).x:                     # length along X for a consistent scan / split
    ob.rotation_euler = (0, 0, math.pi / 2); bpy.ops.object.transform_apply(rotation=True)
mn, mx = bounds(ob)
ob.location = (-(mn.x + mx.x) / 2, -(mn.y + mx.y) / 2, -mn.z); bpy.ops.object.transform_apply(location=True)
mn, mx = bounds(ob)
L0 = mx.x - mn.x

# Weld coincident vertices first. Some Meshy exports are "triangle soup" (no shared vertices); collapse
# decimation then shrinks every triangle on its own and the hull shatters into shards (seen on the Titan Rover).
# UVs live on face corners in Blender, so welding positions keeps texture seams intact.
v_before = len(ob.data.vertices)
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.mesh.remove_doubles(threshold=max(1e-6, L0 * 2e-5))
bpy.ops.object.mode_set(mode="OBJECT")
print("PREP_WELD verts", v_before, "->", len(ob.data.vertices), "tris", src_tris)
mod = ob.modifiers.new("dec", "DECIMATE"); mod.ratio = min(1.0, PER * PIECES / max(1, src_tris)); mod.use_collapse_triangulate = True
bpy.ops.object.modifier_apply(modifier="dec")
dec_tris = sum(len(p.vertices) - 2 for p in ob.data.polygons)
print("PREP_DECIMATED", src_tris, "->", dec_tris)
VERTS = [v.co.copy() for v in ob.data.vertices]
POLYS = [tuple(p.vertices) for p in ob.data.polygons]

def scan(length):
    f = length / L0
    tree = BVHTree.FromPolygons([v * f for v in VERTS], POLYS)
    lo, hi = mn * f, mx * f
    def inside(p):
        n, o, d = 0, Vector(p), Vector((0, 0, 1))
        while n < 40:
            hit = tree.ray_cast(o, d)
            if hit[0] is None:
                break
            n += 1; o = hit[0] + d * 1e-3
        return n % 2 == 1
    def clear(b):
        x0, x1, y0, y1, z0, z1 = b
        v = [Vector((xx, yy, zz)) for zz in (z0, z1) for xx, yy in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
        fc = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        if tree.overlap(BVHTree.FromPolygons(v, fc)):
            return False
        return inside(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    def envelopes(kind, x, y, zf, face):
        sc = CREW["max_h"] / 7.0; hw = CREW["max_w"] / 2; zs = zf + CREW["seat_top"]
        if kind == "walk":
            return [(x - hw, x + hw, y - hw, y + hw, zf + 0.15, zf + CREW["max_h"] + 0.3)]
        out = []
        for (f0, f1, w, z0, z1) in ((-0.6, 1.9 * sc, hw, zs + 0.15, zs + 3.75 * sc + 0.1), (1.3, 1.95 * sc, 0.75 * sc, zf + 0.15, zs + 0.15)):
            xa, xb = (x + f0, x + f1) if face > 0 else (x - f1, x - f0)
            out.append((xa, xb, y - w, y + w, z0, z1))
        return out
    def floor_at(x, y):
        zmid = (lo.z + hi.z) / 2
        if not inside((x, y, zmid)):
            return None
        hit = tree.ray_cast(Vector((x, y, zmid)), Vector((0, 0, -1)))
        return None if hit[0] is None else hit[0].z + 0.3
    fits = dict(seat=[], walk=[])
    x = lo.x + 2.0
    while x < hi.x - 2.0:
        y = lo.y + 2.2
        while y < hi.y - 2.2:
            zf = floor_at(x, y)
            if zf is not None:
                if all(clear(b) for b in envelopes("walk", x, y, zf, 1)):
                    fits["walk"].append([round(x, 1), round(y, 1), round(zf, 2)])
                for face in (1, -1):
                    if all(clear(b) for b in envelopes("seat", x, y, zf, face)):
                        fits["seat"].append([round(x, 1), round(y, 1), round(zf, 2), face])
            y += 0.5
        x += 1.0
    layouts = {}
    for face in (1, -1):
        cand = sorted([s for s in fits["seat"] if s[3] == face], key=lambda s: (-s[0] * face, abs(s[1])))   # front first
        picked = []
        for s in cand:
            if all(abs(s[1] - p[1]) >= CREW["seat_w"] or abs(s[0] - p[0]) >= PITCH for p in picked):
                picked.append(s)
        layouts[face] = picked
    best = max((1, -1), key=lambda fc: len(layouts[fc]))
    return dict(length=length, scale=round(f, 4), size=[round(v, 2) for v in (hi - lo)],
                seat_cells=len(fits["seat"]), standing_cells=len(fits["walk"]), standing=fits["walk"][:40],
                seats_face_plusX=layouts[1], seats_face_minusX=layouts[-1], best_face=best, best_count=len(layouts[best]))

tried = []
chosen = None
for L in LENGTHS:
    r = scan(L); tried.append(r)
    print("PREP_SCAN length", L, "size", r["size"], "seats", len(r["seats_face_plusX"]), "/", len(r["seats_face_minusX"]), "standing cells", r["standing_cells"])
    if chosen is None and r["best_count"] >= MIN_SEATS:
        chosen = r
if chosen is None:
    chosen = max(tried, key=lambda r: r["best_count"])
f = chosen["length"] / L0
ob.scale = (f, f, f); bpy.ops.object.transform_apply(scale=True)
mn2, mx2 = bounds(ob)
print("PREP_CHOSEN length", chosen["length"], "seats", chosen["best_count"], "(min", MIN_SEATS, ")")

pieces = [ob]
if PIECES > 1:
    xs = sorted(p.center.x for p in ob.data.polygons)
    cuts = [xs[len(xs) * k // PIECES] for k in range(1, PIECES)]
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="DESELECT"); bpy.ops.object.mode_set(mode="OBJECT")
    for k in range(PIECES - 1, 0, -1):
        for p in ob.data.polygons:
            p.select = p.center.x >= cuts[k - 1]
        bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.separate(type="SELECTED"); bpy.ops.object.mode_set(mode="OBJECT")
    pieces = [o for o in bpy.context.scene.objects if o.type == "MESH"]
pieces.sort(key=lambda o: bounds(o)[0].x)
base = os.path.splitext(os.path.basename(OUT))[0]
piece_tris = []
for k, o in enumerate(pieces):
    o.name = f"{base}_Part{k + 1}"; o.data.name = o.name
    piece_tris.append(sum(len(p.vertices) - 2 for p in o.data.polygons))
print("PREP_PIECES", piece_tris)
# Roblox SurfaceAppearance has no emissive slot; an extra emissive texture in the GLB (the Titan Rover had an
# all-black one) left the imported meshes untextured, so drop emission before export.
for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    nt = mat.node_tree
    for n in nt.nodes:
        if n.type == "BSDF_PRINCIPLED":
            for name in ("Emission Color", "Emission"):
                if name in n.inputs:
                    for l in list(n.inputs[name].links):
                        nt.links.remove(l)
                    n.inputs[name].default_value = (0, 0, 0, 1)
            if "Emission Strength" in n.inputs:
                n.inputs["Emission Strength"].default_value = 0.0
            if NO_NORMAL and "Normal" in n.inputs:
                for l in list(n.inputs["Normal"].links):
                    nt.links.remove(l)
    if NO_NORMAL:
        for n in list(nt.nodes):
            if n.type == "NORMAL_MAP":
                nt.nodes.remove(n)
    for n in list(nt.nodes):
        if n.type == "TEX_IMAGE" and not any(l for o in n.outputs for l in o.links):
            nt.nodes.remove(n)
for img in list(bpy.data.images):
    if img.users == 0:
        bpy.data.images.remove(img)
for img in bpy.data.images:
    if img.size[0] > 1024 or img.size[1] > 1024:
        w, h = img.size; k = 1024 / max(w, h); img.scale(max(1, int(w * k)), max(1, int(h * k)))
    img.pack()
for o in list(bpy.context.scene.objects):
    if o.type != "MESH":
        bpy.data.objects.remove(o)
bpy.ops.object.select_all(action="DESELECT")
for o in pieces:
    o.select_set(True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", use_selection=True, export_yup=True, export_apply=True,
                          export_image_format="JPEG", export_jpeg_quality=88)
rep = dict(source=os.path.basename(SRC), source_tris=src_tris, decimated_tris=dec_tris, pieces=piece_tris,
           out=os.path.basename(OUT), out_mb=round(os.path.getsize(OUT) / 1e6, 2), min_seats=MIN_SEATS,
           crew=CREW, chosen=chosen, tried=[{k: v for k, v in t.items() if k != "standing"} for t in tried],
           note="Prep space: centred, length along X, Z up. Studio (glTF Y-up): X = x, Y = z, Z = -y.")
json.dump(rep, open(REPORT, "w"), indent=1)
print("PREP_DONE", OUT, rep["out_mb"], "MB")
