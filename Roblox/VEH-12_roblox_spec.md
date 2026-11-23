# VEH-12 Armored VTOL Security Aircraft: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_SEC_ArmoredVtolSecurityAircraft_A` |
| Purpose | Security air patrol / gunship (user 3D model). |
| Interaction | Patrol / pursuit encounter · spotlight search |
| Animation | Rotor spin + tilt, gear, sensor ball |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | L / P2 |
| Dependencies | BLD-07 |

Status: design only. Not built in Studio yet (Phase 9).
