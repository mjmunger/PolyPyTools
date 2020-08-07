#!/bin/bash
function help() {
  cat <<EOF
  Creates symlinks in the firmware root direcotry so phones can find their firmware.
  
  Usage: setup-firmware.sh [/path/to/firmware/root/]
  
  Note:
  You need to have all the firmware directories already setup in the firmware root for this to work, or it will throw errors.
  
EOF
}

if [ $# -nq 1 ]; then
  help
  exit 1
fi

if ! [ -d $1 ]; then
  echo "$1 does not exist!"
  help
fi

FIRMWARE_ROOT=$1
ln -s "${FIRMWARE_ROOT}"/3.1.8.0070 "${FIRMWARE_ROOT}"/SPIP301
ln -s "${FIRMWARE_ROOT}"/3.3.5.0247 "${FIRMWARE_ROOT}"/SPIP320
ln -s "${FIRMWARE_ROOT}"/3.3.5.0247 "${FIRMWARE_ROOT}"/SPIP330
ln -s "${FIRMWARE_ROOT}"/4.0.15.1009 "${FIRMWARE_ROOT}"/SPIP321
ln -s "${FIRMWARE_ROOT}"/4.0.15.1009 "${FIRMWARE_ROOT}"/SPIP331
ln -s "${FIRMWARE_ROOT}"/4.0.15.1009 "${FIRMWARE_ROOT}"/SPIP335
ln -s "${FIRMWARE_ROOT}"/3.2.7.0198 "${FIRMWARE_ROOT}"/SPIP430
ln -s "${FIRMWARE_ROOT}"/4.0.15.1009 "${FIRMWARE_ROOT}"/SPIP450
ln -s "${FIRMWARE_ROOT}"/3.1.8.0070 "${FIRMWARE_ROOT}"/SPIP501
ln -s "${FIRMWARE_ROOT}"/4.0.15.1009 "${FIRMWARE_ROOT}"/SPIP550
ln -s "${FIRMWARE_ROOT}"/4.0.15.1009 "${FIRMWARE_ROOT}"/SPIP560
ln -s "${FIRMWARE_ROOT}"/3.1.8.0070 "${FIRMWARE_ROOT}"/SPIP600
ln -s "${FIRMWARE_ROOT}"/3.1.8.0070 "${FIRMWARE_ROOT}"/SPIP601
ln -s "${FIRMWARE_ROOT}"/4.0.15.1009 "${FIRMWARE_ROOT}"/SPIP650
ln -s "${FIRMWARE_ROOT}"/4.0.15.1009 "${FIRMWARE_ROOT}"/SPIP670
ln -s "${FIRMWARE_ROOT}"/3.1.8.0070 "${FIRMWARE_ROOT}"/SPIP4000
ln -s "${FIRMWARE_ROOT}"/4.0.15.1009 "${FIRMWARE_ROOT}"/SPIP5000
ln -s "${FIRMWARE_ROOT}"/4.0.15.1009 "${FIRMWARE_ROOT}"/SPIP6000
ln -s "${FIRMWARE_ROOT}"/4.0.15.1009 "${FIRMWARE_ROOT}"/SPIP7000
