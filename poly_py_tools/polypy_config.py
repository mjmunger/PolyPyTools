import os
import json
import sys
import site
from typing import List


class PolypyConfig:

    config_path = None
    search_paths = []

    def __init__(self):
        pass

    def find(self):
        for path in self.search_paths:
            config_path = os.path.join(path, "polypy.conf")
            if os.path.exists(config_path):
                self.config_path = config_path
                return True

        return False

    def add_search_path(self, path):
        self.search_paths.append(path)

    def load(self):
        with open(self.config_path) as fp:
            self.config = json.load(fp)

    def write(self):
        try:
            with open(self.config_path, 'w') as fp:
                json.dump(self.config,fp)
        except PermissionError:
            print("Could not write config to {}. Perhaps you need to be root?".format(self.config_path))
            raise PermissionError

    def write_default_config(self, target_path):
        self.config_path = target_path
        configs = {}
        # Setup default values:
        lib_path = '/var/lib/polypy'
        share_path = '/usr/share/polypy/'
        local_bin = '/usr/local/bin/'
        package_path = None

        paths = {}

        package_path = os.path.join(site.getsitepackages()[0], 'poly_py_tools')

        paths["asterisk"] = "/etc/asterisk/"
        paths["tftproot"] = "/srv/tftp/"
        configs['lib_path'] = lib_path
        configs['share_path'] = share_path
        configs['config_path'] = self.config_path
        configs['package_path'] = package_path
        configs['paths'] = paths
        configs['server_addr'] = "127.0.0.1"
        self.config = configs

        self.write()

    def set_path(self, path, target_path):
        if target_path is ".":
            target_path = os.getcwd()

        if not str(target_path).startswith("/"):
            target_path = os.path.join(os.getcwd(), target_path)

        self.config['paths'][path] = target_path
        self.write()

    def set_server(self, server_addr):
        self.config['server_addr'] = server_addr
        self.write()
