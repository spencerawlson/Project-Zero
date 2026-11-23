# VEH-01 Ghost Train: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_TRN_GhostTrain_A` |
| Purpose | Story vehicle for the Ghost Train mission arc. |
| Interaction | Board · door control · moving-platform illusion · defence event · emergency stop (INT-05) |
| Animation | Bogie rotation, doors, light flicker, smoke VFX |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | XL / P2 |
| Dependencies | INT-04, INT-05 |

Status: design only. Not built in Studio yet (Phase 9).
