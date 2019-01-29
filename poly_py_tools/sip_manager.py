#!/usr/bin/env python3
"""
usage: polypy [ -v ... ] [options] sip configure <column_definitions>...
       polypy [ -v ... ] [options] sip generate <extension> from <file> [with voicemail]

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

if args['generate']:

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
    builder.with_config(parser_config)
    builder.from_csv_file(args['<file>'])
    builder.append_device_definitions_to(configs['paths']['asterisk'])
    builder.export_device_definitions(args['<extension>'], (args['with'] and args['voicemail']))
