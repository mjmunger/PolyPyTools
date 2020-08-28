import os

from poly_py_tools.loggable import Loggable
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.polypy_config import PolypyConfig


class PjSipSectionParser(Loggable):

    pjsip_conf_file = None
    sections = None
    resources = None
    factory = None
    templates = None
    verbosity = None
    pconf = None


    def __init__(self):
        self.sections = []
        self.resources = []
        self.templates = []
        super().__init__()

    def use_config(self, pconf: PolypyConfig):
        self.pconf = pconf
        self.pjsip_conf_file = os.path.join(pconf.asterisk_path(), "pjsip.conf")

    def use_factory(self, factory : SipResourceFactory):
        self.factory = factory

    def parse(self):
        f = open(self.pconf.pjsip_path(), 'r')
        buffer = f.readlines()
        f.close()

        section_buffer = []
        new_section = False

        for line in buffer:

            hidden_attributes = [";mac", ";model", ";label", ";order"]
            for attribute in hidden_attributes:
                if line.startswith(attribute):
                    line = line[1:]

            if line.startswith(";"):
                continue

            line = line.strip("\n")

            if line.startswith("["):
                new_section = True
            else:
                new_section = False

            if new_section:
                self.flush(section_buffer)
                section_buffer = []
                new_section = False

            section_buffer.append(line)

        self.flush(section_buffer)

        for section in self.sections:
            object = self.factory.create_template(section)
            if object is None:
                continue
            object.set_attributes()
            self.templates.append(object)
            self.log("Current template count: {}".format(len(self.templates)))

        self.factory.use_templates(self.templates)

        for section in self.sections:
            object = self.factory.create(section)
            if object is None:
                continue
            object.set_attributes()
            if self.debug_mode:
                object.set_debug()
            self.resources.append(object)

    def flush(self, buffer):
        if len(buffer) == 0:
            return

        buffer = self.sanitize_buffer(buffer)

        self.sections.append(buffer)

    def sanitize_line(self, line):

        if ";" in line:
            line = line.split(";")[0].strip()

        return line

    def sanitize_buffer(self, buffer):
        buffer = [self.sanitize_line(line) for line in buffer]
        buffer = [line.strip() for line in buffer]
        buffer = [line.strip("\n") for line in buffer]
        buffer = list(filter(None, buffer))
        buffer = list(filter(len, buffer))
        return buffer

    def get_endpoint(self, mac) -> Endpoint:
        target_mac = str(mac).lower().replace(":","").replace("-","")

        self.log("Target endpoint with mac address: {}".format(target_mac), 3)
        
        for resource in self.resources:
            if resource is None:
                self.log("Skipping a 'None' resource", 5)
                continue

            if not resource.type == 'endpoint':
                self.log("Skipping a non-endpoint resource: {}".format(resource.type), 5)
                continue

            if resource.type == 'endpoint' and resource.mac == target_mac:
                self.log("Found endpoint with mac: {}".format(resource.mac), 1)
                return resource

    def get_templates(self):
        templates = []

        for resource in self.resources:

            if resource is None:
                continue

            if resource.is_template:
                templates.append(resource)

        return templates