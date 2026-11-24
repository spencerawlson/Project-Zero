# NEXUS-01 City

Master plan v2, Phase 2: the civilian city vertical slice. This document grows district by district (decision D10). The story comes from [STORY_BIBLE.md](STORY_BIBLE.md).

## 1. The first district: Founders' Quarter

The oldest part of NEXUS-01, built by the founders around the Stasis Facility. It's where newly woken robots arrive, and where Patch keeps a workshop.

**Why this district first (v2 §42, the first ten minutes):** after M01 the player walks out of the facility straight into a living street:
- robot citizens going about their day
- a charge-and-repair bay
- Patch's workshop: the first job and the first career (engineering)
- a market: the first way to spend NEXUS Credits

The district is in the same place as the facility (city hub server, D5): no loading screen between Chapter 1 and Chapter 2.

### Layout (district frame)
Origin = the street end at the facility's exit. −Z leads away from the facility; X is to the right walking in. All sizes are in studs.

```
 z    0  ── facility exit (D04 side) ───────────────────────────────
         |  sidewalk 8 | road 24 | sidewalk 8 |
 z  -40       [Charge Bay]                      (east, x +30)
 z  -60  [Patch's Workshop 70×43] (west, x -62)        [Residential Tower] (x +88)
 z -100                 ( Plaza ⌀48 )
 z -110                                     [Maintenance Hospital 80×30] (x +64)
 z -160  [Circuit Market 80×79]   (west, x -68)
 z -170                                     [Emergency Station 48×31] (x +56)
 z -210                                     [Police Station 36×33] (x +50)
 z -240 ── end of street (later: transit terminal to other districts) ──
```

Street lights: 8 pylons along both sidewalks. Three are dark at the start: they're the first job.

### Buildings and their purpose

| Building | Model | Size | Gameplay in this slice |
|---|---|---|---|
| **Patch's Workshop** | BLD-02 (customisation garage) + INT-03 interior | 70 long; interior 40 | Patch (NPC mentor) gives the first engineering contract; accessible interior (the door takes you to the interior, which is built apart from the street) |
| **Charge Bay** | Tech Repair Station (owner model, 2026-11-24) | 20 long | Stand on the platform to recharge energy (free) |
| **Circuit Market** | BLD-04 | 80 long | Spend NEXUS Credits: energy cells, the engineering toolkit |
| **Maintenance Hospital** | BLD-09 | 80 long | Exterior and landmark now; the medical career later (Phase 3) |
| **Residential Tower** | BLD-03 | 72 tall | Skyline; homes come in Phase 5 |
| **Emergency Station** | BLD-17 | 48 long | Exterior; the emergency-responder career later |
| **Police Station** | BLD-16 | 36 long | Exterior; security career later |
| Streets, sidewalks, plaza, lights | Built from parts | — | Walkable, readable at night |

## 2. Systems in this slice

### Energy (charging and maintenance)
- Every robot has **energy** from 0 to 100, saved in the profile (`status.energy`). The wings' flight energy is separate.
- It drains slowly while playing (about 25 minutes from full to empty) and never in menus or cutscenes.
- Under 20: an on-screen warning and the waypoint to the nearest Charge Bay.
- At 0: the robot walks at 60 % speed. Nothing worse: no damage, no loss.
- **Charge Bay:** standing on its platform charges 20 per second. Free.
- **Energy cells** (market, 30 credits): instant +50, usable anywhere.

### Contracts: the first job
**C01 "Lights Out" (Patch, engineering):**
1. Talk to Patch in the workshop.
2. Take power cells from the workshop's crate (carry one at a time; the cell is visible in the robot's hands).
3. Install a cell in each of the 3 dark street lights (hold E, 2 s).
4. Return to Patch.

Rewards: **120 NEXUS Credits** and **50 engineering experience** the first time. After that the contract repeats with other dark lights for **40 credits** and 20 experience, with a cooldown.

**C02 "Bay Calibration"** (needs the engineering toolkit): recalibrate the Charge Bay's three arms (hold E at each, then a short timing check). **150 credits**, repeatable. This makes the toolkit worth buying: it's the first step of a career (Phase 3 expands it).

### Market (first spending)
| Item | Price | Effect |
|---|---|---|
| Energy cell | 30 | +50 energy, consumable (up to 5 carried) |
| Engineering toolkit | 200 | Unlocks C02 and later engineering contracts |

Wings and weapons are never sold (Story Bible §7).

### Citizens
Several robot citizens with real names walk routes between the buildings, stop at the market and the bay, and idle in the plaza.
- **Bodies:** the owner's rigged models (Futuristic Utility Robot, Cargo Logistics Robot, Scientific Research Robot, UT-01) through Roblox Avatar Auto Setup, as with Cypher.
- **Behaviour:** routes run on the server. Citizens ignore players, except a short greeting line when one walks close.

### Profile additions (schema v2)
- `status.energy` (number, 0–100)
- `careers.engineering.xp` (number)
- `contracts[id] = { completions, lastCompletedAt }`
- `inventory.energyCells` (number)
- `items.toolkit_engineering`

All server-authoritative and unit tested.

## 3. Completion criteria (checklist Phase 2)
A new player can:
1. wake
2. finish M01
3. walk out into the Founders' Quarter and see citizens
4. find Patch
5. complete C01 and get paid
6. charge at the bay when low
7. buy an energy cell or the toolkit
8. do C02

The district runs at a playable frame rate on a mid-range PC and a phone (StreamingEnabled; models baked to 1024 px textures, about 60k triangles per large building).

## 4. Assets in the place (2026-11-24)
| Model | Roblox asset | Where |
|---|---|---|
| Patch's Workshop (BLD-02 model) | 97302530858946 | `ServerStorage.City.PZ_PatchWorkshop` |
| Workshop interior (INT-03) | 132359776753670 | `ServerStorage.City.PZ_WorkshopInterior` |
| Charge Bay (Tech Repair Station) | 81129535043599 | `ServerStorage.City.PZ_ChargeBay` |
| Power cell (carried in C01) | 71306623252879 | `ServerStorage.City.PZ_PowerCell` |
| Police Station (BLD-16) | 80198618347945 | `ServerStorage.City.PZ_PoliceStation` |
| Maintenance Hospital (BLD-09) | 118681095189922 | `ServerStorage.City.PZ_MaintenanceHospital` |
| Circuit Market (BLD-04) | 121741539857006 | `ServerStorage.City.PZ_CircuitMarket` |
| Residential Tower (BLD-03) | 84184484894086 | `ServerStorage.City.PZ_ResidentialTower` |
| Emergency Station (BLD-17) | 114830054796725 | `ServerStorage.City.PZ_EmergencyStation` |
| Citizen bodies (utility, cargo, research) | 86327307717687, 128153791599552, 110664630060363 | rigged: `ServerStorage.Citizens.{UtilityRobot,CargoRobot,ResearchRobot}` |
| Patch (CHR-03, rigged) | from 79909362444560 | `ServerStorage.Chassis.PatchNPC` |

Building fronts were checked from the street in Studio. The Charge Bay's arm markers sit on floor mapped with a ray grid (they must be reachable walking in from the street).
