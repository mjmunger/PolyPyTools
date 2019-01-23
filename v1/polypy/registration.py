import os


class Registration:

        server = None
        secret = None
        extension = None
        site = None
        mac = None
        phone = None
        debug = False
        root = None

        def __init__(self, root, server=None):
            self.root = root
            self.server = server

        def set_debug(self):
            self.debug = True

        def parse_extension(self, line):

            pos1 = line.find("[") + 1
            pos2 = line.find("]")
            self.extension = line[pos1:pos2]

            if self.debug:
                print("    Parsing extension line: {}".format(line))
                print("    [ found at: {}".format(pos1))
                print("    ] found at: {}".format(pos2))
                print("    Extension parsed as: {}".format(self.extension))

        def parse_template(self, line):
            # Discover the template for this phone.
            pos1 = line.find("(") + 1
            pos2 = line.find(")")
            self.site = line[pos1:pos2]

            if self.debug:
                print("    Site (template) parsed as: {}".format(self.site))

        def parse_mac_phone(self,line):
            # if this line does not start with a comment, we cannot process it. Skip it.
            if line[:1] != ';':
                return False

            line = line[1:].strip()

            if "|" in line:
                buff = line.split("|")
                self.mac = buff[0]
                self.phone = buff[1]

                return True

            self.mac = line

        def parse_secret(self, line):
            line = line.strip()
            if self.debug:
                print("    Looking for secret in line: {}".format(line))
            if "secret" not in line:
                return False

            buff = line.split("=")
            self.secret = buff[1].strip()

            if self.debug:
                print("    Secret parsed as: {}".format(self.secret))

            return True

        def get_target_dir(self):
            return os.path.join(self.root, self.site)

        def get_mac_file(self):
            return os.path.join(self.get_target_dir(), self.mac)

        def get_config_file(self):
            return os.path.join(self.root, self.mac + ".cfg")
