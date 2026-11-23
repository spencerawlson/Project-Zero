#!/bin/sh
# Usage: render_assets.sh <ID> [<ID> ...]   -> <Category>/<ID>/renders
B="/c/Program Files/Blender Foundation/Blender 5.3/blender.exe"
R="D:/Project Zero_Roblox/Project_Zero_Production_Bible"
for id in "$@"; do
  case "$id" in BLD*) c=Buildings;; VEH*) c=Vehicles;; EQP*) c=Equipment;; INF*) c=Infrastructure;; INT*) c=Interiors;; esac
  echo "== $id $(date +%H:%M)"
  "$B" -b --factory-startup -P "$R/Blender/scripts/pz_build_asset.py" -- "$id" "$R/$c/$id/renders" 2>&1 | grep --line-buffered -E "ASSET_DONE|Error|Traceback|line [0-9]+|Exception"
done
echo BATCH_DONE
