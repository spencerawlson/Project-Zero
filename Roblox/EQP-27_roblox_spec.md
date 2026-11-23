# EQP-27 Police Energy Blaster: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_SEC_PoliceEnergyBlaster_A` |
| Purpose | Police sidearm. |
| Interaction | Fire · stun mode |
| Animation | Shot VFX |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | S / P2 |
| Dependencies | cell E-20 |

Status: design only. Not built in Studio yet (Phase 9).
