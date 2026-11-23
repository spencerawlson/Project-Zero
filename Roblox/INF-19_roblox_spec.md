# INF-19 Central Core Hologram Plinth: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_CORE_CentralCoreHologramPlinth_A` |
| Purpose | Central Core plaza hologram plinth (metropolis globe). |
| Interaction | Story beacon · gathering point |
| Animation | Hologram spin |
| Modular construction | Snaps to the 8-stud street grid; repeated instances share one MeshPart asset; states via attributes. |
| Implementation | Model + CollectionService tag; state from CityStateService (Power / Data / Cooling / Security). |
| Collision | One or two box parts for the footprint; decorative parts CanCollide off. |
| LOD | LOD0 < 200 studs · LOD1 merged mesh; StreamingEnabled handles distant instances. |
| Complexity / priority | M / P1 |
| Dependencies | BLD-08 |

Status: design only. Not built in Studio yet (Phase 9).
