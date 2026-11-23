# VEH-07 Freight Elevator: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_IND_FreightElevator_A` |
| Purpose | Industrial vertical movement (server-owned platform). |
| Interaction | Call · ride · gate open/close |
| Animation | Platform travel, gate, cables |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | M / P1 |
| Dependencies | server platform states |

Status: design only. Not built in Studio yet (Phase 9).
