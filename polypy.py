#!/usr/bin/env python3
"""

usage: polypy.py [ -v ... ] [options] [--help]
                 <command> [--] [<args>...]

options:
--version    Show the version of this package
-h           Show this help screen
-v           Be verbose. Levels 1-10 (or more).
-f, --force  Do it anyway.

Commands:

  configure  Configure PolyPyTools.
  provision  Creates provisioning files for Polycom phones from asterisk's sip.conf.
  sip        Manage sip.conf

See polypy help <command> for more information with a specific command.

"""
import sys
from docopt import docopt
from pprint import pprint

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0', options_first=True)

    argv = [args['<command>']] + args['<args>']

    if args['<command>'] == 'configure':
        from poly_py_tools import configure
        docopt(configure.__doc__, argv=argv)

    if args['<command>'] == 'provision':
        from poly_py_tools import provision
        docopt(provision.__doc__, argv=argv)

    if args['<command>'] == 'sip':
        from poly_py_tools import sip_manager
        docopt(sip_manager.__doc__, argv=argv)