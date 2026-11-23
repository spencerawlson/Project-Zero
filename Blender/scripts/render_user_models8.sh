#!/bin/sh
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/blmvkzmq0.output"
while ! grep -q USER7_DONE "$LOG"; do sleep 30; done
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"; R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
"$B" -b --factory-startup -P "$R/Blender/scripts/pz_model_audit.py" -- "D:/Project Zero_Roblox/Meshy_AI_modular_robot_roadway_1121141158_image-to-3d-texture.glb" "$R/Infrastructure/INF-13/renders" 32 length 2>&1 | grep -E "AUDIT_DONE|Error"
echo USER8_DONE
