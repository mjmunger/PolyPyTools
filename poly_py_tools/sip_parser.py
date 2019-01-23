import sys
import os
import re
from poly_py_tools.template import Template
from poly_py_tools.registration import Registration

from pprint import pprint

class SipConfParser:

    templates = []
    devices = []
    sip_conf_path = None
    raw_extensions = []
    raw_templates = []

    def __init__(self, sip_conf_path):
        self.sip_conf_path = sip_conf_path

    def parse(self):
        self.parse_raw()
        self.parse_templates()

        for t in self.templates:
            print(t)

    def parse_templates(self):
        for device in self.raw_extensions:
            template_name = Template.match_template_definition(device[0])
            if template_name is not False:
                self.raw_templates.append(device)

        for t in self.raw_templates:
            template = Template()
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
                    print("Checking to see if %s is in %s" % (section, match.group(1)))

                    if section in match.group(1):
                        flag_extension = not flag_extension

                if len(buffer) > 0:
                    self.raw_extensions.append(buffer)

            if flag_extension:
                buffer.append(line)

            if not flag_extension:
                buffer = []
        f.close()
