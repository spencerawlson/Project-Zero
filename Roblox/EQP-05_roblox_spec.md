# EQP-05 Hacking Terminal: Roblox spec

| Field | Value |
|---|---|
| Roblox name | `PZ_PLR_HackingTerminal_A` |
| Purpose | System Override puzzles. |
| Interaction | Hack mini-game UI |
| Animation | Screen UI, antenna light |
| Modular construction | One Tool per item: Handle part + MeshPart body + emissive part; attachment points GripAttachment / BeamAttachment. |
| Implementation | Tool instance; client plays animation and VFX, server validates use (cooldown, energy, distance). |
| Collision | CanCollide off while held; dropped items use a simple box. |
| LOD | Single LOD (small); disable VFX beyond 80 studs. |
| Complexity / priority | S / P1 |
| Dependencies | — |

Status: design only. Not built in Studio yet (Phase 9).
