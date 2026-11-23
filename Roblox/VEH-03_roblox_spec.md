# VEH-03 Maintenance Train: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_TRN_MaintenanceTrain_A` |
| Purpose | Track repair; ambient life + Ghost Train set dressing. |
| Interaction | Repair objective (crane), salvage crates |
| Animation | Crane boom, beacon rotate |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | M / P2 |
| Dependencies | INF-10 |

Status: design only. Not built in Studio yet (Phase 9).
