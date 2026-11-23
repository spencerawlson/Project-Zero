# BLD-04 Circuit Market: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_MKT_CircuitMarket_A` |
| Purpose | Commerce hub: parts, cosmetics, decals, upgrades. |
| Interaction | Vendor dialogue · purchase · item preview · restock events |
| Animation | Animated holo signs, canopy sway, kiosk ring pulse |
| Modular construction | Studio Parts on the 8-stud grid for floors, walls and roofs (K01/K02 kit). Facade strips and trims are separate parts. Landmark pieces are MeshParts. |
| Implementation | Model with PrimaryPart at origin; interiors streamed; doors and interactables tagged for CollectionService; server-owned state. |
| Collision | Walls and floors = Parts (CanCollide). Roof meshes CanCollide off + invisible roof box. Props < 2 studs: no collision. |
| LOD | LOD0 enterable < 150 studs · LOD1 merged shell < 400 · LOD2 skyline proxy (single MeshPart). |
| Complexity / priority | L / P0 |
| Dependencies | INT-09, INF-06 |

Status: design only. Not built in Studio yet (Phase 9).
