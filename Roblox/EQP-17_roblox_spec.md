# EQP-17 ARC CLAWS Blades: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_ArcClawsBlades_A` |
| Purpose | Melee (wrist): Wrist-mounted, retractable. |
| Interaction | Equip · use · energy cell E-15 |
| Animation | Charge / fire / swing VFX, cell swap |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | M / P2 |
| Dependencies | cell E-15 |

Status: design only. Not built in Studio yet (Phase 9).
