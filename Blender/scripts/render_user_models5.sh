#!/bin/sh
# 21 Nov second batch: clear Project Zero matches. Sizes (studs) are design assumptions.
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
U="D:/Project Zero_Roblox"; M="$R/Source_Documents/user_models"
S="$R/Blender/scripts/pz_model_audit.py"
run() { echo "== $2"; "$B" -b --factory-startup -P "$S" -- "$1" "$2" $3 $4 $5 2>&1 | grep --line-buffered -E "AUDIT_DONE|Error|Traceback"; }
run "$U/Meshy_AI_robotic_shopping_cent_1121150726_image-to-3d-texture.glb" "$R/Buildings/BLD-04/user_model" 100 length
run "$U/Meshy_AI_robotic_command_cente_1121151254_image-to-3d-texture.glb" "$R/Buildings/BLD-07/user_model" 48 length
run "$U/Meshy_AI_robotic_transit_termi_1121160616_image-to-3d-texture.glb" "$R/Buildings/BLD-15/user_model" 90 length
run "$U/Meshy_AI_robot_manufacturing_h_1121161921_image-to-3d-texture.glb" "$R/Buildings/BLD-14/user_model" 128 length
run "$M/Arena_textured.glb" "$R/Buildings/BLD-20/renders" 80 length
run "$U/Meshy_AI_robot_parts_store_int_1121163215_image-to-3d-texture.glb" "$R/Interiors/INT-09/user_model" 24 length
run "$U/Meshy_AI_robot_communal_lounge_1121164036_image-to-3d-texture.glb" "$R/Interiors/INT-13/renders" 32 length
run "$U/Meshy_AI_robot_private_apartme_1121164103_image-to-3d-texture.glb" "$R/Interiors/INT-02/user_model" 24 length
run "$M/GarageInterior_textured.glb" "$R/Interiors/INT-03/user_model" 32 length
run "$M/HospitalRepairHall_textured.glb" "$R/Interiors/INT-11/renders" 48 length
run "$M/ContainmentChamber_textured.glb" "$R/Interiors/INT-12/renders" 32 length
run "$U/Meshy_AI_robotic_police_stun_b_1121164125_image-to-3d-texture.glb" "$R/Equipment/EQP-26/renders" 3 length
run "$M/EnergyBlaster_textured.glb" "$R/Equipment/EQP-27/renders" 3 length
run "$M/RiotShield_textured.glb" "$R/Equipment/EQP-19/user_model" 4.5 height
run "$M/SecurityPulseRifle_textured.glb" "$R/Equipment/EQP-03/user_model" 4.6 length
run "$U/Meshy_AI_thunder_9_heavy_ion_c_1121183112_image-to-3d-texture.glb" "$R/Equipment/EQP-14/user_model" 5.8 length
run "$U/Meshy_AI_titan_breaker_heavy_h_1121183258_image-to-3d-texture.glb" "$R/Equipment/EQP-16/user_model" 5.6 length
run "$U/Meshy_AI_dome_4_shield_project_1121184102_image-to-3d-texture.glb" "$R/Equipment/EQP-20/user_model" 2.5 length
echo USER5_DONE
