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
from poly_py_tools.polypy_config_finder import ConfigFinder
from shutil import copyfile

polycom_files = ['000000000000.cfg', '000000000000-directory~.xml', "Config/applications.cfg", "Config/device.cfg",
                     "Config/features.cfg", "Config/H323.cfg", "Config/polycomConfig.xsd", "Config/reg-advanced.cfg",
                     "Config/reg-basic.cfg", "Config/region.cfg", "Config/sip-basic.cfg", "Config/sip-interop.cfg",
                     "Config/site.cfg", "Config/video.cfg", "Config/video-integration.cfg"]

args = docopt(__doc__)

config_finder = ConfigFinder()
configs = config_finder.get_configs()

if args['-d']:
    print("Debug: {}".format(__file__))
    print("--------------------------------------------------")
    print(args)
    print("--------------------------------------------------\n")
    print(config_finder)


def write_config(configs):
    try:
        f = open(configs['config_path'], 'w')
    except PermissionError:
        print("ERROR: I do not have permission to write to {}. I could not do anything. Check permissions and try again.".format(configs['config_path']))
        exit(1)

    f.write(json.JSONEncoder().encode(configs))
    f.close()

    print("Configs saved.")


def write_default_configs(config_path):
    # Setup default values:
    lib_path = '/var/lib/polypy'
    share_path = '/usr/share/polypy/'
    local_bin = '/usr/local/bin/'
    package_path = None

    paths = {}

    for path in sys.path:
        if '/usr/local/lib' in path:
            package_path = os.path.join(path, "poly_py_tools")

    paths["asterisk"] = "/etc/asterisk/"
    paths["tftproot"] = "/srv/tftp/"
    configs['lib_path'] = lib_path
    configs['share_path'] = share_path
    configs['config_path'] = os.path.join(config_path, 'polypy.conf')
    configs['package_path'] = package_path
    configs['paths'] = paths
    configs['server_addr'] = "126.0.0.1"
    write_config(configs)
    sys.exit(0)


config_dir = config_finder.get_config_dir()

if args['set-defaults']:
    if args['<args>'][0] == 'here':
        config_path = os.getcwd()
    else:
        config_path = config_finder.get_config_dir()

    write_default_configs(config_path)
    print("Defaults written to: {1}" % config_path)

if not config_finder.is_local:
    if os.getegid() != 0:
        print("You must run this as root. Cannot continue")
        sys.exit(1)

if not os.path.exists(config_dir):
    try:
        os.mkdir(config_dir)
    except Exception:
        print("Could not create %s. Configuration cannot continue." % config_dir)
        sys.exit(1)

configs = {}
paths = {}

# Overwrite it with the saved settings if they exist.

configs = config_finder.get_configs()

if args['show']:
    if bool(configs) is False:
        print("PolyPyTools has not been configured. Run polypy configure!")
        sys.exit(1)

    paths = configs['paths']

    print("Current configuration:")
    print("Configuration file: %s" % configs['config_path'])
    print("Asterisk path: %s" % paths['asterisk'])
    print("Tftp root path: %s" % paths['tftproot'])
    print("SIP Server set to: %s" % ("<unset>" if configs['server_addr'] is None else configs['server_addr']))
    sys.exit(1)

# if args['<command>'] == 'set-defaults':
#     if not args['--force'] and not os.path.exists(args['<path>']):
#         print("%s does not exist. Not saving this setting." % args['<path>'])
#         sys.exit(1)
#
#     # Setup default values:
#     paths["asterisk"] = "/etc/asterisk/"
#     paths["tftproot"] = "/srv/tftp/"
#
#     # Overwrite with command values
#     if args['asterisk']:
#         paths['asterisk'] = args['<path>']
#
#     if args['tftproot']:
#         paths['tftproot'] = args['<path>']
#
#     configs['paths'] = paths
#
#     write_config(configs)
#     sys.exit(1)

if args['set-path']:
    path_name = args['<args>'][0]
    path_path = args['<args>'][1]
    if not path_name in configs['paths']:
        print("%s is not a path in settings. Not setting anything." % path_name)
        exit(1)

    if path_path.startswith("."):
        path_path = os.path.join(os.getcwd(), path_path[2:])

    if not os.path.exists(path_path):
        print("%s does not exist. If  you are trying to use a relvant path, did you for get to write it as: ./mydirectory ?" % path_path)
        exit(1)

    configs['paths'][path_name] = path_path
    write_config(configs)
    print("%s set to %s" % (path_name, path_path))
    print("Don't forget to validate this path before you use it. (polypy configure validate) ")
    exit(1)

if args['set-server']:
    server_addr = args['<args>'][0]
    configs['server_addr'] = server_addr
    write_config(configs)

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

    source_path = args['<args>'][0]
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
