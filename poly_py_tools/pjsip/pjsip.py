#!/usr/bin/env python3
"""
usage: polypy [ -v ... ] [options] pjsip generate <extension> from <file> ([assign <template>] | [ use template column <column> ]) [with voicemail]

options:
  -d  --debug    Debug mode
  -f, --force    Force the setting.
  -v             Be verbose

"""

from docopt import docopt
from pwgen_secure.rpg import Rpg

from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.polypy_config_finder import ConfigFinder
from poly_py_tools.pjsip.pjsip_factory import PJSipFactory

args = docopt(__doc__, options_first=True)
debug_mode = False

if args['-d']:
    debug_mode = True
    print("--------------------------------------------------")
    print("Debug mode on.")
    print("Debugging {}".format(__file__))
    print("--------------------------------------------------")
    print(args)
    print("--------------------------------------------------")

pconf = PolypyConfig()
pconf.add_search_path("/etc/polypy/")
pconf.find()
pconf.load()

args['config'] = pconf
args['<args>'] = args
args['rpg'] = Rpg("strong", None)

factory = PJSipFactory()
runner = factory.get_runner(args)
runner.run()
