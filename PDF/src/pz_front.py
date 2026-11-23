"""Front matter: cover, contents, reference audit, visual consistency spec, inventory, naming & workflow."""
from pz_sheet_kit import *
import matplotlib.patches as mp
import pz_inventory as INV
import json

OUT = os.path.join(ROOT, "PDF", "pages")
SRC = os.path.join(ROOT, "Source_Documents")
AR = os.path.join(SRC, "audit_renders")
RD = os.path.join(ROOT, "Stasis_Facility", "renders")
GEN = "—  ·  BIBLE FRONT MATTER"

def cover():
    fig = new_sheet()
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_zorder(0)
    im = Image.open(os.path.join(RD, "int_chamber.png")).convert("RGB")
    ax.imshow(im, extent=(0, 1, 0, 1), aspect="auto", alpha=0.55); ax.axis("off")
    fig.patches.append(mp.Rectangle((0, 0), 0.58, 1, transform=fig.transFigure, color="#0B1220", alpha=0.86, zorder=1))
    fig.patches.append(mp.Rectangle((0.05, 0.62), 0.006, 0.25, transform=fig.transFigure, color=C["orange"], zorder=2))
    fig.text(0.07, 0.84, "PROJECT ZERO", fontsize=40, weight="bold", color=C["white"], zorder=3)
    fig.text(0.07, 0.77, "NEXUS-01 ASSET & ARCHITECTURE", fontsize=24, weight="bold", color=C["cyan"], zorder=3)
    fig.text(0.07, 0.725, "PRODUCTION BIBLE", fontsize=24, weight="bold", color=C["cyan"], zorder=3)
    fig.text(0.07, 0.655, "Year 2187 · the City of Forgotten Machines", fontsize=13, color=C["text"], zorder=3)
    text_block(fig, 0.07, 0.56, [
        ("REV C — FULL BIBLE: ALL ASSET SHEETS", "o"),
        "Reference audit · consistency spec · asset inventory (60 assets)",
        "Robot family: Cypher, Sentinel, Patch + family design language (CHR-00…04)",
        "Stasis Facility architectural package: sheets SF-01 to SF-05 (9 pages)",
        "",
        ("Robot family 12 sheets · Stasis benchmark 9 · buildings, vehicles, equipment, infrastructure, interiors.", "a"),
    ], fs=10.5, lh=0.034)
    text_block(fig, 0.07, 0.25, [
        ("Method", "h"),
        "All technical views are rendered from procedural Blender models built from one",
        "layout file, so every elevation, plan, section and render shows the same object.",
        "Dimensions are design assumptions in Roblox studs, not measurements of concept art.",
    ], fs=9.5, lh=0.026)
    fig.text(0.07, 0.05, "REV C  ·  2026-11-19  ·  STATUS: FOR REVIEW", fontsize=9, color=C["muted"], zorder=3)
    fig.text(0.97, 0.05, "Interior: Stasis Pod Chamber (BLD-01 / INT-01)", fontsize=8, color=C["text"], ha="right", zorder=3)
    save(fig, os.path.join(OUT, "P01_Cover.png"))

def contents():
    fig = new_sheet()
    frame(fig, "00", "CONTENTS", "Full bible · page numbers computed from the assembled PDF", 1, 1, asset=GEN)
    rp = os.path.join(ROOT, "PDF", "page_ranges.json")
    ranges = json.load(open(rp)) if os.path.exists(rp) else []
    y = 0.86
    for k, (name, a, b) in enumerate(ranges):
        fig.patches.append(mp.Rectangle((0.06, y - 0.035), 0.88, 0.046, transform=fig.transFigure, color="#13203A", zorder=1))
        fig.text(0.075, y - 0.012, str(k + 1), fontsize=12, weight="bold", color=C["orange"], va="center", zorder=2)
        fig.text(0.115, y - 0.012, name, fontsize=11, color=C["white"], va="center", zorder=2)
        fig.text(0.9, y - 0.012, f"p. {a}" if a == b else f"pp. {a}–{b}", fontsize=10, color=C["cyan"], ha="right", va="center", zorder=2)
        y -= 0.062
    text_block(fig, 0.075, y - 0.01, [("Roblox construction specs, Meshy/Blender workflow, naming and priorities are inside each sheet (Phase 5 fields)", "m"),
                                       ("and in 4A/4B. Roblox Studio build (Phase 9) has not started.", "m")], fs=8.5, lh=0.022)
    save(fig, os.path.join(OUT, "P02_Contents.png"))

def supplied():
    """03-C: every file of the Nov 2026 supply batch and where it went."""
    fig = new_sheet()
    frame(fig, "03-C", "SUPPLIED ASSETS AUDIT (19 NOV 2026 BATCH)", "Every new file inspected · mapped to an asset ID · issues found", 1, 1, asset=GEN)
    rows = [
        ("6 robot class concept sheets (MED-7, MEDI-X, ORION, ORBIT-7, AURORA, R-TRN-02)", "CHR-05 … CHR-10", "Family-conformant; stud scales conflict → 0.28 m/stud"),
        ("TITAN-R1 vehicle concept sheet", "VEH-04", "Built as blockout from sheet dimensions"),
        ("NX-A17 Raven aircraft concept sheet", "VEH-09 (new)", "Built as blockout (56 × 40 × 16)"),
        ("6 'Nine worlds' collages", "Art direction", "Confirms chapter scenes; used for BLD-02/08/15, VEH-01"),
        ("Design Bible (1).png", "—", "Byte-identical duplicate"),
        ("Futuristic Utility Robot (raw 3.6 M tris) + rigged GLB + zip stages", "CHR-11 UT-01", "Rigged 10 k tris; stray Icosphere"),
        ("Scientific Research Robot rigged GLB + zip stages", "CHR-07 ORION (3D)", "Rigged 10 k tris, 24 bones"),
        ("Cargo Logistics Robot rigged GLB + zip stages", "CHR-10 R-TRN-02 (3D)", "Rigged 10 k tris, 24 bones"),
        ("Industrial Freight Train concept + zip GLBs", "VEH-10 (new)", "Textured 89 MB GLB; needs decimation"),
        ("Armored Security Carrier concept + GLB", "VEH-11 (new)", "5.6 M tris raw; needs remesh to ≤ 8 k"),
        ("Armored VTOL Security Aircraft concept + zip GLBs", "VEH-12 (new)", "Textured 91 MB GLB; needs remesh"),
        ("Industrial Cargo Hauler concept", "VEH-13 (new)", "Concept only; no model yet"),
        ("Weapons & Combat Equipment design sheet (16 items + cells)", "EQP-02/03/06/07 + EQP-13 … 25", "Concept crops + blockouts; 3 Meshy models"),
        ("21 Nov: metropolis concept + 12 building/infra Meshy models", "BLD-02/03/07/09/15-24, INF-11/13-15, INT-08", "Mapped; 4 concept-only districts"),
        ("21 Nov: interiors, police kit, weapons (THUNDER-9, TITAN BREAKER, DOME-4)", "INT-02/03/09-13, EQP-03/14/16/19/20/26/27", "Rendered read-only"),
        ("21 Nov: 33 library models", "16 used (BLD-25-29, INF-16-20, INT-14-16, VEH-14-16)", "11 held: space/Mars/human-type/duplicates"),
    ]
    table(fig, (0.02, 0.3, 0.96, 0.58), ["SUPPLIED FILE(S)", "MAPPED TO", "FINDINGS"], rows, [0.48, 0.18, 0.34], fs=7.3)
    text_block(fig, 0.03, 0.27, [
        ("Rules applied", "o"),
        "• User models are rendered read-only (rest pose, uniform scale); files are never modified. Raw Meshy stages in zips are provenance only.",
        "• Every new robot conforms to the family language (CHR-04). Rule 2 relaxed to 'eyes required, mouth optional'; UT-01 / ORION models are adult-proportion exceptions.",
        "• All heights harmonised at 0.28 m per stud (Roblox convention); sheet-internal stud figures (9 / 9.5 / 19) are inconsistent and are overridden.",
        ("Before Roblox import", "o"),
        "• Remove stray Icosphere objects; remesh raw vehicle models (5.6 M / ~3 M tris) to the VEH budget (≤ 8 k body); keep textures 1024².",
    ], fs=7.6, lh=0.024)
    save(fig, os.path.join(OUT, "P03C_Supplied_Assets.png"))

def audit():
    fig = new_sheet()
    frame(fig, "03-A", "REFERENCE AUDIT", "Every supplied Project Zero source inspected before design · findings carried into this bible", 1, 2, asset=GEN)
    refs = [("NEXUS01_p10_StasisReference.png", "NEXUS-01 Architecture Bible p.10", "PRIMARY REFERENCE — Stasis Facility"),
            ("AssetBible_p02_StasisSheet.png", "Asset Reference Bible p.2", "Prior Stasis sheet: 120×85×32 target"),
            ("NEXUS01_p12_LastSanctuary.png", "NEXUS-01 Architecture Bible p.12", "Last Sanctuary pods (Chapter 4)"),
            ("PROTOTYPE_07_Remeshed_q34.png", "PROTOTYPE_07_Remeshed.glb", "Blender audit render (character)")]
    for i, (f, t, s) in enumerate(refs):
        rect = (0.012 + i * 0.245, 0.56, 0.237, 0.352)
        panel(fig, rect, t, None)
        crop = (330, 100, 870, 900) if "PROTOTYPE" in f else None
        image_axes(fig, rect, os.path.join(AR, f), crop=crop, pad_top=0.045)
        fig.text(rect[0] + 0.008, rect[1] + rect[3] - 0.034, s, fontsize=7.2, color=C["amber"])
    panel(fig, (0.012, 0.05, 0.52, 0.5), "SOURCES INSPECTED", None)
    rows = [("S1", "NEXUS_01_City_Infrastructure_Architecture_Bible.pdf", "19 pp", "World, districts, grid, systems, p.10 ref"),
            ("S1b", "NEXUS_01_… (1).pdf", "—", "Byte-identical duplicate of S1 (MD5)"),
            ("S2", "Project_Zero_Asset_Architecture_Reference_Bible.pdf", "14 pp", "12 sheets, target sizes, naming"),
            ("S3", "Project_Zero_Complete_Bible_With_Visual_References.pdf", "21 pp", "Narrative, cast, chapters, systems"),
            ("S4", "Project Zero Design Bible.png", "1536²", "Palette, gear, buildings, districts"),
            ("S5", "PROTOTYPE_07_Model.glb", "3.05 M tris", "Untextured Meshy source, unrigged"),
            ("S6", "PROTOTYPE_07_Remeshed.glb", "10.2 k tris", "Baked textures; game-ready candidate"),
            ("S7", "PROTOTYPE_08_Model.glb", "3.05 M tris", "Textured variant of the same figure")]
    table(fig, (0.018, 0.06, 0.508, 0.45), ["ID", "FILE", "SIZE", "CONTENT / USE"], rows, [0.06, 0.48, 0.12, 0.34], fs=6.6)
    panel(fig, (0.54, 0.05, 0.448, 0.5), "FINDINGS", None)
    text_block(fig, 0.55, 0.51, [
        ("Established — preserved in this bible", "o"),
        "• Cypher, Sentinel, Patch Meshy models are canonical; not redrawn or replaced.",
        "• Stasis hall language (p.10): cylindrical glass pods on heavy graphite bases,",
        "   orange status strips, cyan cap rings, ribbed barrel vault, octagonal door,",
        "   orange banners with diamond emblem, orange manipulator arms, amber aisle strips.",
        "• 8-stud modular grid; kit list floor 8×8 / wall 8×12 (NEXUS-01 §8).",
        "• Target sizes from Asset Reference Bible kept as starting values.",
        "• Naming PZ_<District>_<Asset>_<Variant> (Asset Reference Bible p.14).",
        "• Server-authoritative state model: Power, Data, Cooling, Transit, Security.",
        ("Gaps & decisions", "o"),
        "• No GLB of any building exists; PROTOTYPE_07/08 is a character (Ch. 4 boss",
        "   ‘Prototype-07’), so facility geometry was built procedurally in Blender.",
        "• Stasis width 85 → 88 studs to snap to the 8-stud grid (documented change).",
        "• Prior Stasis sheet massing was a placeholder grid; replaced by real views.",
        "• Wall height raised 12 → 18 inside the pod hall to fit 14.5-stud pods + crane.",
        ("Open question for review", "a"),
        "• RESOLVED: each player wakes in their own pod as their custom robot;",
        "   Cypher (NPC) wakes first in P01 and guides them; Sentinel trapped in P05.",
    ], fs=7.0, lh=0.0178)
    save(fig, os.path.join(OUT, "P03_Reference_Audit.png"))

def consistency():
    fig = new_sheet()
    frame(fig, "03-B", "VISUAL CONSISTENCY SPECIFICATION", "Art direction & materials — rules every asset sheet must follow", 2, 2, asset=GEN)
    panel(fig, (0.012, 0.6, 0.976, 0.312), "COLOUR PALETTE", "reference swatch sampled from Design Bible PNG → production base / emissive values")
    pal = [("Primary metal", "#A9A9B1", "#8A9099", "brushed steel trim"),
           ("Secondary metal", "#545D6E", "#2B2F36", "graphite body panels"),
           ("Accent orange", "#CB681B", "#E8731A", "hazard, banners, arms"),
           ("Energy blue / cyan", "#2A9FE1", "#22D3EE", "systems, pods, UI"),
           ("Warning red", "#A22625", "#E5383B", "ZERO / lockdown"),
           ("Factory yellow", "#EBAB2E", "#FFB020", "amber civic light"),
           ("Research purple", "#8058B5", "#8B5CF6", "research districts"),
           ("Environment teal", "#29A4AC", "#1FB5A8", "wayfinding")]
    for i, (n, ref, prod, use) in enumerate(pal):
        x = 0.022 + i * 0.121
        fig.patches.append(mp.Rectangle((x, 0.7), 0.05, 0.13, transform=fig.transFigure, fc=ref, ec=C["line"], zorder=2))
        fig.patches.append(mp.Rectangle((x + 0.052, 0.7), 0.05, 0.13, transform=fig.transFigure, fc=prod, ec=C["line"], zorder=2))
        fig.text(x, 0.685, n, fontsize=7.6, weight="bold", color=C["text"], va="top")
        fig.text(x, 0.663, f"ref {ref}", fontsize=6.6, color=C["muted"], va="top", family="DejaVu Sans Mono")
        fig.text(x, 0.645, f"prod {prod}", fontsize=6.6, color=C["muted"], va="top", family="DejaVu Sans Mono")
        fig.text(x, 0.627, use, fontsize=6.6, color=C["muted"], va="top")
    fig.text(0.022, 0.845, "left = reference swatch    right = production value (base metals darkened for contrast; emissives raised for Roblox Neon)",
             fontsize=7, color=C["amber"], style="italic")
    panel(fig, (0.012, 0.05, 0.32, 0.54), "SHAPE LANGUAGE", None)
    text_block(fig, 0.022, 0.55, [
        ("Motifs", "o"), "• Octagon = ZERO-era civic/security portals", "• Ribbed barrel vaults for halls (8-stud rib pitch)",
        "• Cylinders for energy + cryo equipment", "• Heavy chamfered plinths under machinery",
        ("Proportion", "o"), "• Robot-scale doors: 6×10 standard, 12×14 major", "• Ceilings ≥ 17 studs in public interiors",
        "• Every module on the 8-stud grid", ("Wear", "o"), "• Hub & safe districts: clean, warm amber accents",
        "• Contested districts: grime, broken Neon, red alarms",
    ], fs=7.4, lh=0.021)
    panel(fig, (0.34, 0.05, 0.32, 0.54), "MATERIALS (Roblox)", None)
    rows = [("Graphite panel", "Metal", "#2B2F36"), ("Brushed steel", "DiamondPlate / Metal", "#8A9099"),
            ("Aged concrete", "Concrete", "#5A5E63"), ("Floor plate", "Metal", "#3A3F46"),
            ("Grate", "DiamondPlate", "#15181C"), ("Cryo glass", "Glass, T 0.35", "#4FCFE6"),
            ("Energy light", "Neon", "#22D3EE"), ("Civic light", "Neon", "#FFB020"),
            ("Hazard paint", "SmoothPlastic", "#E8731A"), ("Alarm", "Neon", "#E5383B")]
    table(fig, (0.346, 0.06, 0.308, 0.49), ["SURFACE", "MATERIAL", "HEX"], rows, [0.4, 0.37, 0.23], fs=7)
    panel(fig, (0.668, 0.05, 0.32, 0.54), "LIGHTING LANGUAGE & RULES", None)
    text_block(fig, 0.678, 0.55, [
        ("Colour = meaning", "o"), "• Cyan: systems online, interactable tech", "• Amber: safe civic space, guidance strips",
        "• Orange: hazard, industry, the resistance", "• Red: ZERO control, lockdown, danger",
        ("Sheet rules (QA-enforced)", "o"), "• One asset per sheet; views from one model", "• Concept renders labelled separately from",
        "  orthographic technical views", "• Every dimension marked as design assumption", "• Scale bar or robot scale ref. on every view set",
        "• Canonical robots never redrawn",
    ], fs=7.4, lh=0.021)
    save(fig, os.path.join(OUT, "P04_Visual_Consistency.png"))

def inventory():
    cols = ["ID", "ASSET", "ROBLOX NAME", "PRI", "CPLX", "TARGET SIZE (STUDS)", "STATUS"]
    widths = [0.07, 0.2, 0.26, 0.05, 0.05, 0.21, 0.16]
    A = INV.ASSETS; per = 31
    pages = [A[i:i + per * 2] for i in range(0, len(A), per * 2)]
    for pi, chunk in enumerate(pages):
        fig = new_sheet()
        frame(fig, "04-A", "ASSET INVENTORY", f"{len(A)} assets · IDs · Roblox names · priority · complexity · status (sizes are design targets)",
              pi + 1, len(pages), asset=GEN)
        for k, part in enumerate((chunk[:per], chunk[per:])):
            if not part:
                continue
            rows = [(a[0], a[1][:30], INV.roblox_name(a)[:34], a[3], a[4], a[5][:28], INV.status(a)) for a in part]
            x = 0.012 + k * 0.492
            table(fig, (x, 0.07, 0.484, 0.835 * (len(part) + 1) / (per + 1)), cols, rows, widths, fs=5.9)
        fig.text(0.012, 0.052, "Priority: P0 Chapter One + first city milestone · P1 core hub · P2 expansion · P3 later chapters.   "
                 "Complexity: S < 1 day · M 1–3 · L 3–7 · XL > 1 week (blockout → in-game estimate).", fontsize=7, color=C["muted"])
        save(fig, os.path.join(OUT, f"P05_Asset_Inventory{'' if pi == 0 else '_' + str(pi + 1)}.png"))

def naming():
    fig = new_sheet()
    frame(fig, "04-B", "NAMING, DIRECTORIES & PRODUCTION WORKFLOW", "Conventions shared by files, Studio instances and the manifest", 2, 2, asset=GEN)
    panel(fig, (0.012, 0.5, 0.48, 0.412), "NAMING CONVENTION", None)
    text_block(fig, 0.022, 0.87, [
        ("Asset ID", "o"), "<CAT>-<NN>      CAT ∈ BLD · VEH · EQP · INF · INT      e.g. BLD-01",
        ("Studio / mesh name (existing convention, Asset Bible p.14)", "o"),
        "PZ_<District>_<Asset>_<Variant>        e.g. PZ_AWK_StasisFacility_A",
        ("Sub-components", "o"), "<AssetID>-M<NN>  module   ·  <AssetID>-K<NN>  kit piece   ·  e.g. BLD-01-M01 pod",
        ("Image files", "o"), "<AssetID>_<view>[_<state>].png     e.g. BLD-01_elev_front.png, BLD-01-M01_open_hero.png",
        ("Sheets", "o"), "<SheetID>_<Title>_<n>_<Topic>.png     e.g. SF-04_StasisPod_1_Ortho.png",
        ("District codes", "o"), "AWK · HUB · RES · MKT · IND · RSH · SEC · CORE · TRN · UTL · PLR",
    ], fs=7.3, lh=0.02)
    panel(fig, (0.5, 0.5, 0.488, 0.412), "DIRECTORY STRUCTURE", None)
    tree = ["Project_Zero_Production_Bible/", "├ PDF/            bible PDF, pages/, src/ (sheet + PDF build scripts)",
            "├ Source_Documents/  supplied PDFs, PNG, audit_renders/", "├ Stasis_Facility/  renders/ (+ .json camera maps), sheets/",
            "├ Buildings/ BLD-02…   (one folder per asset ID, after approval)", "├ Vehicles/ · Equipment/ · Infrastructure/ · Interiors/",
            "├ Meshy_Prompts/  <AssetID>_meshy.md", "├ Blender/        scripts/ (pz_layout.py, pz_build_stasis.py)",
            "├ Roblox/         <AssetID>_roblox_spec.md, rbxm exports later", "├ QA/             checklist, layout review log",
            "└ manifest.csv    every image → asset ID, view, source, sheet"]
    for i, t in enumerate(tree):
        fig.text(0.51, 0.87 - i * 0.031, t, fontsize=7.2, family="DejaVu Sans Mono", color=C["text"])
    panel(fig, (0.012, 0.05, 0.976, 0.44), "MESHY → BLENDER → ROBLOX WORKFLOW", None)
    steps = [("1  BLOCKOUT", "Studio Parts on 8-stud grid from the sheet’s plan; test with real character rigs and camera."),
             ("2  MESHY", "Only silhouettes & decorative machinery (pod shell, door frame, crane arm). One prompt per module; "
                          "attach the orthographic sheet views as image reference."),
             ("3  BLENDER", "Retopo / decimate to budget, apply transforms, origin at floor centre, 1 BU = 1 stud, "
                            "trim-sheet UVs, bake 1024² max, split moving parts (glass hinge, leaves)."),
             ("4  ROBLOX IMPORT", "FBX/GLB import → MeshPart; CollisionFidelity per SF-05; Anchored; tags for CollectionService; "
                                  "replace blockout parts one module at a time."),
             ("5  SYSTEMS", "Server services own state (Power, Security, Pod wake); clients tween visuals; validate every remote."),
             ("6  PROFILE", "MicroProfiler + Developer Console on desktop and a mid-tier phone; compare with SF-05 budget; simplify.")]
    y = 0.44
    for t, d in steps:
        fig.text(0.024, y, t, fontsize=8.2, weight="bold", color=C["orange"], va="top")
        fig.text(0.16, y, d, fontsize=7.6, color=C["text"], va="top")
        y -= 0.058
    save(fig, os.path.join(OUT, "P06_Naming_Workflow.png"))

def qa(results):
    """results: list of (check, outcome, detail)."""
    fig = new_sheet()
    frame(fig, "QA", "QUALITY ASSURANCE — SAMPLE SECTION", "Checklist results for this review build (automated + visual review)", 1, 1, asset=GEN)
    rows = [(r[0], r[1], r[2]) for r in results]
    table(fig, (0.02, 0.07, 0.96, 0.83), ["CHECK", "RESULT", "DETAIL"], rows, [0.36, 0.1, 0.54], fs=7.2)
    save(fig, os.path.join(OUT, "P16_QA.png"))

if __name__ == "__main__":
    for f in (sys.argv[1:] or ["contents", "audit", "consistency", "inventory", "naming"]):
        globals()[f]()
