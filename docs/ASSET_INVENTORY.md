# Asset Inventory

Generated on 2026-11-23 from `PDF/src/pz_inventory.py` (the bible's inventory) and checked against the files on disk and the ProjectZero Roblox place. All dimensions are design assumptions in Roblox studs.

**Source** describes what exists for each asset:
- *user model*: your Meshy or library 3D file
- *blockout*: the procedural Blender layout model
- *concept / spec only*: no 3D model yet

**In Studio** lists what has been imported into the place.

## Summary

| Category | Assets | In Studio |
|---|---|---|
| Robots and characters | 10 | 3 |
| Buildings | 29 | 0 |
| Vehicles | 17 | 9 |
| Equipment and weapons | 27 | 0 |
| Infrastructure | 20 | 0 |
| Interiors and props | 16 | 0 |
| **Total** | **119** | **12** |

Also in Studio, outside the inventory: **BLD-01 Stasis Facility greybox** (`PZ_StasisFacility`, 324 parts, rebuilt by `Roblox/BLD-01_greybox_build.lua`). It is approved as the activation facility.

## Robots and characters

| ID | Name | Size | Source | In Studio |
|---|---|---|---|---|
| CHR-01 | Cypher (canonical) | 6.0 tall (Meshy, rigged) | user model, rigged (52 bones, 8 animation clips) | yes: PZ_Cypher (asset 70858692745203) |
| CHR-02 | Sentinel (canonical) | 7.5 tall (Meshy, rigged) | user model, rigged (52 bones, 9 animation clips) | yes: PZ_Sentinel (asset 112765322471145) |
| CHR-03 | Patch (canonical) | 4.5 tall (Meshy, needs rig) | user model, not rigged | yes: PZ_Patch (asset 79909362444560) |
| CHR-05 | MED-7 medical robot | 6.6 tall (concept) | concept sheet only | — |
| CHR-06 | MEDI-X medical specialist | 6.8 tall (concept) | concept sheet only | — |
| CHR-07 | ORION research robot | 6.7 tall (concept) | concept sheet only | — |
| CHR-08 | ORBIT-7 recon robot | 6.9 tall (concept) | concept sheet only | — |
| CHR-09 | AURORA utility worker | 6.4 tall (concept) | concept sheet only | — |
| CHR-10 | R-TRN-02 transport robot | 6.8 tall (concept) | concept sheet only | — |
| CHR-11 | UT-01 utility robot | 6.4 tall (Meshy, rigged) | user model, rigged (Mixamo clips) | — |

## Buildings

| ID | Name | Size | Source | In Studio |
|---|---|---|---|---|
| BLD-01 | Stasis Facility | 120×88×32 (ref 120×85×32) | concept/spec only | — |
| BLD-02 | Resistance Workshop | 100×80×28 (ref) | blockout + user model | — |
| BLD-03 | Residential Tower | 48×48, 5 floors (ref) | blockout + user model | — |
| BLD-04 | Circuit Market | 100×70×20 (ref) | blockout + user model | — |
| BLD-05 | Assembly Foundry | 140×95×36 (ref) | blockout | — |
| BLD-06 | Research Laboratory | 90×70×24 (ref) | blockout + user model | — |
| BLD-07 | Security Command Center | 48×36 office (ref) | blockout + user model | — |
| BLD-08 | Nexus Energy Spire | 90×90×180 (ref) | blockout | — |
| BLD-09 | Robot Maintenance Hospital | 80×64×24 | blockout + user model | — |
| BLD-10 | Data Archive | 64×48×28 | blockout | — |
| BLD-11 | Underground Freight Depot | 120×64×28 | blockout | — |
| BLD-12 | Robot Recycling Facility | 96×72×30 | blockout | — |
| BLD-13 | Memory Restoration Laboratory | 64×56×24 | blockout | — |
| BLD-14 | Automated Manufacturing Plant | 128×96×32 | blockout + user model | — |
| BLD-15 | Central Transit Terminal | 90×24 platform (ref) | blockout + user model | — |
| BLD-16 | Compact Police Station | 32 long (user model) | user model | — |
| BLD-17 | Emergency Response Station | 48 long (user model) | user model | — |
| BLD-18 | Nexus PD Headquarters | 56 long (user model) | user model | — |
| BLD-19 | Monorail Station | 90 long (user model) | user model | — |
| BLD-20 | Antigravity Arena | 80 long (user model) | user model | — |
| BLD-21 | Academy (Robot Education) | concept | concept/spec only | — |
| BLD-22 | Botanical Dome | concept | concept/spec only | — |
| BLD-23 | Culture Hub | concept | concept/spec only | — |
| BLD-24 | Nexus Realm Amusement Park | concept | concept/spec only | — |
| BLD-25 | Refinery Complex | 64 long (user model) | user model | — |
| BLD-26 | Reactor Bastion | 40 tall (user model) | user model | — |
| BLD-27 | ZERO Command Base | 80 long (user model) | user model | — |
| BLD-28 | ZERO Steel Citadel | 96 long (user model) | user model | — |
| BLD-29 | Modular Outpost Block | 56 long (user model) | user model | — |

## Vehicles

| ID | Name | Size | Source | In Studio |
|---|---|---|---|---|
| VEH-01 | Ghost Train | 75×16×14 (crew std) | blockout | — |
| VEH-02 | NEXUS-01 Monorail | 57×16×16 (crew std) | blockout | — |
| VEH-03 | Maintenance Train | 40×12×14.2 (crew std) | blockout | — |
| VEH-04 | Cargo Transport TITAN-R1 | 28×13.5×12.8 (crew std) | blockout + user model | yes: PZ_TitanRover (107446849916205), 4 seats |
| VEH-05 | Autonomous Robot Shuttle | 17×12×10.8 (crew std) | blockout | — |
| VEH-06 | Industrial Transport Drone | 8×8×3 | blockout | — |
| VEH-07 | Freight Elevator | 16×16 platform | blockout | — |
| VEH-08 | Passenger Elevator | 8×8 car | blockout | — |
| VEH-09 | NX-A17 Raven VTOL | 50 long, 54 span, 20 (crew std) | blockout | yes: PZ_RavenJet2 (140225470731589), 9 seats |
| VEH-10 | Industrial Freight Train | 96 long (user model) | user model | yes: PZ_FreightTrain (124641651466353), 7 seats |
| VEH-11 | Armored Security Carrier | 32 long (user model) | user model | yes: PZ_ArmoredSecurityCarrier (88628350523039), 5 seats |
| VEH-12 | Armored VTOL Security Aircraft | 50 long (user model) | user model | yes: PZ_SecurityVTOL (76999252171451), 9 seats |
| VEH-13 | Industrial Cargo Hauler | ≈ 36 long (concept) | concept/spec only | — |
| VEH-14 | Tracked Utility Hauler | 28 long (user model) | user model | yes: PZ_TrackedHauler (111991835516707), 3 seats |
| VEH-15 | Armored 8x8 Patrol | 30 long (user model) | user model | yes: PZ_DesertSentinel8x8 (85593428487775), 4 seats |
| VEH-16 | Battle Walker | 14 tall (user model) | user model | yes: PZ_Battlemech (76360997961306), enemy |
| VEH-17 | Thunderfang X-804 Walker Squad | user model (see sheet) | concept/spec only | yes: PZ_ThunderfangX804 (131523247905987), enemy |

## Equipment and weapons

| ID | Name | Size | Source | In Studio |
|---|---|---|---|---|
| EQP-01 | Repair Tool | handheld 2–5 (ref) | blockout | — |
| EQP-02 | PHOTON EDGE Energy Sword | 4.6 long | blockout | — |
| EQP-03 | ARC-7 Plasma Pulse Rifle | 4.6 long | blockout + user model | — |
| EQP-04 | Scanner | handheld 2 | blockout | — |
| EQP-05 | Hacking Terminal | tablet 2×1.4 | blockout | — |
| EQP-06 | AEGIS-S1 Energy Shield | 6.0 tall deployed | blockout | — |
| EQP-07 | Power Core / Energy Cells | 0.6–1.5 (E-10…E-100) | blockout | — |
| EQP-08 | Grappling Device | handheld 3 | blockout | — |
| EQP-09 | Medical Repair Drone | 2×2×1 | blockout | — |
| EQP-10 | Portable Charging Unit | 2×1.5×2 | blockout | — |
| EQP-11 | Memory Storage Module | 0.6×0.4×1 | blockout | — |
| EQP-12 | Industrial Welding Tool | handheld 3 | blockout | — |
| EQP-13 | VOLT-X Energy Carbine | 3.8 long | blockout | — |
| EQP-14 | THUNDER-9 Ion Cannon | 5.8 long | blockout + user model | — |
| EQP-15 | NOVA-3 Precision Rifle | 6.0 long | blockout | — |
| EQP-16 | TITAN BREAKER Hammer | 5.6 long | blockout + user model | — |
| EQP-17 | ARC CLAWS Blades | 1.8 long ×2 | blockout | — |
| EQP-18 | SHOCK STAFF | 7.0 long | blockout | — |
| EQP-19 | BASTION-X Riot Shield | 4.5 tall | blockout + user model | — |
| EQP-20 | DOME-4 Shield Projector | 2.5 wide, dome r 8 | blockout + user model | — |
| EQP-21 | EMP-6 Disruption Launcher | 4.0 long | blockout | — |
| EQP-22 | GRAVITY-8 Manipulator | 4.0 long | blockout | — |
| EQP-23 | PULSE-MINE | 1.5 wide | blockout | — |
| EQP-24 | OVERDRIVE CORE | 1.2 tall | blockout | — |
| EQP-25 | SENTINEL DRONE | 3.0 wide | blockout | — |
| EQP-26 | Police Stun Baton | 3 long (user model) | user model | — |
| EQP-27 | Police Energy Blaster | 3 long (user model) | user model | — |

## Infrastructure

| ID | Name | Size | Source | In Studio |
|---|---|---|---|---|
| INF-01 | Robot Charging Station | 10×8×12 (ref) | blockout | — |
| INF-02 | Energy Substation | 24×16×16 | blockout | — |
| INF-03 | Communication Tower | 8×8×64 | blockout | — |
| INF-04 | Security Access Gate | 24×8×18 (ref) | blockout | — |
| INF-05 | Street Lighting System | 2×2×14 | blockout | — |
| INF-06 | Holographic Signage | 4–12 wide | blockout | — |
| INF-07 | Industrial Ventilation Unit | 8×8×6 | blockout | — |
| INF-08 | Cooling System | 16×8×10 | blockout | — |
| INF-09 | Water Recycling System | 24×16×12 | blockout | — |
| INF-10 | Maintenance Tunnel | 12 wide module | blockout | — |
| INF-11 | Elevated Pedestrian Bridge | 8 wide, 16-stud module | blockout + user model | — |
| INF-12 | Monorail Track Module | 16-stud module, 10 rail (ref) | blockout | — |
| INF-13 | Robot Roadway Module | 32 long (user model) | user model | — |
| INF-14 | Elevated Maglev Highway | 64 long (user model) | user model | — |
| INF-15 | Enclosed Skybridge | 32 long (user model) | user model | — |
| INF-16 | Drone Hive | 24 long (user model) | user model | — |
| INF-17 | Mission Gateway Portal | 24 long (user model) | user model | — |
| INF-18 | Energy Conduit Column | 16 tall (user model) | user model | — |
| INF-19 | Central Core Hologram Plinth | 32 wide (user model) | user model | — |
| INF-20 | Reactor Ring Engine | 24 wide (user model) | user model | — |

## Interiors and props

| ID | Name | Size | Source | In Studio |
|---|---|---|---|---|
| INT-01 | Stasis Chamber | 48×80 (R04 of BLD-01) | concept/spec only | — |
| INT-02 | Robot Residential Apartment | 24×16×12 | blockout + user model | — |
| INT-03 | Workshop Repair Bay | 24×24×16 | blockout + user model | — |
| INT-04 | Train Passenger Compartment | 17×23×8.6 car interior | blockout | — |
| INT-05 | Train Control Cabin | 17×12×8.6 cab interior | blockout | — |
| INT-06 | Research Laboratory Interior | 48×32×16 | blockout | — |
| INT-07 | Factory Assembly Floor | 96×64×28 | blockout | — |
| INT-08 | Security Control Room | 24×20×12 | blockout + user model | — |
| INT-09 | Underground Market Stall | 8×8×10 | blockout + user model | — |
| INT-10 | Energy Reactor Control Room | 32×24×16 | blockout + user model | — |
| INT-11 | Hospital Repair Hall | 48 long (user model) | user model | — |
| INT-12 | Robot Containment Chamber | 32 long (user model) | user model | — |
| INT-13 | Robot Communal Lounge | 32 long (user model) | user model | — |
| INT-14 | Command Console (prop) | 6 long (user model) | user model | — |
| INT-15 | Command Chair (prop) | 4 tall (user model) | user model | — |
| INT-16 | Holo Command Console (prop) | 7 tall (user model) | user model | — |

## Animations

- **Cypher** (`Rigged_Cypher.glb`): 52-bone Meshy skeleton, 8 animation clips embedded in the file.
- **Sentinel** (`Rigged_Sentinel.glb`): 52-bone Meshy skeleton, 9 animation clips embedded in the file.
- **Cargo Logistics, Futuristic Utility and Scientific Research robots** (`Meshy_AI_Rigged_*_animated_mixamo_All_animation.glb`): Mixamo-rigged, with Mixamo clips embedded.
- **Three Armored Sentinels** (`Meshy_AI_Three_Armored_Sentinels_*_animated_mixamo_All_animation.glb`): Mixamo clips.
- **Patch**: no skeleton and no clips.

None of these are uploaded as Roblox Animation assets yet; the place contains 0 Animation objects. Cypher and Sentinel are in Studio as skinned meshes driven by an AnimationController, not as playable Humanoid characters.

## Loose files in `D:\Project Zero_Roblox` not yet in the bible
- **Space and sci-fi structures:** Aegis Outpost, Steel Citadel, Outpost Emberfall, Quantum Gateway, Drone Hive.
- **Duplicates:** `Patch_Low_Untextured.glb` (same size as `Patch_LowPoly.glb`) and the `(1)` copy of the robotic command centre.
- **Download archives:** 27 `Meshy_models_*.zip` files (about 3.3 GB) and 5 `Infra/Meshy_AI_assets_*.zip` files (about 3.3 GB), which hold the originals.
