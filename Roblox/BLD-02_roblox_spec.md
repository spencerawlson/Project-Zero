# BLD-02 Resistance Workshop: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_HUB_ResistanceWorkshop_A` |
| Purpose | Player home: return, upgrade, craft, queue missions, socialise. |
| Interaction | Customization platform · 4 workbenches · mission terminal · archive wall · testing bay |
| Animation | Crane jib swing, workbench arms, holo platform spin, bay lights |
| Modular construction | Studio Parts on the 8-stud grid for floors, walls and roofs (K01/K02 kit). Facade strips and trims are separate parts. Landmark pieces are MeshParts. |
| Implementation | Model with PrimaryPart at origin; interiors streamed; doors and interactables tagged for CollectionService; server-owned state. |
| Collision | Walls and floors = Parts (CanCollide). Roof meshes CanCollide off + invisible roof box. Props < 2 studs: no collision. |
| LOD | LOD0 enterable < 150 studs · LOD1 merged shell < 400 · LOD2 skyline proxy (single MeshPart). |
| Complexity / priority | XL / P0 |
| Dependencies | INT-03, EQP-01 |

Status: design only. Not built in Studio yet (Phase 9).
