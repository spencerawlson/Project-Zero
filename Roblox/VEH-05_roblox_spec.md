# VEH-05 Autonomous Robot Shuttle: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_HUB_AutonomousRobotShuttle_A` |
| Purpose | Driverless robot shuttle for civic districts. |
| Interaction | Hail · board · sit (4 seats) |
| Animation | Door slide, eye blink, wheels |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | M / P2 |
| Dependencies | — |

Status: design only. Not built in Studio yet (Phase 9).
