# INF-05 Street Lighting System: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_HUB_StreetLightingSystem_A` |
| Purpose | Street lighting tied to Power state. |
| Interaction | None (state-driven) |
| Animation | Lamp on/dim/off, flicker |
| Modular construction | Snaps to the 8-stud street grid; repeated instances share one MeshPart asset; states via attributes. |
| Implementation | Model + CollectionService tag; state from CityStateService (Power / Data / Cooling / Security). |
| Collision | One or two box parts for the footprint; decorative parts CanCollide off. |
| LOD | LOD0 < 200 studs · LOD1 merged mesh; StreamingEnabled handles distant instances. |
| Complexity / priority | S / P0 |
| Dependencies | Power state |

Status: design only. Not built in Studio yet (Phase 9).
