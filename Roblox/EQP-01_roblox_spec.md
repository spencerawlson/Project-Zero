# EQP-01 Repair Tool: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_RepairTool_A` |
| Purpose | Patch/Engineering primary: repair beam and fabrication. |
| Interaction | Equip · hold to repair · cooldown |
| Animation | Jaw open/close, beam VFX |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | M / P0 |
| Dependencies | Tool instance |

Status: design only. Not built in Studio yet (Phase 9).
