# EQP-04 Scanner: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_Scanner_A` |
| Purpose | Cypher/Intelligence: Pulse Scan, find objectives. |
| Interaction | Scan pulse · reveal markers |
| Animation | Ring spin, pulse VFX |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | S / P0 |
| Dependencies | Tool instance |

Status: design only. Not built in Studio yet (Phase 9).
