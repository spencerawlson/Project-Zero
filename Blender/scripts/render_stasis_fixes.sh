#!/bin/sh
# Second pass: pod heroes (tighter framing), right view without human, plan cuts, new kit layout.
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/bf0gt5jwd.output"
while ! grep -q ALL_DONE "$LOG"; do sleep 20; done
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
S="$R/Blender/scripts/pz_build_stasis.py"
O="$R/Stasis_Facility/renders"
run() { "$B" -b --factory-startup -P "$S" -- "$@" 2>&1 | grep --line-buffered -E "RENDERED|Error|Traceback|line [0-9]+"; }
run pod "$O" pod_closed_right pod_closed_plancut pod_closed_hero
run pod "$O" pod_open_plancut pod_open_hero
run kit "$O" kit_axo
echo FIXES_DONE
