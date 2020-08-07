import os

from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.provision.polycom_config_writer import PolycomConfigWriter


class ProvisionPolycom:
    args = None
    configs = None

    def __init__(self, args):
        self.args = args
        self.configs = args['config']

    def run(self):
        pass
        # aors = []
        # endpoints = []
        # target_macaddress = str(self.args['<macaddress>']).lower().replace(":", "").replace("-", "")
        # count = 0
        # config_writer = PolycomConfigWriter()
        # # parser = SipConfParser(os.path.join(self.configs['paths']['asterisk'], 'sip.conf'))
        # # parser.parse()
        # # print("Device count: {}".format(len(parser.devices)))
        #
        # section_parser = PjSipSectionParser(os.path.join(self.configs['paths']['asterisk'], 'pjsip.conf'))
        # section_parser.parse()
        #
        # for section in section_parser.sections:
        #     factory = SipResourceFactory()
        #     resource = factory.create(section)
        #     if resource is None:
        #         continue
        #
        #     resource.set_attributes()
        #
        #     if isinstance(resource, Endpoint):
        #         endpoints.append(resource)
        #
        #     if isinstance(resource, Aor):
        #         aors.append(Aor)
        #
        #     # print("Phone type:{}\n".format(phone.type))
        #     # if not phone.type == "Polycom":
        #     #     continue
        #
        #     # print("Mac: {}".format(phone.mac_address))
        #     # print("Match? {}".format("Yes" if phone.mac_address == target_macaddress else "No"))
        #
        # for ep in endpoints:
        #     if target_macaddress != "all" and ep.mac != target_macaddress:
        #         continue
        #
        #     for aor in aors:
        #         print(aors)
        #
        #     count = count + 1
        #
        #     config_writer.set_verbosity(self.args['-v'])
        #     config_writer.use(resource)
        #     config_writer.use_configs(self.configs)
        #     config_writer.set_path()
        #     config_writer.write_config()
