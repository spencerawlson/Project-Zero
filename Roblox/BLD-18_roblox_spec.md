# BLD-18 Nexus PD Headquarters: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_SEC_NexusPdHeadquarters_A` |
| Purpose | Nexus PD headquarters (metropolis 'Nexus PD'). |
| Interaction | Security story hub · lockup |
| Animation | Doors, lights |
| Modular construction | Studio Parts on the 8-stud grid for floors, walls and roofs (K01/K02 kit). Facade strips and trims are separate parts. Landmark pieces are MeshParts. |
| Implementation | Model with PrimaryPart at origin; interiors streamed; doors and interactables tagged for CollectionService; server-owned state. |
| Collision | Walls and floors = Parts (CanCollide). Roof meshes CanCollide off + invisible roof box. Props < 2 studs: no collision. |
| LOD | LOD0 enterable < 150 studs · LOD1 merged shell < 400 · LOD2 skyline proxy (single MeshPart). |
| Complexity / priority | L / P1 |
| Dependencies | BLD-07, EQP-26/27 |

Status: design only. Not built in Studio yet (Phase 9).
