#!/usr/bin/env python3

import os
import sys
import json

class ConfigFinder():

    config_path = None
    is_local = False

    def __init__(self):
        config_dir = "/etc/polypy/"
        local_config = os.path.join(os.getcwd(),"polypy.conf")
        default_config = os.path.join(config_dir, "polypy.conf")
        self.config_path =  local_config if os.path.exists(local_config) else default_config
        self.is_local = True if os.path.exists(local_config) else False

    def get_configs(self):
        if not os.path.exists(self.config_path):
            return None

        f = open(self.config_path, 'r')

        try:
            configs = json.load(f)
        except json.JSONDecodeError:
            return {}
            f.close()

        f.close()

        return configs

    def get_config_dir(self):
        return os.path.dirname(self.config_path)

    def __str__(self):
        buffer = []
        buffer.append("Config path: {0}".format(self.config_path))
        buffer.append("Config is local: {0}".format("True" if self.is_local else "False"))

        return "\n".join(buffer)
