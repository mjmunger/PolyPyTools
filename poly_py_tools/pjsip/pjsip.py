#!/usr/bin/env python3
"""
usage: polypy pjsip [ -v ... ] [options] generate <extension> from <file> ([assign <template>] | [ use template column <column> ]) [with voicemail]

options:
  -d  --debug    Debug mode
  -f, --force    Force the setting.
  -v             Be verbose

"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json

from poly_py_tools.polypy_config_finder import ConfigFinder
from poly_py_tools.pjsip.pjsip_factory import PJSipFactory

args = docopt(__doc__)
debug_mode = False

if args['-d']:
    debug_mode = True
    print("Debug mode on. Debugging {}".format(__file__))
    print("--------------------------------------------------")
    print(args)
    print("--------------------------------------------------")

config_finder = ConfigFinder()
configs = config_finder.get_configs()
args['config'] = configs

factory = PJSipFactory()
runner = factory.get_runner(args)
runner.run()
