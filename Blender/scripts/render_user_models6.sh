#!/bin/sh
# 21 Nov library models that fit Project Zero → new IDs. Waits for batch 5. Sizes (studs) are design assumptions.
LOG="C:/Users/spenc/AppData/Local/Temp/claude/61d04c85e440f3a3/9f88cfaa-bf1d-4ea6-bfcd-21e7252f56c4/tasks/bq0h0utht.output"
while ! grep -q USER5_DONE "$LOG"; do sleep 30; done
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"; U="D:/Project Zero_Roblox"
S="$R/Blender/scripts/pz_model_audit.py"
run() { echo "== $2"; f=$(ls $1 | head -1); "$B" -b --factory-startup -P "$S" -- "$f" "$2" $3 $4 $5 2>&1 | grep --line-buffered -E "AUDIT_DONE|Error|Traceback"; }
cd "$U"
run "Meshy_AI_Starship_Command_Cons_*.glb" "$R/Interiors/INT-14/renders" 6 length
run "Meshy_AI_Command_Center_Chair_*.glb" "$R/Interiors/INT-15/renders" 4 height
run "Meshy_AI_Nebula_Command_Consol_*.glb" "$R/Interiors/INT-16/renders" 7 height
run "Meshy_AI_Quantum_Core_Nova_7_*.glb" "$R/Interiors/INT-10/user_model" 14 height
run "Meshy_AI_Drone_Hive_*.glb" "$R/Infrastructure/INF-16/renders" 24 length
run "Meshy_AI_Quantum_Gateway_*.glb" "$R/Infrastructure/INF-17/renders" 24 length
run "Meshy_AI_A_standalone_sci_fi_m_*.glb" "$R/Infrastructure/INF-18/renders" 16 height
run "Meshy_AI_Sci_Fi_Energy_Core_Sp_*.glb" "$R/Infrastructure/INF-19/renders" 32 length
run "Meshy_AI_Quantum_Ring_Engine_*.glb" "$R/Infrastructure/INF-20/renders" 24 length
run "Meshy_AI_Aegis_Refinery_Comple_*.glb" "$R/Buildings/BLD-25/renders" 64 length
run "Meshy_AI_Aegis_Reactor_Bastion_*.glb" "$R/Buildings/BLD-26/renders" 40 height
run "Meshy_AI_Orbital_Research_Outp_*.glb" "$R/Buildings/BLD-06/user_model" 90 length
run "Meshy_AI_Sci_Fi_Command_Base_*.glb" "$R/Buildings/BLD-27/renders" 80 length
run "Meshy_AI_Steel_Citadel_*.glb" "$R/Buildings/BLD-28/renders" 96 length
run "Meshy_AI_vehicle_tracked_haule_*.glb" "$R/Vehicles/VEH-14/renders" 28 length
run "Meshy_AI_Desert_Sentinel_8x8_*.glb" "$R/Vehicles/VEH-15/renders" 30 length
echo USER6_DONE
