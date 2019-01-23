#!/usr/bin/env python3
#!/usr/bin/env python3
"""
usage: polypy [options] provision extension <extension>
       polypy [options] provision extension all

options:
  -v, --verbose  Be verbose
  -f, --force    Force the setting.

"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json
from poly_py_tools.sip_parser import SipConfParser

args = docopt(__doc__)

config_dir = "/etc/polypy/"
config_path = os.path.join(config_dir, "polypy.conf")
configs = None

if not os.path.exists(config_path):
    print("PolyPy has not been configured. Run polypy configure")
    sys.exit(1)


f = open(config_path, 'r')
configs = json.load(f)
f.close()
paths = configs['paths']

parser = SipConfParser(os.path.join(paths['asterisk'],'sip.conf'))
parser.parse()