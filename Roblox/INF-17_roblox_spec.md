# INF-17 Mission Gateway Portal: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_HUB_MissionGatewayPortal_A` |
| Purpose | District gateway to mission places (TeleportService portal). |
| Interaction | Queue · teleport |
| Animation | Portal shimmer |
| Modular construction | Snaps to the 8-stud street grid; repeated instances share one MeshPart asset; states via attributes. |
| Implementation | Model + CollectionService tag; state from CityStateService (Power / Data / Cooling / Security). |
| Collision | One or two box parts for the footprint; decorative parts CanCollide off. |
| LOD | LOD0 < 200 studs · LOD1 merged mesh; StreamingEnabled handles distant instances. |
| Complexity / priority | M / P1 |
| Dependencies | TeleportService |

Status: design only. Not built in Studio yet (Phase 9).
