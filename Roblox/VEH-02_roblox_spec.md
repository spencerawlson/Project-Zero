# VEH-02 NEXUS-01 Monorail: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_TRN_Nexus01Monorail_A` |
| Purpose | Everyday fast travel between districts. |
| Interaction | Board (5 × 8 doors) · sit (8 robot seats / car) · choose destination · ride camera |
| Animation | Path follow along guideway, doors |
| Modular construction | Separate models per car / body / chassis / bogies; seats are Seat instances; doors are hinge models. |
| Implementation | Scripted path following (TweenService / AlignPosition, network owner = server); passengers weld to seats. |
| Collision | Box-fidelity hull parts + floor part; no collision on wheels and rotors; ramp collision only when lowered. |
| LOD | LOD0 < 120 studs · LOD1 merged body · LOD2 silhouette card for distant tracks/sky. |
| Complexity / priority | L / P1 |
| Dependencies | INF-12 |

Status: design only. Not built in Studio yet (Phase 9).
