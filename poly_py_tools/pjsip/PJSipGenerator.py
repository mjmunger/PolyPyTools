import os
from poly_py_tools.dialplan import Dialplan
from poly_py_tools.dialplan_entry import Entry
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.template import Template


class PJSipGenerator(object):

    source_csv = None
    config = None

    def __index__(self):
        pass

    def use(self, config):
        self.config = config

    def generate_from(self, csv):
        if not os.path.exists(csv):
            raise FileNotFoundError("Could not find {}".format(csv))

        self.source_csv = csv

    def conf(self):
        if self.config is None:
            raise ValueError("Polypy config (self.config) must be set before attempting to generate conf files. Try: generator.use('someconfig')")

        dialplan = Dialplan(self.source_csv)
        dialplan.with_config(self.config)
        dialplan.parse()

        endpoints = []
        templates = {}

        for entry in dialplan.entries:
            template = Template()
            template.from_entry(entry)
            if not template.section in templates:
                templates[template.section] = template

        print(templates)


