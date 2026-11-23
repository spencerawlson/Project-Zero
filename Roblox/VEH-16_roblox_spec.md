# VEH-16 Battle Walker: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_SEC_BattleWalker_A` |
| Purpose | ZERO war machine / boss support (vehicle class: no family face required). |
| Interaction | Boss encounter · weak points |
| Animation | Walk cycle, cannon |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | L / P3 |
| Dependencies | BLD-27 |

Status: design only. Not built in Studio yet (Phase 9).
