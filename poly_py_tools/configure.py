#!/usr/bin/env python3
"""
usage: polypy [-v | --verbose] configure set-path asterisk <path>
       polypy [-v | --verbose] configure set-path tftproot <path>
       polypy [-v | --verbose] configure show

"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json

args = docopt(__doc__)

print("configure!")
pprint(args)

config_dir = "/etc/polypy/"
config_path = os.path.join(config_dir,"polypy.conf")
configs = None

if os.getegid() != 0:
    print("You must run this as root. Cannot continue")
    sys.exit(1)

if not os.path.exists(config_dir):
    try:
        os.mkdir(config_dir)
    except Exception:
        print("Could not create %s. Configuration cannot continue." % config_dir)
        sys.exit(1)

if os.path.exists(config_path):
    f = open(config_path,'r')
    configs = f.readlines()
    f.close()
    configs = json.JSONDecoder.decode(configs)

pprint(configs)

