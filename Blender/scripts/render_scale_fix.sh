#!/bin/sh
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/bbcveuw15.output"
while ! grep -q BATCH_DONE "$LOG"; do sleep 20; done
export PZ_SHOTS=scale
sh "D:/Project Zero_Roblox/Project_Zero_Production_Bible/Blender/scripts/render_assets.sh" EQP-01 EQP-02 EQP-03 EQP-04 EQP-05 EQP-06 EQP-07
