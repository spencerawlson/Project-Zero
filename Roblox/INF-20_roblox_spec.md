# INF-20 Reactor Ring Engine: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_CORE_ReactorRingEngine_A` |
| Purpose | Reactor ring engine (Spire / reactor rooms). |
| Interaction | Power objective |
| Animation | Ring spin |
| Modular construction | Snaps to the 8-stud street grid; repeated instances share one MeshPart asset; states via attributes. |
| Implementation | Model + CollectionService tag; state from CityStateService (Power / Data / Cooling / Security). |
| Collision | One or two box parts for the footprint; decorative parts CanCollide off. |
| LOD | LOD0 < 200 studs · LOD1 merged mesh; StreamingEnabled handles distant instances. |
| Complexity / priority | M / P2 |
| Dependencies | INT-10 |

Status: design only. Not built in Studio yet (Phase 9).
