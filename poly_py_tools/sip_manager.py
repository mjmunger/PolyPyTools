#!/usr/bin/env python3
"""
usage: polypy [ -v ... ] [options] sip configure <column_definitions>...
       polypy [ -v ... ] [options] sip generate <extension> from <file> [assign <template>] [with voicemail]
       polypy [ -v ... ] [options] sip dump

 sip commands:
    configure      Create a configuration file that is used to read your CSV data source.
    generate       Generate one or more sip.conf device definitions from your CSV data source.

    column definitions for the configure command:
    first=<first>            The column which contains first name of this user.
    last=<last>              The column which contains last name of this user.
    exten=<exten>            The column which contains the extension of this user.
    vm=<vm>                  The column which contains the voicemail mailbox of this user.
    mac=<mac>                The column which contains the mac address of the phone for this user.
    email=<email>            The column which contains email address of this user.
    device=<device>          The column which contains the model of the phone for this user.
    cid_number=<cid_number>  The caller ID number that should be used for this user.
    startrow=<startrow>      The row in the csv file that we should start processing. (Ignore rows before this row).

    Columns may be defined numerically or using A-Z.

options:
   -v             Be verbose
   -h, --help     Help
   -f, --force    Force the setting.
 
"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json
from poly_py_tools.sip_parser import SipConfParser
from poly_py_tools.pw_strength_calculator import PasswordStrengthCalculator
from poly_py_tools.csv_parser_config import CSVParserConfig
from poly_py_tools.sip_builder import SipBuilder

args = docopt(__doc__)

config_dir = "/etc/polypy/"
config_path = os.path.join(config_dir, "polypy.conf")
f = open(config_path, 'r')
configs = json.load(f)

if args['configure']:
    parser_config = CSVParserConfig()
    if os.path.exists('csv_columns.map'):
        parser_config.load('csv_columns.map')
    parser_config.import_column_defs(args['<column_definitions>'])
    parser_config.save()
    sys.exit(1)

if args['dump']:
    print("Dumping sip.conf entries...")
    sip_conf_path = os.path.join(configs['paths']['asterisk'], 'sip.conf')
    parser = SipConfParser(sip_conf_path)
    parser.set_verbosity(args['-v'])
    parser.parse()

    if args['-v'] >= 3:
        print("%s raw devices found." % len(parser.raw_extensions))

    c1 = len("device")
    c2 = len("template")
    c3 = len("name")
    c4 = len("type")
    c5 = len("host")
    c6 = len("context")
    c7 = len("mac")
    c8 = len("model")
    c9 = len("mailbox")

    for device in parser.devices:
        c1 = len(device.device_type) if len(device.device_type) > c1 else c1
        c2 = len(device.template) if len(device.template) > c2 else c2
        c3 = len(device.name) if len(device.name) > c3 else c3
        c4 = len(device.type) if len(device.type) > c4 else c4
        c5 = len(device.host) if len(device.host) > c5 else c5
        c6 = len(device.context) if len(device.context) > c6 else c6
        c7 = len(device.mac) if len(device.mac) > c7 else c7
        c8 = len(device.model) if len(device.model) > c8 else c8
        c9 = len(device.mailbox) if len(device.mailbox) > c9 else c9

    c1 = c1 + 2
    c2 = c2 + 2
    c3 = c3 + 2
    c4 = c4 + 2
    c5 = c5 + 2
    c6 = c6 + 2
    c7 = c7 + 2
    c8 = c8 + 2
    c9 = c9 + 2

    print("%s%s%s%s%s%s%s%s%s" % ("device".ljust(c1),
                                  "template".ljust(c2),
                                  "name".ljust(c3),
                                  "type".ljust(c4),
                                  "host".ljust(c5),
                                  "context".ljust(c6),
                                  "mac".ljust(c7),
                                  "model".ljust(c8),
                                  "mailbox".ljust(c9)))

    for device in parser.devices:
        print("%s%s%s%s%s%s%s%s%s" %
              (device.device_type.ljust(c1),
              device.template.ljust(c2),
              device.name.ljust(c3),
              device.type.ljust(c4),
              device.host.ljust(c5),
              device.context.ljust(c6),
              device.mac.ljust(c7),
              device.model.ljust(c8),
              device.mailbox.ljust(c9)))

    print("%s devices found." % len(parser.devices))

if args['generate']:

    if not os.path.exists(args['<file>']):
        print("%s does not exist. Check your file and try again." % args['<file>'])
        sys.exit(1)

    if os.getegid() != 0:
        print("You must run this as root. Cannot continue")
        sys.exit(1)

    parser_config = CSVParserConfig()

    if os.path.exists('csv_columns.map'):
        parser_config.load('csv_columns.map')
    else:
        parser_config.import_column_defs(args['<column_definitions>'])

    builder = SipBuilder()
    builder.set_verbosity(args['-v'])
    builder.set_template(args['assign'], args['<template>'])
    builder.with_config(parser_config)
    builder.from_csv_file(args['<file>'])
    builder.append_device_definitions_to(configs['paths']['asterisk'])
    builder.export_device_definitions(args['<extension>'], (args['with'] and args['voicemail']))
