"""Entry point: blender -b --factory-startup -P pz_build_asset.py -- <ASSET_ID> <outdir> [quick]"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
_args = sys.argv[sys.argv.index("--") + 1:]
AID, OUTDIR = _args[0], _args[1]
QUICK = "quick" in _args[2:]
# pz_build_stasis parses argv as <mode> <outdir> <shots...>; give it a neutral mode
sys.argv = [sys.argv[0], "--", "asset", OUTDIR]
import pz_build_stasis as K          # resets scene, builds materials (no run())
import pz_asset_lib as A
import pz_assets_bld, pz_assets_veh, pz_assets_eqp, pz_assets_inf, pz_assets_int, pz_assets_wpn
REG = {}
for mod in (pz_assets_bld, pz_assets_veh, pz_assets_eqp, pz_assets_inf, pz_assets_int, pz_assets_wpn):
    REG.update(mod.REG)
cat, fn, opts = REG[AID]
fn()
if "dry" in _args[2:]:
    A.resolve_figure_clashes()
    mn, mx = A.scene_bbox()
    print("DRY_OK", AID, [round(v, 1) for v in mn], [round(v, 1) for v in mx], len(A.NOTES), "notes")
else:
    A.run_shots(cat, OUTDIR, quick=QUICK, **opts)
print("ASSET_DONE", AID)
