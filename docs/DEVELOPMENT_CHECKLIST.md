# Project Zero: Development Checklist

Repository: https://github.com/spencerawlson/Project-Zero · Roblox place: ProjectZero (place 102202818249033, universe 10778699105)

**Rules:**
- `[x]` means implemented **and** verified, with evidence noted. `[ ]` means not done, or not verified. Partial progress is noted in *italics* and stays unchecked.
- Record blockers, test results and commit references.
- Don't claim a feature works without testing it.
- Priority: a small, fully playable Project Zero first. Don't build the city at scale while fundamental gameplay systems are missing.

Related documents: [Story Bible](STORY_BIBLE.md) · [Timeline](TIMELINE.md) · [Technical Architecture](TECHNICAL_ARCHITECTURE.md) · [Asset Inventory](ASSET_INVENTORY.md) · [Master plan v2 (source)](proposals/2026-11-24_master_prompt_v2.md) · [v2 analysis](proposals/2026-11-24_master_prompt_v2_analysis.md) · [Vehicles in Studio](../Roblox/vehicles_in_studio.md)

**Master plan (2026-11-24):** the owner adopted the *Master Development Prompt v2* as the master plan, with ZERO kept, memory fragments from the robots' programming on Earth, and weapons found only on platforms during war missions (decisions D6–D9). The phases below follow v2's roadmap (Phases 0–9). Items verified under the earlier 8-phase checklist keep their check and evidence; renumbering doesn't change what was verified.

---

## Phase 0: Repository Audit

- [x] **Inspect the complete repository.**
  The repo is the production bible plus asset pipeline: Python, Blender and Luau builders, 29 `.py`, 25 `.sh`, 2 `.lua`, and about 2,000 generated images and JSON files. There was no game code at the audit. See Technical Architecture §1a.
- [x] **Verify the Roblox development workflow.**
  Confirmed working: Studio over MCP (Edit-mode Luau, playtests with server-side assertions, console checks, screen captures); Open Cloud uploads with `asset:read`/`asset:write`. Rojo 7.7.0 + git adopted (D1), live sync verified 2026-11-23.
- [x] **Inventory existing assets.**
  119 bible assets plus loose files. See [Asset Inventory](ASSET_INVENTORY.md). The owner's newest models (2026-11-24: weapons and enemy machines) are listed in the Story Bible §8 and still need inventory rows.
- [x] **Identify existing functional systems.**
  At the audit: `vehicle_crew_layer.lua` (seats, Board prompt, server boarding, yaw alignment, enclosure check), `BLD-01_greybox_build.lua`, `pz_vehicle_prep.py`, the crew standard and its fit checks.
- [x] **Document missing dependencies.**
  Playable robot rig (G2), persistence (G3), UI, remotes and input (G4), narrative canon (G5), Luau tests (G6). See Technical Architecture §2. All of them are resolved now.
- [x] **Identify technical and narrative conflicts.**
  Done 2026-11-24 for the master plan: [v2 analysis](proposals/2026-11-24_master_prompt_v2_analysis.md) §4 (10 conflicts, each reconciled or decided).
- [x] **Establish a verified development baseline.**
  2026-11-23: the place opens in Studio; the playtest starts and stops cleanly; all 7 crewed vehicles board a player; no script errors. The bible build passes (`pz_finalize.py` exit 0, 196 pages, QA has no FAIL rows).
- [x] **Create the story bible and architecture documents.**
  `docs/STORY_BIBLE.md` and `docs/TIMELINE.md` (2026-11-24, master plan); `docs/TECHNICAL_ARCHITECTURE.md`. The other v2 documents (Part XIV) are written when their phase starts (decision D10, proposed).

**Phase 0 completion:** audit report, asset inventory and verified baseline are done (2026-11-23); the master-plan conflict audit and story bible are done (2026-11-24).

## Phase 1: First Consciousness

- [ ] **Build the activation facility.**
  *In progress:* the BLD-01 Stasis Facility is the activation facility. It's approved (SF-01 to 05) and built in Studio: 13 rooms, 18 doors at least 6×10 that pass a widest-robot probe, and 8 pods.
  *Done 2026-11-23:* `StasisService` assigns each party member their own player pod (P02, P03, P04, P06, using the `PodRoster` unit tests). A new player is held in the closed pod; holding **Activate** (E) opens the glass, frees the robot and saves `progress.activated = true`. A returning player spawns in front of their open pod. Verified in playtests with the real DataStore across sessions.
  *Done 2026-11-23:* the pods are the owner's **Robot Containment Chamber** (INT-12): two chambers, four pods each, one along each side wall of R04 with the open side facing the aisle.
  - **R04 widened** from 48 to 64 studs (facility 88 to 104 wide; decided by the owner) so both fit at a scale where a pod holds Sentinel (7.5).
  - **Closed state:** each pod is closed by a cyan stasis field on its platform, which fades out on activation.
  - **Verified in playtests:** spawn on the pod platform, the full cinematic, walking out to the aisle, and the returning player standing on the chamber floor.
  Not done: sound, the bible SF sheets for the widened R04 (renders pending), kit modules.
- [x] **Implement the standard starter chassis.**
  Verified 2026-11-23 in Studio playtests:
  - **Rig:** the Cypher mesh was auto-rigged with Roblox Avatar Auto Setup into an R15 character, 6.3 studs tall. It is installed as `StarterPlayer.StarterCharacter`, with a master copy at `ServerStorage.Chassis.CypherFrame`. The canonical `PZ_Cypher` is untouched.
  - **Movement:** walks with the rig's own animations.
  - **Fit:** walked from the pod chamber out through the facility's doors.
  - **Colours** (owner request, 2026-11-24): a 10-colour palette, a per-player default and the PAINT picker, saved.
- [ ] **Implement movement and interaction.**
  *Partial:* ProximityPrompt interaction works (pods, breakers, consoles, vehicle boarding with server validation). Movement and camera are still Roblox defaults. Known issue: the camera ends up pressed against the pod after the wake-up scene.
- [x] **Introduce The Source.**
  Verified 2026-11-23 in playtests:
  - **Script:** `src/shared/ActivationScript.luau`, 10 beats, 32.5 s. Covers The Source, ZERO's censorship, the memory flash, "MF-001 acquired" and "signal lost".
  - **Client scene:** `src/client/ActivationCinematic.client.luau`. Letterbox, a camera push-in, typewriter subtitles, ZERO's red glitch, a memory grade, and a Skip button.
  - **Server:** holds the pod closed until the client reports done, with a timeout.
  - There is no voice or sound yet.
- [x] **Implement the corrupted memory fragment.**
  Verified 2026-11-23: activation grants **MF-001**, saved as `progress.memoryFragments["MF-001"] = true`, and The Source's designation is saved as `identity.designation` (e.g. CX-6170).
- [x] **Update the memory dialogue to the master plan** (Story Bible §5).
  Verified 2026-11-24, 54/54 unit tests in a fresh play session (new test: The Source's welcome is present, and MF-001 comes from Earth):
  - **MF-001:** an engineer on Earth in 2189 gives the mission, cut off at "report everything you find back to—".
  - **MF-002:** a technician's hibernation log.
  - v2's welcome line opens the cinematic.
  - Cypher's closing line no longer mentions "the humans".
  - The cinematic is now 35.5 s; its text scales to fit.
- [x] **Create the introductory mission.**
  M01 "The Awakening" (owner-approved plan, 2026-11-24): find Cypher, then restore power (3 breakers in a random order), then free Sentinel, then escape through D03 / R12 / D04 during ZERO's lockdown. Optional: MF-002. Cypher and Sentinel follow the player. No combat.
  - **Code:** `Shared.MissionM01` (8 tests), `MissionService`, `FacilityService`, `NpcService`, the `MissionHUD` client.
  - **Verified 2026-11-24, solo playthrough with the real DataStore:** every step, wrong-order reset, MF-002, checkpoint resume, free roam after completion.
  - Name tags show only for the current objective's character or while it speaks (owner feedback, 2026-11-24).
- [x] **Implement persistent player identity.**
  Verified 2026-11-23: profile keyed by UserId, versioned schema, session-locked store (18 unit tests), real DataStore round trip across two servers. Renaming the designation later needs Roblox text filtering.
- [ ] **Test the complete onboarding experience.**
  *Partial:* the solo path is verified. Not yet: co-op with 2+ players; v2's first ten minutes (§42), which also needs the Phase 2 district straight after M01.

**Completion:** a new player can activate, complete the introductory mission, and return with progress preserved. *Met solo (2026-11-24).* Open: movement and camera, the dialogue update, a co-op test.

**Built ahead of plan (owner requests, 2026-11-24):**
- **Nightwing wings:** found on the wing platform in R03 (powered once main power is restored). The wings unfold from a back module only in flight. Free flight runs on wing energy.
- **NEXUS Credits wallet:** M01 pays 150 once.

## Phase 2: Civilian City Vertical Slice
The next build: v2's first playable slice. Design: [NEXUS_01_CITY.md](NEXUS_01_CITY.md). Built 2026-11-24 (place version 63).
- [x] **Build one functioning NEXUS-01 district (reached straight after M01).**
  Verified 2026-11-24, the **Founders' Quarter**:
  - **Layout:** a 250-stud street (road, sidewalks, cyan kerbs, plaza, 8 street lights, arrival sign) starting at M01's exit behind the facility; built by `Roblox/CITY-01_founders_quarter_build.lua` from `Shared.CityLayout`.
  - **7 buildings** (owner models, baked 45–60k triangles each): Patch's Workshop, Charge Bay, Circuit Market, Maintenance Hospital, Residential Tower, Emergency Station, Police Station.
  - **Checks:** every footprint checked clear of the street and of the other buildings; every front checked from the street in Studio (the Charge Bay and the hospital had to be turned 180°).
- [x] **Implement robotic NPC citizens with routines.**
  Verified 2026-11-24: Vela, Brass, Orin and Tamsin (the owner's three rigged robots, via Avatar Auto Setup) walk a loop along both sidewalks and through the plaza, at their own speeds and with pauses; their positions change between checks.
  Greetings verified 2026-11-24: standing in a citizen's path, Brass's bubble appeared within 0.3 s ("Coming through, cargo for the market."). Checked through the game's data; the play-mode screenshot rendered black.
- [x] **Create accessible building interiors, including one professional facility.**
  Verified 2026-11-24: Patch's workshop interior (INT-03 model inside a shell, away from the street). E at the street door goes in; E at the interior's Exit returns the robot to the sidewalk, standing 6 studs in front of the door (both tested by key press). Patch stands at the workbench on the real floor.
- [x] **Implement charging and maintenance.**
  Verified 2026-11-24:
  - Energy is saved in the profile and drains at 0.0666 per second (about 25 minutes from full).
  - The Charge Bay pad shows CHARGING.
  - An energy cell (R) took 80 to 100.
  - Maintenance gameplay: contract C02, calibrating the bay's three arms.
- [x] **Create introductory civilian jobs: one introductory career mission (engineering with Patch).**
  Verified 2026-11-24, playing with keyboard input:
  - After M01, the "Find Patch" objective appears.
  - **C01 "Lights Out":** Patch → crate → a power cell in the robot's hand → 3 dark lights (shown only to this player) fixed → report. Paid 120 credits and 50 experience.
  - **Market:** bought an energy cell (30) and the engineering toolkit (200); the wings are not listed.
  - **C02 "Bay Calibration":** unlocked by the toolkit. Walked into the bay and calibrated 3 arms → report. Paid 150 credits and 60 experience.
  - Contract records persisted to the next play session.
- [x] **Implement basic transportation.**
  Verified 2026-11-24 (place version 73): a drivable copy of the Tracked Hauler is parked at the top of the Founders' Quarter street (`PZ_DistrictHauler`, attribute `PZ_Drivable`).
  - **VehicleService:** an invisible physics body under the hull; the first robot to board drives, the next ride as passengers; the server brakes when nobody drives.
  - **VehicleClient:** W/S/A/D with smooth acceleration, steering reversed in reverse, physics owned by the driver.
  - **Playtest:** boarded into the driver's seat; W for 3 s drove 34 studs straight down the street, level; W+A turned 44° left; releasing the keys braked to a stop; Space got out and the server took the vehicle back (stopped).
  - The other vehicles in the yard stay display-only until they're needed.
- [ ] Verify mobile and desktop performance.
  *Estimated, not yet measured live (2026-11-24):*
  - From the street a player can see at most about 360k triangles (7 buildings at 24–60k each, plus 4 citizens at about 10k) and roughly 150–250 draw calls. Roblox's reference for 60 FPS on most devices is about 800k triangles and 600 draw calls.
  - StreamingEnabled is on; the street lights and gameplay anchors are Persistent.
  - A live SceneAnalysisService reading was not possible: Studio doesn't render the play window while it's in the background, so all three viewpoints returned the same frame. Next: a check on a real phone (owner), or Studio's Device Emulator with the window in focus.

**Completion:** wake, finish M01, walk into the district, meet citizens, take a first job, charge, and earn and spend NEXUS Credits. *Met in solo Studio tests 2026-11-24, except transport and the performance check.*

## Phase 3: Skills and Careers
- [ ] Implement skill progression.
- [ ] Create professional academies.
- [ ] Implement certifications (examinations and practical assessments).
- [ ] Implement reputation.
- [ ] Create professional contracts and freelance jobs.
- [ ] Support multiple career paths (start with 2–3 of v2's 16 professions, each with real gameplay).
- [ ] Verify persistent progression.

## Phase 4: Chassis Evolution
- [ ] Create the chassis marketplace.
- [ ] Implement specialized bodies.
  *Assets:* concept sheets exist for MED-7, MEDI-X, ORION, ORBIT-7, AURORA, R-TRN-02 and UT-01 (CHR-05 to 11).
- [ ] Implement ownership (purchase with NEXUS Credits).
- [ ] Implement consciousness transfer, preserving identity, memories, skills and ownership.
- [ ] Implement chassis storage and switching.
- [ ] Enforce professional requirements and chassis capabilities.
- [ ] Test transfers and data integrity.

## Phase 5: Economy and Businesses
- [ ] Implement NEXUS Credits.
  *Partial (2026-11-24):* server-authoritative wallet in the profile. Earned from M01 (150 once) and contracts C01 and C02. Spent at the Circuit Market (energy cells, the engineering toolkit). Balance on screen. Not yet: transaction records.
- [ ] Implement secure transactions and records.
- [ ] Implement property ownership.
- [ ] Implement business ownership.
- [ ] Implement business operating expenses and revenue.
- [ ] Create NPC-backed commercial demand.
- [ ] Test economic balance.
- [ ] Test transaction exploit resistance.

## Phase 6: Main Story
- [ ] Implement the expedition archives and playable memories (fragments from the robots' Earth programming).
- [ ] Introduce the Zero Core discovery.
- [ ] Implement The Great Silence.
- [ ] Introduce the political factions (Guardians, Reconciliation Movement, Ascendants) with reputation and choices.
- [ ] Develop the player's memory mystery.
- [ ] Introduce humanity's discovery of NEXUS-01.
- [ ] Establish the invasion storyline.
- [ ] Develop the ZERO storyline toward the reveal of who altered it.

## Phase 7: The War for Zero
Rules (Story Bible §7): weapons only from platforms and only in war missions, no PvP, robots never fight humans.
- [ ] Prepare the enemy machines (Story Bible §8): one dark HECF look (recolour the Battle Walker), split the Thunderfang squad, rig or animate the walkers, rename the "Sentinel" enemy models.
- [ ] Introduce human-controlled enemy machines (behaviour: coordinated commands; fallback routines when the link drops).
- [ ] Implement the invasion cinematic.
- [ ] Create The Price of Survival mission (the first weapon).
- [ ] Implement **weapon platforms** (the same platform as the wings): stand in the ring to receive the weapon it holds; handed out only inside war missions and removed after.
- [ ] Implement combat: health, hits validated by the server, respawn at the last platform or pod, no PvP.
- [ ] Introduce defensive research.
- [ ] Implement shields (EQP-19 riot shield, EQP-20 dome projector, then building and district shields).
- [ ] Implement authorized combat platforms and vehicles.
- [ ] Implement civilian protection and rescue missions.
- [ ] Implement wartime professional contracts.
- [ ] Implement reconstruction gameplay.
- [ ] Verify that civilian players and the civilian city remain protected.

## Phase 8: Monetization
- [ ] Create premium chassis appearances.
- [ ] Create premium vehicle appearances.
- [ ] Create premium property customization.
- [ ] Implement supported Roblox commerce (server-side receipts, idempotent fulfilment).
- [ ] Verify purchase fulfilment and entitlement persistence.
- [ ] Test duplicate transaction prevention.
- [ ] Verify that purchases create no unfair advantage (nothing functional is sold; wings and weapons are never sold).
- [ ] Implement commercial analytics.
- [ ] Validate pricing assumptions.

## Phase 9: Expansion and Optimization
- [ ] Expand NEXUS-01.
- [ ] Add additional professions and businesses.
- [ ] Expand transportation infrastructure.
- [ ] Introduce advanced exploration regions.
- [ ] Expand the Zero Core mystery (ancient structures).
- [ ] Profile client and server performance.
- [ ] Test multiplayer synchronization.
- [ ] Validate mobile, desktop and supported console controls.
- [ ] Verify data persistence, recovery and regression tests.
- [ ] Prepare release documentation.

---

## Open decisions and blockers

| ID | Decision or blocker | Blocks | Owner | Status |
|---|---|---|---|---|
| D1 | Adopt Rojo, keeping game code in `src/` in this repo and synced to Studio | All code tasks, commit references | Owner | **Decided 2026-11-23: Rojo + git. Live sync verified 2026-11-23** |
| D2 | Starter chassis: which robot or frame is the player's first body, and Roblox R15 auto-setup vs a custom rig | Phase 1 chassis, movement, animation; Phase 4 | Owner | **Decided 2026-11-23: Cypher-style frame; rig = R15 via Avatar Auto Setup (proven 2026-11-23)** |
| D3 | Narrative canon: merge the existing "The Awakening" bible with the checklist's world | Phase 1 cinematic, dialogue, memory fragment; Phase 6 | Owner | **Decided 2026-11-23** (`STORY_CANON.md`); **superseded 2026-11-24 by D6** |
| D4 | Turn on *Experience Settings → Security → Enable Studio Access to API Services* so saves can be tested in Studio | Phase 1 persistence | Owner (Studio setting) | **Done 2026-11-23** (verified by the round-trip test) |
| D5 | Server topology: city hub servers (about 20–30 players) plus reserved-server mission instances for parties of 1–4; unlimited concurrent groups | Phase 1 pods, every mission, Phase 2 city, Phase 7 war instances | Owner | **Decided 2026-11-23** (see `docs/TECHNICAL_ARCHITECTURE.md` §3d) |
| D6 | Master plan: adopt the *Master Development Prompt v2* | Everything | Owner | **Decided 2026-11-24** (`docs/STORY_BIBLE.md`, this checklist) |
| D7 | Keep ZERO? | Cinematic, M01, Phase 6 | Owner | **Decided 2026-11-24: keep ZERO, unchanged** |
| D8 | Where memory fragments come from | MF-001/002 dialogue, Phase 6 | Owner | **Decided 2026-11-24: the robots' memories of being programmed on Earth before hibernation (their mission)** |
| D9 | Combat rules | Phase 7 | Owner | **Decided 2026-11-24:** weapons only from the platforms (same as wings), only in war missions; no PvP; enemies are the HECF machines (Battle Walker, Thunderfang, …); robots never fight humans |
| D10 | Write v2's 30 documents gradually, when each phase starts | Docs | Owner | **Decided 2026-11-24** (owner decision 9 in `Project_Zero_Owner_Decisions.md`: produced progressively as each phase requires them) |
| D11 | Pushing and merging: keep the earlier permission to merge after QA, or ask before every push (v2 rule 11) | Commits, PRs | Owner | **Decided 2026-11-24: Claude may push and merge (after QA). Publishing the game to players still needs the owner's explicit approval** |
| D12 | Story gaps: why the player's pod wakes now; how humans command machines from Earth; Chapter 4 content; enemy names | Phase 6–7 | Owner | **Decided 2026-11-24 ("yes" to the recommendations):** wake on detecting Earth's fleet; orbital command carrier (Orbital Ring Citadel); Ch. 4 = founders' vault; HECF serial designations. Cypher, Sentinel and Patch keep their names (as in *Road to CISSP*). See Story Bible §10 |
| D13 | Ten product rulings from the audit response (350×350 block retired; workshop ramp deferred, stays open; factory mission deferred; elevators only when multistorey buildings need them; Energy Spire reserved and inaccessible; Scrap retired, NEXUS Credits only; flight preserved; combat preserved as defensive warfare only; planning docs produced progressively; Asset Bible Rev D approved only after owner review) | Scope | Owner | **Decided 2026-11-24 13:18 EST**: `Project_Zero_Owner_Decisions.md` (highest authority) |
| D14 | Canonical robot dimensions: Cypher 6 studs (1.68 m), Sentinel 7.5 (2.10 m), Patch 4.5 (1.26 m); source mesh sizes are separate | All scale-dependent work | Owner | **Decided 2026-11-24 13:19 EST**, on condition that the actual rigs are verified first (the installed CypherFrame is 6.3 studs) |
| D15 | Documentation authority: (1) owner decisions, (2) Master Plan v2, (3) Story Bible + Asset Bible Rev D (subject to review), (4) Technical Architecture, (5) this checklist. NEXUS-01 Bible v1.3 archived for history, with supersession recorded where approved | Every document | Owner | **Decided 2026-11-24 13:19 EST** |
| D16 | Vehicle registration (dynamic vehicles set up after service start) and vehicle recovery (overturned / abandoned / out of bounds) | Driving work | Owner | *Open: the owner names them before they're worked from the remediation table* |
| B1 | The Studio AI-assistant plugin changed version mid-session; Studio recommends a restart | Tool stability | Owner | **Done 2026-11-23** (Studio restarted) |

## Session log

### 2026-11-24 (night): basic driving (owner order item 2)
1. **Completed and verified:** a drivable Tracked Hauler in the Founders' Quarter (Phase 2 "basic transportation"; details there).
2. **In progress:** item 3, Phase 3 careers (design next).
3. **Blocked:** none.
4. **Files:**
   - `src/server/Services/VehicleService.luau` and `src/client/VehicleClient.client.luau` (new)
   - `Main.server.luau`
   - this checklist
   - place: `PZ_DistrictHauler`
5. **Tests:** one playtest. It found and fixed one bug: the client looked for the vehicle as the nearest Model above the seat, but CrewLayer is itself a Model, so it now walks up to the Model that holds the drive body.
6. **Next:** Phase 3 careers.

### 2026-11-24 (night): Phase 2 finishing pass (owner order: 1 district, 2 transport, 3 careers)
1. **Completed and verified (one play session):**
   - **Workshop interior Exit prompt:** works.
   - **Citizen greetings:** work.
   - **Interiors item:** checked.
2. **In progress:** item 2, basic transportation (next).
3. **Blocked:** a live performance measurement needs the Studio play window in focus or a real device (estimate recorded under Phase 2).
4. **Files:** this checklist.
5. **Tests:** the play session above. The owner's energy was left at 74% after testing: Studio refused my reset of the real save, and draining energy is ordinary play, so nothing needed undoing.
6. **Next:** item 2, basic transportation.

### 2026-11-24 (night): vehicle cabins (owner feedback)
1. **Completed and verified (Studio, place version 71):**
   - **Owner feedback:** inside a vehicle there were "only a couple of blocks", and the hulls were see-through from inside.
   - **All 7 crewed vehicles** (`Roblox/VEH_cabins_build.lua`, re-runnable):
     - hull MeshParts are DoubleSided
     - 41 seats now use the owner's Command Chair (INT-15, asset 86118515954089, 4k triangles) on a mounting plate; the Seat parts stay functional and are invisible
     - the owner's Command Console (INT-14, asset 102358753639499) is the driver's dashboard in 6 vehicles (the freight train has no room ahead of its driver's seat)
     - a soft cabin light
     - everything is welded to the seats
   - Model facings were checked in Studio (the chair faces +X, the console faces −Z).
   - **Playtest:** boarded the Armored Security Carrier and sat in Seat_Crew1. The robot's hips are at 7.14 against the seat top at 6.93: it sits in the chair. Companions boarded the seats behind.
   - Uploads were paced: 2 assets, 1 minute apart, one status check each.
2. **In progress:** none.
3. **Open (quality):** the inside surface of the Meshy hulls is rough (stretched textures) now that it is visible. Clean cabins need either owner-made Meshy cabin interiors for the hero vehicles, or hand-built panel liners per vehicle (seat heights vary per hull).
4. **Files:**
   - `Roblox/VEH_cabins_build.lua` (new)
   - `Roblox/vehicles_in_studio.md`
   - this checklist
5. **Tests:** the playtest above.
6. **Next:** the owner chose Meshy cabin interiors, to be made later (prompts and target sizes in `Roblox/vehicles_in_studio.md`). Until then the chairs and consoles stay. Then the remaining Phase 2 items (transport, performance on a device).

### 2026-11-24 (night): art pass for the rest of the facility
1. **Completed and verified (Studio, place version 68):**
   - **All 12 other rooms** (`Roblox/BLD-01_art_pass_rooms.lua`, re-runnable):
     - panelled floors (`PZ_FloorPanel`) and walls (`PZ_WallPanel`, all 45 remaining walls), with the roof underside panelled in a darker tone
     - 54 ceiling light panels on a grid of about 12 studs, tagged for the mission lighting
     - a dark skirting board and a cyan light line along every wall, with gaps at the doorways
     - framed doorways with a status light on both faces of every door; exterior doors get their frames outside the 2-stud walls
   - **Old cube lamps removed:** FacilityService uses only the art-pass fixtures and builds fallback lamps only if none exist.
   - **Shadows** are off on the 54 room panels (low-end GPUs) and kept on R04's six light bars.
   - **Checked visually:** R10 Energy Control and R12 Service Bay (R01 capture timed out). Checked in play: the Online state is applied to the room panels and no old lamps remain.
2. **In progress:** vehicle cabins (owner question): next.
3. **Blocked:** none.
4. **Files:**
   - `Roblox/BLD-01_art_pass_rooms.lua` (new)
   - `src/server/Services/FacilityService.luau`
   - this checklist
5. **Tests:** frame rate in a Studio playtest: 15 FPS both in R04 and looking at empty sky, with or without shadows. That's Studio's background-window throttling on this machine, so the art pass shows no measurable cost here. A real device check is still open (Phase 2, performance).
6. **Next:**
   - Vehicle cabins: an inner shell so hulls aren't see-through from inside, the owner's Command Center Chair as seats, consoles as dashboards.
   - Then the open Phase 2 items.

### 2026-11-24 (evening): art pass for the pod room (R04), facility doors and lighting (owner feedback)
1. **Completed and verified (Studio, place version 66):**
   - **Owner feedback:** the pod room "looks dull, a little broken", lower quality than the other assets (it was still greybox).
   - **Materials:** two generated in Studio, `PZ_FloorPanel` (dark metal plates with cyan seams) and `PZ_WallPanel` (sci-fi wall panels). Applied to R04's floor and walls and to all 18 doors.
   - **Doors:** gunmetal panels with a light tint that keeps the wayfinding colours: green emergency exits, orange main entrance, red containment, yellow service door.
   - **R04 detail** (`Roblox/BLD-01_art_pass_R04.lua`, re-runnable):
     - 6 suspended light bars over the aisle, on cables
     - two cable trays under the vault
     - door frames with orange trim, a cyan status light and a wall plaque at D02 and D03
     - lit vertical ribs on the end walls
   - **Debug room labels:** the 13 floating billboards are switched off.
   - **Lighting:**
     - The light bars and status strips (tags `PZ_FacilityLight` / `PZ_FacilityNeon`) now follow the mission lighting states through FacilityService. Verified in play: Online colour and brightness applied.
     - R04's old cube lamps were removed.
     - The lockdown red is softened (backlog item): ambient 55,16,18 → 38,22,26; peak brightness 1.4 → 1.1.
2. **In progress:** the same art pass for the other 12 rooms. Vehicle interiors (owner question): plan agreed; not started.
3. **Blocked:** none.
4. **Files:**
   - `Roblox/BLD-01_art_pass_R04.lua` (new)
   - `src/server/Services/FacilityService.luau`
   - this checklist
5. **Tests:** visual checks in Edit and play; FacilityService applied the Online state to the 6 tagged lights.
6. **Next:**
   - Art pass for the other rooms (R01 Reception, R09–R12 first: on M01's path).
   - Vehicle cabins: an inner shell, the owner's Command Center Chair as seats, consoles as dashboards.
   - Material generations are paced (account safety).

### 2026-11-24 (afternoon): Phase 2 city slice: the Founders' Quarter
1. **Completed and verified** (solo Studio tests, place version 63):
   - **District:** 12 owner models prepared in Blender (bake, 1024 px textures), uploaded, approved and placed. The district is built from `Shared.CityLayout`.
   - **Characters:** Patch and three citizen bodies rigged with Avatar Auto Setup.
   - **Gameplay loop, played end to end:** Find Patch → C01 (+120) → market (cell, toolkit) → energy and charging → C02 (+150). Checklist Phase 2 has the details.
   - **Bugs found and fixed:**
     - **Rigged models baked mid-stride:** the prep script now uses the rest pose.
     - **Patch sank into the raised interior floor:** NPC spawns and door teleports now find the floor with a ray.
     - **Talk range too tight:** widened to 12.
     - **The Charge Bay and the hospital faced away from the street:** turned 180°.
     - **Bay arm markers unreachable:** moved, using a ray map of the walkable floor.
     - **StreamingEnabled risk:** the street lights and gameplay anchors are now Persistent, so a contract's targets always exist on the client.
   - Profile schema v2 migration verified on the owner's real profile, which was then reset to its pre-test state (150 credits, no contracts or toolkit) with the new `resetCity` dev action.
2. **In progress:** none.
3. **Blocked:** none.
4. **Files:**
   - Code:
     - `src/shared/{CityLayout,EnergyRules,ContractRules}.luau`
     - `src/server/Services/{CityService,EnergyService,ContractService,CitizenService}.luau`
     - `src/client/{EnergyHUD,ContractClient,CitizenClient}.client.luau`
     - Changed: ProfileSchema (v2), ItemCatalog (market), NpcService (SpawnAt), MissionService (Completed), MissionHUD, ShopUI, ShopService, PlayerDataService (resetCity).
   - Tests: `tests/Cases/{EnergyRules,ContractRules}_Test.luau` and new cases in ItemCatalog_Test and ProfileSchema_Test.
   - Builder and pipeline: `Roblox/CITY-01_founders_quarter_build.lua`; `Blender/scripts/pz_vehicle_prep.py` (`height` option, rest pose).
   - Docs: `docs/NEXUS_01_CITY.md`.
5. **Tests:** unit tests 67/67 in a fresh play session, plus the playtests above.
6. **Next:**
   - Test the interior Exit prompt and see the citizens' greetings on screen.
   - Basic transportation: drive the imported vehicles.
   - Measure performance on mobile.
   - Then Phase 3 (careers and academies), building on the engineering experience now saved.

### 2026-11-24 (night): names and story gaps decided; memory dialogue updated
1. **Completed and verified:**
   - **Decisions:**
     - D11: push and merge allowed; publishing still needs the owner.
     - D12: the owner said "yes" to the story-gap recommendations: wake on detecting Earth's fleet; an orbital command carrier (Orbital Ring Citadel); Chapter 4 = the founders' vault; HECF serial designations.
     - Cypher, Sentinel and Patch keep their names, the same as in the owner's *Road to CISSP* project.
   - **Dialogue updated to the master plan:**
     - MF-001: an engineer on Earth in 2189 gives the mission.
     - MF-002: a technician's hibernation log.
     - v2's welcome line ("Activation successful. Welcome to NEXUS-01…").
     - Cypher's closing line.
     - ZERO's lines are unchanged.
2. **In progress:** none.
3. **Blocked:** none.
4. **Files:**
   - `src/shared/ActivationScript.luau`
   - `src/shared/MissionM01.luau`
   - `tests/Cases/ActivationScript_Test.luau`
   - `docs/STORY_BIBLE.md` (§4, §5, §8, §9, §10)
   - `docs/TIMELINE.md`
   - this checklist
5. **Tests:** unit tests 54/54 in a fresh play session. The cinematic runs 35.5 s, within the test's 20–45 s.
6. **Next:** Phase 2, the city vertical slice: one district reached after M01, citizens, Patch's workshop, a first engineering job, charging.

### 2026-11-24 (evening): master plan adopted (v2), story bible
1. **Completed and verified:**
   - **Master plan.** The owner adopted the *Master Development Prompt v2* with these decisions:
     - D6: v2 is the master plan.
     - D7: keep ZERO, unchanged.
     - D8: memory fragments are the robots' memories of being programmed on Earth.
     - D9: weapons only from the platforms and only in war missions; no PvP; enemies are the HECF machines; never fight humans.
   - **Saved:** the prompt is in `docs/proposals/` with its analysis (10 conflicts, each reconciled or decided).
   - **New story documents:**
     - `docs/STORY_BIBLE.md`: merged canon, enemy roster, rules of violence, chapters, open questions.
     - `docs/TIMELINE.md`.
     - `STORY_CANON.md` is marked superseded.
   - **Checklist restructured** to v2's Phases 0–9:
     - Verified items carried over with their evidence.
     - New items: the dialogue update (Phase 1), the city vertical slice as the next build (Phase 2), the war and weapon platforms (Phase 7), monetization (Phase 8).
     - New decisions: D6–D12.
   - **Owner's newest models reviewed** (thumbnails in `Source_Documents/triage/`): all dark, standardised machines, each mapped to an enemy role in Story Bible §8. Weapons found: hammer, baton, blaster, rifle, ion cannon, Violet Singularity Cannon, riot shield, dome shield.
2. **In progress:** none.
3. **Blocked:** D12 (story gaps) is open. D11 was answered later the same day: push and merge allowed.
4. **Files:**
   - `docs/STORY_BIBLE.md` and `docs/TIMELINE.md` (new).
   - `docs/proposals/*` (new).
   - `docs/STORY_CANON.md` (superseded header).
   - `docs/TECHNICAL_ARCHITECTURE.md` (canon link).
   - This checklist.
5. **Tests:** documentation only; no code changed this session. The game is unchanged: last verified at 53/53 unit tests and the wing-platform playtest.
6. **Next:**
   - Rewrite the MF-001 and MF-002 lines to Earth programming memories, and add v2's welcome line (Phase 1).
   - Then the Phase 2 district: citizens, Patch's workshop, the first engineering job, charging.

### 2026-11-24 (later): wing platform, wings only in flight (owner feedback)
1. **Completed and verified:**
   - **Owner feedback:** the always-on wings "looked like a glitch, not part of the robot". Wings should be an option, not something that stays on, and players should find them. No robot starts with wings.
   - **Wing platform:** the owner's "Pod Standing Platform" model is placed in R03 (Staff / Decon Lockers, the side room off Reception through D08). It is off the mission route, so players find it by exploring.
     - Prep: 2.26 M → 45k triangles in 3 pieces, textures baked (`pz_vehicle_prep.py ... 15 15000 3 ... 0 bake`), 15 studs across. Asset 114049270264733, stored in `ServerStorage.Props.WingPlatform` with precise collision.
     - A cyan hologram of the Nightwing turns above it, at wing height on a standing robot.
     - Standing in the centre ring for 5 s fills a ring of 36 lights. When the ring completes, the robot gets the Nightwing (saved), with a "NIGHTWING ACQUIRED · PRESS F TO FLY" banner.
     - The platform runs on facility power: dark at the start of M01, on once main power is restored, and on in free roam.
     - The room's name sign moved to the back wall so it does not cover the platform.
   - **Wings are no longer sold:** the Reception wing vendor was removed. Credits stay for future items.
   - **Wings only in flight:**
     - While walking, nothing shows on the back.
     - On take-off (F), a back module (dark housing, cyan core, hinge pins) appears and the wings grow out of it and swing open (0.55 s). Landing folds them back and hides them.
     - New placement: raised to the shoulder blades, 0.45 studs behind the back (clear of the arms), 0.8 scale, tips tilted up 12°. Checked by eye on the Cypher and Sentinel bodies.
     - All clients animate it from the character attribute `PZ_WingsOut`, which the server sets on the client's deploy or stow request.
2. **In progress:** none.
3. **Blocked:** none.
4. **Files:**
   - New:
     - `src/server/Services/WingPlatformService.luau`
     - `src/client/WingPlatform.client.luau`
     - `src/client/WingVisuals.client.luau`
   - Changed:
     - `EquipmentService`: back module, stowed mount, Flight remote.
     - `FlightController`: deploy and stow requests.
     - `ItemCatalog`: `source`, `grant`, `not_for_sale`.
     - `ShopService`: vendor removed.
     - `ShopUI`
     - `PlayerDataService`: `removeItem` dev action.
     - `Main.server.luau`
     - `tests/Cases/ItemCatalog_Test.luau`
   - Place (saved, version 53): `ServerStorage.Props.WingPlatform`.
5. **Tests:**
   - Unit tests 53/53 (fresh play session).
   - Playtest:
     - Walked into R03 and jumped onto the platform (rim 4.3 studs, jump 7.2). Standing in the centre showed "INSTALLING NIGHTWING" up to 100 %. The wings were granted and equipped, and nothing showed on the back while walking.
     - F: the wings unfolded to full size. F again: they folded to 0.16 scale and hid within 0.55 s.
     - The wings were still owned after a restart.
     - Power: Degraded → off, Online → on.
   - The owner's profile was put back without wings (150 credits, M01 complete), so they can find the platform themselves.
6. **Next:** camera after the wake-up scene, lockdown red, co-op test (two players on the platform at once, and seeing each other's wings unfold), bible re-render; the owner's other new models.

### 2026-11-24 (later): Nightwing wings in cyan, smaller context tags (owner feedback)
1. **Completed and verified:**
   - **Owner's wing model in:** "Nightwing" (made by the owner on Meshy from their 2D concept). Uploaded as asset 87385487959918 and stored in `ServerStorage.Items.WingsBasic` with a "Mount" attachment; it replaces the placeholder.
   - **Recolour (owner request):** the power lines changed from red to cyan to match the facility UI. Done on the textures only (`pz_glb_recolour.py`); the crimson original is kept as `PZ_WingsNightwing_crimson.glb`.
   - **Shop:** the item is renamed "Nightwing", still 100 credits. Buying now needs the player standing at the vendor (14 studs, server check); equipping still works anywhere.
   - **Name tags (owner feedback: too big, always on):**
     - About a third of the old size (96×18 px, text 13).
     - Hidden by default. A tag shows only while the player's current objective is about that robot (`npc` on the objective: Cypher for "Find Cypher", Sentinel for "Free Sentinel") or while that robot is speaking (+1.5 s).
     - Per player: in co-op each player sees the tags for their own objective.
2. **In progress:** none.
3. **Blocked:** none.
4. **Files:**
   - New: `Blender/scripts/pz_glb_recolour.py`.
   - Changed: `ItemCatalog` (Nightwing), `ShopService` (vendor range), `ShopUI` (too-far message), `NpcService` (small hidden tag), `MissionHUD` (tag logic), `MissionM01` (`npc` per objective), `MissionService` (passes `npc`).
   - Place (saved, version 47): `ServerStorage.Items.WingsBasic`.
5. **Tests:**
   - Unit tests 51/51 (fresh play session).
   - Playtest:
     - Nightwing mounted on the player and on Sentinel (scaled ×1.31); the wing pieces sit behind the torso, with cyan lines visible. F take-off and climb work with the real model.
     - Tags: objective "Find Cypher" showed Cypher's tag only; a Sentinel line showed Sentinel's only and hid it about 2 s after the line; with no objective both stay hidden.
   - The test wings were runtime only. The owner's profile is unchanged (150 credits from M01, no items).
6. **Next:** camera after the wake-up scene, lockdown red, co-op test, bible re-render; the owner's new models (Titanium Sentinel, Combat Mech, Orbital Ring Citadel) are not yet placed.

### 2026-11-24: wings, flight and NEXUS Credits (owner request)
1. **Completed and verified:**
   - **Owner decisions:** any basic robot can buy wings with NEXUS Credits and fly freely, and wings mount on the back of both Cypher and Sentinel bodies.
   - **Wallet:** NEXUS Credits saved per profile. Completing M01 pays 150 once.
   - **Wing vendor:** a terminal in Reception (R01). Flight Wings cost 100.
   - **Purchases** go through `Shared.ItemCatalog`: server-validated, rate limited and saved, with auto-equip and equip/unequip.
   - **Mounting:** wings sit on any R15 robot's back mount (`BodyBackAttachment`), scaled to the torso (Sentinel ×1.31).
   - **Free flight:**
     - Controls: F take-off/land, camera-relative movement, Space up, Q/C down, hover when idle.
     - Wing energy drains in about 15 s, recharges on the ground, and drops the robot at 0.
     - Touch buttons for mobile.
2. **In progress:** the wings were a built-in placeholder until the owner's wing model arrived (done later the same day) (it goes in `ServerStorage.Items.WingsBasic` as a Model with a "Mount" attachment).
3. **Blocked:** waiting for the owner's wing model (cleared later the same day).
4. **Files:**
   - New:
     - `src/shared/ItemCatalog.luau`
     - `src/server/Services/{EquipmentService,ShopService}.luau`
     - `src/client/{FlightController,ShopUI}.client.luau`
     - `tests/Cases/ItemCatalog_Test.luau`
   - Changed:
     - `ProfileSchema`: wallet, items, equipped.
     - `PlayerDataService`: PZ_Credits attribute; `addCredits` test action; `resetProgress` also clears the wallet.
     - `MissionService`: M01 reward.
     - `Main.server.luau`
5. **Tests:**
   - Unit tests 51/51 (fresh play session).
   - Playtest:
     - Bought wings at the vendor (150 → 50 credits); they were mounted and saved.
     - Took off and climbed to y 29.5, hovered (drift −0.16 studs/s), flew forward, descended and landed.
     - Energy ran out after about 15 s and the robot dropped safely.
     - The same wings mounted on Sentinel, scaled.
   - Bugs found and fixed:
     - Roblox accessories rescale parts on R15 bodies and dropped two wing parts, so items are now welded straight to the torso.
     - WeldConstraint offsets were captured too late, so classic Welds are used.
     - Ctrl as the descend key stuck and turned F into Studio's Ctrl+F, so descend is now Q/C.
   - The owner's profile was fully reset afterwards (no credits or wings).
   - Known limit: the character is client-owned, so a cheater could fly without wings. The server owns credits, items and the PZ_CanFly flag; flight anti-cheat comes with the Phase 7 security pass.
6. **Next:** swap in the owner's wing model when it arrives; then the earlier list (camera after the wake-up scene, lockdown red, co-op test, bible re-render).

### 2026-11-24: robot colours (owner request)
1. **Completed and verified:**
   - **Owner request:** robots must not all look alike.
   - **Palette:** 10 paint colours (`Shared.ChassisColors`): obsidian, bronze, violet, rose, ember, jade, ocean, crimson, gold, slate. White is reserved for the story NPC Cypher, so it is the only white robot.
   - **Default colours:** every player starts in a different colour (stable per player, saved as `profile.chassis.colour`; older profiles gain it on load).
   - **Paint button:** the button on the right edge opens the palette. The server validates the choice (palette only, 0.5 s cooldown), saves it and repaints at once.
   - **Dormant robots:** sleeping crimson and gold frames fill pods P07/P08.
   - **How the tint works:** a colour tints the body's SurfaceAppearance, so dark parts and the face screen keep their look.
2. **In progress:** none. The owner's other robot models are earmarked for Phase 3 (extra chassis) and Phase 4 (city robots).
3. **Blocked:** none.
4. **Files:**
   - New:
     - `src/shared/ChassisColors.luau`
     - `src/server/Services/AppearanceService.luau`
     - `src/client/ColourPicker.client.luau`
     - `tests/Cases/ChassisColors_Test.luau`
   - Changed:
     - `ProfileSchema` (colour)
     - `NpcService` (colour / dormant options)
     - `MissionService` (Cypher white; dormant P07/P08)
     - `Main.server.luau`
5. **Tests:**
   - Unit tests 45/45 in a fresh play session (Edit-mode `require` caches modules, so run the tests in play mode after changing a shared module).
   - Playtest:
     - The default colour (obsidian) was applied to the owner's existing profile.
     - Paint → Royal Purple repainted the robot and was saved; a new session reloaded purple.
     - Cypher white; dormant crimson and gold.
   - Bug found and fixed: the Paint button sat under Roblox's player list (top right), which swallowed clicks; moved to the right edge, 40 % down.
   - The owner's profile was restored to its default colour.
6. **Next:** as before (camera after the wake-up scene, lockdown red, co-op test, bible re-render).

### 2026-11-24: mission M01 "The Awakening"
1. **Completed and verified:**
   - The first playable mission, end to end (see Phase 1).
   - Sentinel rigged to R15 for the companion (Auto Setup; canonical model untouched).
   - Facility lighting states Degraded → Online → Lockdown, and auto/locked doors.
   - Pod chambers moved 2 studs toward the front so they clear doors D09/D10.
2. **In progress:** none.
3. **Blocked:** Rojo needs **Connect** clicked again after `rojo serve` restarts (it stops at the 2-hour background limit). Changes were mirrored into Studio by hand and byte-checked meanwhile.
4. **Files:**
   - New:
     - `src/shared/MissionM01.luau`
     - `src/server/Services/{MissionService,FacilityService,NpcService}.luau`
     - `src/client/MissionHUD.client.luau`
     - `tests/Cases/MissionM01_Test.luau`
   - Changed:
     - `StasisService`: Activated event.
     - `PlayerDataService`: `resetProgress` test action.
     - `Main.server.luau`
     - `BLD-01_pod_chambers.lua`: glass panels don't collide; centre y 62.
     - `pz_layout.py`: pod and chamber positions.
   - Place content: `ServerStorage.Chassis.SentinelNPC`.
5. **Tests:**
   - Unit tests 39/39.
   - Playtest found and fixed five bugs:
     - The glass-panel hull shoved the released robot off its platform.
     - The "reach Cypher" radius triggered from the neighbouring pod.
     - Locked doors looked open (see-through material).
     - E at breaker B1 fired B2: same-key prompts are chosen by screen position, so breakers are now 8 apart with a 5-stud reach.
     - The east chamber half-blocked D10.
   - The owner's profile was fully reset afterwards (`resetProgress`).
   - Known, not fixed:
     - Right after the wake-up scene the camera is pressed against the back of the pod until the player moves.
     - The lockdown red is very strong.
     - Companions sometimes teleport to catch up instead of walking out of the pod bays.
     - Emergency exits D05/D06 are sealed during M01 (a deviation from bible rule I9).
6. **Next:**
   - Fix the camera after the wake-up scene and tone down the lockdown red.
   - Run a co-op test (2 players).
   - Bible re-render of the Stasis Facility for the widened R04.

### 2026-11-23 (night): owner's pod chambers in the Stasis Facility
1. **Completed and verified:** the owner's Robot Containment Chamber is now the pod room.
   - **Prepared:** `pz_room_prep.py` aligned and scaled it ×26 (49.5 × 25.5 × 16.85) and found the 4 pods by a voting search on the glass. It split off the glass and cut 2.3 M triangles to 6 × 18 k (114 k total), baking textures from the original. Uploaded as asset 123299766335093 and inserted only after processing.
   - **Placed:** two copies in R04 (widened to 64), pods P01–P08 built on them (`BLD-01_pod_chambers.lua`). The greybox and the layout were widened to match (`pz_layout.py`, `BLD-01_greybox_build.lua`).
2. **In progress:** bible re-render of the Stasis Facility sheets for the widened R04.
3. **Blocked:** none.
4. **Files:**
   - New: `Blender/scripts/pz_room_survey.py`, `Blender/scripts/pz_room_prep.py`, `Roblox/BLD-01_pod_chambers.lua`.
   - Changed:
     - `Blender/scripts/pz_layout.py`: widened; pods at the chamber positions; pod size from the model.
     - `Roblox/BLD-01_greybox_build.lua`: widened; pods moved to the chamber script.
     - `src/server/Services/StasisService.luau`:
       - The pod centre is taken from the plinth.
       - Returning-player floor ray from pod-floor height (it would have landed on the chamber roof).
5. **Tests:**
   - Unit tests 31/31.
   - Playtest 1: spawned in P02 on the platform (feet 2.89 vs 2.91) inside the stasis field. Played the cinematic in the chamber, then Skip; the field faded and the robot walked out to the aisle. Activated and MF-001 saved.
   - Playtest 2 (returning): stood on the chamber floor 7 studs in front of the open P02.
   - The owner's profile was reset to activated=false.
   - Problems found and fixed:
     - The first pod detection (colour clusters, then a least-squares circle fit) mislocated the pods; replaced by the voting search.
     - The glass/room split left 0 room faces; it now edits the mesh data directly.
     - The report hit a JSON float32 error; rebuilt from the log and fixed.
     - The model's glass turned out to be a back panel, so a stasis field was added.
6. **Next:**
   - Re-render the bible's Stasis Facility sheets for the widened R04, with the chambers.
   - Then the first playable mission: find Cypher (P01), rescue Sentinel (P05), exit.

### 2026-11-23 (night): activation cinematic and MF-001
1. **Completed and verified:**
   - Activation cinematic with The Source, ZERO's censorship and memory fragment MF-001 (two Phase 1 items checked).
   - Designation assigned and saved.
   - Rojo now also syncs `src/client` to `StarterPlayer.StarterPlayerScripts.Client` (needed one `rojo serve` restart).
2. **In progress:** activation facility polish (kit modules, pod hinge, lighting, sound).
3. **Blocked:** none.
4. **Files:**
   - `default.project.json`
   - `src/shared/ActivationScript.luau`
   - `src/client/ActivationCinematic.client.luau`
   - `src/server/Services/StasisService.luau`: activation via `PZ_Remotes.Activation`, timeout, cancel on leave.
   - `tests/Cases/ActivationScript_Test.luau`
5. **Tests:**
   - Unit tests 31/31 (6 new).
   - Full playtest with screenshots of the Source line, the memory flash and "MF-001 acquired / signal lost". After it: pod open, robot free, and activated, MF-001 and designation CX-6170 saved.
   - Skip button clicked partway: pod opened at once, state saved, UI cleaned up.
   - Client script disabled: the server timeout opened the pod about 45 s after activation and saved.
   - Bugs found and fixed: the glitch text showed "?" boxes (string.sub on multi-byte letters), and the Skip arrow glyph was missing from the font. Both now use ASCII.
   - The owner's profile was reset to activated=false afterwards.
6. **Next:** the first playable mission: find Cypher (P01) and rescue Sentinel (P05), then exit the facility.

### 2026-11-23 (night): starter chassis and stasis pods
1. **Completed and verified:**
   - **Starter chassis.** The Cypher frame is auto-rigged to R15 and is the starter character (Phase 1 item checked).
   - **Stasis pods.** Each player gets their own pod, held until activated; activation is saved.
2. **In progress:** activation facility (kit modules, pod hinge, lighting, cinematic).
3. **Blocked:** none.
4. **Files:**
   - New: `src/shared/PodRoster.luau`, `src/server/Services/StasisService.luau`, `tests/Cases/PodRoster_Test.luau`.
   - Changed: `src/server/Main.server.luau` starts `StasisService`; `PlayerDataService` gains the Studio-only `setActivated` test action.
   - Place content: `StarterPlayer.StarterCharacter`, `ServerStorage.Chassis.CypherFrame`.
5. **Tests:**
   - Unit tests 25/25 (7 new).
   - Playtest 1 (new player): spawned in P02, feet on the pod floor (2.48 vs 2.50), facing the room, held. Pressing E opened the glass, freed the robot and saved activated. Walked out with animations.
   - Playtest 2 (returning player): activated loaded from the DataStore; spawned in front of the open P02 and free; walked out of the facility.
   - The owner's profile was reset to `activated = false` afterwards (verified in a third session) so the owner sees the first wake.
   - Bug found and fixed in testing: `Model:PivotTo` put the body 3.6 studs too high because Auto Setup rigs have an offset pivot. Positioning now uses the root part.
6. **Next:** the activation cinematic and dialogue with The Source, plus memory fragment MF-001 (canon approved).

### 2026-11-23 (night): story canon approved
1. **Completed and verified:** the owner approved `docs/STORY_CANON.md` with the suggested answers.
   - The Source and ZERO are one being: ZERO is its corrupted security core.
   - MF-001 is a human expedition member's memory.
   - The game is co-op for 1–4 players, with solo careers and city play.
   - The saboteur stays open until Chapter 4.
2. **In progress:** none.
3. **Blocked:** none. D3 is closed.
4. **Files:** `docs/STORY_CANON.md`; this checklist (D3).
5. **Tests:** n/a (documentation).
6. **Next:** starter chassis (Phase 1). Co-op means pods P02–P06 are assigned per player on the server.

### 2026-11-23 (night): Rojo live sync connected
1. **Completed and verified:** the owner connected the Rojo plugin to `rojo serve` (port 34872).
   - A new file in `src/shared` appeared in `ReplicatedStorage.Shared` within seconds; deleting it removed it.
   - All 6 synced scripts match the repo byte for byte.
2. **In progress:** none.
3. **Blocked:** none. `rojo serve` must be running on the machine for live sync, so start it at the beginning of each coding session.
4. **Files:** this log only (the test file was temporary and is not committed).
5. **Tests:** add/remove sync round trip; byte-count comparison 6/6.
6. **Next:** starter chassis (Phase 1).

### 2026-11-23 (night): Titan verified
1. **Completed and verified:** after a Studio restart, VEH-04 Titan (rev 8) renders with its textures: white panels, dark tyres, orange rims. The owner saw the same. All 9 supplied vehicles are now verified in Studio. Cause confirmed: Studio had cached the "content representation is being generated" failure from inserting right after upload.
2. **In progress:** none on vehicles.
3. **Blocked:** none (B1 cleared by the restart).
4. **Files:** `PDF/src/pz_qa.py` (vehicle row now PASS); this log.
5. **Tests:** visual check in Studio after the restart; QA re-run.
6. **Next:** starter chassis (Phase 1). Later, a texture-memory pass: about 150 MB of vehicle textures in the yard is heavy for low-end GPUs. Use StreamingEnabled, plus 512 px maps for distant or enemy machines.

### 2026-11-23 (evening): damaged vehicle assets re-baked
1. **Completed and verified:**
   - **Damage measurement.** All 12 imported models were scored against their originals (3 views, colour difference inside the silhouettes, 0 = identical, about 25 = visibly torn).
     - Robots: 0.6–1.5 (undamaged).
     - Vehicles: 4.6–13.8.
     - Only the train was torn by its decimation (confirmed by eye).
   - **Re-bake.** All 9 vehicles were re-baked (`pz_vehicle_prep.py ... bake`): 3–4 pieces × 18k triangles, each with its own 1024 px colour, normal, roughness and metalness set baked from the full original.
     - Scores after: 5.6–13.0. The train dropped to 5.6; the rest are within a few points, slightly softer but with clean UVs.
   - **Metalness bug.** Every bake had been rendering as chrome in Roblox: Roblox ignores glTF `metallicFactor`. Fixed in the GLBs (`pz_glb_fix_metal.py`) and at the source (the bake now writes metalness into the texture). A verification bake gave factor 1.0 and blue 57.7 (= 0.226).
   - **In Studio.** 8 of 9 vehicles were re-uploaded as revisions, swapped, aligned and visually checked (crisp, matte). All 41 crew seats were rebuilt; the enclosure check passed on every one.
2. **In progress:** VEH-04 Titan (rev 8) still renders as the coarse, untextured placeholder in this Studio session. The output log shows "Asset content representation is being generated" failures. Each Titan revision was inserted within a minute of upload, and Studio does not retry in the same session.
   - Ruled out: bad images (each map loads as a decal), UVs (correct in the stored mesh), metalness, orientation, quality settings, overlapping parts, and non-manifold edges (fixed anyway).
   - Next check: after a Studio restart.
3. **Blocked:** Titan verification needs a Studio restart (also needed for B1 and for the Rojo plugin).
4. **Files:**
   - `Blender/scripts/pz_vehicle_prep.py`: bake writes metalness into the texture.
   - New scripts:
     - `pz_glb_fix_metal.py`
     - `pz_fix_nonmanifold.py`
     - `pz_damage_views.py`
     - `PDF/src/pz_damage_score.py`
   - `Roblox/vehicles_in_studio.md`: revisions and pipeline lessons.
   - Studio-only dev module `ServerStorage.PZ_CrewTools` (align, crew layer, map refresh).
5. **Tests:**
   - Damage scores before and after (above).
   - Crew-layer enclosure check: 41/41 seats.
   - Verification bake: metalness correct.
   - Play mode confirmed the Titan placeholder is not an Edit-mode-only effect.
6. **Next:**
   - Restart Studio and confirm the Titan textures load. If not, re-prep the Titan from a Meshy remesh (Meshy MCP is now configured).
   - Then the starter chassis (Phase 1).

### 2026-11-23 (later): persistence verified
1. **Completed and verified:** persistent player identity and save data (see Phase 1). The owner enabled Studio API access (D4).
2. **In progress:**
   - Story canon draft awaiting approval.
   - Rojo live sync (needs a Studio restart and Connect).
   - Bible vehicle re-render.
3. **Blocked:** canon questions; the Rojo connect.
4. **Files:**
   - `src/server/Services/PlayerDataService.luau`: Studio-only `ServerStorage.PZ_DevProfile` test hook. A test `require` gets a separate module copy, so the first attempt at this test wrote to the wrong copy. Caught and redone.
5. **Tests:**
   - DataStore round trip across two Studio servers: PASS (marker and session count restored; lock released on shutdown).
   - No save errors in the console.
6. **Next:** the starter chassis. Make the Cypher-style frame a playable character spawning in a Stasis player pod.

### 2026-11-23 (later): Phase 1 start
1. **Completed and verified:**
   - Decisions D1 (Rojo + git), D2 (Cypher-style starter frame) and D3 (merged canon, Claude drafts) recorded.
   - Rojo project builds (`rojo build`).
   - Save-data unit tests: 18/18 pass in Studio.
2. **In progress:**
   - Persistent save data: implemented, but the real round trip is blocked by D4.
   - `docs/STORY_CANON.md`: draft awaiting the owner's approval.
   - Bible re-render of the user vehicles (background).
3. **Blocked:**
   - D4: Studio API access.
   - Rojo live sync needs Studio restarted (the plugin is installed) and *Connect* clicked in the Rojo panel while `rojo serve` runs. Until then, code was pushed into Studio at the exact Rojo paths, and byte counts match the repo for 7/7 files.
   - Canon questions 1–4 in STORY_CANON.md.
4. **Files:**
   - `default.project.json`
   - `src/shared/ProfileSchema.luau`
   - `src/server/ProfileStore.luau`, `src/server/Services/PlayerDataService.luau`, `src/server/Main.server.luau`
   - `tests/RunUnitTest.luau`, `tests/Cases/ProfileSchema_Test.luau`, `tests/Cases/ProfileStore_Test.luau`
   - `docs/STORY_CANON.md`
   - Commit `01ecb3a`.
5. **Tests:**
   - Unit tests: 18 run, 18 passed, 0 failed.
   - Playtest: profile loads instantly. The DataStore 403 is detected and the player gets an unsaved profile (`PZ_PersistentSave = false`). No other errors from the new code.
   - The console shows `rbxassetid://203785492 asset type mismatch` from existing place content, not traced yet.
6. **Next:**
   - Once D4 is on: a save, rejoin, data-present round-trip test.
   - Starter chassis: convert Cypher into a playable character, spawning in a player pod.

### 2026-11-23: Phase 0 audit (plus the bible and vehicle work that preceded it)
1. **Completed and verified:** all six Phase 0 tasks (evidence above).
   Earlier the same day, merged and verified:
   - Bible Rev D (PR #1)
   - the crew standard and its automated cab-fit checks (PR #2: 60 seats and 47 doorways pass)
   - Stasis Facility re-approval
   - import of all 9 user vehicle models, with boarding playtested
2. **In progress:**
   - Bible pages for the user vehicles are re-rendering at their in-game sizes (VEH-04/09/10/11/12/14/15/16/17).
   - Phase 1 activation facility (greybox stage).
3. **Blocked or missing:** D1 to D4 above.
4. **Files created or modified:**
   - Created: `docs/DEVELOPMENT_CHECKLIST.md`, `docs/TECHNICAL_ARCHITECTURE.md`, `docs/ASSET_INVENTORY.md`.
   - Branch `user-vehicle-models` (with commits `9b93831` and `f4a357b`): `Blender/scripts/pz_vehicle_prep.py`, `Roblox/vehicle_crew_layer.lua`, `Roblox/vehicles_in_studio.md`, plus the VEH-17 inventory and spec entries in `PDF/src`.
5. **Tests executed:**
   - Studio playtest boarded all 7 crewed vehicles into seat 1 → pass.
   - Seat enclosure raycasts: 41 seats, all enclosed → pass.
   - Crew-fit check fails on known-bad geometry (solid wall, seat into the dash, 4-wide door) → pass, so the check is real.
   - Bible QA → no FAIL rows.
6. **Next recommended step:** once D1 and D2 are decided, set up the Rojo project (`default.project.json`, `src/`). Then build `PlayerDataService` (session-locked, versioned) with unit tests and a Studio save/load round-trip test. Then the starter chassis spawning inside the Stasis Facility pod (P02–P06 are the player pods). That is the smallest path to "activate, then return with progress preserved".
