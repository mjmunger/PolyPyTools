#!/usr/bin/env python3
"""
Usage: polypy provision polycom <macaddress>
       polypy provision list endpoints
       polypy provision directory for <macaddress> using <csvfile>...

options:
  -d  --debug    Debug mode
  -f, --force    Force the setting.
  -v             Be verbose

"""

from poly_py_tools.provision.provision_factory import ProvisionFactory


class Provision:

    container = None

    def __init__(self, container):
        self.container = container

    def pconf(self):
        return self.container['pconf']

    def run(self):
        factory = ProvisionFactory()
        runner = factory.get_runner(self.container)
        runner.run()

# args = docopt(__doc__)
# debug_mode = False
#
# if args['-d']:
#     debug_mode = True
#     print("Debug mode on. Debugging {}".format(__file__))
#     print("--------------------------------------------------")
#     print(args)
#     print("--------------------------------------------------")
#
# args['<args>'] = args
#
# pconf = PolypyConfig()
# pconf.add_search_path("/etc/polypy/")
# pconf.find()
# pconf.load()
#
# meta = ModelMeta()
# meta.use_configs(pconf)
# args['meta'] = meta
#
# sip_resource_factory = SipResourceFactory()
# factory = ProvisionFactory()
# parser = PjSipSectionParser()
# parser.use_config(pconf)
# parser.use_factory(sip_resource_factory)
#
# args['pjsipsectionparser'] = parser
# args['pconf'] = pconf
#
# factory = ProvisionFactory()
# runner = factory.get_runner(args)
# runner.run()
