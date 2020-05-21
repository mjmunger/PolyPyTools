#!/usr/bin/env python3
"""
Usage: polypy configure [ -v ... ] [ options ] set-path <name> <path>
       polypy configure [ -v ... ] [ options ] set-server <server_addr>
       polypy configure [ -v ... ] [ options ] show
       polypy configure [ -v ... ] [ options ] set-defaults [here]
       polypy configure [ -v ... ] [ options ] validate
       polypy configure [ -v ... ] [ options ] copy-files <source_path>

  Commands:
      set-path <name> <path>       Set a path in the config file. Possible values: asterisk, tftproot
      set-server <server_addr>     Set the SIP server address.
      show                         Show the current configuration.
      set-defaults [here]          Create a set of default configs and save them at the config path.
      validate                     Validate the configuration.
      copy-files <source_path>     Copies required Polycom files from <source_path> to the tftproot defined in your config.
  Options:
    -d,            Debug mode
    -h, --help     Show this help.
    -v, --verbose  Be verbose
    -f, --force    Force the setting.

"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json
from poly_py_tools.polypy_config import PolypyConfig
from shutil import copyfile

polycom_files = ['000000000000.cfg', '000000000000-directory~.xml', "Config/applications.cfg", "Config/device.cfg",
                     "Config/features.cfg", "Config/H323.cfg", "Config/polycomConfig.xsd", "Config/reg-advanced.cfg",
                     "Config/reg-basic.cfg", "Config/region.cfg", "Config/sip-basic.cfg", "Config/sip-interop.cfg",
                     "Config/site.cfg", "Config/video.cfg", "Config/video-integration.cfg"]

args = docopt(__doc__)

config = PolypyConfig()
config.add_search_path(os.getcwd())
config.add_search_path("/etc/polypy")
if not config.find():
    print("Could not find polypy.conf. Perhaps you need to run set-defaults?")
    print("PolyPyTools has not been configured. Run polypy configure!")
    exit(1)
config.load()

if args['-d']:
    print("Debug: {}".format(__file__))
    print("--------------------------------------------------")
    print(args)
    print("--------------------------------------------------\n")
    print(config)

if args['set-defaults']:
    config_path = os.path.join(os.getcwd(),'polypy.conf')
    config.write_default_config(config_path)
    print("Defaults written to: {}".format(config_path))


if args['show']:
    pprint(config.config)
    sys.exit(0)

if args['set-path']:
    path_name = args['<name>']
    path_path = args['<path>']
    config.set_path(path_name, path_path)
    print("Don't forget to validate this path before you use it. (polypy configure validate) ")
    exit(0)

if args['set-server']:
    server_addr = args['<server_addr>']
    config.set_server(server_addr)

if args['validate']:

    missing_files = []
    paths = configs['paths']

    if not os.path.exists(os.path.join(paths['asterisk'], 'sip.conf')):
        print("Could not find sip.conf. Check the asterisk path and the asterisk installation.")

    if not os.path.exists(os.path.join(paths['tftproot'], 'Config')):
        print(
            'Could not find the blank Config directory for the Polycom configs. Make sure the firmware has been '
            'placed in the tftp root.')

    for file in polycom_files:
        target_path = os.path.join(paths['tftproot'],file)
        if not os.path.exists(target_path):
            missing_files.append(target_path)

    if len(missing_files) > 0:
        print("The following Polycom config files are missing, and must be fixed:")
    for file in missing_files:
        print("  %s" % file)

    if len(missing_files) == 0:
        print("Configuration looks good.")
    sys.exit(1)


if args['copy-files']:
    source_path = args['<source_path>']
    if not os.path.exists(source_path):
        print("Path %s does not exist. Quitting." % source_path)
        exit(1)

    missing_files = []

    for file in polycom_files:
        target_path = os.path.join(source_path, file)
        if not os.path.exists(target_path):
            missing_files.append(target_path)

    if len(missing_files) > 0:
        print("Some required files are missing from {}".format(source_path))
        for file in missing_files:
            print("- {}".format(file))

        exit(1)

    #Copy everything over.

    target_path = os.path.join(os.getcwd(),'tftp')
    target_path = configs['paths']['tftproot']

    if not os.path.exists(target_path):
        os.mkdir(target_path)

    target_config_path = os.path.join(target_path, "Config")
    if not os.path.exists(target_config_path):
        os.mkdir(target_config_path)

    for file in polycom_files:
        source_file = os.path.join(source_path, file)
        target_file = os.path.join(target_path, file)
        print("Copying: {} => {}".format(source_file, target_file))
        copyfile(source_file, target_file)
