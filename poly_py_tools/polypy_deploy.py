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

from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.polypy_config_finder import ConfigFinder
from poly_py_tools.dialplan import Dialplan
from poly_py_tools.deploy import Deploy

args = docopt(__doc__)

configs = PolypyConfig()
configs.add_search_path(os.getcwd())
configs.add_search_path("/etc/polypy")
configs.find()
configs.load()

if args['-d']:
    print("Debug: {}".format(__file__))
    print("--------------------------------------------------")
    print(args)
    print("--------------------------------------------------\n")
    print(configs)

if args['generate'] and args['list']:
    dialplan = Dialplan(args['<csvfile>'])
    dialplan.with_config(configs)
    deploy = Deploy(configs, dialplan)
    deploy.build_rsync_lists()
    deploy.write_scripts()
    print("Run push.sh from the tftproot to upload your updated configs")
    sys.exit(0)


