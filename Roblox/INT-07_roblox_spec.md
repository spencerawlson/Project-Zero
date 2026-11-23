# INT-07 Factory Assembly Floor: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_IND_FactoryAssemblyFloor_A` |
| Purpose | Factory assembly floor (Foundry mission). |
| Interaction | Conveyor/arm timing · salvage |
| Animation | Conveyors, arms, crane |
| Modular construction | Room shell from the 8-stud kit; furniture props are reusable MeshParts; lights grouped by state tag. |
| Implementation | Interior streamed as a separate model; ProximityPrompts on interactables; server validates actions. |
| Collision | Room shell Parts; props > 2 studs use box collision, smaller props none; keep 6-wide clear paths. |
| LOD | Interior only rendered when streamed in; no LOD needed beyond Roblox automatic mesh LOD. |
| Complexity / priority | L / P1 |
| Dependencies | BLD-05 |

Status: design only. Not built in Studio yet (Phase 9).
