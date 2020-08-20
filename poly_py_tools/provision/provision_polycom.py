import os

from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.polycom_config_writer import PolycomConfigWriter


class ProvisionPolycom:
    args = None
    configs = None

    def __init__(self, args):
        self.args = args
        self.configs = args['config']

    def run(self):
        factory = SipResourceFactory()
        meta = ModelMeta()
        parser = PjSipSectionParser(os.path.join(self.configs['paths']['asterisk'], "pjsip.conf"), factory)
        parser.parse()
        ep = parser.get_endpoint(self.args['<macaddress>'])
        ep.set_attributes()
        ep.load_aors(parser.resources)
        ep.load_auths(parser.resources)
        ep.hydrate_registrations()
        ep.write_bootstrap(meta, self.configs['paths']['tftproot'])
        ep.write_configs(meta, self.configs['paths']['tftproot'])


