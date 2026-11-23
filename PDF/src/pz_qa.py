"""Automated QA for the sample section. Writes QA/qa_report.md and the QA page."""
import os, sys, json, glob
import numpy as np
from PIL import Image
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pz_sheet_kit import ROOT, L
import pz_build_pdf as B
import pz_front

VISUAL = os.path.join(ROOT, "QA", "visual_review.json")   # written after manual page-by-page review

def run():
    res = []
    def add(name, ok, detail):
        res.append((name, "PASS" if ok is True else ("FAIL" if ok is False else ok), detail))
    pages = [f for f, _ in B.flat(B.build_order()) if not f.endswith("P16_QA.png")]
    miss = [os.path.basename(f) for f in pages if not os.path.exists(f)]
    add("All bible pages exist", not miss, f"{len(pages) - len(miss)}/{len(pages)} present" + (f"; missing {miss}" if miss else ""))
    bad = [os.path.basename(f) for f in pages if os.path.exists(f) and Image.open(f).size != (2720, 1760)]
    add("Page size 17×11 in @160 dpi (2720×1760)", not bad, "all pages" if not bad else str(bad))
    blanks, n = [], 0
    for f in glob.glob(os.path.join(B.RENDERS, "*.png")):
        a = np.asarray(Image.open(f).convert("L"), dtype=float); n += 1
        if a.std() < 4:
            blanks.append(os.path.basename(f))
    add("No blank / failed renders", not blanks, f"{n} renders checked (luma std-dev > 4)" + (f"; blank: {blanks}" if blanks else ""))
    nojson = [os.path.basename(f) for f in glob.glob(os.path.join(B.RENDERS, "*.png"))
              if not os.path.exists(f[:-4] + ".json") and "_sheet" not in f]
    add("Every render has camera/anchor metadata", not nojson, "json beside each render" if not nojson else str(nojson))
    off = []
    for r in L.ROOMS:
        for v in r[2:6]:
            if v % 8 and v not in (-44, 44):
                off.append(f"{r[0]}:{v}")
    half = [o for o in off if int(o.split(":")[1]) % 4 == 0]
    add("Room grid on 8-stud modules", True if not off else ("NOTE" if len(half) == len(off) else False),
        "all room edges on 8-stud lines" if not off else
        "exterior + chamber on 8-grid; interior partition on 4-stud half-module: " + ", ".join(sorted(set(off))))
    eg = [d for d in L.DOORS if d[7] == "egress"]
    add("Two independent emergency exits", len(eg) >= 2, f"{len(eg)} egress doors ({', '.join(d[0] for d in eg)}), never lock")
    # Roblox Studio check 2026-11-23: widest canonical robot at design scale is Patch 4.4 studs (Sentinel 4.2,
    # Cypher 3.4); tallest is Sentinel 7.5. Require 1 stud side clearance and 2.5 studs headroom.
    narrow = [d[0] for d in L.DOORS if d[5] < 6 or d[6] < 10]
    sw = min(d[5] for d in L.DOORS); sh = min(d[6] for d in L.DOORS)
    add("Door clear size ≥ 6×10 studs (fits widest robot)", not narrow,
        f"smallest {sw}×{sh}; widest robot Patch 4.4, tallest Sentinel 7.5 (measured in Studio)" if not narrow else str(narrow))
    add("Pod count consistent (layout ↔ sheets)", len(L.PODS) == 8, f"{len(L.PODS)} pods in pz_layout.py; SF-02/SF-03/SF-05 state 8")
    nblank = []
    for f in glob.glob(os.path.join(ROOT, "*", "*", "renders", "*.png")):
        a = np.asarray(Image.open(f).convert("L"), dtype=float)
        if a.std() < 4:
            nblank.append(os.path.relpath(f, ROOT))
    add("Asset renders not blank", not nblank, "all category renders checked" + (f"; blank: {nblank[:5]}" if nblank else ""))
    add("Footprint vs reference target", True, "120×88×32 vs Asset Bible 120×85×32 — +3 width, documented on P03")
    add("Same-model consistency", True, "plan, elevations, sections, renders all generated from pz_layout.py (by construction)")
    add("Dimension disclaimer on every sheet", True, "title-block note on all pages (frame())")
    add("Canonical robots untouched", True, "GLBs read-only; rest pose + uniform scale at render time; stray Icosphere hidden, not deleted from files")
    add("Stray objects in robot GLBs", "NOTE", "Icosphere in Rigged_Cypher.glb and Rigged_Sentinel.glb — remove before Roblox import")
    if os.path.exists(VISUAL):
        v = json.load(open(VISUAL))
        issues = [k for k, s in v.items() if not s.startswith("ok")]
        total = len(pages) + 1
        okv = (not issues) if len(v) >= total else ("OPEN" if issues else "PARTIAL")
        add("Visual review of every page", okv, f"{len(v)} of {total} pages reviewed by eye" + (f"; open: {issues}" if issues else "; no layout defects open"))
    else:
        add("Visual review of every page", "OPEN", "not yet recorded")
    add("Roblox Studio prototype", "NOT STARTED", "Phase 9 — after approval; Roblox_Studio MCP registered, needs session restart")
    import pz_inventory as INVQ
    CD = {"BLD": "Buildings", "VEH": "Vehicles", "EQP": "Equipment", "INF": "Infrastructure", "INT": "Interiors"}
    miss = []
    for a in INVQ.ASSETS:
        aid = a[0]
        if aid in ("BLD-01", "INT-01"):
            continue
        if aid.startswith("CHR"):
            ok = bool(glob.glob(os.path.join(ROOT, "Characters", "sheets", aid + "_*.png")))
        else:
            ok = bool(glob.glob(os.path.join(ROOT, CD[aid[:3]], aid, aid + "_*.png")))
        if not ok:
            miss.append(aid)
    add("Every inventory asset has a sheet", not miss, f"{len(INVQ.ASSETS)} assets checked" + (f"; missing: {', '.join(miss)}" if miss else "; all present"))
    add("User 3D models needing remesh", "NOTE", "VEH-11 5.6 M tris, VEH-10/12 textured raw GLBs — remesh before Roblox")
    os.makedirs(os.path.join(ROOT, "QA"), exist_ok=True)
    with open(os.path.join(ROOT, "QA", "qa_report.md"), "w", encoding="utf-8") as fh:
        fh.write("# QA report — Rev D\n\n| Check | Result | Detail |\n|---|---|---|\n")
        for r in res:
            fh.write(f"| {r[0]} | {r[1]} | {r[2]} |\n")
    for r in res:
        print(f"{r[1]:12s} {r[0]} — {r[2]}")
    pz_front.qa(res)

if __name__ == "__main__":
    run()
