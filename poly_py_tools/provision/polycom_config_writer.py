from xml.dom import minidom
from xml.dom.minidom import Document

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
    debug_mode = False
    firmware_dir = None
    model_meta = None

    def set_debug_mode(self, debug_mode):
        if debug_mode is False:
            return False

        self.debug_mode = True
        self.verbosity = 10

    def set_path(self):

        paths = self.configs['paths']
        self.tftproot = paths['tftproot']
        self.firmware_dir = os.path.join(self.tftproot, "firmware/{}".format(self.model_meta.get_firmware_version(self.device.model)))
        self.config_dir = os.path.join(self.firmware_dir, "Config")
        self.config_template = os.path.join(self.config_dir, 'reg-basic.cfg')
        self.phone_boostrap_file = os.path.join(self.tftproot, self.device.mac + ".cfg")

        self.phone_config_dir = self.tftproot if self.device.template is None else os.path.join(self.tftproot, self.device.template)
        self.phone_config = os.path.join(self.phone_config_dir,  self.device.mac)

    def load(self, model_meta):
        self.model_meta = model_meta
        
    def get_config(self):
        xmldoc = minidom.parse(self.config_template)
        itemlist = xmldoc.getElementsByTagName('reg')
        count = 0

        self.log("Sorting %s registrations in preparation for writing the config." % len(self.device.registrations), 1)

        self.device.sort_registrations()

        self.log("%s registrations sorted." % len(self.device.registrations), 1)
        for registration in self.device.registrations:
            self.log("Writing Registration {} for {}".format(registration.extension, self.device.mac), 1)
            count = count + 1
            for s in itemlist:
                s.attributes['reg.{}.address'.format(count)] = '{}@{}'.format(registration.extension, self.configs['server_addr'])
                s.attributes['reg.{}.auth.password'.format(count)] = registration.secret
                s.attributes['reg.{}.auth.userId'.format(count)] = registration.mac
                s.attributes['reg.{}.extension'.format(count)] = registration.extension
                s.attributes['reg.{}.label'.format(count)] = registration.label if registration.label is not None else registration.extension
                # s.attributes['reg.1.outboundProxy.address']
        output = xmldoc.toxml()

        return output

    def get_cfg_application_element(self):
        return "APPLICATION_{}".format(self.device.model)

    def get_file_path_attribute(self):
        return "APP_FILE_PATH_{}".format(self.device.model)

    def get_config_file_attribute(self):
        return "CONFIG_FILES_{}".format(self.device.model)

    def get_app_file_path(self):
        return "firmware/{}/{}.sip.ld".format(self.model_meta.get_firmware_version(self.device.model), self.model_meta.get_part(self.device.model))

    def get_cfg(self) -> Document:

        xmldoc = minidom.parse(os.path.join(self.firmware_dir, '000000000000.cfg'))

        app = xmldoc.getElementsByTagName(self.get_cfg_application_element())

        if not app:
            app = xmldoc.getElementsByTagName("APPLICATION")[0]
            child = xmldoc.createElement(self.get_cfg_application_element())
            app.appendChild(child)
            app = xmldoc.getElementsByTagName(self.get_cfg_application_element())

        for a in app:
            a.attributes[self.get_config_file_attribute()] = self.assemble_config_file_list()
            a.attributes[self.get_file_path_attribute()] = self.get_app_file_path()

        return xmldoc

    def assemble_config_file_list(self):
        # Assemble config file list
        files = ['site.cfg', 'sip-interop.cfg', 'features.cfg', 'sip-basic.cfg', 'reg-advanced.cfg']
        paths = []
        for f in files:
            if self.device.template is None:
                path = f
            else:
                path = "%s/%s" % (self.device.template, f)

            paths.append(path)

        # Add the last one.

        if self.device.template is None:
            config = self.device.mac
        else:
            config = "%s/%s" % (self.device.template, self.device.mac)

        paths.append(config)
        setting = ", ".join(paths)
        return setting

    def write_bootstrap_file(self):
        try:
            f = open(self.phone_boostrap_file, 'w')
        except PermissionError:
            print("I don't have write access for %s. Check file permissions and try again." % self.phone_boostrap_file)
            return False
        f.close()
        self.get_cfg().write()

    def write_phone_config(self):
        if not os.path.exists(self.phone_config_dir):
            try:
                os.mkdir(self.phone_config_dir)
            except Exception:
                self.log("Could not create %s" % self.phone_config_dir)

    def write_config(self):

        self.log("Writing bootstrap file: %s" % self.phone_boostrap_file, 1)
        self.write_bootstrap_file()


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
