from xml.dom import minidom
import sys
import os


class Config:

    server = ""
    site = ""
    extension = ""
    secret = ""
    mac = ""
    registration = []
    target_dir = ""
    root = None

    def __init__(self, sip_config,root):

        self.server = sip_config.server
        self.root = root
        self.registration = sip_config.registrations

    def provision(self, extension):
        print("Provisioning: {}".format(extension))
        for reg in self.registration:
            print("Extension: {}".format(reg.extension))
            if extension == reg.extension:
                print("Provisioning extension: {}".format(reg.extension))
                self.write_config(reg)
                self.write_cfg(reg)

    def check_target_dir(self,path):

        if not os.path.exists(path):
            os.mkdir(path)

    def create_config(self, reg):
        xmldoc = minidom.parse('Config/reg-basic.cfg')
        itemlist = xmldoc.getElementsByTagName('reg')
        count = 0

        print("Writing Registration {} for {}".format(reg.extension, reg.mac))
        count = count + 1
        for s in itemlist:
            s.attributes['reg.{}.address'.format(count)] = '{}@{}'.format(reg.extension, reg.server)
            s.attributes['reg.{}.auth.password'.format(count)] = reg.secret
            s.attributes['reg.{}.auth.userId'.format(count)] = reg.extension
            s.attributes['reg.{}.label'.format(count)] = reg.extension
            # s.attributes['reg.1.outboundProxy.address']
        output = xmldoc.toxml()

        return output

    def write_config(self, reg):

        config = self.create_config(reg)

        print("Writing MAC file: %s" % reg.get_mac_file())
        print(reg.site)
        print(reg.mac)

        xp = open(reg.get_mac_file(), 'w')
        xp.write(config)
        xp.close()

    def write_cfg(self, reg):

        xmldoc = minidom.parse('000000000000.cfg')
        app = xmldoc.getElementsByTagName('APPLICATION')

        # Assemble config file list
        files = ['site.cfg', 'sip-interop.cfg', 'features.cfg', 'sip-basic.cfg', 'reg-advanced.cfg']
        paths = []

        for f in files:
            path = "%s/%s" % (reg.site, f)
            paths.append(path)

        # Add the last one.
        config = "%s/%s" % (reg.site, reg.mac)
        paths.append(config)

        setting = ", ".join(paths)

        for a in app:
            a.attributes['CONFIG_FILES'] = setting

        output = xmldoc.toxml()

        print("Writing: %s" % reg.get_config_file())
        cp = open(reg.get_config_file(), "w")
        cp.write(output)
        cp.close()

    def clean(self):
        """
        Cleans all the configs for all registrations. DANGEROUS.
        :return:
        """

        for reg in self.registration:
            target = reg.get_config_file()
            if os.path.exists(target):
                print("Removing: {}".format(target))
                os.unlink(target)

            target = reg.get_mac_file()
            if os.path.exists(target):
                print("Removing: {}".format(target))
                os.unlink(target)

        print("Provisioning files cleaned.\n")

    def provision_all(self):
        print("Provisioning all extensions...")
        for reg in self.registration:
            self.provision(reg.extension)

        print("Complete.")

    def dump(self):
        for reg in self.registration:
            print("""
[{}]({}]
;{}|{}
secret={}
""".format(reg.extension, reg.site, reg.mac, reg.phone, reg.secret))
