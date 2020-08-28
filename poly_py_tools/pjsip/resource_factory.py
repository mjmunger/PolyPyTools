from copy import deepcopy

from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.transport import Transport
from poly_py_tools.pjsip.auth import Auth
from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.registration import Registration
from poly_py_tools.pjsip.domain_alias import DomainAlias
from poly_py_tools.pjsip.acl import Acl
from poly_py_tools.pjsip.contact import Contact
import re

class SipResourceFactory:

    templates = None

    def __init__(self):
        self.templates = []

    def create(self, section):
        if not len(section) > 0:
            return None
        template = self.get_template_for_section(section[0])

        if template is not None:
            section_lines = deepcopy(template.section)
            section_lines.pop(0)
            section = section + section_lines

        type = self.extract_type(section)

        if type == "endpoint":
            return Endpoint(section)

        if type == "transport":
            return Transport(section)

        if type == "auth":
            return Auth(section)

        if type == "aor":
            return Aor(section)

        if type == "registration":
            return Registration(section)

        if type == "domain_alias":
            return DomainAlias(section)

        if type == "acl":
            return Acl(section)

        if type == "contact":
            return Contact(section)

    def create_template(self, section):
        if section is None or section == []:
            return None

        if "(!)" not in section[0]:
            return None

        type = self.extract_type(section)

        if type is None:
            raise ValueError("A template must have a type to be generated with polypy.")

        object = self.create(section)
        object.is_template = True
        object.set_attributes()
        return object

    def extract_type(self, section):

        for line in section:
            if not "=" in line:
                continue

            option, value = line.split("=")
            if option.strip() == "type":
                return str(value.strip()).lower()

        return None

    def use_templates(self, templates):
        self.templates = templates

    def get_template_for_section(self, section_header):
        pattern = r"\[([a-zA-Z0-9]{1,})\]\((.+)\)"
        match = re.match(pattern, section_header)
        if not match:
            return None

        target_section_name = match.group(2).strip()
        for template in self.templates:
            if template.section_name == target_section_name:
                return template
        return None