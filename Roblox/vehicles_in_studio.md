# Supplied vehicles in Roblox Studio

These are the user's Meshy vehicle models, prepared with `Blender/scripts/pz_vehicle_prep.py` and imported into the ProjectZero place (universe 10778699105) on 2026-11-23. Each hull is reduced to three or four pieces of at most 18,000 triangles. Since the 2026-11-23 evening re-bake, each piece has its own 1024 px texture set (colour, normal, roughness and metalness) baked from the full-detail original onto clean UVs. Earlier revisions used the original textures on decimated UVs, which tore and smeared them.

In the place, the user model is the visible exterior. A `CrewLayer` inside each vehicle holds the robot seats, the Board prompt and a server script; `Roblox/vehicle_crew_layer.lua` builds it. Robots board with the prompt and are seated. Walk-in entry would make these hulls oversized, so it isn't used. Every seat was checked as enclosed by the hull, and a playtest boarded every crewed vehicle into its first seat.

| Bible ID | Vehicle (user model) | Roblox asset | Length (studs) | Seats | Faces | Position in yard (X, Z) |
|---|---|---|---|---|---|---|
| VEH-04 | TITAN-R1 Cargo Transport (DROE Titan Rover) | 107446849916205 (rev 8) | 32 | 4 (driver, co-driver, 2 crew) | −X | (−32, 36) |
| VEH-09 | NX-A17 Raven (Jet2) | 140225470731589 (rev 2) | 48 (41.6 span) | 9 (pilot + 8) | −X | (0, 80) |
| VEH-10 | Industrial Freight Train | 124641651466353 (rev 3) | 96 | 7 (locomotive) | −X | (0, 140) |
| VEH-11 | Armored Security Carrier | 88628350523039 (rev 3) | 40 | 5 | −X | (32, 34) |
| VEH-12 | Armored Security VTOL | 76999252171451 (rev 2) | 50 | 9 | −X | (−45, 205) |
| VEH-14 | Tracked Utility Hauler | 111991835516707 (rev 2) | 28 | 3 (behind the cab) | −X | (10, 205) |
| VEH-15 | Armored 8x8 Patrol (Desert Sentinel 8x8) | 85593428487775 (rev 2) | 38 | 4 | −X | (55, 205) |
| VEH-16 | Battle Walker (Battlemech) | 76360997961306 (rev 2) | 11.9 tall, 14 wide | none (enemy machine) | — | (30, 268) |
| VEH-17 | Thunderfang X-804 walker squad | 131523247905987 (rev 2) | 30 | none (enemy squad) | — | (−30, 268) |

## Pipeline lessons (2026-11-23)
- **Weld before decimating.** Some Meshy exports are "triangle soup", and the hull shattered without welding (Titan Rover).
- **Strip emissive maps.** Roblox has no emissive slot.
- **Bake, don't decimate the textures.** Decimation collapses UV seams, which tears and smears the original textures. The prep script's `bake` mode makes fresh UVs per piece and bakes colour, normal and roughness from the full-detail original (Cycles, selected-to-active).
- **Metalness must be in the texture, not the factor.** Blender's exporter writes a constant Metallic as blue = 1 plus a small `metallicFactor`. Roblox ignores the factor, so every baked vehicle rendered as chrome. The prep script now writes metalness into the blue channel. `pz_glb_fix_metal.py` repairs an existing GLB.
- **Don't insert an upload straight away.** Roblox generates each new mesh and texture's streamable form in the background. Studio tries three times ("Asset content representation is being generated"), then shows the coarse placeholder mesh with no textures for the rest of the session. Identical files reuse the same IDs, so re-uploading doesn't help. Insert into ServerStorage first, wait a few minutes, check the output log, then move the model into Workspace. A hull that is uniformly light grey and lumpy is this problem, not a bad normal map (the earlier `nonormal` diagnosis for the Titan was wrong).
- **Split non-manifold edges after welding.** Welding a triangle soup leaves edges shared by three or more faces (300 to 500 per Titan piece). `pz_fix_nonmanifold.py` splits them.
- **Fix the import rotation.** Roblox inserts imports at an arbitrary yaw; align before placing seats (`align()` in the builder).
- **Re-upload as a revision.** Use `PATCH /assets/v1/assets/{id}` instead of creating a duplicate asset.
- **Don't trust dark Blender Workbench thumbnails of Meshy files.** They can show the black emissive map rather than the real colours.

## Supplied rooms in Roblox Studio

| Bible ID | Room (user model) | Roblox asset | Size (studs) | Use |
|---|---|---|---|---|
| INT-12 | Robot Containment Chamber | 123299766335093 | 49.5 × 25.5 × 16.85 | Two copies form the R04 pod bays: pods P01–P08, built by `Roblox/BLD-01_pod_chambers.lua` |

Prepared with `Blender/scripts/pz_room_prep.py`:
- The scale is set so a pod holds Sentinel (7.5).
- Pods were found by a voting (Hough) search on the pale-blue glass.
- The glass was split into its own pieces, and the 2.3 M triangles were cut to 6 × 18 k with textures baked from the original.

The model's glass panels sit at the back of each bay, so the pods are closed in game by a cyan ForceField "stasis field" on each platform.

## Cabins (2026-11-24)
Owner feedback: inside a vehicle there were "only a couple of blocks", and the hull was see-through from inside.
`Roblox/VEH_cabins_build.lua` (edit time, re-runnable) fixes every crewed vehicle:
- **Hulls:** MeshParts are `DoubleSided`, so the outer skin also renders from inside.
- **Seats:** each crew Seat stays functional (boarding unchanged) but is invisible. The owner's Command Chair (INT-15, `ServerStorage.Props.PZ_CabinChair`, 4k triangles) sits in its place on a diamond-plate mounting plate. The seats are at different heights because the fit scan places each one where a robot fits inside that hull.
- **Driver console:** the owner's Command Console (INT-14, `ServerStorage.Props.PZ_CabinConsole`) goes in front of seat Order 1. It's pulled back if the hull is close, and skipped if there's no room.
- **Light:** one soft cabin light.

Everything is welded to the seats (unanchored, massless, non-colliding), so it moves with the vehicle once driving exists.
For hero vehicles, an owner-made Meshy cabin interior can replace this later.

## Meshy cabin interiors (owner decision 2026-11-24: to be made on Meshy later)
The owner prefers Meshy-made interiors over hand-built liners. Until they exist, the chairs, consoles and double-sided hulls stay.
Interiors should be **empty** (no seats): the owner's Command Chair is fitted on each fit-scanned seat, and the driver console stays.
When an interior arrives, I prep and bake it, scale it to the size below, fit it inside the hull, and keep the chairs.

Shared style for every prompt (matches the facility and city): *white and dark grey panels, orange accents, thin cyan light strips, clean futuristic robot vehicle, no seats, no people*.

| Vehicle | Inside size to aim for (L × W × H, studs) | Prompt |
|---|---|---|
| Armored Security Carrier | 26 × 10 × 9 | "armored troop carrier cabin interior, long narrow cabin, padded wall panels, grab rails on the ceiling, small side windows, rear ramp door" |
| Titan Rover | 21 × 9 × 9 | "heavy cargo rover crew cabin interior, compact cab, overhead equipment racks, small windshield at the front" |
| Tracked Hauler | 17 × 9 × 8 | "tracked utility hauler cab interior, compact industrial cab, toolboxes and pipes on the walls" |
| Desert Sentinel 8x8 | 22 × 9 × 9 | "armored 8x8 patrol vehicle interior, crew compartment, wall screens, storage lockers" |
| Raven VTOL (Jet 2) | 31 × 18 × 8 | "VTOL aircraft cockpit and passenger cabin interior, wide cabin, cockpit windows at the front, overhead panels" |
| Security VTOL | 41 × 15 × 10 | "large security VTOL troop bay interior, two-level seating platforms, side doors, cargo netting" |
| Freight Train | 31 × 13 × 8 | "freight train crew car interior, long narrow carriage, side windows, overhead cable trays" |

Sizes are the seats' footprint plus room to move; the height fits Sentinel (7.5 studs).
