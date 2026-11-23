# BLD-01 Stasis Facility — Meshy generation prompts

Use Meshy only for distinctive silhouettes and decorative machinery (NEXUS-01 bible §8).
Walls, floors, vault collision and every gameplay surface stay as Studio parts built from sheet SF-02 / SF-05.

**Reference images to attach:** the orthographic renders in `Stasis_Facility/renders/` named in each entry, plus `Source_Documents/audit_renders/NEXUS01_p10_StasisReference.png` for style.

**Shared style suffix (append to every prompt):**
> futuristic industrial sci-fi, graphite brushed metal panels, orange industrial accents, cyan emissive light strips, clean hard-surface panel lines, chamfered edges, believable engineering, game-ready, no text, no logos

**Shared negative prompt:**
> organic, rust holes, cartoon, toy, plastic, glossy chrome, characters, humans, robots, text, watermark, base plate, ground

| Module | Prompt (before suffix) | Reference renders | Target after Blender | Notes |
|---|---|---|---|---|
| BLD-01-M01 Stasis pod shell (K06) | cylindrical cryogenic stasis pod, octagonal heavy base plinth, tall glass cylinder, thick round cap with a glowing ring band, small crown housing on top, two coolant pipes and one conduit at the back | pod_closed_front, pod_closed_left, pod_closed_rear, pod_closed_top | ≤ 6 k tris; glass split into two half-shells; origin at floor centre | Generate the shell without glass. Model the glass in Blender as two half-cylinders so the front half can hinge |
| BLD-01-M02 Octagonal door frame (K07) | thick octagonal blast door frame set in a square wall plate, two sliding door leaves with a vertical glowing seam, orange horizontal band | elev_front (Detail A on SF-01) | ≤ 2.5 k tris | Leaves become separate Parts for tweening |
| BLD-01-M03 Manipulator arm | industrial ceiling-mounted robotic arm, orange painted segments, dark graphite joints, two-finger gripper | int_chamber, section_chamber | ≤ 4 k tris, 3 bones (base, elbow, wrist) | Rig in Blender; AnimationController in Studio |
| BLD-01-M04 Pod console (K10) | small floor-standing control console pedestal with a tilted glowing screen | pod_closed_right | ≤ 600 tris | Screen face separate material for Neon/SurfaceGui |
| BLD-01-M05 Power / diagnostic unit | boxy power diagnostic cabinet, side screen, amber status strip, vents | pod_closed_front | ≤ 800 tris | |
| BLD-01-M06 Cryo tank | vertical cryogenic coolant tank, domed caps, blue band, pipe flanges | section_chamber | ≤ 1.5 k tris | Reused on the roof (horizontal) and in R06 |
| BLD-01-M07 Roof cooling unit | rooftop industrial cooling unit with a large circular fan grille, orange hub | roof_plan, elev_right | ≤ 1.2 k tris | Fan as separate part for spin |

**Do not use Meshy for:** walls, floors, vault shell, ribs, stairs or mezzanine. These are Studio parts, because exact grid snapping and collision matter more than surface detail.
