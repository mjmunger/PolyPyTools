import os
import csv
from pwgen_secure.rpg import Rpg
from poly_py_tools.registration import Registration


class SipBuilder:

    csv_path = None
    sip_conf_path = None
    voicemail_conf_path = None
    csv_config = {}
    devices = []
    verbosity = 0

    def __str__(self):
        pass

    def set_verbosity(self, verbosity):
        self.verbosity = verbosity

    def with_config(self, csv_config):
        self.csv_config = csv_config
        self.log(csv_config, 10)

    def log(self, message, minimum_verbosity=1):
        if self.verbosity >= minimum_verbosity:
            print(message)

    def from_csv_file(self, path):
        self.csv_path = path

        self.log("Loading csv file. Start row=%s" % int(self.csv_config.startrow), 3)

        with open(self.csv_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            counter = 0
            for row in csvreader:
                counter = counter + 1
                self.log("Counter: %s" % counter, 10)
                if counter >= int(self.csv_config.startrow):
                    self.log(row, 10)
                    device = Registration()
                    device.import_csv_row(row, self.csv_config)
                    if device.secret is None:
                        rpg = Rpg("strong", None)
                        device.secret = rpg.generate_password()
                    self.log(device, 10)
                    self.devices.append(device)

    def append_device_definitions_to(self, asterisk_conf_path):
        self.sip_conf_path = os.path.join(asterisk_conf_path, 'sip.conf')
        self.voicemail_conf_path = os.path.join(asterisk_conf_path, 'voicemail.conf')

    def export_device_definitions(self, target_device, with_voicemail=False):
        self.log("Writing config for target device: %s" % target_device, 3)
        for device in self.devices:
            self.log("Checking device: %s" % device.name, 10)
            if target_device == "all" or device.name == target_device:
                self.log("Target device found (%s). Appending config to %s" % (device.name, self.sip_conf_path), 3)
                f = open(self.sip_conf_path, 'a')
                f.write(device.get_device_definition())
                f.close

                if with_voicemail:
                    self.log("Adding voicemail definitions to %s" % self.voicemail_conf_path, 3)
                    f = open(self.voicemail_conf_path, 'a')
                    f.write(device.get_voicemail_definition())
                    f.close()