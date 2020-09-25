#!/usr/bin/env python3
"""
usage: polypy [ -v ... ] [options] pjsip generate <extension> from <file> ([assign <template>] | [ use template column <column> ]) [with voicemail]
       polypy [ -v ... ] [options] pjsip guess columns from <file> [ --startrow=<startrow> ] [ --save ]

options:
  -a             Append generated records to the output file.
  -r             Re-write the generated pjsip file, and append generated entries to it.
  -d  --debug    Debug mode
  -f, --force    Force the setting.
  -v             Be verbose

"""

from docopt import docopt
from pwgen_secure.rpg import Rpg

from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.polypy_config_finder import ConfigFinder
from poly_py_tools.pjsip.pjsip_factory import PJSipFactory


# pconf = PolypyConfig()
# pconf.add_search_path("/etc/polypy/")
# pconf.find()
# pconf.load()
#
# args['config'] = pconf
# args['<args>'] = args
# args['rpg'] = Rpg("strong", None)
#
# factory = PJSipFactory()
# runner = factory.get_runner(args)
# runner.run()

class PJSip:

    container = None

    def __init__(self, container):
        self.container = container

    def pconf(self):
        return self.container['pconf']

    def run(self):
        factory = PJSipFactory()
        runner = factory.get_runner(self.container)
        runner.run()
