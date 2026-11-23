# EQP-02 PHOTON EDGE Energy Sword: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_PhotonEdgeEnergySword_A` |
| Purpose | Melee: Fast and precise. |
| Interaction | Equip · use · energy cell E-10 |
| Animation | Charge / fire / swing VFX, cell swap |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | M / P1 |
| Dependencies | EQP-07 cell E-10 |

Status: design only. Not built in Studio yet (Phase 9).
