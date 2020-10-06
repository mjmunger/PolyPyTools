from typing import Dict
import sys
import importlib
from poly_py_tools.site.site_configurator import SiteConfigurator


class SiteFactory(object):

    cmd_callbacks = None

    def __init__(self):
        self.cmd_callbacks = {}
        self.cmd_callbacks['site init'] = ["poly_py_tools.site.site_configurator", "SiteConfigurator"]
        self.cmd_callbacks['site flush'] = ["poly_py_tools.site.site_configurator", "SiteConfigurator"]
        self.cmd_callbacks['site setup sntp'] = ["poly_py_tools.site.sntp_setup", "SntpSetup"]
        self.cmd_callbacks['site setup syslog'] = ["poly_py_tools.site.syslog_setup", "SyslogSetup"]
        self.cmd_callbacks['site setup nat'] = ["poly_py_tools.site.nat_setup", "NatSetup"]
        self.cmd_callbacks['site setup password'] = ["poly_py_tools.site.password_setup", "PasswordSetup"]
        self.cmd_callbacks['site setup digitmap'] = ["poly_py_tools.site.digitmap_setup", "DigitMapSetup"]
        self.cmd_callbacks['site setup voipprot'] = ["poly_py_tools.site.setup_voipprot", "SetupVoipProt"]
        self.cmd_callbacks['site setup vlan'] = ["poly_py_tools.site.setup_vlan", "SetupVlan"]
        self.cmd_callbacks['site disable nat'] = ["poly_py_tools.site.disable_nat", "DisableNat"]
        self.cmd_callbacks['site enable presence'] = ["poly_py_tools.site.enable_presence", "EnablePresence"]
        self.cmd_callbacks['site disable presence'] = ["poly_py_tools.site.disable_presence", "DisablePresence"]
        self.cmd_callbacks['site disable ptt'] = ["poly_py_tools.site.disable_ptt", "DisablePtt"]
        self.cmd_callbacks['site enable ptt'] = ["poly_py_tools.site.enable_ptt", "EnablePtt"]

    def create(self, container : Dict):
        args = container['<args>']

        for command in self.cmd_callbacks:
            match = True
            tokens = command.split(" ")
            for token in tokens:
                if token not in args:
                    match = False
            if match is False:
                continue

            for token in tokens:
                if args[token] is False:
                    match = False

            if match is False:
                continue

            lib = self.cmd_callbacks[command][0]
            target_class = self.cmd_callbacks[command][1]
            return_class = getattr(importlib.import_module(lib), target_class)
            return return_class(container)

        raise NotImplementedError("No class implemented for {}".format(" ".join(sys.argv)))


