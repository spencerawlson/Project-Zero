# BLD-10 Data Archive: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_RSH_DataArchive_A` |
| Purpose | Memory fragment storage; Data relay node. |
| Interaction | Archive terminals · fragment collection · Data state restore |
| Animation | Stripe pulses (Data state), dish rotate |
| Modular construction | Studio Parts on the 8-stud grid for floors, walls and roofs (K01/K02 kit). Facade strips and trims are separate parts. Landmark pieces are MeshParts. |
| Implementation | Model with PrimaryPart at origin; interiors streamed; doors and interactables tagged for CollectionService; server-owned state. |
| Collision | Walls and floors = Parts (CanCollide). Roof meshes CanCollide off + invisible roof box. Props < 2 studs: no collision. |
| LOD | LOD0 enterable < 150 studs · LOD1 merged shell < 400 · LOD2 skyline proxy (single MeshPart). |
| Complexity / priority | M / P1 |
| Dependencies | EQP-11 |

Status: design only. Not built in Studio yet (Phase 9).
