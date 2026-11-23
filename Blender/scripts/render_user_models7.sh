#!/bin/sh
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/bqo5a80x3.output"
while ! grep -q USER6_DONE "$LOG"; do sleep 30; done
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"; S="$R/Blender/scripts/pz_model_audit.py"
cd "D:/Project Zero_Roblox"
"$B" -b --factory-startup -P "$S" -- "$(ls Meshy_AI_Battlemech_*.glb)" "$R/Vehicles/VEH-16/renders" 14 height 2>&1 | grep -E "AUDIT_DONE|Error"
"$B" -b --factory-startup -P "$S" -- "$(ls Meshy_AI_Aegis_Outpost_*.glb)" "$R/Buildings/BLD-29/renders" 56 length 2>&1 | grep -E "AUDIT_DONE|Error"
echo USER7_DONE
