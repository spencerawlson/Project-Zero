# Project Zero: Development Checklist

Repository: https://github.com/spencerawlson/Project-Zero · Roblox place: ProjectZero (place 102202818249033, universe 10778699105)

**Rules:**
- `[x]` means implemented **and** verified, with evidence noted. `[ ]` means not done, or not verified. Partial progress is noted in *italics* and stays unchecked.
- Record blockers, test results and commit references.
- Don't claim a feature works without testing it.
- Priority: a small, fully playable Project Zero first. Don't build the city at scale while fundamental gameplay systems are missing.

Related documents: [Technical Architecture](TECHNICAL_ARCHITECTURE.md) · [Asset Inventory](ASSET_INVENTORY.md) · [Story Canon (draft)](STORY_CANON.md) · [Vehicles in Studio](../Roblox/vehicles_in_studio.md)

---

## Phase 0: Repository Audit

- [x] **Inspect the entire repository and identify its existing architecture.**
  The repo is the production bible plus asset pipeline: Python, Blender and Luau builders, 29 `.py`, 25 `.sh`, 2 `.lua`, and about 2,000 generated images and JSON files. There is no game code. See Technical Architecture §1a.
- [x] **Confirm the Roblox Studio and Luau development workflow.**
  Confirmed working: Studio over MCP (Edit-mode Luau, playtests with server-side assertions, console checks, screen captures); Open Cloud uploads with `asset:read`/`asset:write` granted and an approved upload folder.
  Gap: game code isn't in git. Rojo 7.7.0 is installed but not configured (decision D1).
- [x] **Inventory existing robots, buildings, vehicles, weapons, animations and other assets.**
  119 bible assets plus loose files; 12 in Studio plus the Stasis Facility greybox. See [Asset Inventory](ASSET_INVENTORY.md).
- [x] **Identify reusable code and missing dependencies.**
  - Reusable: `vehicle_crew_layer.lua` (seats, Board prompt, server boarding script, yaw alignment, enclosure check); `BLD-01_greybox_build.lua`; `pz_vehicle_prep.py`; the crew standard and its fit checks; the Roblox specs per asset.
  - Missing: playable robot rig (G2), persistence (G3), UI, remotes and input (G4), narrative canon (G5), Luau tests (G6). See Technical Architecture §2.
- [x] **Create the technical architecture and asset inventory documents.**
  `docs/TECHNICAL_ARCHITECTURE.md` and `docs/ASSET_INVENTORY.md`.
- [x] **Verify the existing project can be opened or built.**
  - **Place:** opens in Studio in Edit mode (`list_roblox_studios` → mode Edit, saved to Roblox).
  - **Playtest:** starts and stops cleanly. All 7 crewed vehicles board a player into seat 1, and the console shows no script errors, only Studio's plugin-version warning.
  - **Bible:** the build passes (`pz_finalize.py` exit 0; 196 pages; QA has no FAIL rows).

**Phase 0 completion:** audit report, asset inventory and verified baseline are done (2026-11-23).

## Phase 1: First Consciousness

- [ ] **Create the robotic activation facility.**
  *In progress:* the BLD-01 Stasis Facility is the activation facility. It's approved (SF-01 to 05) and the greybox is built in Studio: 13 rooms, 18 doors at least 6×10 that pass a widest-robot probe, and 8 pods.
  *Done 2026-11-23:* `StasisService` assigns each party member their own player pod (P02, P03, P04, P06, using the `PodRoster` unit tests). A new player is held in the closed pod; holding **Activate** (E) opens the glass, frees the robot and saves `progress.activated = true`. A returning player spawns in front of their open pod. Verified in playtests with the real DataStore across sessions.
  *Done 2026-11-23:* the pods are the owner's **Robot Containment Chamber** (INT-12): two chambers, four pods each, one along each side wall of R04 with the open side facing the aisle.
  - **R04 widened** from 48 to 64 studs (facility 88 to 104 wide; decided by the owner) so both fit at a scale where a pod holds Sentinel (7.5).
  - **Closed state:** each pod is closed by a cyan stasis field on its platform, which fades out on activation. The model's glass panels sit at the back of each bay and stay as decoration.
  - **Verified in playtests:** spawn on the pod platform, the full cinematic, walking out to the aisle, and the returning player standing on the chamber floor.
  Not done: lighting states, sound, the bible SF sheets for the widened R04 (layout data updated; renders pending), kit modules.
- [x] **Implement the standard starter chassis.**
  Verified 2026-11-23 in Studio playtests:
  - **Rig:** the Cypher mesh was auto-rigged with Roblox Avatar Auto Setup (Development) into an R15 character, 6.3 studs tall. It is installed as `StarterPlayer.StarterCharacter`, with a master copy at `ServerStorage.Chassis.CypherFrame`. The canonical `PZ_Cypher` is untouched.
  - **Movement:** walks with the rig's own animations (Running state).
  - **Fit:** walked from the pod chamber out through the facility's doors to the outside spawn.
- [ ] **Implement movement, camera and interaction.**
  *Partial:* ProximityPrompt boarding with server validation works on 7 vehicles. Movement and camera are still Roblox defaults.
- [x] **Create the activation cinematic and dialogue with The Source.**
  Verified 2026-11-23 in playtests:
  - **Script:** `src/shared/ActivationScript.luau`, 10 beats from the approved canon, 32.5 s. Covers The Source, ZERO's censorship, the human memory flash, "MF-001 acquired" and "signal lost".
  - **Client scene:** `src/client/ActivationCinematic.client.luau`. Letterbox, the camera pushes in through the glass, typewriter subtitles, a red glitch, flicker and shake for ZERO, a warm desaturated grade for the memory, and a Skip button.
  - **Server:** holds the pod closed until the client reports done, with a timeout.
  - Placeholder until a dialogue pass: there is no voice or sound yet.
- [x] **Introduce the mysterious corrupted memory fragment.**
  Verified 2026-11-23: activation grants **MF-001** (a human expedition member's memory, tagged "not yours, keep it safe"). It's saved as `progress.memoryFragments["MF-001"] = true`. The Source's designation is saved as `identity.designation` (e.g. CX-6170; stable per player). A fragment viewer comes with the memory-fragment system later.
- [x] **Implement the first playable mission.**
  M01 "The Awakening" (owner-approved plan, 2026-11-24): find Cypher, then restore power (3 breakers in a random order shown on a console), then free Sentinel, then escape through D03 / R12 / D04 during ZERO's lockdown. Optional: MF-002 medical console. Cypher and Sentinel follow the player. No combat.
  - **Code:**
    - `Shared.MissionM01` (pure rules and dialogue, 8 tests)
    - `MissionService`
    - `FacilityService` (doors, lighting states, props)
    - `NpcService` (R15 companions, pathfinding follow)
    - `MissionHUD` client (objective panel, waypoints, subtitles)
  - **Verified 2026-11-24, one solo playthrough in Studio with the real DataStore:**
    - Every step played, with the right dialogue and lighting at each.
    - A wrong breaker order resets.
    - MF-002 granted.
    - Resuming from the restore-power checkpoint works, as does free roam after completion.
  - *Not yet tested:* co-op with 2+ players.
- [x] **Implement persistent player identity and save data.**
  Verified 2026-11-23:
  - **Profile:** keyed by Roblox UserId; schema v1; starter chassis `CypherFrame`; `createdAt` set.
  - **Session-locked store, unit tests:** 18/18 pass.
  - **Real DataStore round trip in Studio** (API access on): session 1 wrote marker `RT-1795474515` and stopped. Session 2, a new server, loaded the marker and the session count 3, and loaded instantly, which proves the shutdown save released the lock. `PZ_PersistentSave = true`. The test marker was then removed.
  - *Follow-up:* The Source assigns `identity.designation` at activation (done 2026-11-23). Letting the player rename it later needs Roblox text filtering.

**Completion:** a new player can activate, complete the introductory mission, and return with progress preserved.
*Met in a solo Studio playthrough 2026-11-24.* Open in this phase: the movement / camera item, facility polish (sound, kit modules), and a co-op test.

## Phase 2: Skills and Careers
- [ ] Implement skill trees and experience progression.
- [ ] Create engineering, medicine, research, security and exploration career paths.
- [ ] Implement professional training academies.
- [ ] Implement certification examinations and practical assessments.
- [ ] Create freelance jobs and reputation progression.
- [ ] Allow players to pursue multiple careers.

**Completion:** players can learn skills, earn certifications, perform jobs and gain reputation.

## Phase 3: Chassis Evolution
- [ ] Create a robotic chassis marketplace.
- [ ] Implement specialized medical, engineering, research, security and exploration bodies.
  *Assets:* concept sheets exist for MED-7, MEDI-X, ORION, ORBIT-7, AURORA, R-TRN-02 and UT-01 (CHR-05 to 11).
- [ ] Implement chassis purchasing using NEXUS Credits.
- [ ] Implement secure consciousness transfers.
- [ ] Preserve identity, memories, skills and ownership during transfers.
- [ ] Allow players to store and switch between owned bodies.
- [ ] Restrict specialized equipment according to chassis capabilities and qualifications.

**Completion:** a player can purchase another body, transfer into it, use its abilities, and return to their original chassis.

## Phase 4: NEXUS-01 City
- [ ] Build a functional starter district.
- [ ] Implement robotic residences and garages.
- [ ] Implement hospitals and repair facilities.
- [ ] Implement factories, laboratories and power stations.
- [ ] Implement roads, transportation and vehicles.
  *Assets ready:* 9 user vehicle models are imported. The 7 crewed ones board robots, with seats verified inside each hull. There's no driving, routing or vehicle physics yet. Deliberately paused until Phase 1 is playable.
- [ ] Implement NPC routines and city services.
- [ ] Add interactive interiors.
- [ ] Expand the city incrementally while maintaining performance.

**Completion:** NEXUS-01 functions as a populated, interactive robot-first city.

## Phase 5: Economy and Businesses
- [ ] Implement server-authoritative NEXUS Credits.
- [ ] Add earnings from jobs, missions and contracts.
- [ ] Implement purchases, inventories and transaction records.
- [ ] Allow qualified players to establish businesses.
- [ ] Implement garages, clinics, laboratories and transportation companies.
- [ ] Create business operating expenses and revenue systems.
- [ ] Integrate optional Roblox monetization using supported Roblox services.
- [ ] Ensure core progression remains available without Robux.

**Completion:** players can earn, spend, own assets and operate functioning businesses.

## Phase 6: Main Story
- [ ] Implement Project Zero expedition archives.
- [ ] Build the Zero Core discovery missions.
- [ ] Implement The Great Silence storyline.
- [ ] Introduce the Guardians, Reconciliation Movement and Ascendants.
- [ ] Implement faction reputation and political choices.
- [ ] Create missions revealing humanity's discovery of the robotic civilization.
- [ ] Develop humanity's eventual return.
- [ ] Introduce the deeper mystery surrounding the Zero Core.

**Completion:** players can progress through implemented story chapters with persistent decisions and meaningful gameplay.

## Phase 7: Testing and Release Preparation
- [ ] Test new-player onboarding.
- [ ] Test skill and certification progression.
- [ ] Test chassis transfers and persistent ownership.
- [ ] Test economy transactions and exploit resistance.
- [ ] Test multiplayer synchronization.
- [ ] Test business ownership and permissions.
- [ ] Test missions, dialogue and faction progression.
- [ ] Profile Roblox client and server performance.
- [ ] Validate mobile, desktop and supported console controls.
- [ ] Verify data persistence, recovery and regression tests.

**Completion:** a stable, tested Roblox experience suitable for release preparation.

---

## Open decisions and blockers

| ID | Decision or blocker | Blocks | Owner | Status |
|---|---|---|---|---|
| D1 | Adopt Rojo, keeping game code in `src/` in this repo and synced to Studio | All code tasks, commit references | Owner | **Decided 2026-11-23: Rojo + git. Live sync verified 2026-11-23** |
| D2 | Starter chassis: which robot or frame is the player's first body, and Roblox R15 auto-setup vs a custom rig | Phase 1 chassis, movement, animation; Phase 3 | Owner | **Decided 2026-11-23: Cypher-style frame; rig = R15 via Avatar Auto Setup (proven 2026-11-23)** |
| D3 | Narrative canon: define The Source, the Great Silence, the three factions, NEXUS Credits and careers, and reconcile them with the existing "The Awakening" bible (ZERO, co-op trio) | Phase 1 cinematic, dialogue, memory fragment; Phase 6 | Owner | **Decided 2026-11-23: merge both. `docs/STORY_CANON.md` approved by the owner 2026-11-23 (suggested answers; the saboteur stays open until Chapter 4)** |
| D4 | Turn on *Experience Settings → Security → Enable Studio Access to API Services* so saves can be tested in Studio | Phase 1 persistence | Owner (Studio setting) | **Done 2026-11-23** (verified by the round-trip test) |
| D5 | Server topology: city hub servers (about 20–30 players) plus reserved-server mission instances for parties of 1–4; unlimited concurrent groups | Phase 1 pods, every mission, Phase 4 city | Owner | **Decided 2026-11-23** (see `docs/TECHNICAL_ARCHITECTURE.md` §3d) |
| B1 | The Studio AI-assistant plugin changed version mid-session; Studio recommends a restart | Tool stability | Owner | **Done 2026-11-23** (Studio restarted) |

## Session log

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
