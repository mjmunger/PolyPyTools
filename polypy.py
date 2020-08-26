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

from poly_py_tools.polypy import Polypy


if __name__ == '__main__':

    polypy = Polypy(docopt(__doc__, options_first=True))
    polypy.run()
