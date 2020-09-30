import os
import sys
from unittest.mock import MagicMock

from poly_py_tools.loggable import Loggable
from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.polycom_config_writer import PolycomConfigWriter
from poly_py_tools.provision.polycom_phone import PolycomPhone


class ProvisionPolycom(Loggable):
    container = None
    args = None
    configs = None
    pconf = None
    meta = None

    def __init__(self, container):
        self.container = container
        self.args = container['<args>']
        self.pconf = container['pconf']
        self.configs = self.pconf.configs()
        self.meta = container['meta']
        # self.factory = args['sip_factory']

        super().__init__()

    def run(self):
        meta = self.container['meta']

        # factory = self.container['factory']
        # if self.container['-d']:
        #     factory.set_debug()

        parser = self.container['pjsipsectionparser']
        parser.parse()
        endpoints = parser.get_endpoints_for_mac(self.args['<macaddress>'])

        phone = PolycomPhone()
        phone.use_configs(self.pconf)
        phone.use_model_meta(self.meta)
        phone.is_model("SPIP670")
        phone.has_mac(self.args['<macaddress>'])

        for ep in endpoints:
            ep.set_attributes()
            ep.use_proxy(self.container['pconf'].sip_proxy())
            ep.load_aors(parser.resources)
            ep.load_auths(parser.resources)
            phone.is_model(ep.model)
            phone.add_endpoint(ep)

        phone.hydrate_registrations(parser.resources)
        phone.write_bootstrap()
        phone.write_configs()

        print("Complete.")
