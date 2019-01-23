import re
from poly_py_tools.registration import Registration


class Template(Registration):
    device_type = "template"

    @staticmethod
    def match_template_definition(definition):
        template_pattern = r"^(\[[a-zA-Z0-9]+?\])(\(!\))"
        match = re.search(template_pattern, definition)
        return match.group(1)[1:-1] if match else False

    def parse_template(self, raw_device):
        self.name = self.match_template_definition(raw_device[0].strip())
        self.parse_registration(raw_device)
