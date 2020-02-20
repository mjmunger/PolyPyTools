#!/usr/bin/env python3
"""
usage: polypy provision [ -v ... ] [options] polycom <macaddress>
       polypy provision [ -v ... ] [options] list [ templates | devices | all ]
       polypy provision [ -v ... ] [options] show-extension <extension>
       polypy provision [ -v ... ] [options] show-mac <macaddress>
       polypy provision [ -v ... ] [options] clean <macaddress>
       polypy provision [ -v ... ] [options] swap <phonemac1> <phonemac2>
       polypy provision [ -v ... ] [options] passwords audit [ failures-only | passing-only ]
       polypy provision [ -v ... ] [options] passwords reset <extension>

options:
  -d  --debug    Debug mode
  -f, --force    Force the setting.
  -v             Be verbose

"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json
from poly_py_tools.sip_parser import SipConfParser
from poly_py_tools.polycom_config_writer import PolycomConfigWriter
from poly_py_tools.pw_strength_calculator import PasswordStrengthCalculator
from poly_py_tools.polypy_config_finder import ConfigFinder

args = docopt(__doc__)
debug_mode = False

if args['-d']:
    debug_mode = True
    print("Debug mode on. Debugging {}".format(__file__))
    print("--------------------------------------------------")
    print(args)
    print("--------------------------------------------------")

config_finder = ConfigFinder()
configs = config_finder.get_configs()

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
            if device is None:
                continue
            print(device)
        print("%s devices provisioned." % len(parser.devices))

    sys.exit(0)

if args['show-extension']:
    for device in parser.devices:
        for registration in device.registrations:
            if registration.extension == args['<extension>']:
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

        if args['<macaddress>'] != "all" and device.mac_address != args['<macaddress>']:
            continue

        if debug_mode:
            print("Cleaning: {}".format(device.mac_address))
            print(device)

        config_writer = PolycomConfigWriter()
        config_writer.set_debug_mode(debug_mode)
        config_writer.use(device)
        config_writer.use_configs(configs)
        config_writer.set_path()
        config_writer.remove()

    sys.exit(0)

if args['swap']:
    device1 = None
    device2 = None

    for device in parser.devices:
        if device.mac_address == args['<phonemac1>']:
            device1 = device

        if device.mac_address == args['<phonemac2>']:
            device2 = device

    mac1 = device1.mac_address
    mac2 = device2.mac_address

    device1.mac_address = mac2
    device2.mac_address = mac1

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

    print("Swap: {} <=> {} complete.".format(mac1, mac2))
    sys.exit(0)

if args['audit']:
    f = open(os.path.join(configs['lib_path'], "10k-most-common.txt"))
    passwords = f.read().splitlines()
    f.close()

    results = {}

    for device in parser.devices:
        pass_fail = False
        for registration in device.registrations:
            for password in passwords:
                if registration.secret == password:
                    results[registration.mac] = "Secret is in top 10k. Must be changed!"
                    pass_fail = True
                    break;
            if pass_fail:
                continue

        Calc = PasswordStrengthCalculator(registration.secret)
        Calc.verbosity = parser.verbosity
        results[registration.name] = "Passed" if Calc.evaluate() else "FAILED"

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




