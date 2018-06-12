from polypy.registration import Registration


class Sipconf:
    server = None
    sip_path = None
    list_mac = []
    list_servers = {}
    list_skip = ['[general]', '[authentication]']
    registrations = []
    debug = False
    root = None

    def __init__(self, server, sip_path, root):

        self.server = server
        self.sip_path = sip_path
        self.root = root

    def set_debug(self):
        print("Debug mode enabled\n")
        self.debug = True

    def is_definition(self, line):
        if self.debug:
            print("\nChecking line: {}".format(line))

        r = True if line.startswith("[") else False

        if self.debug:
            print("  Is definition: {}".format("YES" if r else "no"))

        return r

    def is_blank(self, line):
        line = line.strip()
        if len(line) == 0:
            return True

        return False

    def is_remarked(self,line):
        line = line.strip()
        # Skip lines that are remarked.
        first_char = line[:1]
        if first_char == ';':
            return True

        return False

    # Don't process lines with bad keywords in them.
    def should_skip(self, line):

        if self.is_blank(line):
            return True

        if self.is_remarked(line):
            return True

        if line in self.list_skip:
            if self.debug:
                print("  Skipping this line because it is on the skip list")
            return True

        if self.debug:
            print("  Do not skip this line.")

        return False

    def is_template(self, line):
        # Let's see if it's a template. If it is, we need to grab the server IP for this template.
        if "!" in line:
            # It's a template! Parse the name, and find the server IP for this template
            if self.debug:
                print(" This line is a template.")
            return True

        return False

    def parse_template(self, line, fp):

        # Get the location of "]"
        pos = line.find("]")
        template = line[1:pos]

        if self.debug:
            print("  Template found: {}".format(template))

        while line != "\n":
            if "host" in line.strip():
                buff = line.strip().split("=")
                server_uri = buff[1]
                self.list_servers[template] = server_uri

    def is_phone(self, line):
        """
        This should return True ONLY if the line starts with a ;, which indicates that this is a line with a mac
        and model
        """

        if line[:1] == ';':
            return True

        return False


    def parse_registration(self, line, fp):
        if self.debug:
            print("\n--------------------------------------------------\n")
            print("  Processing: {}".format(line))

        reg = Registration(self.root, self.server)
        if self.debug:
            reg.set_debug()

        reg.parse_extension(line)
        reg.parse_template(line)

        line = next(fp)

        # Aborts if this is not a phone registration
        if not self.is_phone(line):
            return False

        reg.parse_mac_phone(line)

        line = next(fp)

        if not reg.parse_secret(line):
            return False

        self.registrations.append(reg)

        if self.debug:
            print("  Registration added to registrations list: {}".format(reg.extension))
            print("\n--------------------------------------------------\n")

    def parse(self):
        fp = open(self.sip_path)

        for line in fp:
            buff = line.strip()

            if self.should_skip(line):
                continue

            if self.is_template(buff):
                self.parse_template(line, fp)
                continue

            if not self.is_definition(buff):
                continue
            # OK, now we can process because this line should be "good"

            self.parse_registration(line, fp)

    def write_config(self):

        thisConfig = Config(server, site, extension, secret, mac, root)
        # print(thisConfig.extension)
