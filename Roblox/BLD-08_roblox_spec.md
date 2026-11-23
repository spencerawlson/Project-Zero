# BLD-08 Nexus Energy Spire: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_CORE_NexusEnergySpire_A` |
| Purpose | City landmark; communicates district power and ZERO's influence. |
| Interaction | Power restoration objectives · mission unlocks (base console room) |
| Animation | Ring rotation, core pulse, colour by Power/Security state |
| Modular construction | Studio Parts on the 8-stud grid for floors, walls and roofs (K01/K02 kit). Facade strips and trims are separate parts. Landmark pieces are MeshParts. |
| Implementation | Model with PrimaryPart at origin; interiors streamed; doors and interactables tagged for CollectionService; server-owned state. |
| Collision | Walls and floors = Parts (CanCollide). Roof meshes CanCollide off + invisible roof box. Props < 2 studs: no collision. |
| LOD | LOD0 enterable < 150 studs · LOD1 merged shell < 400 · LOD2 skyline proxy (single MeshPart). |
| Complexity / priority | XL / P0 |
| Dependencies | INT-10, INF-02 |

Status: design only. Not built in Studio yet (Phase 9).
