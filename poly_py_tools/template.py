import re
from poly_py_tools.registration import Registration


class Template(Registration):

    @staticmethod
    def match_template_definition(definition):
        template_pattern = r"^(\[[a-zA-Z0-9]+?\])(\(!\))"
        match = re.search(template_pattern, definition)
        return match.group(1)[1:-1] if match else False

    def parse_template(self, raw_device):

        self.name = self.match_template_definition(raw_device[0])

        for line in raw_device:
            if "=" not in line:
                continue

            buff = line.split("=")
            if buff[0] == "allow":
                self.allow.append(buff[1])
                continue

            if buff[0] == "disallow":
                self.disallow.append(buff[1])
                continue

            setattr(self, buff[0], buff[1].strip())
