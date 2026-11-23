# INT-09 Underground Market Stall: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_MKT_UndergroundMarketStall_A` |
| Purpose | Underground market stall module (BLD-04). |
| Interaction | Vendor dialogue · purchase · preview |
| Animation | Sign flicker |
| Modular construction | Room shell from the 8-stud kit; furniture props are reusable MeshParts; lights grouped by state tag. |
| Implementation | Interior streamed as a separate model; ProximityPrompts on interactables; server validates actions. |
| Collision | Room shell Parts; props > 2 studs use box collision, smaller props none; keep 6-wide clear paths. |
| LOD | Interior only rendered when streamed in; no LOD needed beyond Roblox automatic mesh LOD. |
| Complexity / priority | S / P0 |
| Dependencies | BLD-04 |

Status: design only. Not built in Studio yet (Phase 9).
