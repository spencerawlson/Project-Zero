# INF-12 Monorail Track Module: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_TRN_MonorailTrackModule_A` |
| Purpose | Modular monorail guideway. |
| Interaction | None (VEH-02 path) |
| Animation | Route strip pulse |
| Modular construction | Snaps to the 8-stud street grid; repeated instances share one MeshPart asset; states via attributes. |
| Implementation | Model + CollectionService tag; state from CityStateService (Power / Data / Cooling / Security). |
| Collision | One or two box parts for the footprint; decorative parts CanCollide off. |
| LOD | LOD0 < 200 studs · LOD1 merged mesh; StreamingEnabled handles distant instances. |
| Complexity / priority | S / P1 |
| Dependencies | VEH-02 |

Status: design only. Not built in Studio yet (Phase 9).
