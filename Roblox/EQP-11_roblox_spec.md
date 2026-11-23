# EQP-11 Memory Storage Module: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_MemoryStorageModule_A` |
| Purpose | Collectible memory fragments. |
| Interaction | Collect · insert into archive |
| Animation | Glow pulse |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | S / P0 |
| Dependencies | — |

Status: design only. Not built in Studio yet (Phase 9).
