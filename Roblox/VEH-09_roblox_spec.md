# VEH-09 NX-A17 Raven VTOL: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_TRN_NxA17RavenVtol_A` |
| Purpose | NX-A17 RAVEN multi-role VTOL: transport, recon, cargo, extraction (user concept sheet). |
| Interaction | Board via 9 × 8 ramp · pilot seat + systems bay · 8 robot seats · mission module swap · extraction set piece |
| Animation | Rotor spin + tilt, gear retract, ramp, canopy |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | XL / P2 |
| Dependencies | mission modules |

Status: design only. Not built in Studio yet (Phase 9).
