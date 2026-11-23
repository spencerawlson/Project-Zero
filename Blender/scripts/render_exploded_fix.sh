#!/bin/sh
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/bbcveuw15.output"
while ! grep -q BATCH_DONE "$LOG"; do sleep 20; done
export PZ_SHOTS=exploded
sh "D:/Project Zero_Roblox/Project_Zero_Production_Bible/Blender/scripts/render_assets.sh" VEH-01 VEH-02 VEH-03 VEH-04 VEH-05 VEH-06
