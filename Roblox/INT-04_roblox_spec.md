# INT-04 Train Passenger Compartment: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_TRN_TrainPassengerCompartment_A` |
| Purpose | Ghost Train passenger car. |
| Interaction | Sit · walk · defence event |
| Animation | Window flicker, sway |
| Modular construction | Room shell from the 8-stud kit; furniture props are reusable MeshParts; lights grouped by state tag. |
| Implementation | Interior streamed as a separate model; ProximityPrompts on interactables; server validates actions. |
| Collision | Room shell Parts; props > 2 studs use box collision, smaller props none; keep 6-wide clear paths. |
| LOD | Interior only rendered when streamed in; no LOD needed beyond Roblox automatic mesh LOD. |
| Complexity / priority | M / P2 |
| Dependencies | VEH-01 |

Status: design only. Not built in Studio yet (Phase 9).
