"""Write Meshy_Prompts/<ID>_meshy.md and Roblox/<ID>_roblox_spec.md for every asset with a spec (Phase 8 file structure)."""
import os
import pz_inventory as INV
from pz_asset_specs import SPECS, CAT_TEMPLATES
ROOT = r"D:\Project Zero_Roblox\Project_Zero_Production_Bible"
SUFFIX = "futuristic industrial sci-fi, graphite brushed metal panels, orange industrial accents, cyan emissive light strips, clean hard-surface panel lines, game-ready, no text, no logos"
NEG = "organic, rust holes, cartoon toy, glossy chrome, humans, text, watermark, base plate"
inv = {a[0]: a for a in INV.ASSETS}
n = 0
for aid, s in SPECS.items():
    a = inv.get(aid); t = CAT_TEMPLATES[aid[:3]]
    name = a[1] if a else aid
    with open(os.path.join(ROOT, "Meshy_Prompts", f"{aid}_meshy.md"), "w", encoding="utf-8") as f:
        f.write(f"# {aid} {name}: Meshy prompt\n\n**Prompt:** {s[4]}, {SUFFIX}\n\n**Negative:** {NEG}\n\n"
                f"**Reference images:** the orthographic renders on the {aid} sheet (front, side, top) plus any user concept named on the sheet.\n\n"
                f"**Target after Blender:** {t['blender']}\n\n_Dimensions ({a[5] if a else '-'} studs) are design assumptions._\n")
    with open(os.path.join(ROOT, "Roblox", f"{aid}_roblox_spec.md"), "w", encoding="utf-8") as f:
        f.write(f"# {aid} {name}: Roblox spec\n\n| Field | Value |\n|---|---|\n"
                f"| Roblox name | `{INV.roblox_name(a) if a else ''}` |\n| Purpose | {s[0]} |\n| Interaction | {s[2]} |\n"
                f"| Animation | {s[3]} |\n| Modular construction | {t['modular']} |\n| Implementation | {t['roblox']} |\n"
                f"| Collision | {t['collision']} |\n| LOD | {t['lod']} |\n| Complexity / priority | {a[4] if a else ''} / {a[3] if a else ''} |\n"
                f"| Dependencies | {a[6] if a else ''} |\n\nStatus: design only. Not built in Studio yet (Phase 9).\n")
    n += 1
print("WROTE", n, "assets x 2 files")
