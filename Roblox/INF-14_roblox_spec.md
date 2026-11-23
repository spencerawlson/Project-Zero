# INF-14 Elevated Maglev Highway: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_TRN_ElevatedMaglevHighway_A` |
| Purpose | Elevated maglev highway between districts. |
| Interaction | Vehicle routes |
| Animation | Lights |
| Modular construction | Snaps to the 8-stud street grid; repeated instances share one MeshPart asset; states via attributes. |
| Implementation | Model + CollectionService tag; state from CityStateService (Power / Data / Cooling / Security). |
| Collision | One or two box parts for the footprint; decorative parts CanCollide off. |
| LOD | LOD0 < 200 studs · LOD1 merged mesh; StreamingEnabled handles distant instances. |
| Complexity / priority | L / P2 |
| Dependencies | VEH-04, VEH-11 |

Status: design only. Not built in Studio yet (Phase 9).
