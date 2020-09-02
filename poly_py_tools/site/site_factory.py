from typing import Dict
import importlib
from poly_py_tools.site.site_configurator import SiteConfigurator


class SiteFactory(object):

    cmd_callbacks = None

    def __init__(self):
        self.cmd_callbacks = {}
        self.cmd_callbacks['site init'] = ["poly_py_tools.site.site_configurator", "SiteConfigurator"]
        self.cmd_callbacks['site flush'] = ["poly_py_tools.site.site_configurator", "SiteConfigurator"]

    def create(self, container : Dict):
        args = container['<args>']

        for command in self.cmd_callbacks:
            match = True
            tokens = command.split(" ")
            for token in tokens:
                if token not in args:
                    match = False
            if match is True:
                lib = self.cmd_callbacks[command][0]
                target_class = self.cmd_callbacks[command][1]
                return_class = getattr(importlib.import_module(lib), target_class)
                return return_class(container)


