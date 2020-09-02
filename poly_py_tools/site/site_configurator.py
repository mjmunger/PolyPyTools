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
        if self.container['<args>']['init']:
            self.init()
        elif self.container['<args>']['flush']:
            self.flush()

    def init(self):
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

        sip_ver_file_src = os.path.join(os.path.dirname(self.get_config_source()), "sip.ver")
        sip_ver_file_dst = os.path.join(self.siteroot(), "sip.ver")
        copy(sip_ver_file_src, sip_ver_file_dst)

        print("Directory initialized: {}".format(self.siteroot()))

    def flush(self):
        """
        Surgically remove the files for the firmware configs (only) leaving other files including phone configs.
        :return:
        """

        sip_ver_file = os.path.join(self.siteroot(), "sip.ver")

        if not os.path.exists(sip_ver_file):
            raise FileNotFoundError("Cannot flush the siteroot without sip.ver being present in the directory.")

        f = open(sip_ver_file, 'r')
        buffer = f.read()
        f.close()

        sip_version = "".join(buffer)

        src_dir = os.path.join(self.get_config_source())
        files = os.listdir(src_dir)

        for file in files:
            target_file = os.path.join(self.siteroot(), file)
            if os.path.exists(target_file):
                os.remove(target_file)

        print("Configs flushed for {}".format(self.siteroot()))







