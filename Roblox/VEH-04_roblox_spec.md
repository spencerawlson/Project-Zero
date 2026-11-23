# VEH-04 Cargo Transport TITAN-R1: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_IND_CargoTransportTitanR1_A` |
| Purpose | Ground utility transport (TITAN-R1 reference): personnel, cargo, field power. |
| Interaction | Enter via 5 × 8 side doors · drive (2 cab seats) · 2 crew seats · winch · rear power core |
| Animation | Wheels, suspension, doors, winch, roof modules |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | L / P1 |
| Dependencies | BLD-11 |

Status: design only. Not built in Studio yet (Phase 9).
