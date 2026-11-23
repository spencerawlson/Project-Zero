# QA report — Rev D

| Check | Result | Detail |
|---|---|---|
| All bible pages exist | PASS | 195/195 present |
| Page size 17×11 in @160 dpi (2720×1760) | PASS | all pages |
| No blank / failed renders | PASS | 29 renders checked (luma std-dev > 4) |
| Every render has camera/anchor metadata | PASS | json beside each render |
| Room grid on 8-stud modules | NOTE | exterior + chamber on 8-grid; interior partition on 4-stud half-module: R09:60, R10:60 |
| Two independent emergency exits | PASS | 2 egress doors (D05, D06), never lock |
| Door clear size ≥ 6×10 studs (fits widest robot) | PASS | smallest 6×10; widest robot Patch 4.4, tallest Sentinel 7.5 (measured in Studio) |
| Pod count consistent (layout ↔ sheets) | PASS | 8 pods in pz_layout.py; SF-02/SF-03/SF-05 state 8 |
| Asset renders not blank | PASS | all category renders checked (blank = >99.5% of pixels one colour) |
| Footprint vs reference target | PASS | 120×88×32 vs Asset Bible 120×85×32 — +3 width, documented on P03 |
| Same-model consistency | PASS | plan, elevations, sections, renders all generated from pz_layout.py (by construction) |
| Dimension disclaimer on every sheet | PASS | title-block note on all pages (frame()) |
| Canonical robots untouched | PASS | GLBs read-only; shown only on character / supplied-model sheets; blockout scenes use grey stand-in figures at design height |
| Stray objects in robot GLBs | PASS | none in the files: each GLB holds one mesh; the Icosphere seen in Blender is an importer bone-shape helper (checked 2026-11-23 before the Roblox upload) |
| Visual review of every page | PARTIAL | 110 of 196 pages reviewed by eye; no layout defects open |
| Roblox Studio prototype | STARTED | Phase 9 — BLD-01 greybox built from Roblox/BLD-01_greybox_build.lua; Cypher, Sentinel, Patch imported at design scale; all 18 doors pass a widest-robot clearance probe |
| Every inventory asset has a sheet | PASS | 118 assets checked; all present |
| Robots fit vehicle cabs (crew standard) | PASS | 60 seats + 47 doors/aisles in 10 assets clear for the largest robot |
| User 3D models needing remesh | NOTE | VEH-11 5.6 M tris, VEH-10/12 textured raw GLBs — remesh before Roblox |
