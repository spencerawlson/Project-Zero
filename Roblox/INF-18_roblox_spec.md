# INF-18 Energy Conduit Column: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_CORE_EnergyConduitColumn_A` |
| Purpose | Power conduit pylon / containment column. |
| Interaction | Power puzzle node |
| Animation | Core pulse |
| Modular construction | Snaps to the 8-stud street grid; repeated instances share one MeshPart asset; states via attributes. |
| Implementation | Model + CollectionService tag; state from CityStateService (Power / Data / Cooling / Security). |
| Collision | One or two box parts for the footprint; decorative parts CanCollide off. |
| LOD | LOD0 < 200 studs · LOD1 merged mesh; StreamingEnabled handles distant instances. |
| Complexity / priority | S / P2 |
| Dependencies | INF-02 |

Status: design only. Not built in Studio yet (Phase 9).
