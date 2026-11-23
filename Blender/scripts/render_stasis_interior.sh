#!/bin/sh
# Third pass: interior + lighting states with pod glow lights hidden from camera rays.
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/b8ioq4061.output"
while ! grep -q FIXES_DONE "$LOG"; do sleep 20; done
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
"$B" -b --factory-startup -P "$R/Blender/scripts/pz_build_stasis.py" -- facility "$R/Stasis_Facility/renders" int_chamber light_normal light_wake light_lockdown light_offline 2>&1 | grep --line-buffered -E "RENDERED|Error|Traceback"
echo INTERIOR_DONE
