# QA report — sample section Rev A

| Check | Result | Detail |
|---|---|---|
| All bible pages exist | PASS | 159/159 present |
| Page size 17×11 in @160 dpi (2720×1760) | PASS | all pages |
| No blank / failed renders | PASS | 29 renders checked (luma std-dev > 4) |
| Every render has camera/anchor metadata | PASS | json beside each render |
| Room grid on 8-stud modules | NOTE | exterior + chamber on 8-grid; interior partition on 4-stud half-module: R09:60, R10:60 |
| Two independent emergency exits | PASS | 2 egress doors (D05, D06), never lock |
| Door clear size ≥ 4×9 studs | PASS | smallest 4×9 |
| Pod count consistent (layout ↔ sheets) | PASS | 8 pods in pz_layout.py; SF-02/SF-03/SF-05 state 8 |
| Asset renders not blank | FAIL | all category renders checked; blank: ['Infrastructure\\INF-13\\renders\\front.png', 'Infrastructure\\INF-13\\renders\\left.png', 'Infrastructure\\INF-13\\renders\\rear.png', 'Infrastructure\\INF-13\\renders\\right.png', 'Infrastructure\\INF-13\\renders\\top.png'] |
| Footprint vs reference target | PASS | 120×88×32 vs Asset Bible 120×85×32 — +3 width, documented on P03 |
| Same-model consistency | PASS | plan, elevations, sections, renders all generated from pz_layout.py (by construction) |
| Dimension disclaimer on every sheet | PASS | title-block note on all pages (frame()) |
| Canonical robots untouched | PASS | GLBs read-only; rest pose + uniform scale at render time; stray Icosphere hidden, not deleted from files |
| Stray objects in robot GLBs | NOTE | Icosphere in Rigged_Cypher.glb and Rigged_Sentinel.glb — remove before Roblox import |
| Visual review of every page | PASS | 20 pages reviewed by eye; no layout defects open |
| Roblox Studio prototype | NOT STARTED | Phase 9 — after approval; Roblox_Studio MCP registered, needs session restart |
| Every inventory asset has a sheet | FAIL | 118 assets checked; missing: INT-02, INT-03, INT-04, INT-05, INT-06, INT-07, INT-09, INT-10, INT-11, INT-12, INT-13, INT-14, INT-15, INT-16 |
| User 3D models needing remesh | NOTE | VEH-11 5.6 M tris, VEH-10/12 textured raw GLBs — remesh before Roblox |
