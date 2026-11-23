# BLD-29 Modular Outpost Block: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_RES_ModularOutpostBlock_A` |
| Purpose | Modular housing / outpost block (residential fringe). |
| Interaction | Enterable lobby (optional) |
| Animation | Lights |
| Modular construction | Studio Parts on the 8-stud grid for floors, walls and roofs (K01/K02 kit). Facade strips and trims are separate parts. Landmark pieces are MeshParts. |
| Implementation | Model with PrimaryPart at origin; interiors streamed; doors and interactables tagged for CollectionService; server-owned state. |
| Collision | Walls and floors = Parts (CanCollide). Roof meshes CanCollide off + invisible roof box. Props < 2 studs: no collision. |
| LOD | LOD0 enterable < 150 studs · LOD1 merged shell < 400 · LOD2 skyline proxy (single MeshPart). |
| Complexity / priority | M / P2 |
| Dependencies | — |

Status: design only. Not built in Studio yet (Phase 9).
