# BLD-05 Assembly Foundry: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_IND_AssemblyFoundry_A` |
| Purpose | Industrial production + mission gateway; source of materials. |
| Interaction | Conveyor puzzles · arm timing hazards · salvage nodes · power rerouting (annex) |
| Animation | Conveyors, arms, gantry trolley, stack steam |
| Modular construction | Studio Parts on the 8-stud grid for floors, walls and roofs (K01/K02 kit). Facade strips and trims are separate parts. Landmark pieces are MeshParts. |
| Implementation | Model with PrimaryPart at origin; interiors streamed; doors and interactables tagged for CollectionService; server-owned state. |
| Collision | Walls and floors = Parts (CanCollide). Roof meshes CanCollide off + invisible roof box. Props < 2 studs: no collision. |
| LOD | LOD0 enterable < 150 studs · LOD1 merged shell < 400 · LOD2 skyline proxy (single MeshPart). |
| Complexity / priority | XL / P1 |
| Dependencies | INT-07, VEH-07 |

Status: design only. Not built in Studio yet (Phase 9).
