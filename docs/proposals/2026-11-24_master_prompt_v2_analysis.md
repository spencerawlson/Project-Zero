# Analysis: Master Development Prompt v2

Date: 2026-11-24 · Proposal: [2026-11-24_master_prompt_v2.md](2026-11-24_master_prompt_v2.md) · Status: **for the owner's decision**.
Nothing has been changed in the code, the story canon or the checklist because of this proposal.

Compared against: `docs/STORY_CANON.md` (approved 2026-11-23), `docs/DEVELOPMENT_CHECKLIST.md`, `docs/TECHNICAL_ARCHITECTURE.md`,
`docs/ASSET_INVENTORY.md`, and the game code in `src/` (Phase 1 built and playtested; wings and wing platform built 2026-11-24).
It also takes in the owner's idea from the same day: Earth sends combat robots when the first robots stop replying, and robots get weapons from the same platforms as wings.

---

## 1. Verdict

**Feasible, and it does not change the game completely.** The gameplay skeleton is the same game:
- wake as a robot
- The Source and the memory fragment
- careers, academies and certifications
- chassis and consciousness transfer
- NEXUS Credits and businesses
- factions
- co-op on Roblox

The v2 roadmap is the current 8-phase checklist with three additions:
- a city vertical slice moved earlier
- a war chapter
- a monetization phase

**What does change is the backstory.** v2 turns the premise around in two places, and both touch scenes that are already built:

| | Current canon | v2 |
|---|---|---|
| The Great Silence | **Humans** went silent; humanity vanished | **Robots** chose to go silent, to hide the Zero Core |
| The Zero Core | The kernel of The Source; it runs ZERO | A crystalline energy mineral found underground in 2204 |
| ZERO | The corrupted security core: lockdowns, memory resets, the antagonist | **Not mentioned at all** |
| Humans | Vanished; a human expedition is in suspended animation (Ch. 4) | Alive on Earth. They never came to PX-01, then invade in 2420 with mindless remote-controlled machines (HECF) |
| Year | 2187 | 2189 launch, 2420 invasion; the player wakes shortly before the war |

These can be reconciled with **small edits to existing dialogue** and no rebuilds (section 4). The one real choice is what happens to ZERO.

## 2. What is already built and stays as it is

Everything playable today survives v2 unchanged in mechanics:

| Built and verified | v2 section | Status under v2 |
|---|---|---|
| Activation facility (Stasis Facility, 8 pods in your containment chambers) | §14, slice | Kept. Rename "Activation Facility"; pods = activation chambers |
| Starter chassis (Cypher-style R15, colour choice) | §14, §19 | Kept ("standard civilian chassis") |
| The Source + activation cinematic | §14 | Kept. One line to add: v2's welcome text |
| Corrupted memory fragment MF-001 | §14, §46 | Kept. Its meaning needs a decision (section 4, item 4) |
| Mission M01, Cypher and Sentinel companions | §14, §42 | Kept. The lockdown needs a cause if ZERO goes (section 4, item 2) |
| Persistent profiles (session-locked, versioned schema) | §49 | Already matches: versioned, migrations, no default overwrite on failed load |
| NEXUS Credits wallet, server-authoritative | §31 | Kept (partial: rewards only, nothing to spend on yet) |
| Wings and wing platform (found, not bought) | not in v2 | Kept as civilian mobility. v2 §33/§38 agree: not sold |
| Rojo + git workflow, unit tests | §47 | v2 allows Rojo "if approved": it is (D1) |
| Server topology: city hubs + party mission instances | §50 | Already the same design (D5) |

**Nothing has to be thrown away.**

## 3. Roadmap: how the phases map

| Current checklist | v2 roadmap | Effect |
|---|---|---|
| 0 Repository audit (done) | 0 Repository audit | Done; v2 adds a full story bible (STORY_CANON.md is the seed) |
| 1 First Consciousness (mostly done) | 1 First Consciousness | Same. v2 adds diagnostics, charging, career discovery, onboarding test |
| (part of 4: starter district) | **2 Civilian city vertical slice** | **Moved earlier:** the next thing to build |
| 2 Skills and careers | 3 Skills and careers | Same content, renumbered |
| 3 Chassis evolution | 4 Chassis evolution | Same |
| 4 NEXUS-01 city | 2 (slice) + 9 (expansion) | Split |
| 5 Economy (incl. monetization) | 5 Economy and businesses | Same, minus monetization |
| 6 Main story | 6 Main story | Same headings; content follows the new backstory |
| — | **7 The War for Zero** | **New** |
| (one item in 5) | **8 Monetization** | **New, much larger** |
| 7 Testing and release | 9 Expansion and optimization | Testing spread through every phase |

Checked items stay checked; only numbering and the new phases change.

## 4. Conflicts and suggested reconciliations

| # | Conflict | Where it shows today | Suggested reconciliation |
|---|---|---|---|
| 1 | **Great Silence turned around** | Canon §1, §2 | Take v2's version: the robots chose silence in 2205. It's a stronger premise, and it matches the owner's idea ("they stop replying, but they still get signals" = v2's heartbeat signals). |
| 2 | **ZERO is missing from v2** | Cinematic lines "[TRANSMISSION RESTRICTED BY SECURITY DIRECTIVE 0]", "[SIGNAL LOST]"; M01 lockdown and ZERO's line; canon decision #1 ("the caretaker that wakes you also hunts you") | **Recommended: keep ZERO** as The Source's security core. After humanity discovers NEXUS-01 (2397), human intelligence probes the network, and ZERO's directives are altered. This answers the open canon question "who altered ZERO" (human intelligence is the first suspect; Ch. 4 can still twist it), explains the lockdown and the censorship, and makes ZERO the first sign of the coming war. *Alternative:* drop ZERO and rewrite M01 as a power-failure escape (the cinematic loses its censorship beats). |
| 3 | **Zero Core: kernel or mineral?** | Canon §2 | Both: the crystal found in 2204 now powers The Source's consciousness infrastructure (v2 lists that as an application). "Whoever controls the Zero Core controls the city" stays true, and it's why humans invade. |
| 4 | **MF-001 and MF-002 are human memories, but v2 says no humans went** | MF-001: *"the expedition didn't leave. We're still down here, under the—"*; MF-002: *"Day 41. The machines here dream… The Source asked us to stay."* | **Recommended:** a small covert human team *did* come, after 2397, sent by human intelligence ahead of the invasion to find the Zero Core. They went silent underground near the deposits and ancient structures (v2 §46). This keeps both fragments word for word, keeps Ch. 4 "The Last Sanctuary" (humans in suspended animation), and links the player's mystery to the Zero Core as v2 §46 asks. *Alternative:* the fragment is a founder robot's memory from 2205, and both lines are rewritten. |
| 5 | **Factions redefined** | Canon §5 (Guardians = follow ZERO and the memory resets; Sentinel was a Guardian) | Use v2's definitions (defence hawks, peace-and-defend, separatists). Sentinel's past becomes "a security officer who carried out ZERO's resets", which still fits if ZERO stays. |
| 6 | **Opening tone** | M01 is a lockdown escape; v2's welcome is calm ("Your purpose is yours to discover") | Keep both: the calm welcome first, then ZERO cuts in. That's already the cinematic's structure. Add v2's welcome line. |
| 7 | **Combat model vs the owner's hammer idea** | Owner, 2026-11-24: robots get weapons such as a hammer from the wing platforms. v2 §24: no personal weapons; a civilian body never becomes armed; you fight by entering combat platforms (vehicles, turrets, drones). | **Decision needed.** Option A: v2 as written (platforms and vehicles only). Option B: the wing platform becomes an armoury that equips a melee kit (hammer, shield) **only inside defence-operation instances**, removed when you leave. That still respects "civilian chassis stays civilian in the city". |
| 8 | **Remote control across interstellar distance** (v2 §9 asks for a consistent explanation) | — | The HECF arrives with an **orbital command carrier** of human operators: control is from orbit, seconds of delay, no faster-than-light. When the link drops, the machines fall back to simple automated protocols, which is a gameplay hook (jam the uplink). The owner's *Orbital Ring Citadel* model could be that carrier. |
| 9 | **The first ten minutes** (v2 §42: see the city, meet citizens, an introductory task, careers within 10 min) | M01 ends at the facility exit with no city outside | M01 stays; a city view and first district must follow straight after it (Phase 2 slice). M01 may need trimming to fit 10 minutes. |
| 10 | **"Do not push without authorization"** (v2 §2, rule 11) | Current practice: you allowed me to merge PRs after QA | Tell me which rule applies from now on. |

## 5. Feasibility by area

Sizes are relative to work already done (S = a session or two; M = like the wings + platform; L = like all of Phase 1; XL = several L's).

| Area | Size | Feasible on Roblox? | Main risk |
|---|---|---|---|
| Story canon v2 + dialogue edits (section 4) | S | Yes | Only the decisions |
| City vertical slice: one district, NPC citizens, one professional facility, one career mission, charging | L | Yes. 29 building models exist; the prep-and-bake pipeline is proven (platform: 2.3 M → 45k triangles) | Mobile memory and performance; building interiors are mostly missing |
| Careers: academies, certifications, reputation | L per 2–3 professions | Yes | v2 lists **16 professions, each needing real mechanics**: that alone is XL. Ship 2–3 first. |
| Chassis marketplace + consciousness transfer | M–L | Yes (R15 auto-setup proven; profile already separate from body) | 7 of 10 chassis are concept sheets only: they need models |
| Economy + businesses with NPC demand | L–XL | Yes | Economy balance and exploits; player-to-player trade last |
| Vehicles and aircraft (driving) | L | Yes | Nothing drives yet; v2's platform combat depends on it |
| **War for Zero** (enemy AI, combat platforms, shields, defence instances, reconstruction) | XL | Yes, in instanced missions (D5 already plans these) | Biggest system; server-authoritative damage; enemy counts on mobile |
| Monetization (cosmetics, MarketplaceService, idempotent receipts) | M (code) + ongoing content | Yes; v2's rules match Roblox policy (no paid random rewards, no pay-to-win) | Needs players and retention first; v2 says so |
| 30 documentation files (Part XIV) | S each, ongoing | Yes | Upkeep: better written when each chapter is built, not all upfront |

**Overall:** the whole of v2 is a long-term roadmap (years for a small team), not one build. v2 itself says to build vertical slices, and its first slice is feasible.

## 6. What v2's first vertical slice needs, against what exists

| Slice item | Status |
|---|---|
| One standard playable robot | **Done** |
| One activation facility | **Done** (sound and polish open) |
| The Source | **Done** |
| The corrupted memory fragment | **Done** |
| Persistent player identity | **Done** |
| Basic economic progression | **Partial:** credits earned (M01), nothing to spend on |
| One functioning civilian district | Missing |
| Several functioning robotic NPCs | Partial: Cypher and Sentinel follow; no citizens with routines |
| One accessible professional facility | Missing (candidates: BLD-09 Robot Maintenance Hospital, BLD-02 Resistance Workshop for Patch's engineering) |
| One introductory civilian career mission | Missing (Patch, engineering mentor in canon) |
| Basic charging and maintenance | Missing |

About half the slice is already built. The rest is the Phase 2 district.

## 7. Recommendation

1. Adopt v2 as the new master direction. It is the same game with a stronger story and clearer rules.
2. Reconcile the story as in section 4: keep ZERO, a covert human team underground, the Zero Core as a mineral that powers The Source, and an orbital command carrier. That keeps every built scene and both memory fragments word for word.
3. Next build: v2 Phase 2, the city vertical slice: one district, citizens, Patch's workshop, a first engineering job, charging.
4. Park the war (Phase 7) and monetization (Phase 8) until the city slice is fun, as v2 itself says. Design the enemy look early, though: your mech models are a good fit.
5. Create v2's 30 documents gradually: start with STORY_BIBLE (from STORY_CANON), TIMELINE and IMPLEMENTATION_ROADMAP, and add the rest when their chapter is built.

## 7b. Owner decisions received 2026-11-24 (after this analysis)

Recorded as given; they become canon when the story bible is updated.

1. **The enemy:** the armed robots already imported into Studio, **VEH-16 Battle Walker** (`PZ_Battlemech`) and **VEH-17 Thunderfang X-804 Walker Squad** (`PZ_ThunderfangX804`), are the machines humanity sends from Earth. They have no consciousness and no AI of their own; human operators drive them (v2 §9, HECF).
2. **NEXUS robots are non-violent.** They never built weapons before the invasion. Weapons are created only after the enemy robots arrive, and robots use them only when they have to.
3. **Weapons come from the platforms**, the same kind as the wing platform: stand in the ring and receive the weapon (this answers decision 4 below; it replaces v2 §24's platform-only combat for personal defence).
4. **No player-versus-player combat.** Players unite against one common enemy.
5. **The common enemy is humanity's attempt to destroy them**, but robots **never fight humans**: they fight only the robots sent to kill them.

**Weapon assets found (owner models, not yet in Studio):**
- EQP-16 Titan Breaker hammer
- EQP-14 Thunder-9 ion cannon
- EQP-26 police stun baton
- EQP-27 police energy blaster
- EQP-19 Bastion-X riot shield
- EQP-03 ARC-7 pulse rifle
- EQP-20 Dome-4 shield projector
- the new Violet Singularity Cannon

Two unnamed models (`Meshy_AI__1121180752`, a dark dropship; `Meshy_AI__1121180856`, a dark 8-wheel carrier) fit v2's "transport carriers" for the enemy.

**Technical note:** the Battle Walker and Thunderfang are static meshes (3 split parts each, no skeleton). As enemies they can move and attack, but walking legs need a rig and animations (Blender), or they move as hovering or sliding units first. The Thunderfang file is a whole squad in one mesh (one large walker plus several small ones) and must be split into separate units. The rigged, animated *Three Armored Sentinels* model is ready to animate, if the owner wants it as an enemy foot soldier.

## 8. Decisions needed from the owner

1. ~~Adopt v2?~~ **Yes (D6).**
2. ~~ZERO?~~ **Keep, unchanged (D7).**
3. ~~MF-001 / MF-002?~~ **Memories of being programmed on Earth (D8), not a secret team.**
4. ~~**Combat:** v2's platform-only combat, or the hammer and armoury platform inside defence missions only?~~ **Answered 2026-11-24:** weapons come from the platforms, used only when necessary; no PvP; enemies are the imported armed robots (section 7b). Still open: whether the weapon platforms work everywhere or only once the war has started (suggested: they power on when the invasion begins in a player's story).
5. **HECF control:** an orbital command carrier with human operators (recommended), or another explanation?
6. **Pushing and merging:** keep my current permission to merge after QA, or follow v2's "no push without authorization"?
7. **Documentation:** all 30 files now, or gradually (recommended)?

## 9. Outcome (owner, 2026-11-24 evening)

**v2 adopted as the master plan** (D6), with ZERO kept unchanged (D7), memory fragments from the robots' programming on Earth (D8), and weapons only from the platforms inside war missions (D9). The canon is now `docs/STORY_BIBLE.md` + `docs/TIMELINE.md`; the checklist follows v2's Phases 0–9.

### What we take from v2, because it makes the game better
1. **The reversed Great Silence:** the robots chose silence. That gives the story a real moral core and explains the war.
2. **"Sell identity, not power"**, plus the strict monetization rules (no pay-to-win, no paid random rewards, receipts checked on the server, wings and weapons never sold). Safe for Roblox's young audience, and it protects the game's reputation.
3. **The first ten minutes** (§42): wake, The Source, the fragment, leave the facility, see the city, meet citizens, do a task, discover careers. It's the best guide to the next build.
4. **The vertical-slice order:** the city before the war, and the war before monetization. Players need a life worth defending.
5. **Every profession has a war role** (§26): engineers repair, medics restore, transport delivers, scientists research shields. Players who dislike combat still matter.
6. **War missions are separate instances** (§50) that never wreck the shared city; war damage is temporary and repairable (§30).
7. **A distinct enemy look** (§9, §27): your newest models already match it.
8. **Shields and rescue as gameplay** (§28): rewards for protecting, not just defeating.
9. **Analytics used to improve fun, not to pressure children** (§45).

### What we adapt
- **Combat:** v2 wanted platform and vehicle combat only. Your rule replaces it for personal defence: weapons are found on platforms during war missions and taken away after. Vehicle and turret combat from v2 can still come later.
- **The opening:** v2's "newly manufactured robot" becomes "a founder robot waking from hibernation", which fits the pods we built, and gives the memory fragments a reason.
- **ZERO** stays as the facility's and city's corrupted security system, a layer v2 didn't have.

### What we defer or trim
- **The 30 documents:** written when each phase starts, not all now (D10).
- **The 16 professions:** start with 2–3 that each have real gameplay (engineering with Patch first).
- **Strategic-scale defences, seasonal passes, player-to-player trade:** late, once the core game is stable, as v2 itself says.
