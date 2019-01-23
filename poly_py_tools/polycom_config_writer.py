from xml.dom import minidom
from poly_py_tools.config_writer import ConfigWriter
import os
import sys

from pprint import pprint

class PolycomConfigWriter(ConfigWriter):

    tftproot = None
    config_dir = None
    config_template = None
    phone_boostrap_file = None
    phone_config_dir = None
    phone_config = None

    def set_path(self):

        paths = self.configs['paths']
        self.tftproot = paths['tftproot']
        self.config_dir = os.path.join(self.tftproot, "Config")
        self.config_template = os.path.join(self.config_dir, 'reg-basic.cfg')
        self.phone_boostrap_file = os.path.join(self.tftproot, self.device.mac + ".cfg")

        self.phone_config_dir = self.tftproot if self.device.site is None else os.path.join(self.tftproot, self.device.site)
        self.phone_config = os.path.join(self.phone_config_dir, self.device.mac)

    def get_config(self):
        xmldoc = minidom.parse(self.config_template)
        itemlist = xmldoc.getElementsByTagName('reg')
        count = 0

        self.log("Writing Registration {} for {}".format(self.device.name, self.device.mac), 1)
        count = count + 1
        for s in itemlist:
            s.attributes['reg.{}.address'.format(count)] = '{}@{}'.format(self.device.name, self.configs['server_addr'])
            s.attributes['reg.{}.auth.password'.format(count)] = self.device.secret
            s.attributes['reg.{}.auth.userId'.format(count)] = self.device.name
            s.attributes['reg.{}.label'.format(count)] = self.device.name
            # s.attributes['reg.1.outboundProxy.address']
        output = xmldoc.toxml()

        return output

    def get_cfg(self):

        xmldoc = minidom.parse(os.path.join(self.tftproot, '000000000000.cfg'))

        app = xmldoc.getElementsByTagName('APPLICATION')

        # Assemble config file list
        files = ['site.cfg', 'sip-interop.cfg', 'features.cfg', 'sip-basic.cfg', 'reg-advanced.cfg']
        paths = []

        for f in files:
            if self.device.site is None:
                path = f
            else:
                path = "%s/%s" % (self.device.site, f)

            paths.append(path)

        # Add the last one.
        if self.device.site is None:
            config = self.device.mac
        else:
            config = "%s/%s" % (self.device.site, self.device.mac)

        paths.append(config)

        setting = ", ".join(paths)

        for a in app:
            a.attributes['CONFIG_FILES'] = setting

        return xmldoc.toxml()

    def write_config(self):
        if not os.path.exists(self.phone_config_dir):
            try:
                os.mkdir(self.phone_config_dir)
            except Exception:
                self.log("Could not create %s" % self.phone_config_dir)
                sys.exit(1)

        f = open(self.phone_boostrap_file, 'w')
        f.write(self.get_cfg())
        f.close()

        f = open(self.phone_config, 'w')
        f.write(self.get_config())
        f.close()

    def remove(self):
        self.log("Removing %s" % self.phone_boostrap_file, 1)
        if os.path.exists(self.phone_boostrap_file):
            os.remove(self.phone_boostrap_file)

        self.log("Removing %s" % self.phone_config, 1)
        if os.path.exists(self.phone_config):
            os.remove(self.phone_config)
