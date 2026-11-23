# INT-15 Command Chair (prop): Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_SEC_CommandChair_A` |
| Purpose | Command chair prop. |
| Interaction | Sit (Seat) |
| Animation | Swivel |
| Modular construction | Room shell from the 8-stud kit; furniture props are reusable MeshParts; lights grouped by state tag. |
| Implementation | Interior streamed as a separate model; ProximityPrompts on interactables; server validates actions. |
| Collision | Room shell Parts; props > 2 studs use box collision, smaller props none; keep 6-wide clear paths. |
| LOD | Interior only rendered when streamed in; no LOD needed beyond Roblox automatic mesh LOD. |
| Complexity / priority | S / P1 |
| Dependencies | INT-05/08 |

Status: design only. Not built in Studio yet (Phase 9).
