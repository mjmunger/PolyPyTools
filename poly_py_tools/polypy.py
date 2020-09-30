from docopt import docopt
from pwgen_secure.rpg import Rpg

from poly_py_tools.pjsip.pjsip import PJSip
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.provision import Provision
from poly_py_tools.site.site import Site
from poly_py_tools.versionator import Versionator


class Polypy():

    args = None

    def __init__(self, args):
        self.args = args

    def run(self):

        argv = [self.args['<command>']] + self.args['<args>']
        container = {}
        pconf = PolypyConfig()
        pconf.add_search_path("/etc/polypy/")
        pconf.find()
        pconf.load()
        container['pconf'] = pconf

        container['rpg'] = Rpg("strong", None)

        container['meta'] = ModelMeta()
        container['meta'].use_configs(pconf)

        container['sip_factory'] = SipResourceFactory()

        sip_factory = SipResourceFactory()

        parser = PjSipSectionParser()
        parser.use_config(container['pconf'])
        parser.use_factory(sip_factory)

        container['pjsipsectionparser'] = parser

        if self.args['<command>'] == 'pjsip':
            parser = PjSipSectionParser()
            parser.use_config(pconf)
            parser.use_factory(sip_factory)
            container['pjsipparser'] = parser
            from poly_py_tools.pjsip import pjsip
            container['args'] = docopt(pjsip.__doc__, argv=argv)
            pjsip = PJSip(container)
            pjsip.run()

        elif self.args['<command>'] == 'configure':
            from poly_py_tools import polypy_configure
            docopt(polypy_configure.__doc__, argv=argv)

        elif self.args['<command>'] == 'provision':
            from poly_py_tools.provision import provision
            container['<args>'] = docopt(provision.__doc__, argv=argv)
            provision = Provision(container)
            provision.run()

        elif self.args['<command>'] == 'site':
            from poly_py_tools.site import site
            container['<args>'] = docopt(site.__doc__, argv=argv)
            site = Site(container)
            site.run()

        elif self.args['<command>'] == 'version':
            Versionator.show_version()
        else:
            print("Command '{}' not recognized. Use polypy --help".format(self.args['<command>']))
            raise SystemExit
