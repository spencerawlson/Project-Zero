# INF-16 Drone Hive: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_IND_DroneHive_A` |
| Purpose | Drone hangar and launch hive. |
| Interaction | Drone spawn · sabotage |
| Animation | Drone launches |
| Modular construction | Snaps to the 8-stud street grid; repeated instances share one MeshPart asset; states via attributes. |
| Implementation | Model + CollectionService tag; state from CityStateService (Power / Data / Cooling / Security). |
| Collision | One or two box parts for the footprint; decorative parts CanCollide off. |
| LOD | LOD0 < 200 studs · LOD1 merged mesh; StreamingEnabled handles distant instances. |
| Complexity / priority | M / P2 |
| Dependencies | VEH-06 |

Status: design only. Not built in Studio yet (Phase 9).
