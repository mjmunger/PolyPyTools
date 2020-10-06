import os
import xml.etree.ElementTree as ET

from poly_py_tools.site.site_runner import SiteRunner


class ManagePtt(SiteRunner):
    def site_cfg(self):
        return os.path.join(self.siteroot(), "site.cfg")

    def set_ptt(self, enable_value):
        tree = ET.parse(self.site_cfg())
        root = tree.getroot()
        ptt_node = root.find("ptt")

        # Don't think this is needed.
        # callwaiting_node = ptt_node.find("ptt.callWaiting")
        # callwaiting_node.attrib['ptt.callWaiting.enable'] = 0

        mode_node = ptt_node.find("ptt.pttMode")
        mode_node.attrib['ptt.pttMode.enable'] = enable_value


        tree.write(self.site_cfg())

    def run(self):
        self.set_ptt(self.ptt_mode())
        print("Presence {} for {}.".format("enabled" if self.ptt_mode() is "1" else "disabled", self.container['<args>']['<site>']))
