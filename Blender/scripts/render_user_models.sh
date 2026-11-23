#!/bin/sh
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
S="$R/Blender/scripts/pz_model_audit.py"
run() { "$B" -b --factory-startup -P "$S" -- "$@" 2>&1 | grep --line-buffered -E "AUDIT_DONE|Error|Traceback|line [0-9]+"; }
run "D:/Project Zero_Roblox/Meshy_AI_Rigged_Scientific_Research_Robot_20261120_animated_mixamo_All_animation.glb" "$R/Characters/models/Research" 6.7 height
run "D:/Project Zero_Roblox/Meshy_AI_Rigged_Cargo_Logistics_Robot_20261120_animated_mixamo_All_animation.glb" "$R/Characters/models/Cargo" 6.8 height
run "D:/Project Zero_Roblox/Meshy_AI_Rigged_Futuristic_Utility_Robot_20261120_animated_mixamo_All_animation.glb" "$R/Characters/models/Utility" 6.4 height
run "D:/Project Zero_Roblox/Armored_Security_Carr.glb" "$R/Vehicles/VEH-11/renders" 32 length
run "$R/Source_Documents/user_models/SecurityVTOL_textured.glb" "$R/Vehicles/VEH-12/renders" 50 length
run "$R/Source_Documents/user_models/FreightTrain_textured.glb" "$R/Vehicles/VEH-10/renders" 96 length
echo USER_DONE
