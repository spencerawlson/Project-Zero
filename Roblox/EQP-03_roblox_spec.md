# EQP-03 ARC-7 Plasma Pulse Rifle: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_Arc7PlasmaPulseRifle_A` |
| Purpose | Ranged: Standard issue; stable, versatile. |
| Interaction | Equip · use · energy cell E-40 |
| Animation | Charge / fire / swing VFX, cell swap |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | M / P1 |
| Dependencies | EQP-07 cell E-40 |

Status: design only. Not built in Studio yet (Phase 9).
