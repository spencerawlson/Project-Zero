# BLD-21 Academy (Robot Education): Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_RSH_Academy_A` |
| Purpose | Academy district: robot education (concept). |
| Interaction | Tutorial missions |
| Animation | — |
| Modular construction | Studio Parts on the 8-stud grid for floors, walls and roofs (K01/K02 kit). Facade strips and trims are separate parts. Landmark pieces are MeshParts. |
| Implementation | Model with PrimaryPart at origin; interiors streamed; doors and interactables tagged for CollectionService; server-owned state. |
| Collision | Walls and floors = Parts (CanCollide). Roof meshes CanCollide off + invisible roof box. Props < 2 studs: no collision. |
| LOD | LOD0 enterable < 150 studs · LOD1 merged shell < 400 · LOD2 skyline proxy (single MeshPart). |
| Complexity / priority | L / P3 |
| Dependencies | — |

Status: design only. Not built in Studio yet (Phase 9).
