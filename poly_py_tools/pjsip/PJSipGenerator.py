import os


class PJSipGenerator(object):

    source_csv = None
    config = None

    def __index__(self):
        pass

    def use(self, config):
        self.config = config

    def generate_from(self, csv):
        print("Generate from {}".format(csv))
        print("Exists: {}".format("Yes" if os.path.exists(csv) else "No"))
        if not os.path.exists(csv):
            raise FileNotFoundError("Could not find {}".format(csv))
        self.source_csv = csv