# INF-04 Security Access Gate: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_SEC_SecurityAccessGate_A` |
| Purpose | District border checkpoint. |
| Interaction | Clearance scan · alarm · bypass |
| Animation | Door slide, scan sweep |
| Modular construction | Snaps to the 8-stud street grid; repeated instances share one MeshPart asset; states via attributes. |
| Implementation | Model + CollectionService tag; state from CityStateService (Power / Data / Cooling / Security). |
| Collision | One or two box parts for the footprint; decorative parts CanCollide off. |
| LOD | LOD0 < 200 studs · LOD1 merged mesh; StreamingEnabled handles distant instances. |
| Complexity / priority | M / P0 |
| Dependencies | — |

Status: design only. Not built in Studio yet (Phase 9).
