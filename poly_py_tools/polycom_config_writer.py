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

    def log(self, message, minimum_level=1):
        if self.verbosity < minimum_level:
            return True

        print("%s" % message)

    def set_verbosity(self, level):
        self.verbosity = level
        self.log("Verbosity set to: %s" % level)

    def set_path(self):

        paths = self.configs['paths']
        self.tftproot = paths['tftproot']
        self.config_dir = os.path.join(self.tftproot, "Config")
        self.config_template = os.path.join(self.config_dir, 'reg-basic.cfg')
        self.phone_boostrap_file = os.path.join(self.tftproot, self.device.mac_address + ".cfg")

        self.phone_config_dir = self.tftproot if self.device.registrations[0].site is None else os.path.join(self.tftproot, self.device.registrations[0].site)
        self.phone_config = os.path.join(self.phone_config_dir, self.device.mac_address)

    def get_config(self):
        xmldoc = minidom.parse(self.config_template)
        itemlist = xmldoc.getElementsByTagName('reg')
        count = 0

        self.log("Sorting %s registrations in preparation for writing the config." % len(self.device.registrations), 1)

        self.device.sort_registrations()

        self.log("%s registrations sorted." % len(self.device.registrations), 1)
        for registration in self.device.registrations:
            self.log("Writing Registration {} for {}".format(registration.name, self.device.mac_address), 1)
            count = count + 1
            for s in itemlist:
                s.attributes['reg.{}.address'.format(count)] = '{}@{}'.format(registration.name, self.configs['server_addr'])
                s.attributes['reg.{}.auth.password'.format(count)] = registration.secret
                s.attributes['reg.{}.auth.userId'.format(count)] = registration.name
                s.attributes['reg.{}.label'.format(count)] = registration.label if registration.label is not None else registration.name
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
            if self.device.registrations[0].site is None:
                path = f
            else:
                path = "%s/%s" % (self.device.registrations[0].site, f)

            paths.append(path)

        # Add the last one.
        if self.device.registrations[0].site is None:
            config = self.device.mac_address
        else:
            config = "%s/%s" % (self.device.registrations[0].site, self.device.mac_address)

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

        try:
            f = open(self.phone_boostrap_file, 'w')
        except PermissionError:
            print("I don't have write access for %s. Check file permissions and try again." % self.phone_boostrap_file)
            exit(1)

        self.log("Writing bootstrap file: %s" % self.phone_boostrap_file, 1)
        f.write(self.get_cfg())
        f.close()

        self.log("Writing phone config: %s" % self.phone_config, 1)
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
