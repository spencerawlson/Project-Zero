#!/bin/sh
# BLD-03 user model: orthos were empty (texture alpha) -> re-render with forced-opaque materials. Waits for the vehicle fix.
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/b02imdxkh.output"
while ! grep -q VEHFIX_DONE "$LOG"; do sleep 30; done
cd "D:/Project Zero_Roblox"
"/c/Program Files/Blender Foundation/Blender 5.3/blender.exe" -b --factory-startup -P "D:/Project Zero_Roblox/Project_Zero_Production_Bible/Blender/scripts/pz_model_audit.py" -- "D:/Project Zero_Roblox/robot_residential_tow.glb" "D:/Project Zero_Roblox/Project_Zero_Production_Bible/Buildings/BLD-03/user_model" 72 height 2>&1 | grep --line-buffered -E "AUDIT_DONE|Error|Traceback"
echo BLD03FIX_DONE
