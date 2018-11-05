#!/usr/bin/env python3
"""Parses sip.conf entries to generate the sip-basic.cfg registrations.
It's expecting an entry like the one below where:
* The extension is in the brackets
* The first line after the extension is a COMMENTED mac address for the phone / user.
* The next line is the secret
* The last line is the CID.

EXAMPLE

[111](l3office)
;0004f2f957f9
secret=shoonfa9s3k
callerid="Conference Phone" <111>

NOTE: It's probably best to copy the extensions from sip.conf into a separate file before running thisscript. This way,
      you can ensure the formatting is correct, and there will not be any erroneous files created from ther configs that
      which may match the patterns this script looks for.

Usage: configline.py [options]

OPTION LIST
-a       --all             Process all extensions.
-c       --show-configs    Show the configs for this app
-e EXT   --extension EXT   Process extension NNN only.
-l       --license         Display the license for this software
-d       --debug           Debug mode
-m       --dump            Dump current config
-n       --clean           Clean the config

"""

import os
import sys
import getopt
import configparser

from pprint import pprint
from docopt import docopt
from polypy.config import Config
from polypy.sipconf import Sipconf

# Parses sip.conf entries to generate the sip-basic.cfg registrations.
# It's expecting an entry like the one below where:
# * The extension is in the brackets
# * The first line after the extension is a COMMENTED mac address for the phone / user.
# * The next line is the secret
# * The last line is the CID.
##
# Example
##
# [111](l3office)
# ;0004f2f957f9
# secret=shoonfa9s3k
# callerid="Conference Phone" <111>
###




def showLicense():
    print("""
Process sip.conf into Polycom configs.

Copyright (C) 2015-2018 High Powered Help, Inc. All Rights Reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """)


def check_locations():

    paths = {('/etc/polypy.conf', 'Config not found. Please create {}'),
             ('Config/reg-basic.cfg', 'Polycom Config directory not found ({}). Run this from the provisioning directory'),
             ('000000000000.cfg', 'Default mac cfg file not found ({}), Run this from the provisioning directory')
             }

    for path, msg in paths:
        if not os.path.exists(path):
            print(msg.format(path))
            exit(1)

    # print("Pre-reqs satisfied. Continuing.")

args = docopt(__doc__)

check_locations()

config_path='/etc/polypy.conf'
config = configparser.RawConfigParser()
config.read(config_path)

root = config.get('polycom', 'root')
server = config.get('polycom', 'server')
sip_path = config.get('polycom', 'sip_path')
sip = Sipconf(server, sip_path, root)
sip.parse()
if args["-d"]:
    sip.set_debug()

thisConfig = Config(sip, root)


if args["-l"]:
    showLicense()
    sys.exit()

if args["-a"]:
    thisConfig.clean()
    thisConfig.provision_all()

if args["-e"] is not None:
    print("Provisioning extension {} only".format(args["-e"]))
    thisConfig.provision(args["-e"])

if args["-m"]:
    # Show all discovered sip registrations
    thisConfig.dump()

if args["-n"]:
    thisConfig.clean()