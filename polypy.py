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
import subprocess
import os
from docopt import docopt

from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.versionator import Versionator


if __name__ == '__main__':

    args = docopt(__doc__, options_first=True)

    config = PolypyConfig()
    config.add_search_path(os.getcwd())
    config.add_search_path("/etc/polypy")
    if not config.find():
        print("Could not find polypy.conf. Perhaps you need to run set-defaults?")
        print("PolyPyTools has not been configured. Run polypy configure!")
        exit(1)
    config.load()

    if args['-d']:
        t = "{}: {}"
        print("Debug mode enabled")
        print("")
        print("args:")
        print(args)
        print("configs:")
        print(config)

    args['config'] = config
    argv = [args['<command>']] + args['<args>']

    if args['<command>'] == 'version':
        Versionator.show_version()

    if args['<command>'] == 'configure':
        from poly_py_tools import polypy_configure
        docopt(polypy_configure.__doc__, argv=argv)

    if args['<command>'] == 'provision':
        from poly_py_tools.provision import provision
        docopt(provision.__doc__, argv=argv)

    if args['<command>'] == 'sip':
        from poly_py_tools import sip_manager
        docopt(sip_manager.__doc__, argv=argv)

    # if args['<command>'] == 'ssl':
    #     from poly_py_tools import ssl_manager
    #     docopt(ssl_manager.__doc__, argv=argv)

    if args['<command>'] == 'site':
        from poly_py_tools import polypy_site
        docopt(polypy_site.__doc__, argv=argv)

    if args['<command>'] == 'deploy':
        from poly_py_tools import polypy_deploy
        docopt(polypy_deploy.__doc__, argv=argv)

    if args['<command>'] == 'dialplan':
        from poly_py_tools import polypy_dialplan
        docopt(polypy_dialplan.__doc__, argv=argv)
