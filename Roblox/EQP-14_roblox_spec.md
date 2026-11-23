# EQP-14 THUNDER-9 Ion Cannon: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_Thunder9IonCannon_A` |
| Purpose | Ranged (heavy): Heavy damage, armour penetration. |
| Interaction | Equip · use · energy cell E-100 |
| Animation | Charge / fire / swing VFX, cell swap |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | L / P2 |
| Dependencies | cell E-100 |

Status: design only. Not built in Studio yet (Phase 9).
