# Project Zero — NEXUS-01 Asset & Architecture Production Bible

**Status: Rev C, for review.** The bible covers 118 inventory assets across robots, buildings, vehicles, equipment and weapons, infrastructure, and interiors and props. The Stasis Facility benchmark (SF-01…05) is approved. The other sheets are marked FOR REVIEW. Phase 9, the Roblox Studio build, has not started.

## Contents
| Path | What it holds |
|---|---|
| `PDF/PROJECT_ZERO_NEXUS-01_Production_Bible_RevC.pdf` | The current bible. Landscape 17×11 in, bookmarked: front matter, robot family, Stasis Facility, every asset sheet, QA. Stored with Git LFS. |
| `PDF/…_RevB.pdf`, `PDF/…_SAMPLE_StasisFacility_RevA.pdf` | Earlier revisions, kept for reference. |
| `PDF/pages/` | Front-matter pages: cover, contents, reference audit, supplied assets, consistency spec, inventory, naming, QA. |
| `Characters/` | Canonical robot turnarounds, the family lineup, CHR-00…11 sheets and model pages. |
| `Stasis_Facility/` | SF-01…05 sheets and their renders. |
| `Buildings/`, `Vehicles/`, `Equipment/`, `Infrastructure/`, `Interiors/` | One folder per asset ID. Each holds the sheet(s), `renders/` (procedural blockout; each `.json` has the camera and anchor data), and `user_model/` where a supplied 3D model was rendered. |
| `Meshy_Prompts/<ID>_meshy.md` | Meshy prompt for each asset. |
| `Roblox/<ID>_roblox_spec.md` | Roblox spec for each asset: naming, modules, collision, LOD, budgets. |
| `Blender/scripts/` | `pz_layout.py` (Stasis layout, the single source of truth), the procedural builders (`pz_assets_*.py`), `pz_model_audit.py` (read-only renders of supplied models) and the render batch scripts. |
| `PDF/src/` | Sheet composers, inventory, specs, QA and the PDF builder (`pz_finalize.py` runs the whole build). |
| `Source_Documents/` | Supplied reference PDFs and images, reference crops and triage thumbnails. |
| `QA/` | Automated QA report, plus `visual_review.json` (the record of pages checked by eye). |
| `manifest.csv` | Maps every image to its asset ID, view, engine, source script and sheet. |

The 1.1 GB of supplied GLBs extracted under `Source_Documents/user_models/` is not committed. The originals stay in the parent `Project Zero_Roblox` folder.

## Regenerate
```sh
# renders (Blender 5.3 headless; Cycles CPU heroes, Workbench orthos)
sh Blender/scripts/render_stasis_all.sh
sh Blender/scripts/render_assets.sh BLD-02 VEH-01 ...      # procedural blockouts
blender -b --factory-startup -P Blender/scripts/pz_model_audit.py -- <glb> <outdir> <size> <height|length> [front]
# sheets + PDF
cd PDF/src && PYTHONIOENCODING=utf-8 python pz_finalize.py
python pz_export_md.py                                      # Meshy prompts + Roblox specs
```

## Honesty notes
- All dimensions are **design assumptions in Roblox studs** (1 stud ≈ 0.28 m). None are measurements taken from concept art.
- Procedural renders are production blockouts, not a final art pass. Their orthographic views are exact projections of the blockout, not CAD drawings.
- Supplied Meshy and library models are rendered **read-only**: rest pose, uniform scale, and opaque materials applied at render time only. Some exceed Roblox budgets; the QA notes say which need a remesh.
- Cypher, Sentinel and Patch are the canonical robots and are used unmodified. Every other robot belongs to the same family. No faceless figures are used.
- Weapons are blockouts and concept crops until the Meshy models arrive.
- Nothing has been built in Roblox Studio yet.
