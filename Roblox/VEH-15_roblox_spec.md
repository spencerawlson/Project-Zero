# VEH-15 Armored 8x8 Patrol: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_SEC_Armored8X8Patrol_A` |
| Purpose | Armoured 8x8 patrol (renamed from 'Desert Sentinel' to avoid the canonical Sentinel name). |
| Interaction | Patrol encounter |
| Animation | Wheels, turret |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | M / P2 |
| Dependencies | BLD-07 |

Status: design only. Not built in Studio yet (Phase 9).
