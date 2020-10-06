import os
import xml.etree.ElementTree as ET

from poly_py_tools.site.site_runner import SiteRunner


class ManagePaging(SiteRunner):
    def site_cfg(self):
        return os.path.join(self.siteroot(), "site.cfg")

    def set_paging(self, value):
        tree = ET.parse(self.site_cfg())
        root = tree.getroot()
        ptt_node = root.find("ptt")
        pagemode_node = ptt_node.find("ptt.pageMode")

        ptt_pagemode = ptt_node.find("ptt.pageMode")
        ptt_pagemode.attrib["ptt.pageMode.enable"] = value

        if value ==1:
            ptt_pagemode.attrib["ptt.pageMode.displayName"] = self.container['<args>']['--name']
        else:
            ptt_pagemode.attrib["ptt.pageMode.displayName"] = ""

        tree.write(self.site_cfg())

    def run(self):
        self.set_paging(self.paging_value())
        print("Paging {} for {}.".format("enabled" if self.paging_value() is "1" else "disabled", self.container['<args>']['<site>']))
