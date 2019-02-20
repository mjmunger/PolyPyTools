import sys
import os
import re
from poly_py_tools.template import Template
from poly_py_tools.registration import Registration
from poly_py_tools.polycom_phone import PolycomPhone
from pprint import pprint
import uuid


class SipConfParser:
    verbosity = 0
    templates = []
    registrations = []
    devices = []
    sip_conf_path = None
    raw_extensions = []
    raw_templates = []

    def __init__(self, sip_conf_path):
        self.sip_conf_path = sip_conf_path

    def log(self, message, minimum_level=1):
        if self.verbosity < minimum_level:
            return True

        print("%s" % message)

    def set_verbosity(self, level):
        self.verbosity = level
        self.log("Verbosity set to: %s" % level)

    def parse(self):

        self.parse_raw()
        self.parse_templates()
        self.parse_registrations()
        self.parse_devices()

        for phone in self.devices:
            phone.sort_registrations()

    def parse_devices(self):
        device_macs = []

        for registration in self.registrations:

            if registration.mac is None:
                continue

            if registration.mac in device_macs:
                continue

            self.log("Found unique mac address: %s" % registration.mac, 2)
            device_macs.append(registration.mac)

        phones = []
        for mac_address in device_macs:
            self.log("Creating Polycom phone with mac address: %s" % mac_address, 2)
            phone = PolycomPhone(mac_address)
            phone.verbosity = self.verbosity
            phones.append(phone)

        self.log("%s phones found." % len(phones))

        for phone in phones:

            self.log("Adding registrations to phone with mac %s..." % phone.mac_address)

            for registration in self.registrations:
                if registration.mac != phone.mac_address:
                    self.log("Trying to match mac %s to this phones mac: %s" % (registration.mac, phone.mac_address), 3)
                    continue

                if registration.mac == phone.mac_address:
                    phone.registrations.append(registration)
                    self.log("Adding registration %s to phone with mac %s" % (registration.name, phone.mac_address), 1)

        for phone in phones:
            self.log("Phone with mac address %s has %s registrations." % (phone.mac_address, len(phone.registrations)), 1)

        self.devices = phones

    def parse_registrations(self):
        for raw_entry in self.raw_extensions:
            template_name = Template.match_template_definition(raw_entry[0])
            if template_name is not False:
                continue

            registration = Registration()
            registration.set_verbosity(self.verbosity)
            template = False

            if registration.implements_template(raw_entry):
                template = registration.implements_template(raw_entry)[1:-1]

            if template is not False:
                self.log("%s template in use" % template, 3)
                registration.template = template
                registration.site = template
                for t in self.templates:
                    if t.name == template:
                        registration.import_template(t)
                        break

            registration.parse_registration(raw_entry)
            self.registrations.append(registration)

    def parse_templates(self):
        for device in self.raw_extensions:
            template_name = Template.match_template_definition(device[0])
            if template_name is not False:
                self.raw_templates.append(device)

        for t in self.raw_templates:
            template = Template()
            template.set_verbosity(self.verbosity)
            template.parse_template(t)
            self.templates.append(template)

    def is_device_definition(self, line):
        message = "Checking %s to see if it's a device entry" % line

        extension_pattern = r"^(\[[a-zA-Z0-9]+?\])(\([a-zA-Z0-9-]+?\)){0,}"

        match = re.search(extension_pattern, line)

        if not match:
            self.log("%s...FALSE" % message, 10)
            return False

        self.log("%s...TRUE" % message, 10)
        self.log("Returing: %s" % match.group(1), 3)
        return match.group(1)

    def is_unwanted(self, raw_registration):

        unwanted_sections = ['general', 'authentication']

        for section in unwanted_sections:
            self.log("Checking to see if %s is in %s" % (section, raw_registration[0]), 3)

            if section in raw_registration[0]:
                return True

        return False

    def remove_unwanted_sections(self):
        #Remove banned extensions.
        buffer = []
        for section in self.raw_extensions:
            if not self.is_unwanted(section):
                buffer.append(section)

        self.raw_extensions = buffer

    def parse_raw(self):
        self.log("Parsing: %s" % self.sip_conf_path, 3)

        f = open(self.sip_conf_path, 'r')
        in_extension = False
        buffer = []

        for line in f:
            line = line.strip()
            self.log("Parsing raw line: " + line, 3)

            definition = self.is_device_definition(line)
            if definition is not False:
                in_extension = True
                #Flush to the raw extensions and start over.
                if len(buffer) > 0:
                    self.log("Flushing definition for %s to the the raw_extensions list" % buffer[0], 3)
                    self.raw_extensions.append(buffer)
                    buffer = []

            if in_extension:
                buffer.append(line)

        f.close()

        # Add the last one if we haven't already.
        if len(buffer) > 0:
            self.raw_extensions.append(buffer)

        self.remove_unwanted_sections()

    def swap_mac(self, mac1, mac2):
        uuid1 = str(uuid.uuid4())
        uuid2 = str(uuid.uuid4())

        f = open(self.sip_conf_path, 'r')
        buffer = f.readlines()
        f.close()

        output = []

        for line in buffer:
            line = line.replace(mac1, uuid2)
            line = line.replace(mac2, uuid1)
            line = line.replace(uuid1, mac1)
            line = line.replace(uuid2, mac2)
            output.append(line)

        f = open(self.sip_conf_path, 'w')
        f.writelines(output)
        f.close()




