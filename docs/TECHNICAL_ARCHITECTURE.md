# Technical Architecture

Status as of 2026-11-23 (Phase 0 audit). Section 1 describes what exists and was verified. Section 3 is a proposal for Phase 1 and is not built yet.

## 1. What exists today (verified)

Project Zero currently has two halves that are not connected by code.

### 1a. This repository: the production bible and asset pipeline
| Area | Contents | Tooling |
|---|---|---|
| `PDF/` | Bible Rev D (196 pages), sheet composers, QA (`pz_qa.py`), PDF builder (`pz_finalize.py`) | Python 3.14 + matplotlib + Pillow + reportlab |
| `Blender/scripts/` | Procedural blockout builders (`pz_assets_*.py`), Stasis Facility (`pz_build_stasis.py`, `pz_layout.py` = single source of truth), model audit and render scripts, **`pz_vehicle_prep.py`** (Meshy model → Roblox-ready GLB with a robot-fit scan) | Blender 5.3 (headless) |
| `Buildings/ Vehicles/ Equipment/ Infrastructure/ Interiors/ Characters/ Stasis_Facility/` | Per-asset renders, sheets, camera metadata, crew-fit results (`crew_check.json`) | generated |
| `Roblox/` | Per-asset Roblox specs (`*_roblox_spec.md`); the only Luau in the repo: `BLD-01_greybox_build.lua`, `vehicle_crew_layer.lua`; `vehicles_in_studio.md` | run in Studio |
| `Meshy_Prompts/` | Meshy prompt for each asset | — |
| `QA/` | Automated QA report and the record of pages reviewed by eye | — |

The repository has 2 Luau files, 29 Python scripts, 25 shell scripts and about 2,000 generated images and JSON files. It has **no game code**, no Rojo project file, and no linter, formatter or test framework.

### 1b. The Roblox place (the game)
- **Place:** "ProjectZero", place 102202818249033 in universe 10778699105, private, owned by the user's account, saved to Roblox. A local `ProjectZero.rbxl` copy predates the robots and vehicles.
- **Workspace:** the Stasis Facility greybox; Cypher, Sentinel and Patch as anchored display models; and 9 imported vehicles, each with a `CrewLayer` (seats, a Board prompt and a server script). See `Roblox/vehicles_in_studio.md`.
- **Scripts:** the only scripts are 7 identical `BoardServer` scripts inside the vehicles. ServerScriptService, ReplicatedStorage, ServerStorage, StarterGui, StarterPack and StarterPlayerScripts are all empty.
- **Players** spawn as default Roblox avatars. None of the robots is a playable character yet.
- **Settings:** StreamingEnabled is on. No DataStore, RemoteEvent, UI or animation assets exist.

### 1c. Development workflow (verified)
1. **Code and building:** Roblox Studio driven over the Studio MCP connection: `execute_luau` in Edit mode, playtests through `start_stop_play`, then `execute_luau` against the Server data model for in-game assertions, plus console checks and screen captures.
2. **Assets:** Meshy GLB → `pz_vehicle_prep.py` (weld, decimate to pieces of at most 18,000 triangles, 1024 px textures, robot-fit scan) → Open Cloud upload (`asset:read` and `asset:write` granted for this place; upload folder `D:\Project Zero_Roblox\Roblox_Import`) → `insert_asset` → align the yaw, because Roblox inserts imports at an arbitrary rotation → crew layer → enclosure check → playtest.
3. **Version control:** git + Git LFS (PDFs) on GitHub `spencerawlson/Project-Zero`, using a pull request per change. Game state in the place is **not** under version control.
4. **Installed tooling:** Rojo 7.7.0, git-lfs 3.8.1 and gh 2.97. Not installed: Wally, Selene, StyLua, Lune and Rokit/Aftman.

## 2. Gaps found by the audit
| # | Gap | Impact |
|---|---|---|
| G1 | No game code in the repository; the place is the only copy of its scripts | Code can't be reviewed, diffed or restored, and the checklist's commit references can't apply to gameplay code |
| G2 | No playable robot character. The robots are Meshy skeletons (52 bones) or Mixamo rigs, not Humanoid R15 avatars | Blocks "starter chassis", movement, chassis transfer and animation |
| G3 | No persistence layer: no DataStore usage, and Studio API access not yet confirmed | Blocks save data, identity and every later progression system |
| G4 | No UI, remotes, input handling or camera code | Blocks movement, camera and interaction polish, dialogue and missions |
| G5 | The narrative canon for the checklist (The Source, the Great Silence, the Guardians, the Reconciliation Movement, the Ascendants, NEXUS Credits, chassis and careers) is not in any project document. The existing design bible ("The Awakening") names the central intelligence ZERO, makes Cypher, Sentinel and Patch the protagonists, and frames the game as a co-op action RPG | Phase 1 dialogue, cinematic and memory fragment, and the Phase 6 story, need an approved canon |
| G6 | No automated tests for Luau | Verification relies on in-Studio playtest assertions |

## 3. Proposed architecture for Phase 1 (not yet built; needs owner approval)

### 3a. Source layout synced by Rojo
```
default.project.json            Rojo map → DataModel
src/
  server/                       ServerScriptService.Server
    Services/PlayerDataService.luau     session-locked DataStore, versioned schema, retries, autosave, BindToClose
    Services/ChassisService.luau        starter chassis spawn, owned bodies (Phase 3)
    Services/InteractionService.luau    ProximityPrompt registry, server-side validation (distance, cooldown)
    Services/MissionService.luau        mission state machine, objectives, rewards (server authority)
    Services/DialogueService.luau       dialogue graph playback triggers
  client/                       StarterPlayer.StarterPlayerScripts.Client
    Controllers/CameraController.luau, InputController.luau (keyboard/gamepad/touch), DialogueUI.luau, HUD.luau
  shared/                       ReplicatedStorage.Shared
    Config/*.luau (tunables), Types.luau, Remotes.luau (one place that creates/validates RemoteEvents)
tests/                          ModuleScript unit tests (Roblox rbx-unit-test workflow)
```
Existing Studio content (the facility greybox, vehicles and robots) stays in the place. Rojo syncs code only, so the binary place isn't rewritten.

### 3b. Principles
- **Server authority:** the server owns progress, currency, ownership and mission state. Clients send intents through validated remotes with rate limits, and never results.
- **Persistence:** one profile per user ID, holding a schema version, identity, starter chassis, mission flags, memory fragments and timestamps. It uses session locking against duplication across servers, `UpdateAsync` with retries, an autosave interval, and a save on `PlayerRemoving` and `BindToClose`. Every schema change ships with a migration.
- **Testability:** game logic lives in pure ModuleScripts that can be unit tested. Services are thin adapters around them.
- **Assets:** continue the prep pipeline. Every imported hull goes through yaw alignment and the crew-fit and enclosure checks.

### 3c. Decisions (all decided 2026-11-23)
1. **Code workflow:** Rojo with game code in this repository. Live sync is verified.
2. **Starter chassis:** a Cypher-style standard frame. The rig approach (R15 auto-setup or a custom rig) gets settled while building it.
3. **Canon:** see `docs/STORY_BIBLE.md` (master plan, 2026-11-24; supersedes `docs/STORY_CANON.md`).
4. **Studio API access:** on. The DataStore round trip is verified.
5. **Server topology (D5):** see 3d.

### 3d. Server topology (decision D5, 2026-11-23)
Roblox starts as many servers as needed automatically. The player count per server is a setting (up to 100), and there is no total cap, so 20 or 100 groups of four play at once without limits.
- **City hub (NEXUS-01):** shared public servers of about 20–30 players. Players meet, take jobs, run businesses and form groups here.
- **Mission instances:** each story mission runs in a reserved server (`TeleportService:ReserveServer` + `TeleportAsync`) holding one party of 1–4. The party teleports in together with its mission context in the teleport data, and returns to the hub afterwards. A solo player is a party of 1.
- **Consequences for every system:**
  - Mission state lives on the instance server.
  - Progress is written to each player's own profile through `PlayerDataService`.
  - Nothing assumes a single player per server: pods, seats and objectives are assigned per player on the server.
  - The session lock already protects a profile while a player moves between hub and instance.
- **The Stasis Facility opening** is the first mission instance. Each party member gets their own player pod (P02–P06).
