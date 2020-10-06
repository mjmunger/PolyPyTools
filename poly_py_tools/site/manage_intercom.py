import os
import xml.etree.ElementTree as ET

from poly_py_tools.site.site_runner import SiteRunner


class ManageIntercom(SiteRunner):
    def sip_cfg(self):
        return os.path.join(self.siteroot(), "sip-interop.cfg")

    def set_alert(self, value):
        tree = ET.parse(self.sip_cfg())
        root = tree.getroot()
        protocol_node = root.find("voIpProt")
        sip_node = protocol_node.find("voIpProt.SIP")
        alert_node = sip_node.find("voIpProt.SIP.alertInfo")

        alert_node.attrib["voIpProt.SIP.alertInfo.1.value"] = value

        tree.write(self.sip_cfg())

    def run(self):
        self.set_alert(self.alert_value())
        self.message()
