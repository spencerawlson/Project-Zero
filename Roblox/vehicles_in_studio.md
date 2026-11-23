# Supplied vehicles in Roblox Studio

These are the user's Meshy vehicle models, prepared with `Blender/scripts/pz_vehicle_prep.py` and imported into the ProjectZero place (universe 10778699105) on 2026-11-23. Each hull is reduced to three or four pieces of at most 18,000 triangles, with 1024 px textures.

In the place, the user model is the visible exterior. A `CrewLayer` inside each vehicle holds the robot seats, the Board prompt and a server script; `Roblox/vehicle_crew_layer.lua` builds it. Robots board with the prompt and are seated. Walk-in entry would make these hulls oversized, so it isn't used. Every seat was checked as enclosed by the hull, and a playtest boarded every crewed vehicle into its first seat.

| Bible ID | Vehicle (user model) | Roblox asset | Length (studs) | Seats | Faces | Position in yard (X, Z) |
|---|---|---|---|---|---|---|
| VEH-04 | TITAN-R1 Cargo Transport (DROE Titan Rover) | 107446849916205 (rev 4) | 32 | 4 (driver, co-driver, 2 crew) | −X | (−32, 36) |
| VEH-09 | NX-A17 Raven (Jet2) | 140225470731589 | 48 (41.6 span) | 9 (pilot + 8) | −X | (0, 80) |
| VEH-10 | Industrial Freight Train | 124641651466353 | 96 | 7 (locomotive) | −X | (0, 140) |
| VEH-11 | Armored Security Carrier | 88628350523039 | 40 | 5 | −X | (32, 34) |
| VEH-12 | Armored Security VTOL | 76999252171451 | 50 | 9 | −X | (−45, 205) |
| VEH-14 | Tracked Utility Hauler | 111991835516707 | 28 | 3 (behind the cab) | −X | (10, 205) |
| VEH-15 | Armored 8x8 Patrol (Desert Sentinel 8x8) | 85593428487775 | 38 | 4 | −X | (55, 205) |
| VEH-16 | Battle Walker (Battlemech) | 76360997961306 | 14 tall | none (enemy machine) | — | (30, 268) |
| VEH-17 | Thunderfang X-804 walker squad | 131523247905987 | 30 | none (enemy squad) | — | (−30, 268) |

## Pipeline lessons (2026-11-23)
- **Weld before decimating.** Some Meshy exports are "triangle soup", and the hull shattered without welding (Titan Rover).
- **Strip emissive maps.** Roblox has no emissive slot.
- **Watch for baked normal maps that wash a material out to flat grey.** Pass `nonormal` to the prep script, and isolate maps on clones in Studio if a hull renders grey.
- **Fix the import rotation.** Roblox inserts imports at an arbitrary yaw; align before placing seats (`align()` in the builder).
- **Re-upload as a revision.** Use `PATCH /assets/v1/assets/{id}` instead of creating a duplicate asset.
- **Don't trust dark Blender Workbench thumbnails of Meshy files.** They can show the black emissive map rather than the real colours.
