#!/bin/sh
# 21 Nov batch: user Meshy models → read-only turnarounds. Sizes in studs are design assumptions.
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
U="D:/Project Zero_Roblox"
S="$R/Blender/scripts/pz_model_audit.py"
run() { echo "== $2"; "$B" -b --factory-startup -P "$S" -- "$1" "$2" $3 $4 $5 2>&1 | grep --line-buffered -E "AUDIT_DONE|Error|Traceback"; }
run "$U/Meshy_AI_futuristic_police_hq__1121142758_image-to-3d-texture.glb" "$R/Buildings/BLD-07/user_model" 56 length
run "$U/compact_police_statio.glb" "$R/Buildings/BLD-16/renders" 32 length
run "$U/emergency_response_st.glb" "$R/Buildings/BLD-17/renders" 48 length
run "$U/Meshy_AI_robotic_hospital_3d_1121144207_image-to-3d-texture.glb" "$R/Buildings/BLD-09/user_model" 80 length
run "$U/Meshy_AI_futuristic_monorail_s_1121142445_image-to-3d-texture.glb" "$R/Buildings/BLD-15/user_model" 90 length
run "$U/Meshy_AI_futuristic_modular_wa_1121141730_image-to-3d-texture.glb" "$R/Infrastructure/INF-11/user_model" 24 length
run "$U/Meshy_AI_futuristic_enclosed_s_1121142111_image-to-3d-texture.glb" "$R/Infrastructure/INF-15/renders" 32 length
run "$U/Meshy_AI_modular_robot_roadway_1121141158_image-to-3d-texture.glb" "$R/Infrastructure/INF-13/renders" 32 length
run "$U/Meshy_AI_elevated_magnetic_hig_1121141254_image-to-3d-texture.glb" "$R/Infrastructure/INF-14/renders" 64 length
run "$U/Meshy_AI_Control_Desk_1121141055_texture.glb" "$R/Interiors/INT-08/user_model" 8 length
run "$U/Meshy_AI_robot_customization_g_1121145120_image-to-3d-texture.glb" "$R/Buildings/BLD-02/user_model" 100 length
run "$U/robot_residential_tow.glb" "$R/Buildings/BLD-03/user_model" 72 height
echo USER4_DONE
