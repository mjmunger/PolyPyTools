import os
import json
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
        with open(self.config_path, 'w') as fp:
            json.dump(self.config,fp)