import os

from poly_py_tools.site.site_runner import SiteRunner
import xml.etree.ElementTree as ET

class DigitMapSetup(SiteRunner):

    def site_cfg(self):
        return os.path.join(self.siteroot(), "site.cfg")

    def sip_interop_config(self):
        return os.path.join(self.siteroot(), "sip-interop.cfg")

    def del_digitmap(self):
        tree = ET.parse(self.site_cfg())
        root = tree.getroot()
        dialplan_node = root.find("dialplan")
        digitmaps = dialplan_node.attrib['dialplan.digitmap'].split("|")
        target_index = digitmaps.index(self.container['<args>']['<pattern>'])
        digitmaps.remove(digitmaps[target_index])
        dialplan_node.attrib['dialplan.digitmap'] = "|".join(digitmaps)

        digitmap_node = dialplan_node.find("dialplan.digitmap")
        timeouts = digitmap_node.attrib['dialplan.digitmap.timeOut'].split("|")
        timeouts.remove(timeouts[target_index])
        digitmap_node.attrib['dialplan.digitmap.timeOut'] = "|".join(timeouts)

        tree.write(self.site_cfg())

        print("{} removed from digit map for {}.".format(self.container['<args>']['<pattern>'],
                                                 self.container['<args>']['<site>']))

    def add_digitmap(self):
        tree = ET.parse(self.site_cfg())
        root = tree.getroot()
        dialplan_node = root.find("dialplan")
        digitmaps = dialplan_node.attrib['dialplan.digitmap'].split("|")
        digitmaps.append(self.container['<args>']['<pattern>'])
        dialplan_node.attrib['dialplan.digitmap'] = "|".join(digitmaps)

        digitmap_node = dialplan_node.find("dialplan.digitmap")
        timeouts = digitmap_node.attrib['dialplan.digitmap.timeOut'].split("|")
        timeouts.append("3")

        digitmap_node.attrib['dialplan.digitmap.timeOut'] = "|".join(timeouts)

        tree.write(self.site_cfg())

        print("{} added to digit map for {}.".format(self.container['<args>']['<pattern>'], self.container['<args>']['<site>']))

    def setup_digitmap(self):
        """
        Service these commands:
          polypy [ options ] site setup digitmap for <site> add <pattern>
          polypy [ options ] site setup digitmap for <site> del <pattern>
        :return:
        """

        if self.container['<args>']['del']:
            self.del_digitmap()

        if self.container['<args>']['add']:
            self.add_digitmap()

    def run(self):
        self.setup_digitmap()
