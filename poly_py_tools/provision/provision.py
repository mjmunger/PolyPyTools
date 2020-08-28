#!/usr/bin/env python3
"""
Usage: polypy provision [ -v ... ] [options] polycom <macaddress>
       polypy provision [ -v ... ] [options] list endpoints
       polypy provision [ -v ... ] [options] directory for <macaddress> using <csvfile>...

options:
  -d  --debug    Debug mode
  -f, --force    Force the setting.
  -v             Be verbose

"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json

from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.polypy_config_finder import ConfigFinder
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision_factory import ProvisionFactory

args = docopt(__doc__)
debug_mode = False

if args['-d']:
    debug_mode = True
    print("Debug mode on. Debugging {}".format(__file__))
    print("--------------------------------------------------")
    print(args)
    print("--------------------------------------------------")

args['<args>'] = args

pconf = PolypyConfig()
pconf.add_search_path("/etc/polypy/")
pconf.find()
pconf.load()

meta = ModelMeta()
args['meta'] = meta

sip_resource_factory = SipResourceFactory()
factory = ProvisionFactory()
parser = PjSipSectionParser()
parser.use_config(pconf)
parser.use_factory(sip_resource_factory)

args['pjsipsectionparser'] = parser
args['pconf'] = pconf

factory = ProvisionFactory()
runner = factory.get_runner(args)
runner.run()