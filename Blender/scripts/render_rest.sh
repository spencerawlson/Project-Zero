#!/bin/sh
# Waits for the building batch, then renders vehicles, equipment, infrastructure, interiors, and re-renders BLD-02..05 (note groups).
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/blye6jtxr.output"
while ! grep -q BATCH_DONE "$LOG"; do sleep 20; done
sh "D:/Project Zero_Roblox/Project_Zero_Production_Bible/Blender/scripts/render_assets.sh" \
  VEH-01 VEH-02 VEH-03 VEH-04 VEH-05 VEH-06 VEH-07 VEH-08 VEH-09 \
  EQP-01 EQP-02 EQP-03 EQP-04 EQP-05 EQP-06 EQP-07 EQP-08 EQP-09 EQP-10 EQP-11 EQP-12 \
  INF-01 INF-02 INF-03 INF-04 INF-05 INF-06 INF-07 INF-08 INF-09 INF-10 INF-11 INF-12 \
  INT-02 INT-03 INT-04 INT-05 INT-06 INT-07 INT-08 INT-09 INT-10 \
  BLD-02 BLD-03 BLD-04 BLD-05
