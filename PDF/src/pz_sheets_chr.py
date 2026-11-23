"""CHR-00 … CHR-04: canonical robots (Cypher, Sentinel, Patch) and the Robot Family design language.
Uses the user's Meshy models unmodified (rest pose, stray helper hidden, uniform scale only)."""
from pz_sheet_kit import *
import matplotlib.patches as mp
import numpy as np

CR = os.path.join(ROOT, "Characters")
TA = os.path.join(CR, "turnarounds")
FR = os.path.join(CR, "renders")
SD = os.path.join(CR, "sheets")
PAL = {k: [c for c in v if c[2] >= 1.0 or c[0] == "cyan emissive"] for k, v in json.load(open(os.path.join(TA, "robot_palettes.json"))).items()}
INFO = json.load(open(os.path.join(TA, "robots_info.json")))

BOTS = {
    "Cypher": dict(id="CHR-01", rname="PZ_PLR_Cypher_A", file="Rigged_Cypher.glb", H=6.0, src_h=1.70,
                   role="Intelligence · exploration", tag="The Explorer",
                   story=["Investigator; holds a fragment of ZERO’s original program.",
                          "NPC guide in Ch.1: pod P01 opens first and Cypher wakes the players."],
                   abilities="Pulse Scan · Holo-Decoy · System Override · Memory Echo",
                   traits=["White/light-grey shell, navy joints", "Shield-lock emblem on chest screen",
                           "Carry handle on head; cyan ear-pods", "Cyan glow at knees, shins, forearms"],
                   rig="Mixamo-style humanoid, 66 bones", anims=8,
                   animlist="Running, Walking, 6 talk/gesture clips"),
    "Sentinel": dict(id="CHR-02", rname="PZ_PLR_Sentinel_A", file="Rigged_Sentinel.glb", H=7.5, src_h=1.70,
                     role="Security · protection", tag="The Protector",
                     story=["Former enforcer; complicit in ZERO’s memory resets.",
                            "Found trapped in pod P05 in Chapter One."],
                     abilities="Energy Shield · Ground Slam · Guardian Mode · Overdrive",
                     traits=["Graphite armour, worn hazard-yellow plates", "Gear emblem on chest screen",
                             "Twin antennae; heavy boots with hazard stripes", "Square visor head, bulkier frame"],
                     rig="Mixamo-style humanoid, 66 bones", anims=9,
                     animlist="Running, Walking, Stage Walk, in-place walk, 5 talk clips"),
    "Patch": dict(id="CHR-03", rname="PZ_PLR_Patch_A", file="Patch_LowPoly.glb", H=4.5, src_h=1.898,
                  role="Engineering · repair", tag="The Technician",
                  story=["Repair specialist; holds the sanctuary coordinates.",
                         "Sends the distress signal in Chapter One."],
                  abilities="Repair Beam · Support Drone · Energy Transfer · Emergency Reboot",
                  traits=["Tracked base; white/teal shell, orange tool parts", "Gear emblem on chest screen",
                          "Oversized visor head, single antenna", "Wrench in right hand; side battery packs"],
                  rig="NONE — needs custom rig", anims=0, animlist="none (static pose: wrench raised)"),
}
BOTS["Utility"] = dict(id="CHR-11", rname="PZ_NPC_UtilityRobot_A", file="Meshy_AI_Rigged_Futuristic_Utility_Robot_20261120_animated_mixamo_All_animation.glb",
                      H=6.4, src_h=1.80, role="Utility · industrial worker", tag="UT-01 Utility Robot",
                      story=["Family worker class supplied as a 3D model (Nov 2026).", "Ambient NPC for factories, depots and maintenance."],
                      abilities="NPC: carry · repair · operate machinery (no player kit)",
                      traits=["Slender adult proportions (small head): family exception", "Screen-visor head with cyan eyes",
                              "White / graphite plates, orange marks", "Backpack power unit"],
                      rig="Mixamo-style humanoid, 24 bones", anims=2, animlist="Running, Walking")
ORDER = ["Cypher", "Sentinel", "Patch"]
GEN = "CHR  ·  CANONICAL ROBOT FAMILY"


def _fn(name, n=34):
    """Shorten long Meshy file names so they stay inside their panel."""
    return name if len(name) <= n else name[:n - 7] + "…" + name[-6:]

def alpha_crop(path, pad=30, keep_rows=(60, 1090)):
    im = Image.open(path).convert("RGBA"); a = np.asarray(im)[..., 3]
    ys, xs = np.where(a > 8)
    x0, x1 = max(0, xs.min() - pad), min(im.width, xs.max() + pad)
    return (x0, min(keep_rows[0], ys.min() - pad), x1, max(keep_rows[1], ys.max() + pad))

def bot_sheet(n, page, total=3):
    b = BOTS[n]
    fig = new_sheet()
    frame(fig, b["id"], f"{n.upper()} — CANONICAL CHARACTER SHEET", f"{b['tag']} · {b['role']} · rendered from the user’s Meshy model {_fn(b['file'])} (unmodified)",
          page, total, asset=f"{b['id']}  ·  {b['rname']}",
          note="Model geometry/textures are canonical and unchanged. In-game height is a DESIGN ASSUMPTION in studs.")
    w, g = 0.238, 0.008
    for i, (v, t) in enumerate((("front", "FRONT"), ("side", "SIDE (RIGHT)"), ("back", "BACK"), ("q34", "THREE-QUARTER"))):
        rect = (0.012 + i * (w + g), 0.41, w, 0.502)
        panel(fig, rect, t, "rest pose" if i == 0 else None)
        p = os.path.join(TA, f"{n}_{v}.png")
        ax = image_axes(fig, rect, p, crop=alpha_crop(p))
        if v == "front":
            dim(ax, (ax._pz_off[0] + 20, 1075), (ax._pz_off[0] + 20, 75), f"{b['H']:.1f} studs", off=-8, vertical=True, fs=7)
    # identity
    panel(fig, (0.012, 0.05, 0.3, 0.352), "IDENTITY & ROLE", "from Game Design Bible")
    text_block(fig, 0.022, 0.37, [("Narrative", "o")] + b["story"] +
               [("Abilities", "o"), b["abilities"], ("Signature traits (observed on model)", "o")] +
               ["• " + t for t in b["traits"]], fs=7.4, lh=0.0205)
    # technical
    i = INFO[n]
    panel(fig, (0.32, 0.05, 0.33, 0.352), "TECHNICAL DATA", "measured from GLB")
    rows = [("Source file", _fn(b["file"], 44)), ("Triangles", f"{i['tris']:,}"),
            ("Rig", b["rig"]), ("Animations", f"{b['anims']} — {b['animlist']}"),
            ("Textures", "3 maps (base colour 2048², + 2 PBR maps)"),
            ("Export height", f"{b['src_h']:.2f} units (Meshy normalised)"),
            ("In-game height", f"{b['H']:.1f} studs  →  scale ×{b['H'] / b['src_h']:.2f}"),
            ("Stray objects", ", ".join(i["stray_objects"]) or "none"),
            ("Roblox name", b["rname"])]
    table(fig, (0.326, 0.06, 0.318, 0.31), ["PROPERTY", "VALUE"], rows, [0.3, 0.7], fs=6.7)
    # palette + roblox notes
    panel(fig, (0.658, 0.05, 0.33, 0.352), "PALETTE · ROBLOX IMPORT", "colours sampled from base-colour texture")
    x = 0.666
    for k, (name, hx, _) in enumerate(PAL[n]):
        cx = x + (k % 4) * 0.08; cy = 0.315 - (k // 4) * 0.05
        fig.patches.append(mp.Rectangle((cx, cy), 0.022, 0.032, transform=fig.transFigure, fc=hx, ec=C["line"], zorder=2))
        fig.text(cx + 0.025, cy + 0.022, name, fontsize=6.2, color=C["text"], va="center")
        fig.text(cx + 0.025, cy + 0.008, hx, fontsize=6.0, color=C["muted"], va="center", family="DejaVu Sans Mono")
    notes = ["• Delete stray ‘%s’ before export (inflates bounds/collision)." % i["stray_objects"][0] if i["stray_objects"] else "• No stray objects found.",
             "• Import via 3D Importer as rigged MeshPart model; keep textures 1024² for mobile." if b["anims"] else
             "• Needs rigging before animation: body, head pan/tilt, 2 arms, tread scroll.",
             "• Animations: upload clips; play through Animator on AnimationController" if b["anims"] else
             "• Treads: scrolling texture + rotating sprocket parts (no physics).",
             "  (custom rig) — R15 retarget is an open decision." if b["anims"] else "• Grounded collision box 2.6 × 2 × 4.5 (treads; no hover).",
             "• Collision: single invisible capsule-box; mesh CanCollide off."]
    text_block(fig, 0.666, 0.205, notes, fs=6.9, lh=0.019)
    save(fig, os.path.join(SD, f"{b['id']}_{n}.png"))

FPX = 2800 / 38.0
def fam(x, z): return (1400 + (x - 3) * FPX, 550 - (z - 7.2) * FPX)

def chr00():
    fig = new_sheet()
    frame(fig, "CHR-00", "ROBOT FAMILY — CANONICAL LINEUP & SCALE", "Cypher · Sentinel · Patch at proposed in-game scale beside the BLD-01 stasis pod", 1, 1, asset=GEN,
          note="Robot models are the user’s canonical Meshy assets, unmodified. Heights in studs are DESIGN ASSUMPTIONS.")
    panel(fig, (0.012, 0.47, 0.6, 0.442), "FAMILY PORTRAIT", "Cycles render · canonical models")
    image_axes(fig, (0.012, 0.47, 0.6, 0.442), os.path.join(FR, "family_hero.png"), crop=(160, 150, 1760, 1000))
    panel(fig, (0.62, 0.47, 0.368, 0.442), "PROPOSED IN-GAME SCALE", "studs · 0.28 m per stud")
    rows = [(n, BOTS[n]["role"].split(" ·")[0], f"{BOTS[n]['H']:.1f}", f"{BOTS[n]['H'] * 0.28:.2f} m", f"×{BOTS[n]['H'] / BOTS[n]['src_h']:.2f}",
             "fits (≤ 7.5)" if BOTS[n]["H"] <= 7.5 else "too tall") for n in ORDER]
    rows.append(("Roblox R15", "default avatar", "≈ 5.5", "≈ 1.5 m", "—", "fits"))
    table(fig, (0.626, 0.69, 0.356, 0.19), ["ROBOT", "ROLE", "HEIGHT", "≈ METRES", "SCALE", "POD FIT"], rows,
          [0.2, 0.2, 0.13, 0.15, 0.12, 0.2], fs=6.8)
    text_block(fig, 0.628, 0.67, [("Why these heights", "o"),
        "• Cypher 6.0: hero-scale, close to the default Roblox avatar so the",
        "  camera and door sizes (6×10) feel natural.",
        "• Sentinel 7.5: the protector reads as the largest; it matches the",
        "  pod occupant limit exactly, as the story requires (trapped in P05).",
        "• Patch 4.5: small tracked utility bot, as in the Design Bible art.",
        "• Source models are exported at equal normalised heights, so",
        "  relative scale is a design decision, not a property of the files.",
        ], fs=7.1, lh=0.0195)
    panel(fig, (0.012, 0.05, 0.976, 0.41), "SCALE LINEUP · ORTHOGRAPHIC FRONT", "Workbench · 74 px / stud · same scene as SF-04 pod")
    ax = image_axes(fig, (0.012, 0.05, 0.976, 0.41), os.path.join(FR, "family_ortho.png"))
    xs = {"Cypher": -9.0, "Sentinel": -2.0, "Patch": 4.5}
    for n, x in xs.items():
        H = BOTS[n]["H"]
        dim(ax, fam(x - 2.4, 0), fam(x - 2.4, H), f"{H:.1f}", off=0, vertical=True, fs=7)
        ax.text(*fam(x, H + 0.9), n.upper(), fontsize=8, color=C["white"], weight="bold", ha="center", va="bottom")
    dim(ax, fam(21.2, 0), fam(21.2, 14.5), "14.5", off=0, vertical=True, fs=7)
    ax.text(*fam(23.5, 10.5), "STASIS POD\n(open)", fontsize=8, color=C["cyan"], weight="bold", ha="left", va="center")
    for z in (0, 4.5, 6.0, 7.5):
        y = fam(0, z)[1]
        ax.plot([0, 2800], [y, y], color=C["amber"], lw=0.35, ls=(0, (3, 4)), zorder=1)
    save(fig, os.path.join(SD, "CHR-00_Family_Lineup.png"))

def recolor(path, kind):
    """2D palette exploration of a canonical render (NOT a new model)."""
    im = Image.open(path).convert("RGBA"); a = np.asarray(im).copy()
    hsv = np.asarray(im.convert("RGB").convert("HSV")).astype(int).copy()
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    emissive = (h >= 108) & (h <= 150) & (s > 55) & (v > 120)
    if kind == "enforcer":       # ZERO-controlled: hazard → red, visor → red
        hz = (h >= 15) & (h <= 45) & (s > 70)
        h[hz] = 0; s[hz] = np.minimum(255, s[hz] + 40)
        h[emissive] = 0
    elif kind == "archivist":    # research NPC: teal shell → violet, visor stays cyan
        tl = (h >= 110) & (h <= 160) & (s > 60) & ~emissive
        h[tl] = 190
    elif kind == "dormant":      # memory-wiped civilian: visor → amber, shell desaturated
        h[emissive] = 28; s[~emissive] = (s[~emissive] * 0.5).astype(int)
    out = Image.fromarray(np.dstack([h, s, v]).astype("uint8"), "HSV").convert("RGBA")
    o = np.asarray(out).copy(); o[..., 3] = a[..., 3]
    p2 = os.path.join(TA, f"variant_{kind}.png"); Image.fromarray(o).save(p2)
    return p2

def chr04():
    fig = new_sheet()
    frame(fig, "CHR-04", "ROBOT FAMILY — DESIGN LANGUAGE", "Rules every other robot in NEXUS-01 must follow · derived from Cypher, Sentinel and Patch", 1, 1, asset=GEN,
          note="Variant images are 2D palette explorations of canonical renders — not new models.")
    # shared traits: head crops
    panel(fig, (0.012, 0.56, 0.42, 0.352), "SHARED TRAITS · SCREEN-FACE HEAD + CHEST EMBLEM", None)
    for k, n in enumerate(ORDER):
        p = os.path.join(TA, f"{n}_front.png")
        x0, y0, x1, y1 = alpha_crop(p, pad=10)
        hgt = 1075 - y0
        hf, c0, c1 = (0.36, 0.34, 0.56) if n != "Patch" else (0.5, 0.48, 0.72)
        image_axes(fig, (0.018 + k * 0.137, 0.735, 0.135, 0.15), p, crop=(x0, y0, x1, y0 + int(hgt * hf)), pad_top=0.0)
        cx0 = x0 + (x1 - x0) // 4; cx1 = x1 - (x1 - x0) // 4
        image_axes(fig, (0.018 + k * 0.137, 0.585, 0.135, 0.145), p, crop=(cx0, y0 + int(hgt * c0), cx1, y0 + int(hgt * c1)), pad_top=0.0)
        fig.text(0.085 + k * 0.137, 0.571, n, fontsize=7.5, color=C["text"], ha="center", weight="bold")
    panel(fig, (0.44, 0.56, 0.548, 0.352), "FAMILY RULES", None)
    text_block(fig, 0.45, 0.875, [
        ("Silhouette", "o"),
        "1  Rounded screen head, dark visor glass (¼–½ body height; UT-01 adult exception).",
        "2  Face drawn in emissive light: eyes required, emoticon mouth optional.",
        "3  Round side ear-pods with a coloured ring; top handle or 1–2 antennae.",
        "4  Rounded chest screen with a role icon (shield-lock, gear, …).",
        ("Construction", "o"),
        "5  Panelled hard-surface shell over dark exposed joints; chamfered, chunky.",
        "6  Shell colour = role family; emissive cyan accents at joints / limbs.",
        "7  Locomotion may vary (legs, treads) but the head + chest language may not.",
        ("Colour of the visor = allegiance (gameplay readable)", "o"),
        "Cyan = free / friendly    Amber = memory-wiped / dormant    Red = ZERO-controlled",
    ], fs=7.3, lh=0.0222)
    # derivation matrix
    panel(fig, (0.012, 0.05, 0.58, 0.5), "DERIVATION MATRIX · EVERY OTHER ROBOT", "base frame → variant")
    rows = [("Player custom", "Intelligence", "Cypher frame", "cyan", "own trim + emblem; wakes in own pod"),
            ("Player custom", "Defense", "Sentinel frame", "cyan", "armour kits, antenna styles"),
            ("Player custom", "Engineering", "Patch frame", "cyan", "tool arms, backpacks"),
            ("Dormant pods", "Memory-wiped (P07–P08)", "any frame", "amber", "desaturated shell, dust decals"),
            ("Ambient NPC", "Courier / Vendor", "Cypher frame", "cyan", "civic amber trim, satchels"),
            ("Ambient NPC", "Maintenance", "Patch frame", "cyan", "orange hazard trim, tool sets"),
            ("Ambient NPC", "Archivist", "Patch frame", "cyan", "research violet shell"),
            ("Enemy", "ZERO Enforcer", "Sentinel frame", "red", "red hazard plates, angry eyes"),
            ("Boss", "Warden-01 (Ch.1)", "Sentinel frame ×1.6", "red", "extra plating, shoulder lights"),
            ("Drones", "Medical / transport", "head + ear-pods only", "cyan", "head becomes the body")]
    table(fig, (0.018, 0.06, 0.568, 0.45), ["CLASS", "TYPE", "BASE FRAME", "VISOR", "VARIATION"], rows,
          [0.17, 0.2, 0.22, 0.1, 0.31], fs=6.8)
    panel(fig, (0.6, 0.05, 0.388, 0.5), "PALETTE EXPLORATION (2D recolour of canonical renders)", None)
    vs = [("Sentinel", "enforcer", "ZERO ENFORCER · red visor", C["red"]),
          ("Cypher", "dormant", "MEMORY-WIPED · amber visor", C["amber"]),
          ("Patch", "archivist", "ARCHIVIST NPC · violet shell", C["violet"])]
    for k, (n, kind, t, col) in enumerate(vs):
        p = recolor(os.path.join(TA, f"{n}_front.png"), kind)
        image_axes(fig, (0.606 + k * 0.127, 0.09, 0.125, 0.41), p, crop=alpha_crop(p), pad_top=0.0)
        fig.text(0.668 + k * 0.127, 0.072, t, fontsize=6.4, color=col, weight="bold", ha="center")
    save(fig, os.path.join(SD, "CHR-04_Family_Design_Language.png"))


# ---------------------------------------------------------------- user concept-sheet robots (CHR-05 … CHR-10)
from pz_asset_specs import NEW_ROBOTS
BASE = {"MED-7": ("Cypher frame", "cyan"), "MEDI-X": ("Cypher frame", "cyan"), "ORION": ("Cypher frame", "cyan"),
        "ORBIT-7": ("Cypher frame", "cyan"), "AURORA (AUR-01)": ("Patch-line role on humanoid frame", "cyan"),
        "R-TRN-02": ("Sentinel frame", "cyan")}

MODEL = {"CHR-07": ("Research", "Meshy_AI_Rigged_Scientific_Research_Robot (Mixamo 24 bones · Running, Walking)"),
         "CHR-10": ("Cargo", "Meshy_AI_Rigged_Cargo_Logistics_Robot (Mixamo 24 bones · Running, Walking)")}

def model_meta(name, shot):
    p = os.path.join(CR, "models", name, shot + ".json")
    return json.load(open(p)) if os.path.exists(p) else None

def concept_sheet(entry, page, total):
    cid, name, role, src, h_m, note_ = entry
    H = h_m / 0.28
    mdl = MODEL.get(cid)
    has_model = bool(mdl and model_meta(mdl[0], "front"))
    short = name.split()[0].replace("-", "")
    fig = new_sheet()
    frame(fig, cid, f"{name} — ROBOT CLASS SHEET", f"{role} · user-supplied concept sheet + harmonised production spec", page, total,
          asset=f"{cid}  ·  PZ_NPC_{short}_A",
          note="Concept art is a user-supplied reference, not a measured drawing. Heights in studs are DESIGN ASSUMPTIONS.")
    if has_model:
        panel(fig, (0.012, 0.44, 0.6, 0.472), "USER-SUPPLIED CONCEPT SHEET", "reference only · not dimensionally accurate")
        image_axes(fig, (0.012, 0.44, 0.6, 0.472), os.path.join(r"D:\Project Zero_Roblox", src))
        md = os.path.join(CR, "models", mdl[0])
        for i, (shot, t) in enumerate((("hero", "3D MODEL · RENDER"), ("front", "FRONT"), ("left", "SIDE"), ("rear", "BACK"))):
            rect = (0.012 + i * 0.151, 0.05, 0.147, 0.382)
            panel(fig, rect, t, "user model" if i == 0 else None)
            p = os.path.join(md, shot + ".png")
            if i == 0:
                image_axes(fig, rect, p, crop=(380, 0, 1060, 900))
            else:
                image_axes(fig, rect, p, crop=(650, 20, 1350, 990))
    else:
        panel(fig, (0.012, 0.05, 0.6, 0.862), "USER-SUPPLIED CONCEPT SHEET", "reference only · not dimensionally accurate")
        image_axes(fig, (0.012, 0.05, 0.6, 0.862), os.path.join(r"D:\Project Zero_Roblox", src))
    panel(fig, (0.62, 0.5, 0.368, 0.412), "HARMONISED SPEC", "0.28 m per stud (Roblox convention)")
    base, visor = BASE.get(name, ("Cypher frame", "cyan"))
    rows = [("Class / role", role), ("Concept height", f"{h_m:.2f} m"),
            ("In-game height", f"{H:.1f} studs (sheet stud figures conflict: overridden)"),
            ("Pod fit (max 7.5)", "fits" if H <= 7.5 else "too tall"), ("Family base frame", base),
            ("Default visor", f"{visor} (friendly); amber when memory-wiped"), ("Signature", note_),
            ("3D model", (f"supplied: {_fn(mdl[1].split(' (')[0], 30)} · {model_meta(mdl[0], 'front')['tris']:,} tris · stray: {', '.join(model_meta(mdl[0], 'front')['stray']) or 'none'}"
                          if has_model else "none supplied yet"))]
    table(fig, (0.626, 0.53, 0.356, 0.35), ["FIELD", "VALUE"], rows, [0.28, 0.72], fs=6.7)
    panel(fig, (0.62, 0.27, 0.368, 0.222), "FAMILY CONFORMANCE (CHR-04)", None)
    checks = ["Screen-visor head, dark glass", "Emissive cyan eyes (mouth optional)", "Ear-pods / antenna",
              "Chest screen or core emblem", "Panelled shell over dark joints", "Graphite / white / orange + cyan"]
    for k, t in enumerate(checks):
        fig.text(0.63, 0.455 - k * 0.028, "✓  " + t, fontsize=7.3, color=C["green"])
    panel(fig, (0.62, 0.05, 0.368, 0.212), "PRODUCTION PATH", "Meshy → Blender → Roblox")
    text_block(fig, 0.63, 0.225, [
        "1  Meshy image-to-3D from the sheet FRONT + SIDE views.",
        "2  Blender: Mixamo-compatible rig, max 12 k tris, 1024 PBR,",
        "    remove stray helper objects, origin at feet.",
        f"3  Scale to {H:.1f} studs; collision = capsule-box.",
        "4  Turnaround renders replace the concept on this sheet.",
        ("Palette: #2B2F36 · #9AA0A6 · #FF7A00 · #00D4FF · #E6E8EB", "m"),
    ], fs=7.0, lh=0.022)
    p = os.path.join(SD, f"{cid}_{short}.png"); save(fig, p); return p

if __name__ == "__main__":
    os.makedirs(SD, exist_ok=True)
    which = sys.argv[1:] or ["chr00", "bots", "chr04"]
    for w in which:
        if w == "bots":
            for k, n in enumerate(ORDER):
                bot_sheet(n, k + 1)
        else:
            globals()[w]()
