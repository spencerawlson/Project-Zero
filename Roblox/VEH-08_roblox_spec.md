# VEH-08 Passenger Elevator: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_HUB_PassengerElevator_A` |
| Purpose | Accessible vertical route in civic buildings. |
| Interaction | Call · ride |
| Animation | Car travel, bi-parting doors |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | S / P1 |
| Dependencies | — |

Status: design only. Not built in Studio yet (Phase 9).
