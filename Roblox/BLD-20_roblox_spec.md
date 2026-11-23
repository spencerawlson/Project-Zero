# BLD-20 Antigravity Arena: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_HUB_AntigravityArena_A` |
| Purpose | Arena district: combat / racing challenges. |
| Interaction | Matches · spectating · racing |
| Animation | Holo boards, lifts |
| Modular construction | Studio Parts on the 8-stud grid for floors, walls and roofs (K01/K02 kit). Facade strips and trims are separate parts. Landmark pieces are MeshParts. |
| Implementation | Model with PrimaryPart at origin; interiors streamed; doors and interactables tagged for CollectionService; server-owned state. |
| Collision | Walls and floors = Parts (CanCollide). Roof meshes CanCollide off + invisible roof box. Props < 2 studs: no collision. |
| LOD | LOD0 enterable < 150 studs · LOD1 merged shell < 400 · LOD2 skyline proxy (single MeshPart). |
| Complexity / priority | XL / P2 |
| Dependencies | — |

Status: design only. Not built in Studio yet (Phase 9).
