#!/usr/bin/env python3
"""
Usage: polypy dialplan [ -v ... ] [ options ] dictionary add <word> for <column>
       polypy dialplan [ -v ... ] [ options ] dictionary del <word> for <column>
       polypy dialplan [ -v ... ] [ options ] dictionary show

  Commands:
      dictionary                   Manage the guessing dictionary. Add or del (remove) words. Or show everything.

  Options:
    -d,            Debug mode
    -h, --help     Show this help.
    -v, --verbose  Be verbose
    -f, --force    Force the setting.

"""

from docopt import docopt
from poly_py_tools.configure.config_finder import ConfigFinder

args = docopt(__doc__)

config_finder = ConfigFinder()
configs = config_finder.get_configs()

if args['-d']:
    print("Debug: {}".format(__file__))
    print("--------------------------------------------------")
    print(args)
    print("--------------------------------------------------\n")
    print(config_finder)

if args['dialplan'] and args['dictionary']:
    pass

if args['generate'] and args['list']:
    pass