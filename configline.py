#!/usr/bin/python3
import os
import sys
import getopt
import configparser
from pprint import pprint
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

def usage():

    print("""
Usage: configline.py [options]

FUNCTION SUMMARY
Parses sip.conf entries to generate the sip-basic.cfg registrations.
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

OPTION LIST

-a       --all             Process all extensions.
-c       --show-configs    Show the configs for this app
-e[NNN]  --extension NNN   Process extension NNN only.
-s[foo]  --site foo        Set the site name to bar. (This is the directory where the phone will look for configs under document root)
-l       --license         Display the license for this software
    """)


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


options = "mdacse:hls:t:"
long_opts = ['all', 'extension=', 'help', 'server=', 'site=', 'license', 'show-configs', 'debug', 'dump', 'clean']
optlist, args = getopt.getopt(sys.argv[1:], options, long_opts)

check_locations()

config_path='/etc/polypy.conf'
config = configparser.RawConfigParser()
config.read(config_path)

root = config.get('polycom', 'root')
server = config.get('polycom', 'server')
sip_path = config.get('polycom', 'sippath')
sip = Sipconf(server, sip_path, root)

for o, a in optlist:
    if o in ["-s", '--site']:
        site = a
    elif o in ['-c', '--show-configs']:
        print("Current Config Settings:")
        print("Root: {}".format(root))
        print("Server: {}".format(server))
        print("Sippath: {}".format(sip_path))
        sys.exit()
    elif o in ['-d', '--debug']:
        sip.set_debug()

sip.parse()
thisConfig = Config(sip, root)

for o, a in optlist:
    print(o)
    if o in ["-h", '--help']:
        usage()
        sys.exit()
    elif o in ["-l", '--license']:
        showLicense()
        sys.exit()
    elif o in ['-a', '--all']:
        thisConfig.clean()
        thisConfig.provision_all()
    elif o in ['-e', '--extension']:
        print("Provisioning extension {} only".format(a))
        thisConfig.provision(a)

    elif o in ['-m', '--dump']:
        # Show all discovered sip registrations
        thisConfig.dump()

    elif o == '--clean':
        thisConfig.clean()

    else:
        usage()

# for line in fp:
# print("")
# print("REGISTRATION SUMMARY")
# for mac in reg1:
#     r1 = reg1[mac]
#     #r2 = reg2[mac]
#     #print("%s has %s and %s" % (mac, r1, r2))
#     print("%s has %s" % (mac, r1))
# fp.close()
#