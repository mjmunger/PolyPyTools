from poly_py_tools.directory import Directory
from poly_py_tools.directory import DirectoryItem


class ProvisionDirectory():

    args = None
    configs = None

    def __init__(self, args):
        self.args = args
        self.configs = args['config']

    def run(self):
        directory = Directory(self.args['<macaddress>'])
        for csv in self.args['<csvfile>']:
            directory.add_csv(csv)
        directory.read()
        directory.save(self.configs)
