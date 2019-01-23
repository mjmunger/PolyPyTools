#!/usr/bin/env python3
"""

usage: polypy.py [-v | --verbose ] [--version] [--help]
                 <command> [<args>...]

options:
--version      Show the version of this package
--help         Show this help screen
-v, --verbose  Be verbose

Commands:

  configure  Configure PolyPyTools.
  provision  Creates provisioning files for asterisk.
  secure     Secure sip.conf with strong passwords.
  validate   Validates asterisk and Polycom installation and files.

See polypy help <command> for more information with a specific command.

"""
from sys import argv

from docopt import docopt
from pprint import pprint

if __name__ == '__main__':
    args = docopt(__doc__)

    if args['<command>'] == 'configure':
        from poly_py_tools import configure
        docopt(configure.__doc__)

    if args['<command>'] == 'provision':
        from poly_py_tools import provision

    if args['<command>'] == "validate":
        from poly_py_tools import validate
        docopt(validate.__doc__, argv=argv)