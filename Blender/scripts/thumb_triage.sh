#!/bin/sh
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
O="D:/Project Zero_Roblox/Project_Zero_Production_Bible/Source_Documents/triage"; mkdir -p "$O"
cd "/d/Project Zero_Roblox"
for f in Meshy_AI_Starship_Command_Cons_*.glb Meshy_AI_A_sleek_starship_cap_*.glb Meshy_AI_Aegis_Refinery_Comple_*.glb Meshy_AI_Command_Center_Chair_*.glb Meshy_AI_Alien_Ship_Officer_*.glb Meshy_AI_Nebula_Command_Consol_*.glb Meshy_AI_Drone_Hive_*.glb Meshy_AI_Quantum_Ring_Engine_*.glb Meshy_AI_Sci_Fi_Command_Base_*.glb Meshy_AI_Sci_Fi_Energy_Core_Sp_*.glb Meshy_AI_Quantum_Gateway_*.glb Meshy_AI_Steel_Citadel_*.glb Meshy_AI_Aegis_Orbital_Station_*.glb Meshy_AI_Aegis_Reactor_Bastion_*.glb Meshy_AI_vehicle_tracked_haule_*.glb Meshy_AI_Outpost_Emberfall_*.glb Meshy_AI_Three_Armored_Sentinels_*animation.glb Meshy_AI_internal_mother_ship__*.glb Meshy_AI_Jet2_*.glb Meshy_AI_A_standalone_sci_fi_m_*.glb Meshy_AI_Orbital_Research_Outp_*.glb Meshy_AI_Desert_Sentinel_8x8_*.glb Meshy_AI_mars_habitat_hybrid_*.glb Meshy_AI_Mars_Vanguard_Rover_*.glb Meshy_AI_Quantum_Core_Nova_7_*.glb Meshy_AI__1121180752_texture.glb Meshy_AI__1121180856_texture.glb Meshy_AI_Thunderfang_X_804_*.glb Meshy_AI_Aegis_Outpost_*.glb Meshy_AI_Battlemech_*.glb Meshy_AI_DROE_Titan_Rover_*.glb; do
  n=$(echo "$f" | sed 's/Meshy_AI_//; s/_112118[0-9]*_texture.glb//; s/_112117[0-9]*_texture.glb//; s/_[0-9]*_image-to-3d-texture.glb//; s/\.glb//')
  "$B" -b --factory-startup -P "D:/Project Zero_Roblox/Project_Zero_Production_Bible/Blender/scripts/pz_thumb.py" -- "$f" "$O/$n.png" 2>&1 | grep -E "THUMB_DONE|Error"
done
echo TRIAGE_DONE
