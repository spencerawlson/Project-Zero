#!/bin/sh
# Exploded framing fix (scene refresh after explode) for VEH-01..09 + elevator plan cut heights. Waits for the cut fix.
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/b4qfgnnoh.output"
while ! grep -q CUTFIX_DONE "$LOG"; do sleep 30; done
RA="D:/Project Zero_Roblox/Project_Zero_Production_Bible/Blender/scripts/render_assets.sh"
PZ_SHOTS=exploded sh "$RA" VEH-01 VEH-02 VEH-03 VEH-04 VEH-05 VEH-06 VEH-09
PZ_SHOTS=plan,exploded sh "$RA" VEH-07 VEH-08
echo VEHFIX_DONE
