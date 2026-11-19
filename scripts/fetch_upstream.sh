#!/usr/bin/env bash
# Downloads Warioo's "Carvera Air ATC Mod" files from Instructables.
# License: CC BY-NC-ND 4.0 (https://creativecommons.org/licenses/by-nc-nd/4.0)
#   -> personal use / reference only. Do NOT redistribute modified versions or sell.
#   -> These files are gitignored on purpose. Our commercial kit must be an original design.
set -euo pipefail
DEST="$(cd "$(dirname "$0")/.." && pwd)/third_party/warioo-atc"
mkdir -p "$DEST/step" "$DEST/images"
B=https://content.instructables.com
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
dl() { curl -fsSL -A "$UA" -e "https://www.instructables.com/" -o "$DEST/$1" "$B/$2"; echo "  $1"; }
echo "STEP + config -> $DEST"
dl step/TopGear_v2_3DPrint.step        FMD/IDRS/MVRCOR73/FMDIDRSMVRCOR73.step
dl step/TopGear_v2_milled_keyway.step  FOZ/1LZK/MVRCOR74/FOZ1LZKMVRCOR74.step
dl step/TopGear_v1.step                FM2/RS71/MLVCVA5U/FM2RS71MLVCVA5U.step
dl step/BottomGear.step                FHZ/0QTK/MLVCVA4L/FHZ0QTKMLVCVA4L.step
dl step/MotorMount.step                FOB/8LWE/MLVCVA59/FOB8LWEMLVCVA59.step
dl step/ATCSensorMount.step            FKV/XBD7/MLVCVA4E/FKVXBD7MLVCVA4E.step
dl step/SensorMount_GTRIC_M5.step      FZD/1ZJH/MM9SZ2E5/FZD1ZJHMM9SZ2E5.step
dl step/SMW_atcMagazine_v3.step        FB2/3ERC/MMF87EL9/FB23ERCMMF87EL9.step
dl step/Cover.step                     FEK/RJOO/MLVCVA4S/FEKRJOOMLVCVA4S.step
dl step/Frontplate.step                FEC/U5Q2/MLVCVA50/FECU5Q2MLVCVA50.step
dl custom_tool_slots.txt               FYE/4YBH/MLVCVMVO/FYE4YBHMLVCVMVO.txt
echo "Reference photos"
i=0
for p in FGY/U63U/MLSKBG1M/FGYU63UMLSKBG1M.jpg FDA/HCMG/MLVCVA74/FDAHCMGMLVCVA74.jpg F69/GT73/MLVCVA7H/F69GT73MLVCVA7H.jpg \
         FN1/33ZH/MLVCVA7V/FN133ZHMLVCVA7V.jpg F5J/3RWY/MLVCVA8A/F5J3RWYMLVCVA8A.jpg FSB/XYEE/MVRCOR9T/FSBXYEEMVRCOR9T.jpg \
         FQA/VGEG/MLVCVDC7/FQAVGEGMLVCVDC7.jpg FCL/W85S/MM9SZ20M/FCLW85SMM9SZ20M.jpg FDD/8A5W/MLVCVFAF/FDD8A5WMLVCVFAF.jpg \
         FUO/ADPY/MLVCVF6Y/FUOADPYMLVCVF6Y.jpg F0P/FXGK/MM9SZ2EW/F0PFXGKMM9SZ2EW.jpg FG6/2BR4/MMF87F9I/FG62BR4MMF87F9I.jpg \
         FL0/2MH9/MMF87ESO/FL02MH9MMF87ESO.png FML/MZBH/MM9SZ2M4/FMLMZBHMM9SZ2M4.jpg FR3/YCGD/MLVCVK1S/FR3YCGDMLVCVK1S.jpg \
         FI5/YJXO/MLVCVKCB/FI5YJXOMLVCVKCB.jpg F9C/EOTU/MMZAN6PE/F9CEOTUMMZAN6PE.jpg FA2/ERVC/MLVCVNYD/FA2ERVCMLVCVNYD.jpg; do
  i=$((i+1)); ext="${p##*.}"; dl "images/$(printf %02d $i)_$(basename "$p" .$ext).$ext" "$p"
done
echo "Done. Open the .step files directly in OrcaSlicer (File > Import) or run scripts/step_to_stl.py"
