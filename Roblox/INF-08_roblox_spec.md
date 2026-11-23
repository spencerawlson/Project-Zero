# INF-08 Cooling System: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_IND_CoolingSystem_A` |
| Purpose | Cooling state hardware; hazard source. |
| Interaction | Valve puzzle · Cooling state |
| Animation | Fans, steam VFX |
| Modular construction | Snaps to the 8-stud street grid; repeated instances share one MeshPart asset; states via attributes. |
| Implementation | Model + CollectionService tag; state from CityStateService (Power / Data / Cooling / Security). |
| Collision | One or two box parts for the footprint; decorative parts CanCollide off. |
| LOD | LOD0 < 200 studs · LOD1 merged mesh; StreamingEnabled handles distant instances. |
| Complexity / priority | M / P1 |
| Dependencies | Cooling state |

Status: design only. Not built in Studio yet (Phase 9).
