import re
import sys
from pprint import pprint


class PJSIPRegistration:
    name = None

    verbosity = 0
    debug_mode = False
    extension = None
    row = None
    csv_config = None
    column_letters = None

    # pjsip directives
    disallow = []
    allow = []

    aors = None
    auth = None
    context = None
    device_state_busy_at = None
    direct_media = None
    dtmf_mode = None
    max_contacts = 1
    password = None
    trust_id_outbound = None
    type = None
    username = None

    # Non-asterisk directives

    mac = None
    model = None
    site = None
    template = None
    email = None
    first_name = None
    last_name = None
    label = None
    order = None

    def __init__(self):
        self.type = "endpoint"
        self.order = 0
        if not "ulaw" in self.allow:
            self.allow.append("ulaw")

        self.column_letters = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()

    def set_verbosity(self, level):
        self.verbosity = level

    def set_debug_mode(self):
        self.debug_mode = True
        self.verbosity = 10

    def log(self, message, minimum_level=1):
        if self.verbosity < minimum_level:
            return True

        print("%s", message)

    def __str__(self):
        return self.get_device_definition()

    @staticmethod
    def implements_template(raw_device):
        template_pattern = r"^(\[[a-zA-Z0-9]+?\])(\([a-zA-Z0-9-]+?\){1})"

        match = re.search(template_pattern, raw_device[0])
        if match:
            return match.group(2).strip()
        return False

    def parse_registration(self, raw_entry):

        if self.type == "endpoint":
            pattern = r"^(\[[a-zA-Z0-9]+?\])(\([a-zA-Z0-9-]+?\)){0,}$"
            match = re.match(pattern, raw_entry[0])
            self.name = match.group(1)[1:-1]

        for line in raw_entry:
            line = line.strip()
            if "=" not in line:
                continue

            buff = line.split("=")
            if buff[0] == "allow":
                self.allow.append(buff[1])
                continue

            if buff[0] == "disallow":
                self.disallow.append(buff[1])
                continue

            directive = buff[0]
            if(directive[:1]) == ";":
                directive = directive[1:]

            value = buff[1]
            # remove comments
            if ";" in value:
                value = value.split(";")[0].strip()

            self.log("Setting registration attribute %s to %s" % (directive, value), 3)
            setattr(self, directive, value)

    def import_template(self, template):
        raise Exception("Template imports not implemented yet")

    def import_csv_row(self, row, csv_config):

        self.row = row
        self.csv_config = csv_config

        if self.debug_mode:
            print("CSV Configuration:")
            print(csv_config)
            print("Importing this row for parsing: ")
            print(row)

        try:
            self.extension = row[csv_config.extension_column]
            self.name = self.extension
            self.aors = self.extension

        except IndexError:
            print("The target csv file (%s) does not appear to have %s columns. Re-run polypy sip configure and check "
                  "your file.")
            sys.exit(1)

        try:
            self.username = str(row[csv_config.mac_column]).lower().strip()
            self.log("I think the mac is in column {} and is [{}]".format(csv_config.mac_column, self.name), 9)
        except IndexError:
            print("The target csv file (%s) does not appear to have %s columns. Re-run polypy sip configure and check "
                  "your file.")
            sys.exit(1)

        try:
            self.mac = str(row[csv_config.mac_column]).lower().strip()
        except IndexError:
            print("The target csv file (%s) does not appear to have %s columns. Re-run polypy sip configure and check "
                  "your file.")
            sys.exit(1)

        try:
            self.first_name = str(row[csv_config.first_name_column]).strip()
        except IndexError:
            print("The target csv file (%s) does not appear to have %s columns. Re-run polypy sip configure and check "
                  "your file.")

        try:
            self.last_name = str(row[csv_config.last_name_column]).strip()
        except IndexError:
            print("The target csv file (%s) does not appear to have %s columns. Re-run polypy sip configure and check "
                  "your file.")

        try:
            self.callerid = '"%s %s" <%s>' % (self.first_name.title(),
                                              self.last_name.title(),
                                              row[csv_config.cid_number])
        except IndexError:
            print("The target csv file (%s) does not appear to have %s columns. Re-run polypy sip configure and check "
                  "your file.")
            sys.exit(1)

        if csv_config.voicemail_column is not None:
            self.mailbox = row[csv_config.voicemail_column]

        if csv_config.device_column is not None:
            self.model = row[csv_config.device_column]

        if csv_config.email_column is not None:
            self.email = row[csv_config.email_column]

    def set_template_from_column(self, column):
        try:
            self.template = str(self.row[self.column_letters.index(column)]).replace(" ", "-").lower()
        except ValueError:
            print("Tried to set the template using column {}, but it seems the row doesn't have that value?".format(column))
            print("Quitting.")
            exit(1)

    def get_device_definition(self):
        lines = []
        lines.append("\n")

        if self.template is None:
            lines.append("[%s]" % self.name)
        else:
            lines.append("[%s](%s)" % (self.name, self.template))

        lines.append(";mac=%s" % self.mac)
        lines.append(";model=%s" % self.model)
        lines.append(";extension=%s" % self.extension)
        lines.append("type={}".format(self.type))
        lines.append("disallow={}".format("all"))
        lines.append("allow={}".format(" ".join(self.allow)))
        lines.append("auth={}".format("auth{}".format(self.name)))
        lines.append("aors={}".format(self.aors))
        lines.append("callerid=%s" % self.callerid)
        lines.append("")
        lines.append("[{}]({}-single-reg)".format(self.extension,self.template))
        lines.append("mailboxes=%s" % self.mailbox)
        lines.append("")
        lines.append("[auth{}]".format(self.extension))
        lines.append("type=auth")
        lines.append("auth_type=userpass")
        lines.append("password={}".format(self.password))
        lines.append("username={}".format(str(self.username).lower()))
        buffer = "\n".join(lines)

        if self.debug_mode:
            self.log("-------------------Device definition---------------------")
            self.log(buffer)
            self.log("------------------End Device definition------------------")
        return buffer

    def get_voicemail_definition(self):

        components = []
        components.append("%s => 1234" % self.extension)
        if len(self.first_name.strip()) > 0 and len(self.last_name.strip()) > 0:
            components.append("%s %s" % (self.first_name, self.last_name))

        if len(self.email.strip()) > 0:
            components.append(self.email)

        line = ",".join(components)

        lines = []
        lines.append("\n")
        lines.append(line)
        buffer = "\n".join(lines)
        return buffer
