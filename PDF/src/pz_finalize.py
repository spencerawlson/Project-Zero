"""Recompose every sheet and assemble the full bible PDF.  python pz_finalize.py"""
import os, sys, subprocess
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pz_sheets_asset as SA, pz_sheets_chr as CH, pz_sheets_sf as SF, pz_sheets_pod as POD, pz_stasis_sheets as ST, pz_front as FR
from pz_asset_specs import NEW_ROBOTS

ids = ([f"BLD-{n:02d}" for n in range(2, 30)] + [f"VEH-{n:02d}" for n in range(1, 18)] +
       [f"EQP-{n:02d}" for n in range(1, 28)] + [f"INF-{n:02d}" for n in range(1, 21)] + [f"INT-{n:02d}" for n in range(2, 17)])
fails = []
for a in ids:
    try:
        SA.compose(a)
    except Exception as e:
        fails.append((a, repr(e)[:120]))
CH.chr00(); CH.chr04()
for k, n in enumerate(CH.ORDER):
    CH.bot_sheet(n, k + 1)
CH.bot_sheet("Utility", 1, 1)
for k, e in enumerate(NEW_ROBOTS):
    CH.concept_sheet(e, k + 1, len(NEW_ROBOTS))
for f in (SF.sf01a, SF.sf01b, SF.sf03a, SF.sf03b, SF.sf05a, SF.sf05b, POD.sf04a, POD.sf04b, ST.sf02):
    f()
FR.cover(); FR.audit(); FR.supplied(); FR.consistency(); FR.inventory(); FR.naming()
open(os.path.join(SA.ROOT, "PDF", "pages", "P16_QA.png"), "a").close() if False else None
here = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, PYTHONIOENCODING="utf-8")
subprocess.run([sys.executable, os.path.join(here, "pz_build_pdf.py"), "--ranges-only", "--allow-missing"], env=env)
FR.contents()
subprocess.run([sys.executable, os.path.join(here, "pz_qa.py")], env=env)
subprocess.run([sys.executable, os.path.join(here, "pz_build_pdf.py")] + sys.argv[1:], env=env)
print("COMPOSE_FAILS", fails)
