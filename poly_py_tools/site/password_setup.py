import os

from poly_py_tools.site.site_runner import SiteRunner
import xml.etree.ElementTree as ET

class PasswordSetup(SiteRunner):

    def site_cfg(self):
        return os.path.join(self.siteroot(), "site.cfg")

    def sip_interop_config(self):
        return os.path.join(self.siteroot(), "sip-interop.cfg")

    def setup_password(self):
        """
        Service this command: polypy [ options ] site setup password for <site> to <password>
        :return:
        """

        tree = ET.parse(self.site_cfg())
        root = tree.getroot()
        node = root.find("device")
        node = node.find("device.auth")
        node.attrib['device.auth.localAdminPassword'] = self.container['<args>']['<password>']

        tmp = node.find("device.auth.localAdminPassword")
        tmp.attrib['device.auth.localAdminPassword.set'] = "1"

        tree.write(self.site_cfg())

    def run(self):
        self.setup_password()
        print("Phone password for {} set to {}".format(self.container['<args>']['<site>'], self.container['<args>']['<password>']))
