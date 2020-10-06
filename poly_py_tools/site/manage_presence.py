import os
import xml.etree.ElementTree as ET

from poly_py_tools.site.site_runner import SiteRunner


class ManagePresence(SiteRunner):
    def sip_features_cfg(self):
        return os.path.join(self.siteroot(), "features.cfg")

    def set_presence(self, value):
        tree = ET.parse(self.sip_features_cfg())
        root = tree.getroot()
        feature_node = root.find("feature")
        presence_node = feature_node.find("feature.presence")

        presence_node.attrib['feature.presence.enabled'] = value

        tree.write(self.sip_features_cfg())

    def run(self):
        self.set_presence(self.presence_value())
        print("Presence {} for {}.".format("enabled" if self.presence_value() is "1" else "disabled", self.container['<args>']['<site>']))
