import os


class PolypyConfig:

    config_path = None

    def __init__(self):
        pass

    def find(self, paths):
        for path in paths:
            config_path = os.path.join(path, "polypy.conf")
            if os.path.exists(config_path):
                self.config_path = config_path
                return True

        return False