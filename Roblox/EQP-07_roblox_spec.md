# EQP-07 Power Core / Energy Cells: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_PowerCoreEnergyCells_A` |
| Purpose | Power: Unified swappable cells across all weapons. |
| Interaction | Equip · use |
| Animation | Charge / fire / swing VFX, cell swap |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | S / P0 |
| Dependencies | INF-01 |

Status: design only. Not built in Studio yet (Phase 9).
