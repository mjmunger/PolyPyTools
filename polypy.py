#!/usr/bin/env python3
"""PolyPy Command Line Provisioning Tool!
 
Usage: polypy.py [ -v ... ] [ options ] <command> [ <args> ... ]
 
Options:
  -d           Debug mode
  -h           Show this help screen
  -v           Be verbose. Levels 1-10 (or more).
  -f, --force  Do it anyway.
 
Commands:

  configure  Configure PolyPyTools.
  provision  Creates provisioning files for Polycom phones from asterisk's sip.conf.
  sip        Manage sip.conf
  site       Manage site files
  version    Show the version of this package
  deploy     Deploy files rendered to tftproot
 
See polypy help <command> for more information with a specific command.
 
"""
import os
from docopt import docopt

from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.versionator import Versionator
from poly_py_tools.polypy import Polypy


if __name__ == '__main__':

    args = docopt(__doc__, options_first=True)

    config = PolypyConfig()
    config.add_search_path(os.getcwd())
    config.add_search_path("/etc/polypy")
    config.load()

    if args['-d']:
        print("Debug mode enabled")
        print("")
        print("args:")
        print(args)
        print("configs:")
        print(config)

    argv = {}
    argv = [args['<command>']]

    polypy = Polypy(argv)
    polypy.run()
