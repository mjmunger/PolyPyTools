import os

from poly_py_tools.site.site_runner import SiteRunner
import xml.etree.ElementTree as ET

class SetupVlan(SiteRunner):

    def setup_vlan(self):
        """
        Service this command: polypy [ options ] site setup voipprot for <site> --address=<address> [ --port=<port> ]
        :return:
        """

        if self.container['<args>']['enable']:
            enabled = True
        elif self.container['<args>']['disable']:
            enabled = False

        tree = ET.parse(self.site_cfg())
        root = tree.getroot()

        device_node = root.find("device")
        dhcp_node = device_node.find("device.dhcp")
        net_node = device_node.find("device.net")

        net_node.attrib['lldpEnabled'] = "1" if enabled else "0"
        net_node.attrib['cdpEnabled'] = "1" if enabled else "0"

        set_nodes = ['lldpEnabled', 'cdpEnabled']
        for node in set_nodes:
            tmp = net_node.find("device.net.{}".format(node))
            tmp.attrib['device.net.{}.set'.format(node)] = "1" if enabled else "0"

        dhcp_node.attrib['device.dhcp.dhcpVlanDiscUseOpt'] = "fixed" if enabled else "disabled"
        vlan_discovery_node = dhcp_node.find("device.dhcp.dhcpVlanDiscUseOpt")
        vlan_discovery_node.attrib['device.dhcp.dhcpVlanDiscUseOpt.set'] = "1" if enabled else "0"


        tree.write(self.site_cfg())

    def run(self):
        self.setup_vlan()

        print("VLAN for {} has been {}.".format(self.container['<args>']['<site>'], "enabled" if self.container['<args>']['enable'] else "disabled"))
