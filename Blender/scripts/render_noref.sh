#!/bin/sh
# Re-render shots that contained the faceless scale figure (after the robot batch finishes).
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/bvz1zopk8.output"
while ! grep -q ROBOTS_DONE "$LOG"; do sleep 15; done
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
S="$R/Blender/scripts/pz_build_stasis.py"
run() { "$B" -b --factory-startup -P "$S" -- "$@" 2>&1 | grep --line-buffered -E "RENDERED|Error|Traceback|line [0-9]+"; }
run family "$R/Characters/renders" family_ortho family_hero
run pod "$R/Stasis_Facility/renders" pod_closed_front pod_closed_rear pod_closed_left pod_closed_top pod_closed_hero
run pod "$R/Stasis_Facility/renders" pod_open_hero
run kit "$R/Stasis_Facility/renders" kit_axo
echo NOREF_DONE
