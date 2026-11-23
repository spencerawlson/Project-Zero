#!/bin/sh
# Hollow BLD-08/13 base volumes + BLD-10 cut above racks: re-render plan + cutaway only. Waits for the EQP fix.
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/bd72b6ebj.output"
while ! grep -q EQPFIX_DONE "$LOG"; do sleep 30; done
export PZ_SHOTS=plan,cutaway
sh "D:/Project Zero_Roblox/Project_Zero_Production_Bible/Blender/scripts/render_assets.sh" BLD-08 BLD-10 BLD-13
echo CUTFIX_DONE
