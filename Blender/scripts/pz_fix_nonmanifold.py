"""Split edges shared by more than two faces (left behind when a triangle-soup export is welded) so every edge has
at most two faces. UVs, materials and textures are kept; only vertices along those edges are duplicated.
Roblox showed only its coarse placeholder (and no textures) for the welded Titan Rover pieces, which had 300-500
such edges each; the Carrier (8-18) and Raven (0) rendered fine.

blender -b --factory-startup -P pz_fix_nonmanifold.py -- <in.glb> <out.glb>"""
import bpy, bmesh, sys

a = sys.argv[sys.argv.index("--") + 1:]
SRC, DST = a[0], a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
for o in [o for o in bpy.context.scene.objects if o.type == "MESH"]:
    bm = bmesh.new(); bm.from_mesh(o.data)
    # the importer splits vertices at UV seams; weld by position first (UVs live on face corners and are kept)
    ext = max(max(v.co[i] for v in bm.verts) - min(v.co[i] for v in bm.verts) for i in range(3))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=max(1e-6, ext * 1e-6))
    multi = [e for e in bm.edges if len(e.link_faces) > 2]
    before = len(multi)
    if multi:
        bmesh.ops.split_edges(bm, edges=multi)
    after = sum(1 for e in bm.edges if len(e.link_faces) > 2)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    print("NONMANIFOLD", o.name, before, "->", after, flush=True)
for im in bpy.data.images:
    if im.packed_file is None and im.has_data:
        im.pack()
bpy.ops.export_scene.gltf(filepath=DST, export_format="GLB", export_yup=True, export_image_format="AUTO",
                          export_materials="EXPORT", use_selection=False, export_apply=False)
print("WROTE", DST)
