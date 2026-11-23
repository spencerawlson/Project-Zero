# EQP-12 Industrial Welding Tool: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_IND_IndustrialWeldingTool_A` |
| Purpose | Industrial fabrication; Engineering upgrades. |
| Interaction | Weld objectives (hold) |
| Animation | Spark VFX |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | S / P2 |
| Dependencies | — |

Status: design only. Not built in Studio yet (Phase 9).
