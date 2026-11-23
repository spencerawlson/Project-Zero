#!/bin/sh
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/briwiy1ty.output"
while ! grep -q USER2_DONE "$LOG"; do sleep 20; done
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
S="$R/Blender/scripts/pz_model_audit.py"
"$B" -b --factory-startup -P "$S" -- "$R/Source_Documents/user_models/FreightTrain_textured.glb" "$R/Vehicles/VEH-10/renders" 96 length -X 2>&1 | grep -E "AUDIT_DONE|Error"
"$B" -b --factory-startup -P "$S" -- "$R/Source_Documents/user_models/SecurityVTOL_textured.glb" "$R/Vehicles/VEH-12/renders" 50 length -X 2>&1 | grep -E "AUDIT_DONE|Error"
echo USER3_DONE
