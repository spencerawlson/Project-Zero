# BLD-01 Stasis Facility — Roblox implementation spec (prototype)

Status: **design for review**. Do not mass-import other assets until this prototype is built and verified in Studio (Phase 9 gate).
All dimensions are design assumptions in studs. Source of truth: `Blender/scripts/pz_layout.py`.

## Build order
1. Greybox from SF-02. Use an 8-stud grid, origin at the front-centre of the footprint (X = 0, Y = 0), and the entrance faces +Z in Studio (layout −Y maps to Studio +Z, per the mapping below; the building extends toward −Z).
2. Walk the routes with real Cypher, Sentinel and Patch rigs and the default camera. Check the 6×10 doors, the 12-stud aisle, and the mezzanine headroom.
3. Replace blockout parts with kit modules K01–K10 (SF-05), one module type at a time.
4. Add the pod model `PZ_AWK_StasisPod_A` with its hinge, then wire the wake sequence (SF-04 sheet 2).
5. Add `StasisFacilityService` (server): Power, Security and Pod states. Clients only tween visuals.
6. Profile on desktop and on a mid-tier phone against the SF-05 budget.

## Coordinate mapping (Blender → Studio)
Studio X = layout X, Studio Y = layout Z (up), Studio Z = −layout Y. In Blender, 1 BU = 1 stud; export with scale 1.0.

## Server state (shared enum contracts)
- `Power`: Online | Degraded | Offline. Drives the lighting state, door D03 and the pod bands.
- `Security`: Routine | Alert | Lockdown. Lockdown locks D01 and D03 only. **D05 and D06 never lock.**
- `Pod[P01..P08]`: Stasis | Thawing | Open | Fault. Roles: P01 Cypher (NPC, opens first), P02–P04 + P06 player pods (server-assigned on join, shows the player's custom robot), P05 Sentinel (rescue), P07–P08 dormant (amber visor).
- The client never declares a repair, power restoration or reward. The server validates prompt distance (≤ 10 studs) and cooldowns.

## Interactables (CollectionService tags)
`PZ_Prompt_Pod`, `PZ_Prompt_Breaker`, `PZ_Prompt_Hatch`, `PZ_Prompt_Console`, `PZ_Door_Auto`, `PZ_Door_Failsafe`.

## Performance targets (to be measured — not yet verified)
| Metric | Target |
|---|---|
| Parts + MeshParts | ≤ 1,800 |
| Mesh triangles | ≤ 90 k (≤ 6 k per pod) |
| Textures | ≤ 12 at 1024² |
| Light objects | ≤ 24, ≤ 6 shadowed |
| Frame rate | ≥ 30 fps mobile, ≥ 60 fps desktop |
