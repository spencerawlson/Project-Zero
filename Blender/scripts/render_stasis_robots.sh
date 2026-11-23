#!/bin/sh
# Pass with canonical robots as pod occupants + family lineup.
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
S="$R/Blender/scripts/pz_build_stasis.py"
O="$R/Stasis_Facility/renders"
F="$R/Characters/renders"
run() { "$B" -b --factory-startup -P "$S" -- "$@" 2>&1 | grep --line-buffered -E "RENDERED|Error|Traceback|line [0-9]+"; }
run family "$F" family_ortho family_hero
run pod "$O" pod_closed_front pod_closed_rear pod_closed_left pod_closed_right pod_closed_top pod_closed_section pod_closed_plancut pod_closed_hero
run pod "$O" pod_open_plancut pod_open_hero
run facility "$O" section_chamber int_chamber light_normal light_wake light_lockdown light_offline
run cutaway "$O" cutaway_axo
echo ROBOTS_DONE
