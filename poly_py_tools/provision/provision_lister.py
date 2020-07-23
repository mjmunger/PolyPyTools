import os

from poly_py_tools.pjsip_resource_factory import SipResourceFactory
from poly_py_tools.pjsip_section_parser import PjSipSectionParser


class ProvisionLister:

    args = None
    config = None

    def __init__(self, args):
        self.args = args
        self.config = args['config']

    def run(self):
        parser = PjSipSectionParser(os.path.join(self.config['paths']['asterisk'], 'pjsip.conf'))
        parser.parse()
        factory = SipResourceFactory()
        print("Endpoints found in pjsip.conf:")
        for section in parser.sections:
            if factory.extract_type(section) == "endpoint":
                target_object = factory.create(section)
                target_object.set_attributes()
                if target_object.mac is not None:
                    print("{} ({})".format(target_object.aors, target_object.mac))
                else:
                    print(target_object.aors)
