class ConfigWriter:

    verbosity = 0
    device = None
    configs = None
    target_config_path = None

    def __init__(self):
        pass

    def use(self, device):
        self.device = device

    def use_configs(self, configs):
        self.configs = configs

    def set_verbosity(self, level):
        self.verbosity = level

    def log(self, message, minimum_level=1):
        if self.verbosity < minimum_level:
            return True

        print("%s" % message)
