#!/usr/bin/env python3
"""
usage: polypy [ -v ... ] [options] sip generate <extension> from <file>

options:
  -v             Be verbose
  -f, --force    Force the setting.

"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json
from poly_py_tools.sip_parser import SipConfParser
from poly_py_tools.pw_strength_calculator import PasswordStrengthCalculator

args = docopt(__doc__)

config_dir = "/etc/polypy/"
config_path = os.path.join(config_dir, "polypy.conf")
configs = None