# EQP-23 PULSE-MINE: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_PulseMine_A` |
| Purpose | Specialised: Area disable (EMP); proximity trigger. |
| Interaction | Equip · use · energy cell E-20 |
| Animation | Charge / fire / swing VFX, cell swap |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | S / P2 |
| Dependencies | cell E-20 |

Status: design only. Not built in Studio yet (Phase 9).
