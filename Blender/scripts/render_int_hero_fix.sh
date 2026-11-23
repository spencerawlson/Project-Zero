#!/bin/sh
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/bf39wfis8.output"
while ! grep -q USER8_DONE "$LOG"; do sleep 30; done
export PZ_SHOTS=hero
sh "D:/Project Zero_Roblox/Project_Zero_Production_Bible/Blender/scripts/render_assets.sh" INT-02 INT-03 INT-04 INT-05 INT-06 INT-07 INT-08 INT-10
echo INTFIX_DONE
