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
  Not done: kit modules, the pod model with its hinge, the wake sequence, lighting states and `StasisFacilityService`.
- [ ] **Implement the standard starter chassis.**
  Blocked by D2: no Humanoid-compatible robot rig yet.
- [ ] **Implement movement, camera and interaction.**
  *Partial:* ProximityPrompt boarding with server validation works on 7 vehicles. Movement and camera are still Roblox defaults.
- [ ] **Create the activation cinematic and dialogue with The Source.**
  Blocked by D3 (canon).
- [ ] **Introduce the mysterious corrupted memory fragment.**
  Blocked by D3. The design bible already has memory fragments and Cypher's ZERO fragment.
- [ ] **Implement the first playable mission.**
- [x] **Implement persistent player identity and save data.**
  Verified 2026-11-23:
  - **Profile:** keyed by Roblox UserId; schema v1; starter chassis `CypherFrame`; `createdAt` set.
  - **Session-locked store, unit tests:** 18/18 pass.
  - **Real DataStore round trip in Studio** (API access on): session 1 wrote marker `RT-1795474515` and stopped. Session 2, a new server, loaded the marker and the session count 3, and loaded instantly, which proves the shutdown save released the lock. `PZ_PersistentSave = true`. The test marker was then removed.
  - *Follow-up (part of activation, not this item):* the player-chosen `identity.designation` is set during the activation sequence.

**Completion:** a new player can activate, complete the introductory mission, and return with progress preserved.

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
| D2 | Starter chassis: which robot or frame is the player's first body, and Roblox R15 auto-setup vs a custom rig | Phase 1 chassis, movement, animation; Phase 3 | Owner | **Decided 2026-11-23: Cypher-style frame** (rig approach still to be proven) |
| D3 | Narrative canon: define The Source, the Great Silence, the three factions, NEXUS Credits and careers, and reconcile them with the existing "The Awakening" bible (ZERO, co-op trio) | Phase 1 cinematic, dialogue, memory fragment; Phase 6 | Owner | **Decided 2026-11-23: merge both; Claude drafts `docs/STORY_CANON.md` for owner approval** |
| D4 | Turn on *Experience Settings → Security → Enable Studio Access to API Services* so saves can be tested in Studio | Phase 1 persistence | Owner (Studio setting) | **Done 2026-11-23** (verified by the round-trip test) |
| B1 | The Studio AI-assistant plugin changed version mid-session; Studio recommends a restart | Tool stability | Owner | **Done 2026-11-23** (Studio restarted) |

## Session log

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
