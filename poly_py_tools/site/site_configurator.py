import os
from shutil import copy

from poly_py_tools.site.site_runner import SiteRunner


class SiteConfigurator(SiteRunner):

    container = None

    def __init__(self, container):
        self.container = container

    def siteroot(self):
        domain = list(self.container['<args>']['<site>'].split("."))
        domain.reverse()
        return  os.path.join(self.container['pconf'].tftproot_path(), "-".join(domain))

    def get_config_source(self):
        if self.container['<args>']['<model>']:
            return os.path.join(self.container['meta'].get_firmware_dir(self.container['<args>']['<model>']), "Config")
        else:
            return os.path.join(self.container['meta'].get_firmware_dir("VVX601"), "Config")

    def run(self):
        """
        1. Create the site directory.
        2. Copy over all the Configs for that site (Use current configs unless firmware specified)
        :return:
        """

        if not os.path.exists(self.siteroot()):
            os.mkdir(self.siteroot())

        source_dir = self.get_config_source()
        for file in os.listdir(source_dir):
            src = os.path.join(self.get_config_source(), file)
            dst = os.path.join(self.siteroot(), file)
            if not os.path.exists(dst):
                copy(src, dst)

        print("Directory initialized: {}".format(self.siteroot()))

