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

Further steps (backups, driving/flight security, mission instances, service hardening, persistence, QA/paths, performance)
are logged below as they're done.
