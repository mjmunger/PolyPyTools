#!/usr/bin/env python3
#!/usr/bin/env python3
"""
usage: polypy [ -v ... ] [options] provision extension <extension>
       polypy [ -v ... ] [options] provision extension all
       polypy [ -v ... ] [options] provision list [ templates | devices | all ]
       polypy [ -v ... ] [options] provision show <extension>
       polypy [ -v ... ] [options] provision clean <extension>
       polypy [ -v ... ] [options] provision swap <extension1> <extension2>
       polypy [ -v ... ] [options] provision password <extension>

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

    if args['devices']:
        for device in parser.devices:
            print(device)

    sys.exit(0)

if args['extension']:
    for device in parser.devices:

        if args['<extension>'] != "all" and device.name != args['<extension>']:
            continue

        device.valid_registration()

        parser.log("Provisioning %s " % device.name, 1)

        config_writer = PolycomConfigWriter()
        config_writer.use(device)
        config_writer.use_configs(configs)
        config_writer.set_path()
        config_writer.write_config()

    sys.exit(0)

if args['show']:
    for device in parser.devices:
        if device.name == args['<extension>']:
            print(device)
            break
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


