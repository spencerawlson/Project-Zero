# VEH-13 Industrial Cargo Hauler: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_IND_IndustrialCargoHauler_A` |
| Purpose | Industrial heavy hauler with loader crane (concept only). |
| Interaction | Crane objective · cargo pickup |
| Animation | Boom, outriggers, wheels |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | L / P2 |
| Dependencies | BLD-05, BLD-11 |

Status: design only. Not built in Studio yet (Phase 9).
