#!/bin/sh
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
S="D:/Project Zero_Roblox/Project_Zero_Production_Bible/Blender/scripts/pz_build_asset.py"
for id in "$@"; do "$B" -b --factory-startup -P "$S" -- "$id" "C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/scratchpad/dry" dry 2>&1 | grep -E "DRY_OK|Error|Traceback|line [0-9]+|Exception" | tail -4; done
echo DRY_DONE
