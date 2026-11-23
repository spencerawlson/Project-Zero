# EQP-09 Medical Repair Drone: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_MedicalRepairDrone_A` |
| Purpose | Patch: Support Drone; heals allies. |
| Interaction | Deploy · follow · heal pulse |
| Animation | Hover bob, rotor spin, eye blink |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | M / P2 |
| Dependencies | — |

Status: design only. Not built in Studio yet (Phase 9).
