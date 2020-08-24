#!/bin/bash
apt-get install python3-venv
mkdir venv
python3 -m venv venv/
source venv/bin/activate
pip3 install pip --upgrade
pip3 install docopt
