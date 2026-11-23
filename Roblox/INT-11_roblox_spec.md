# INT-11 Hospital Repair Hall: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_RES_HospitalRepairHall_A` |
| Purpose | Hospital repair hall (BLD-09 interior). |
| Interaction | Repair · healing |
| Animation | Arms |
| Modular construction | Room shell from the 8-stud kit; furniture props are reusable MeshParts; lights grouped by state tag. |
| Implementation | Interior streamed as a separate model; ProximityPrompts on interactables; server validates actions. |
| Collision | Room shell Parts; props > 2 studs use box collision, smaller props none; keep 6-wide clear paths. |
| LOD | Interior only rendered when streamed in; no LOD needed beyond Roblox automatic mesh LOD. |
| Complexity / priority | L / P1 |
| Dependencies | BLD-09 |

Status: design only. Not built in Studio yet (Phase 9).
