#!/bin/sh
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/bwq3hyv78.output"
while ! grep -q USER_DONE "$LOG"; do sleep 20; done
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
S="$R/Blender/scripts/pz_model_audit.py"
run() { "$B" -b --factory-startup -P "$S" -- "$@" 2>&1 | grep --line-buffered -E "AUDIT_DONE|Error|Traceback"; }
run "D:/Project Zero_Roblox/Meshy_AI_Rigged_Scientific_Research_Robot_20261120_animated_mixamo_All_animation.glb" "$R/Characters/models/Research" 6.7 height
run "D:/Project Zero_Roblox/Meshy_AI_Rigged_Cargo_Logistics_Robot_20261120_animated_mixamo_All_animation.glb" "$R/Characters/models/Cargo" 6.8 height
run "D:/Project Zero_Roblox/Meshy_AI_Rigged_Futuristic_Utility_Robot_20261120_animated_mixamo_All_animation.glb" "$R/Characters/models/Utility" 6.4 height
"$B" -b --factory-startup -P "$S" -- "D:/Project Zero_Roblox/Armored_Security_Carr.glb" "$R/Vehicles/VEH-11/renders" 32 length -X 2>&1 | grep --line-buffered -E "AUDIT_DONE|Error"
echo USER2_DONE
