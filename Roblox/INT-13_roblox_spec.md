# INT-13 Robot Communal Lounge: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_RES_RobotCommunalLounge_A` |
| Purpose | Residential communal lounge. |
| Interaction | Social · rest |
| Animation | Ambient |
| Modular construction | Room shell from the 8-stud kit; furniture props are reusable MeshParts; lights grouped by state tag. |
| Implementation | Interior streamed as a separate model; ProximityPrompts on interactables; server validates actions. |
| Collision | Room shell Parts; props > 2 studs use box collision, smaller props none; keep 6-wide clear paths. |
| LOD | Interior only rendered when streamed in; no LOD needed beyond Roblox automatic mesh LOD. |
| Complexity / priority | M / P2 |
| Dependencies | BLD-03 |

Status: design only. Not built in Studio yet (Phase 9).
