#!/bin/sh
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/bbcveuw15.output"
while ! grep -q BATCH_DONE "$LOG"; do sleep 20; done
sh "D:/Project Zero_Roblox/Project_Zero_Production_Bible/Blender/scripts/render_assets.sh" EQP-06 EQP-07 EQP-13 EQP-14 EQP-15 EQP-16 EQP-17 EQP-18 EQP-19 EQP-20 EQP-21 EQP-22 EQP-23 EQP-24 EQP-25
