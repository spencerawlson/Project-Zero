# Audit remediation log

Responds to [Claude_Needs_To_Read_This.md](../Claude_Needs_To_Read_This.md) (review of main 44d2da8b), following the
execution order in [Project_Zero_Audit_Response.md](../Project_Zero_Audit_Response.md) §6 and the owner rulings in
[Project_Zero_Owner_Decisions.md](../Project_Zero_Owner_Decisions.md).
Starting commit for this work: **a242a2a** (main, pulled 2026-11-24).

Statuses (audit response §7): CONFIRMED · NOT REPRODUCED · FIXED AND VERIFIED · FIXED BUT UNVERIFIED · DEFERRED · BLOCKED.
Evidence types: *static* = read in code · *Studio* = reproduced in a Studio session by me · *reported* = earlier checklist claim.

## Step 1: findings verified against current code (static)

| Finding (review §) | Status | Evidence |
|---|---|---|
| No reserved mission instances (D5), §6.1 | CONFIRMED | static: no `TeleportService` anywhere in `src/` |
| District timeout fails silently; Patch and citizens never spawn, §6.3 | CONFIRMED | static: `CityService.luau:62-66` returns after `WaitForChild(…, 20)`; ContractService / CitizenService return when `CityService.Ready()` is false |
| M01 never reaches "complete" after `exited`, §6 | CONFIRMED | static: `MissionM01.luau:101-102` returns `complete_player` and leaves `step == "escape"` |
| Doors "D01–D12" in the greybox vs "D01–D18" in FacilityService, §3.1 / §6.5 | NOT REPRODUCED | static: `Roblox/BLD-01_greybox_build.lua` and `pz_layout.py` both define D01–D18; Studio: 18 door parts in `PZ_StasisFacility.Doors` (restyled 2026-11-24) |
| C02 repeat pays the first-time rate (150), §6 | CONFIRMED (as designed in `NEXUS_01_CITY.md`; owner to rule, audit P2) | static: `ContractRules.luau:36` |

## Step 2: governing documents

| Item | Status | Change |
|---|---|---|
| v2 proposal header still "(not approved)" | FIXED AND VERIFIED | `docs/proposals/2026-11-24_master_prompt_v2.md` header: adopted (D6), ranks below owner decisions |
| D10 "proposed" vs settled | FIXED AND VERIFIED | checklist D10 = decided (owner decision 9) |
| Owner decisions not in the checklist's decision table | FIXED AND VERIFIED | checklist D13 (ten rulings), D14 (robot dimensions), D15 (doc hierarchy), D16 (vehicle registration/recovery: open, owner to name) |

## Step 3: private asset and place backups

| Item | Status | Evidence / change |
|---|---|---|
| Original GLBs unavailable from a clone (P1) | FIXED BUT UNVERIFIED (full backup not run) | `tools/asset_manifest.py` + committed `docs/ASSET_MANIFEST.csv`: 248 source files outside the repo (15.5 GB), path relative to `PZ_ASSET_ROOT` (default: the repo's parent folder), size and SHA-256. Nothing proprietary is committed. |
| Backup and restoration | FIXED BUT UNVERIFIED for the real set; tool self-test executed | `backup` copies every manifest file into `PZ_BACKUP_ROOT` (content-addressed, hash-checked, refuses a folder inside the repo) and snapshots the manifest; `restore-test DIR` restores and re-hashes. Self-test on 3 files: backup, repeat backup (0 copied), restore (0 missing, 0 changed), a corrupted and a deleted file both reported by `verify`, a folder inside the repo refused. **BLOCKED on the owner:** choose the private backup location (another physical drive or a private cloud folder; 15.5 GB). C: has 2 GB free, D: 31 GB, Z: 30 GB. |
| Roblox place not version-controlled (P1) | PARTLY ADDRESSED | Code is in git via Rojo (`default.project.json`). Studio-only content (district, art pass, ServerStorage models) lives in the place's Roblox version history (each `save_place` = a version; latest: **81**, 2026-11-24, after this step's model placements). Uploaded Roblox asset ids for the owner batch are in `docs/ASSET_INVENTORY.md`. A local `.rbxl` copy needs the owner to run File > Save to File into the backup folder: Open Cloud offers no place download to this tool. The old `ProjectZero.rbxl` (2026-11-23) is in the manifest but is out of date. |

## Step 4: driving and flight (P0)

Design: robots and driven vehicles stay client-owned (smooth physics), and the server checks what it sees.
`Shared/MovementRules.luau` holds the limits (unit tested), and `Server/Services/MovementGuard.luau` applies them every
0.25 s. VehicleClient and FlightController read the same numbers.

| Finding | Status | Change | Tests executed (Studio, 2026-11-24) |
|---|---|---|---|
| Client-controlled flight energy | FIXED AND VERIFIED | Wing energy moved to the server (`MovementGuard`; player attribute `PZ_WingEnergy`). It drains while the server-set `PZ_WingsOut` is true and recharges on the ground. At 0 the server folds the wings and FlightController lands. | Wings deployed on the server: energy 100→89→…→5, then the wings folded at about 17 s; recharged on the ground to 26 by 18 s. |
| Flight eligibility | FIXED AND VERIFIED | The `Flight` remote deploys only for a living, unseated robot with `PZ_CanFly` and `MovementRules.canTakeOff`; rate limited. | Without wings, `deploy` was refused (`PZ_WingsOut` stayed false). The low-energy refusal is covered by unit tests only. |
| Flying without wings / hovering | FIXED AND VERIFIED | Off the ground (server sphere cast) and not falling for 2 s with the wings stowed: put back where it last stood on the ground. | A client-side LinearVelocity hover over the street was corrected after 1.3 s, back to y 3.97 (ground). *Finding:* `Humanoid.FloorMaterial` was not used, because the first version, which used it, missed a hover. Over the pod chambers the chamber roof counts as ground (a legal place to stand). |
| Robot speed / teleport | FIXED AND VERIFIED | Each sample is checked against walking or flight limits (×1.5 plus 6 studs slack); a teleport of more than 80 studs is corrected at once. | A 150-stud client teleport was corrected (`[MovementGuard] robot … corrected: teleport`). Residual: the server interpolates client positions, so one intermediate sample was accepted (the robot ended 12 studs along the jump). |
| Flight boundaries and altitude | FIXED BUT UNVERIFIED (static + unit) | `WORLD` box and `FLIGHT_CEILING` (Y 250). **Provisional technical bounds, not approved design values: owner to confirm.** | Unit tests: the bounds contain the facility, the district and the interior. |
| Client-controlled driving | FIXED AND VERIFIED | Driven DriveBody: speed, climb, teleport and turn-rate checks and `VEHICLE_ZONE` (the district street, not the facility). A correction takes network ownership back for 1.5 s, restores the last valid place and stops the vehicle. 3 corrections in 30 s unseat the driver. | A 3× speed cheat (100 studs/s) was corrected after 3 samples (z −164 → −270 → back to −167). Legal top speed (34 studs/s) for 1 s logged no correction (the hauler then met the plaza ring, a solid part of the street). |
| Unit tests | VERIFIED | `tests/Cases/MovementRules_Test.luau` (5 tests) | 72/72 pass (was 67). |

Residual risk: honest flying and driving by a person at normal frame rates is not yet playtested (Studio throttles the
unfocused play window). Server moves call `MovementGuard.Grace` (pods, workshop door); a future server teleport that
forgets it would be pulled back. Overturned / abandoned / out-of-bounds vehicle *recovery* is owner decision D16 (open):
the guard only restores the last valid position after a failed check.

Further steps (mission instances, service hardening, persistence, QA/paths, performance) are logged below as they're done.
