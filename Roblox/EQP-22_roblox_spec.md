# EQP-22 GRAVITY-8 Manipulator: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_Gravity8Manipulator_A` |
| Purpose | Specialised: Move / lift objects; combat utility. |
| Interaction | Equip · use · energy cell E-60 |
| Animation | Charge / fire / swing VFX, cell swap |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | M / P2 |
| Dependencies | cell E-60 |

Status: design only. Not built in Studio yet (Phase 9).
