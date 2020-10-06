from poly_py_tools.directory import Directory
from poly_py_tools.directory import DirectoryItem


class ProvisionDirectory():

    container = None
    pconf = None

    def __init__(self, container):
        self.container = container
        self.pconf = container['pconf']

    def run(self):
        directory = Directory(self.container['<args>']['<macaddress>'])
        for csv in self.container['<args>']['<csvfile>']:
            directory.add_csv(csv)
        directory.read()
        directory.save(self.pconf.tftproot_path())
