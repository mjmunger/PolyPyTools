#!/usr/bin/env python3
"""
Usage: polypy configure [ -v ... ] [ options ] set-path <name> <path>
       polypy configure [ -v ... ] [ options ] set-server <server_addr>
       polypy configure [ -v ... ] [ options ] show
       polypy configure [ -v ... ] [ options ] set-defaults [here]
       polypy configure [ -v ... ] [ options ] validate
       polypy configure [ -v ... ] [ options ] copy-files <source_path>

  Commands:
      set-path <name> <path>       Set a path in the config file. Possible values: asterisk, tftproot
      set-server <server_addr>     Set the SIP server address.
      show                         Show the current configuration.
      set-defaults [here]          Create a set of default configs and save them at the config path.
      validate                     Validate the configuration.
      copy-files <source_path>     Copies required Polycom files from <source_path> to the tftproot defined in your config.
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
from poly_py_tools.polypy_config import PolypyConfig

args = docopt(__doc__)

config = PolypyConfig()
config.add_search_path(os.getcwd())
config.add_search_path("/etc/polypy")

if not config.find():
    print("Could not find polypy.conf. Perhaps you need to run set-defaults?")
    print("PolyPyTools has not been configured. Run polypy configure!")
    raise SystemExit

config.load()

if args['-d']:
    print("Debug: {}".format(__file__))
    print("--------------------------------------------------")
    print(args)
    print("--------------------------------------------------\n")
    print(config)

if args['set-defaults']:
    config_path = os.path.join(os.getcwd(),'polypy.conf')
    config.write_default_config(config_path)
    print("Defaults written to: {}".format(config_path))

if args['show']:
    pprint(config.config)
    raise SystemExit

if args['set-path']:
    path_name = args['<name>']
    path_path = args['<path>']
    config.set_path(path_name, path_path)
    print("Don't forget to validate this path before you use it. (polypy configure validate) ")
    raise SystemExit

if args['set-server']:
    server_addr = args['<server_addr>']
    config.set_server(server_addr)

if config.config['paths'] is None:
    print("No paths have been configured. Run polypy configure set-path to resolve.")
    raise SystemExit

if args['validate']:
    config.validate()

if args['copy-files']:
    config.copy_files(args['<source_path>'])
