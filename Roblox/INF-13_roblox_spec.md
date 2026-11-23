# INF-13 Robot Roadway Module: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_HUB_RobotRoadwayModule_A` |
| Purpose | Street surface module for the city grid. |
| Interaction | Traffic lanes · AGV paths |
| Animation | Lane light pulses |
| Modular construction | Snaps to the 8-stud street grid; repeated instances share one MeshPart asset; states via attributes. |
| Implementation | Model + CollectionService tag; state from CityStateService (Power / Data / Cooling / Security). |
| Collision | One or two box parts for the footprint; decorative parts CanCollide off. |
| LOD | LOD0 < 200 studs · LOD1 merged mesh; StreamingEnabled handles distant instances. |
| Complexity / priority | S / P1 |
| Dependencies | — |

Status: design only. Not built in Studio yet (Phase 9).
