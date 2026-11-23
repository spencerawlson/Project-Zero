# VEH-10 Industrial Freight Train: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_TRN_IndustrialFreightTrain_A` |
| Purpose | Heavy freight line; Ghost Train world-building and depot missions (user 3D model). |
| Interaction | Ride / board · freight event · depot gateway |
| Animation | Bogies, pantograph, lights |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | XL / P2 |
| Dependencies | INF-10, BLD-11 |

Status: design only. Not built in Studio yet (Phase 9).
