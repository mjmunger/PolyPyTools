#!/bin/bash
if [ $(whoami) != "root" ]; then
  echo "$0 should be run as root! You're not root. Magic 8 ball says: RTFM."
  usage
fi
source files.list

BINPATH=/usr/local/bin
FILECOUNT=${#INSTALL[@]}
INSTALLDIR=`pwd`

for (( i=0; i<${FILECOUNT}; i++ ))
do
    SOURCEFILE=${INSTALL[${i}]}
    SOURCEPATH=${INSTALLDIR}/${SOURCEFILE}
    DESTFILE=${INSTALLAS[${i}]}
    DESTPATH=${BINPATH}/${DESTFILE}

    echo "Installing ${SOURCEPATH} -> ${DESTPATH}..."
    [ -f ${DESTPATH} ] || ln -s ${SOURCEPATH} ${DESTPATH}
    chmod +x ${DESTPATH}
done

echo "Install complete."