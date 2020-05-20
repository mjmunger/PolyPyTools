#!/usr/bin/env python3
"""
Usage: polypy deploy [ -v ... ] [ options ] push <macaddress>
       polypy deploy [ -v ... ] [ options ] generate list for <csvfile>


  Commands:
      push                         Upload polycom configs for <macaddress> to the production server.
      generate list                Generates a file list for phones in <csvfile>
  Options:
    -d,            Debug mode
    -h, --help     Show this help.
    -v, --verbose  Be verbose
    -f, --force    Force the setting.

"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json
from poly_py_tools.polypy_config_finder import ConfigFinder

args = docopt(__doc__)

config_finder = ConfigFinder()
configs = config_finder.get_configs()

if args['-d']:
    print("Debug: {}".format(__file__))
    print("--------------------------------------------------")
    print(args)
    print("--------------------------------------------------\n")
    print(config_finder)

if args['generate'] and args['list']:



