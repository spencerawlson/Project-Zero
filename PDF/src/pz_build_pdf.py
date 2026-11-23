"""Assemble the full Production Bible PDF (Rev C) from page/sheet PNGs, write manifest.csv.
Order and contents page numbers are computed from the files that exist."""
import os, sys, csv, glob, json
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

ROOT = r"D:\Project Zero_Roblox\Project_Zero_Production_Bible"
PAGES = os.path.join(ROOT, "PDF", "pages")
SHEETS = os.path.join(ROOT, "Stasis_Facility", "sheets")
CHS = os.path.join(ROOT, "Characters", "sheets")
RENDERS = os.path.join(ROOT, "Stasis_Facility", "renders")
OUT_PDF = os.path.join(ROOT, "PDF", "PROJECT_ZERO_NEXUS-01_Production_Bible_RevC.pdf")
CATDIR = {"BLD": "Buildings", "VEH": "Vehicles", "EQP": "Equipment", "INF": "Infrastructure", "INT": "Interiors"}

def P(name): return os.path.join(PAGES, name)

def asset_pages(prefix, ids):
    out = []
    for aid in ids:
        d = os.path.join(ROOT, CATDIR[prefix], aid)
        fs = sorted(glob.glob(os.path.join(d, f"{aid}_*.png")))
        out += [(f, f"{aid} {os.path.basename(f)[len(aid) + 1:-4].replace('_', ' ')}") for f in fs]
    return out

def build_order():
    sections = []
    sections.append(("Front matter", [(P("P01_Cover.png"), "Cover"), (P("P02_Contents.png"), "Contents")]))
    sections.append(("Art direction & materials", [(P("P03_Reference_Audit.png"), "3A Reference audit"),
                                                   (P("P03C_Supplied_Assets.png"), "3C Supplied assets (Nov batch)"),
                                                   (P("P04_Visual_Consistency.png"), "3B Visual consistency")]))
    sections.append(("Asset inventory & conventions", [(P("P05_Asset_Inventory.png"), "4A Asset inventory"),
                                                       (P("P05_Asset_Inventory_2.png"), "4A Asset inventory (2)"),
                                                       (P("P06_Naming_Workflow.png"), "4B Naming & workflow")]))
    chr_ = [(os.path.join(CHS, f), f[:-4].replace("_", " ")) for f in
            ["CHR-00_Family_Lineup.png", "CHR-01_Cypher.png", "CHR-02_Sentinel.png", "CHR-03_Patch.png",
             "CHR-04_Family_Design_Language.png", "CHR-05_MED7.png", "CHR-06_MEDIX.png", "CHR-07_ORION.png",
             "CHR-08_ORBIT7.png", "CHR-09_AURORA.png", "CHR-10_RTRN02.png", "CHR-11_Utility.png"]]
    sections.append(("Robot family (characters)", chr_))
    sf = [(os.path.join(SHEETS, f), f[:-4].replace("_", " ")) for f in
          ["SF-01_Exterior_1_Render_Roof.png", "SF-01_Exterior_2_Elevations.png", "SF-02_FloorPlan.png",
           "SF-03_Interior_1_Chamber_Lighting.png", "SF-03_Interior_2_Construction_Systems.png",
           "SF-04_StasisPod_1_Ortho.png", "SF-04_StasisPod_2_States.png", "SF-05_Roblox_1_Kit_Collision.png",
           "SF-05_Roblox_2_Implementation.png"]]
    sections.append(("Stasis Facility package (BLD-01)", sf))
    sections.append(("Buildings BLD-02 … BLD-29", asset_pages("BLD", [f"BLD-{n:02d}" for n in range(2, 30)])))
    sections.append(("Vehicles VEH-01 … VEH-16", asset_pages("VEH", [f"VEH-{n:02d}" for n in range(1, 17)])))
    sections.append(("Equipment & weapons EQP-01 … EQP-27", asset_pages("EQP", [f"EQP-{n:02d}" for n in range(1, 28)])))
    sections.append(("Infrastructure INF-01 … INF-20", asset_pages("INF", [f"INF-{n:02d}" for n in range(1, 21)])))
    sections.append(("Interiors & props INT-02 … INT-16", asset_pages("INT", [f"INT-{n:02d}" for n in range(2, 17)])))
    sections.append(("Quality assurance", [(P("P16_QA.png"), "QA checklist")]))
    return sections

def flat(sections):
    out = []
    for _, items in sections:
        out += items
    return out

def page_ranges(sections):
    rng, n = [], 1
    for name, items in sections:
        if items:
            rng.append((name, n, n + len(items) - 1)); n += len(items)
    return rng

def manifest(order):
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "renders", "*.png"), recursive=True)) + \
             sorted(glob.glob(os.path.join(ROOT, "Characters", "models", "*", "*.png"))) + \
             sorted(glob.glob(os.path.join(ROOT, "Characters", "turnarounds", "*.png"))):
        rel = os.path.relpath(f, ROOT); parts = rel.split(os.sep)
        aid = parts[1] if parts[0] in CATDIR.values() else ("BLD-01" if parts[0] == "Stasis_Facility" else "CHR")
        js = f[:-4] + ".json"
        rows.append(dict(asset_id=aid, file=rel, kind="render", view=os.path.basename(f)[:-4],
                         camera_meta=os.path.relpath(js, ROOT) if os.path.exists(js) else "",
                         source="Blender/scripts (procedural or user GLB audit)"))
    for i, (f, title) in enumerate(order):
        rows.append(dict(asset_id=title.split(" ")[0], file=os.path.relpath(f, ROOT), kind="sheet/page", view=title,
                         camera_meta="", source=f"PDF page {i + 1}"))
    for f in sorted(glob.glob(os.path.join(ROOT, "Source_Documents", "**", "*.*"), recursive=True)):
        rows.append(dict(asset_id="reference", file=os.path.relpath(f, ROOT), kind="source", view="", camera_meta="", source="supplied"))
    with open(os.path.join(ROOT, "manifest.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
    print("MANIFEST", len(rows), "rows")

def build_pdf(order):
    W, H = 17 * 72, 11 * 72
    c = canvas.Canvas(OUT_PDF, pagesize=(W, H))
    c.setTitle("PROJECT ZERO — NEXUS-01 ASSET & ARCHITECTURE PRODUCTION BIBLE (Rev C)")
    c.setAuthor("Project Zero art & architecture")
    tmp = os.path.join(ROOT, "PDF", "_jpg"); os.makedirs(tmp, exist_ok=True)
    for i, (f, title) in enumerate(order):
        im = Image.open(f).convert("RGB")
        jp = os.path.join(tmp, f"p{i + 1:03d}.jpg"); im.save(jp, quality=86, optimize=True)
        c.drawImage(ImageReader(jp), 0, 0, W, H)
        key = f"p{i + 1}"; c.bookmarkPage(key); c.addOutlineEntry(f"{i + 1:03d}  {title}", key, level=0)
        c.showPage()
    c.save()
    print("PDF", OUT_PDF, os.path.getsize(OUT_PDF) // 1024, "KB", len(order), "pages")

if __name__ == "__main__":
    secs = build_order()
    order = flat(secs)
    missing = [f for f, _ in order if not os.path.exists(f)]
    if missing:
        print("MISSING", len(missing)); [print("  ", m) for m in missing]
        if "--allow-missing" not in sys.argv:
            sys.exit(1)
        order = [o for o in order if os.path.exists(o[0])]
    json.dump(page_ranges(secs), open(os.path.join(ROOT, "PDF", "page_ranges.json"), "w"), indent=1)
    if "--ranges-only" in sys.argv:
        print("RANGES", page_ranges(secs)); sys.exit(0)
    manifest(order); build_pdf(order)
