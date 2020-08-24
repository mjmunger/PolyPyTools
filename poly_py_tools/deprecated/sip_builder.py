import os
import csv
from pwgen_secure.rpg import Rpg
from poly_py_tools.pjsip.registration_old import PJSIPRegistration
from poly_py_tools.registration import Registration


class SipBuilder:
    csv_path = None
    sip_conf_path = None
    voicemail_conf_path = None
    csv_config = {}
    legacy_devices = []
    devices = []
    verbosity = 0
    template = None
    debug_mode = False
    use_column_for_template = False
    template_column = None

    def __str__(self):
        pass

    def set_debug_mode(self, debug_mode):
        if debug_mode:
            self.verbosity = 10
            self.debug_mode = debug_mode

    def set_verbosity(self, verbosity):
        self.verbosity = verbosity

    def set_template(self, assign, template):
        if assign is None or template is None:
            self.log("No template assigned.", 9)
            return False

        if assign == "column":
            self.use_column_for_template = True
            self.template_column = template
            return True

        self.template = template

    def with_config(self, csv_config):
        self.csv_config = csv_config
        self.log(csv_config, 9)

    def log(self, message, minimum_verbosity=1):
        if self.verbosity >= minimum_verbosity:
            print(message)

    def from_csv_file(self, path):
        self.csv_path = path

        self.log("Loading csv file. Start row=%s" % int(self.csv_config.startrow), 3)
        rpg = Rpg("strong", None)

        with open(self.csv_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            counter = 0
            for row in csvreader:
                counter = counter + 1
                self.log("Counter: %s" % counter, 10)
                if counter >= int(self.csv_config.startrow):
                    self.log(row, 10)
                    device = PJSIPRegistration()
                    legacy_device = Registration()
                    if self.debug_mode:
                        device.set_debug_mode()
                    legacy_device.import_csv_row(row, self.csv_config)
                    device.import_csv_row(row, self.csv_config)

                    random_password = rpg.generate_password()


                    if device.password is None:
                        device.password = random_password

                    legacy_device.secret = device.password

                    self.log(device, 10)
                    self.log(legacy_device)
                    self.devices.append(device)
                    self.legacy_devices.append(legacy_device)

    def append_device_definitions_to(self, asterisk_conf_path):
        self.sip_conf_path = os.path.join(asterisk_conf_path, 'sip.conf')
        self.voicemail_conf_path = os.path.join(asterisk_conf_path, 'voicemail.conf')

    def export_device_definitions(self, target_device, with_voicemail=False):
        self.log("Writing config for target device: %s" % target_device, 3)
        for device in self.devices:

            if self.use_column_for_template:
                device.set_template_from_column(self.template_column)
            else:
                device.template = self.template

            self.log("Checking device: %s" % device.name, 10)
            self.log(str(device), 10)
            if target_device == "all" or device.name == target_device:
                if len(device.mac) == 0:
                    continue

                target_path = self.sip_conf_path.replace("sip.conf","pjsip.conf")
                self.log("Target device found (%s). Appending config to %s" % (device.name, target_path), 3)
                f = open(target_path, 'a')
                f.write(device.get_device_definition())
                f.close()

                if with_voicemail:
                    self.log("Adding voicemail definitions to %s" % self.voicemail_conf_path, 3)
                    f = open(self.voicemail_conf_path, 'a')
                    f.write(device.get_voicemail_definition())
                    f.close()

        for device in self.legacy_devices:

            if self.use_column_for_template:
                device.set_template_from_column(self.template_column)
            else:
                device.template = self.template

            self.log("Checking device: %s" % device.name, 10)
            self.log(str(device), 10)
            if target_device == "all" or device.name == target_device:
                if len(device.mac) == 0:
                    continue

                self.log("Target device found (%s). Appending config to %s" % (device.name, self.sip_conf_path), 3)
                f = open(self.sip_conf_path, 'a')
                f.write(device.get_device_definition())
                f.close()

                if with_voicemail:
                    self.log("Adding voicemail definitions to %s" % self.voicemail_conf_path, 3)
                    f = open(self.voicemail_conf_path, 'a')
                    f.write(device.get_voicemail_definition())
                    f.close()
