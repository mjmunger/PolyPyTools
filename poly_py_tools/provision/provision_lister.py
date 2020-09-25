import os

from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser


class ProvisionLister:

    args = None
    pconf = None

    def __init__(self, args):
        self.args = args
        self.pconf = args['pconf']

    def run(self):

        factory = SipResourceFactory()
        parser = PjSipSectionParser(os.path.join(self.config['paths']['asterisk'], 'pjsip.conf'), factory)
        parser.parse()
        print("Endpoints found in pjsip.conf:")
        for section in parser.sections:
            if factory.extract_type(section) == "endpoint":
                target_object = factory.create(section)
                target_object.set_attributes()
                if target_object.mac is not None:
                    print("{} ({})".format(target_object.aors, target_object.mac))
                else:
                    print(target_object.aors)
