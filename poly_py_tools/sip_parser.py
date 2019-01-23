import sys
import os
import re
from poly_py_tools.template import Template
from poly_py_tools.registration import Registration
from pprint import pprint
import uuid


class SipConfParser:
    verbosity = 0
    templates = []
    devices = []
    sip_conf_path = None
    raw_extensions = []
    raw_templates = []

    def __init__(self, sip_conf_path):
        self.sip_conf_path = sip_conf_path

    def log(self, message, minimum_level=1):
        if self.verbosity < minimum_level:
            return True

        print("%s" % message)

    def set_verbosity(self, level):
        self.verbosity = level
        self.log("Verbosity set to: %s" % level)

    def parse(self):
        self.parse_raw()
        self.parse_templates()
        self.parse_extensions()

        # for device in self.devices:
        #     print("Name: %s" % device.name)
        #     print("Device Type: %s" % device.device_type)

    def parse_extensions(self):
        for device in self.raw_extensions:
            template_name = Template.match_template_definition(device[0])
            if template_name is not False:
                continue

            registration = Registration()
            registration.set_verbosity(self.verbosity)
            template = registration.implements_template(device)[1:-1]

            if template is not False:
                self.log("%s template in use" % template, 3)
                registration.template = template
                registration.site = template
                for t in self.templates:
                    if t.name == template:
                        registration.import_template(t)
                        break

            registration.parse_registration(device)
            self.devices.append(registration)

    def parse_templates(self):
        for device in self.raw_extensions:
            template_name = Template.match_template_definition(device[0])
            if template_name is not False:
                self.raw_templates.append(device)

        for t in self.raw_templates:
            template = Template()
            template.set_verbosity(self.verbosity)
            template.parse_template(t)
            self.templates.append(template)

    def parse_raw(self):
        f = open(self.sip_conf_path)
        extension_pattern = r"^(\[[a-zA-Z0-9]+?\])(\([a-zA-Z0-9-]+?\)){0,}"
        flag_extension = False
        buffer = []

        unwanted_sections = ['general', 'authentication']

        for line in f:
            line = line.strip()
            match = re.search(extension_pattern,line)
            if match:
                flag_extension = not flag_extension
                for section in unwanted_sections:
                    self.log("Checking to see if %s is in %s" % (section, match.group(1)), 3)

                    if section in match.group(1):
                        flag_extension = not flag_extension

                if len(buffer) > 0:
                    self.raw_extensions.append(buffer)

            if flag_extension:
                buffer.append(line)

            if not flag_extension:
                buffer = []
        f.close()

    def swap_mac(self, mac1, mac2):
        uuid1 = str(uuid.uuid4())
        uuid2 = str(uuid.uuid4())

        f = open(self.sip_conf_path, 'r')
        buffer = f.readlines()
        f.close()

        output = []

        for line in buffer:
            line = line.replace(mac1, uuid2)
            line = line.replace(mac2, uuid1)
            line = line.replace(uuid1, mac1)
            line = line.replace(uuid2, mac2)
            output.append(line)

        f = open(self.sip_conf_path, 'w')
        f.writelines(output)
        f.close()




