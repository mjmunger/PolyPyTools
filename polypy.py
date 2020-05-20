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
  ssl        Configure SSL for a phone.
  deploy     Deploy files rendered to tftproot

See polypy help <command> for more information with a specific command.

"""
import subprocess
import os
from docopt import docopt


def show_version():
    execution_dir = os.getcwd()
    working_dir = os.path.dirname(os.readlink("/usr/local/bin/polypy")) if os.path.exists(
        "/usr/local/bin/polypy") else os.getcwd()
    os.chdir(working_dir)
    proc = subprocess.Popen(['git', 'describe', '--tags', '--long'], 1024, stdout=subprocess.PIPE)
    try:
        outs, errs = proc.communicate(1)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate(1)
    program_version = outs.decode("utf-8").strip()
    print("polypy version: {}".format(program_version))


if __name__ == '__main__':

    args = docopt(__doc__, options_first=True)

    if args['-d']:
        t = "{}: {}"
        print("Debug mode enabled")
        print("")
        print("args:")
        print(args)

    argv = [args['<command>']] + args['<args>']

    if args['<command>'] == 'version':
        show_version()

    if args['<command>'] == 'configure':
        from poly_py_tools import polypy_configure
        docopt(polypy_configure.__doc__, argv=argv)

    if args['<command>'] == 'provision':
        from poly_py_tools import provision
        docopt(provision.__doc__, argv=argv)

    if args['<command>'] == 'sip':
        from poly_py_tools import sip_manager
        docopt(sip_manager.__doc__, argv=argv)

    if args['<command>'] == 'ssl':
        from poly_py_tools import ssl_manager
        docopt(ssl_manager.__doc__, argv=argv)
    if args['<command>'] == 'site':
        from poly_py_tools import polypy_site
        docopt(polypy_site.__doc__, argv=argv)

