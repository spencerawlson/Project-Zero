#!/bin/sh
# Renders every Stasis Facility view used by sheets SF-01..SF-05.
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
S="$R/Blender/scripts/pz_build_stasis.py"
O="$R/Stasis_Facility/renders"
run() { "$B" -b --factory-startup -P "$S" -- "$@" 2>&1 | grep -E "RENDERED|Error|Traceback|line [0-9]+"; }
run facility "$O" elev_front elev_rear elev_left elev_right roof_plan section_chamber
run pod "$O" pod_closed_front pod_closed_rear pod_closed_left pod_closed_right pod_closed_top pod_closed_section pod_closed_hero
run pod "$O" pod_open_front pod_open_left pod_open_top pod_open_hero
run kit "$O" kit_axo
run cutaway "$O" plan_cut cutaway_axo
run facility "$O" ext_hero int_chamber light_normal light_wake light_lockdown light_offline
echo ALL_DONE
