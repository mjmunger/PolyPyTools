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

from docopt import docopt

from poly_py_tools.configure.config_finder import ConfigFinder
from poly_py_tools.provision_factory import ProvisionFactory

args = docopt(__doc__)
debug_mode = False
print("asdfadf")
if args['-d']:
    debug_mode = True
    print("Debug mode on. Debugging {}".format(__file__))
    print("--------------------------------------------------")
    print(args)
    print("--------------------------------------------------")

config_finder = ConfigFinder()
configs = config_finder.get_configs()
args['config'] = configs

factory = ProvisionFactory()
runner = factory.get_runner(args)
runner.run()
