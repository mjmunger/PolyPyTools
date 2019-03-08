#!/usr/bin/env python3
"""
usage: polypy [ -v ... ] [options] provision polycom <macaddress>
       polypy [ -v ... ] [options] provision list [ templates | devices | all ]
       polypy [ -v ... ] [options] provision show-extension <extension>
       polypy [ -v ... ] [options] provision show-mac <macaddress>
       polypy [ -v ... ] [options] provision clean <macaddress>
       polypy [ -v ... ] [options] provision swap <phone1> <phone2>
       polypy [ -v ... ] [options] provision passwords audit [ failures-only | passing-only ]
       polypy [ -v ... ] [options] provision passwords reset <extension>

options:
  -v             Be verbose
  -f, --force    Force the setting.

"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json
from poly_py_tools.sip_parser import SipConfParser
from poly_py_tools.polycom_config_writer import PolycomConfigWriter
from poly_py_tools.pw_strength_calculator import PasswordStrengthCalculator

args = docopt(__doc__)

config_dir = "/etc/polypy/"
config_path = os.path.join(config_dir, "polypy.conf")
configs = None

if not os.path.exists(config_path):
    print("PolyPy has not been configured. Run polypy configure")
    sys.exit(1)


f = open(config_path, 'r')
configs = json.load(f)
f.close()
paths = configs['paths']

parser = SipConfParser(os.path.join(paths['asterisk'], 'sip.conf'))
if args['-v'] > 0:
    parser.set_verbosity(args['-v'])
parser.parse()

if args['list']:

    if args['all']:
        args['templates'] = True
        args['devices'] = True

    if args['templates']:
        for template in parser.templates:
            print(template)
        print("%s templates provisioned." % len(parser.templates))

    if args['devices']:
        for device in parser.devices:
            print(device)
        print("%s devices provisioned." % len(parser.devices))

    sys.exit(0)

if args['show-extension']:
    for device in parser.devices:
        for registration in device.registrations:
            if registration.name == args['<extension>']:
                print(registration)
                break
    sys.exit(0)

if args['show-mac']:
    for device in parser.devices:
        for registration in device.registrations:
            if registration.mac == args['<macaddress>']:
                print(registration)
    sys.exit(0)

if args['polycom']:
    target_macaddress = str(args['<macaddress>']).lower()
    count = 0
    for phone in parser.devices:
        if not phone.type == "Polycom":
            continue

        if target_macaddress != "all" and phone.mac_address != target_macaddress:
            continue

        count = count + 1

        parser.log("Provisioning Polycom phone with mac %s " % phone.mac_address, 1)

        config_writer = PolycomConfigWriter()
        config_writer.set_verbosity(args['-v'])
        config_writer.use(phone)
        config_writer.use_configs(configs)
        config_writer.set_path()
        config_writer.write_config()

    print("Provisioned %s devices" % count)
    # if args['<macaddress>'] != "all" and count > 1:
    #     print("WARNING: Two devices were provisioned for extension %s. \n"
    #           "This will likely cause problems where only the last config loaded will be active. \n"
    #           "The other phone will either not get provisioned, or not gain access to Asterisk." % args['<extension>'])
    sys.exit(0)

if args['clean']:
    for device in parser.devices:

        if args['<extension>'] != "all" and device.name != args['<extension>']:
            continue

        config_writer = PolycomConfigWriter()
        config_writer.use(device)
        config_writer.use_configs(configs)
        config_writer.set_path()
        config_writer.remove()

    sys.exit(0)

if args['swap']:
    device1 = None
    device2 = None

    for device in parser.devices:
        if device.name == args['<extension1>']:
            device1 = device

        if device.name == args['<extension2>']:
            device2 = device

    mac1 = device1.mac
    mac2 = device2.mac

    device1.mac = mac2
    device2.mac = mac1

    config_writer = PolycomConfigWriter()
    config_writer.use(device1)
    config_writer.use_configs(configs)
    config_writer.set_path()
    config_writer.write_config()

    config_writer = PolycomConfigWriter()
    config_writer.use(device2)
    config_writer.use_configs(configs)
    config_writer.set_path()
    config_writer.write_config()

    parser.swap_mac(mac1, mac2)

    sys.exit(0)

if args['audit']:
    f = open(os.path.join(configs['lib_path'], "10k-most-common.txt"))
    passwords = f.read().splitlines()
    f.close()

    results = {}

    for device in parser.devices:
        pass_fail = False
        for password in passwords:
            if device.secret == password:
                results[device.name] = "Secret is in top 10k. Must be changed!"
                pass_fail = True
                break;
        if pass_fail:
            continue

        Calc = PasswordStrengthCalculator(device.secret)
        Calc.verbosity = parser.verbosity
        results[device.name] = "Passed" if Calc.evaluate() else "FAILED"

    failed = 0
    passed = 0

    for name, result in results.items():
        if result == "FAILED":
            failed = failed + 1

        if result == "Passed":
            passed = passed + 1

        if args['failures-only'] and result is not "FAILED":
            continue

        if args['passing-only'] and result is not "Passed":
            continue

        print("Device: %s => %s" % (name, result))

    print("%s total devices found, %s passed and %s failed." % (len(results), passed, failed))




