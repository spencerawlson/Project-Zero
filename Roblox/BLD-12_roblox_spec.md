# BLD-12 Robot Recycling Facility: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_IND_RobotRecyclingFacility_A` |
| Purpose | Scrap processing; salvage resources and hazard mission. |
| Interaction | Salvage nodes · sorting puzzle · shredder hazard |
| Animation | Conveyor, shredder shake, sorter arms |
| Modular construction | Studio Parts on the 8-stud grid for floors, walls and roofs (K01/K02 kit). Facade strips and trims are separate parts. Landmark pieces are MeshParts. |
| Implementation | Model with PrimaryPart at origin; interiors streamed; doors and interactables tagged for CollectionService; server-owned state. |
| Collision | Walls and floors = Parts (CanCollide). Roof meshes CanCollide off + invisible roof box. Props < 2 studs: no collision. |
| LOD | LOD0 enterable < 150 studs · LOD1 merged shell < 400 · LOD2 skyline proxy (single MeshPart). |
| Complexity / priority | L / P2 |
| Dependencies | INF-07 |

Status: design only. Not built in Studio yet (Phase 9).
