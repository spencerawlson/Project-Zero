# BLD-03 Residential Tower: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_RES_ResidentialTower_A` |
| Purpose | Vertical housing; shows robot daily life; one enterable lobby + sample apartment. |
| Interaction | Lobby charging docks · lift · sample apartment (INT-02) · rooftop bridge |
| Animation | Window flicker by Power state, lift car, beacon blink |
| Modular construction | Studio Parts on the 8-stud grid for floors, walls and roofs (K01/K02 kit). Facade strips and trims are separate parts. Landmark pieces are MeshParts. |
| Implementation | Model with PrimaryPart at origin; interiors streamed; doors and interactables tagged for CollectionService; server-owned state. |
| Collision | Walls and floors = Parts (CanCollide). Roof meshes CanCollide off + invisible roof box. Props < 2 studs: no collision. |
| LOD | LOD0 enterable < 150 studs · LOD1 merged shell < 400 · LOD2 skyline proxy (single MeshPart). |
| Complexity / priority | L / P0 |
| Dependencies | INT-02, INF-01 |

Status: design only. Not built in Studio yet (Phase 9).
