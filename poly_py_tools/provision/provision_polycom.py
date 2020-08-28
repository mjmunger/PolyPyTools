import os

from poly_py_tools.loggable import Loggable
from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.polycom_config_writer import PolycomConfigWriter


class ProvisionPolycom(Loggable):
    args = None
    configs = None

    def __init__(self, args):
        self.args = args
        pconf = args['config']
        self.configs = pconf.configs()

    def run(self):
        factory = SipResourceFactory()
        if self.args['-d']:
            factory.set_debug()

        meta = ModelMeta()
        parser = PjSipSectionParser(os.path.join(self.configs['paths']['asterisk'], "pjsip.conf"), factory)
        if self.args['-d']:
            parser.set_debug()
        parser.parse()
        ep = parser.get_endpoint(self.args['<macaddress>'])
        ep.set_attributes()
        ep.load_aors(parser.resources)
        ep.load_auths(parser.resources)
        ep.hydrate_registrations()
        if self.args['-d']:
            self.log("{} aors loaded.".format(len(ep.addresses)),1)
            self.log("{} auths loaded.".format(len(ep.authorizations)), 1)
        ep.write_bootstrap(meta, self.configs['paths']['tftproot'])
        ep.write_configs(meta, self.configs['paths']['tftproot'])
        print("Complete.")


