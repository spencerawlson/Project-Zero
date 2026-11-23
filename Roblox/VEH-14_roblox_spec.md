# VEH-14 Tracked Utility Hauler: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_IND_TrackedUtilityHauler_A` |
| Purpose | Tracked utility hauler for depots and surface. |
| Interaction | Drive · cargo |
| Animation | Tracks, dish |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | M / P2 |
| Dependencies | BLD-11 |

Status: design only. Not built in Studio yet (Phase 9).
