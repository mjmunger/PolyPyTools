#!/bin/bash
echo "Installing PolyPy Tools..."
ln -s `pwd`/check-everyone.py /usr/local/bin/
ln -s `pwd`/check-registered.py /usr/local/bin/
ln -s `pwd`/configline.py /usr/local/bin/
ln -s `pwd`/gendir.py /usr/local/bin/
ln -s `pwd`/makecfg.py /usr/local/bin/
ln -s `pwd`/randomizepw.py /usr/local/bin/
ln -s `pwd`/restart-polycom.sh /usr/local/bin/
echo "Done."