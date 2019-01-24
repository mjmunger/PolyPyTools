#!/usr/bin/env python3
"""
usage: polypy [options] configure set-path asterisk <path>
       polypy [options] configure set-path tftproot <path>
       polypy [options] configure set-server <server_addr>
       polypy [options] configure show
       polypy [options] configure set-defaults
       polypy [options] configure validate

options:
  -v, --verbose  Be verbose
  -f, --force    Force the setting.

"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json

args = docopt(__doc__)

config_dir = "/etc/polypy/"
config_path = os.path.join(config_dir, "polypy.conf")
configs = None


def write_config(configs):
    f = open(configs['config_path'], 'w')
    f.write(json.JSONEncoder().encode(configs))
    f.close()

    print("Configs saved.")


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

if os.path.exists(config_path):
    f = open(config_path, 'r')
    configs = json.load(f)
    f.close()
    paths = configs['paths']

if args['show']:
    if bool(configs) is False:
        print("PolyPyTools has not been configured. Run polypy configure.")
        sys.exit(1)

    print("Current configuration:")
    print("Asterisk path: %s" % paths['asterisk'])
    print("Tftp root path: %s" % paths['tftproot'])
    print("SIP Server set to: %s" % ("<unset>" if configs['server_addr'] is None else configs['server_addr']))
    sys.exit(1)

if args['set-defaults']:
    # Setup default values:
    lib_path = '/var/lib/polypy'
    config_path = '/etc/polypy/'
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
    configs['server_addr'] = "127.0.0.1"
    write_config(configs)
    sys.exit(1)

if args['set-path']:
    if not args['--force'] and not os.path.exists(args['<path>']):
        print("%s does not exist. Not saving this setting." % args['<path>'])
        sys.exit(1)

    # Setup default values:
    paths["asterisk"] = "/etc/asterisk/"
    paths["tftproot"] = "/srv/tftp/"

    # Overwrite with command values
    if args['asterisk']:
        paths['asterisk'] = args['<path>']

    if args['tftproot']:
        paths['tftproot'] = args['<path>']

    configs['paths'] = paths

    write_config(configs)
    sys.exit(1)

if args['set-server']:
    configs['server_addr'] = args['<server_addr>']
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

    polycom_files = ['000000000000.cfg', '000000000000-directory~.xml', "Config/applications.cfg", "Config/device.cfg",
                     "Config/features.cfg", "Config/H323.cfg", "Config/polycomConfig.xsd", "Config/reg-advanced.cfg",
                     "Config/reg-basic.cfg", "Config/region.cfg", "Config/sip-basic.cfg", "Config/sip-interop.cfg",
                     "Config/site.cfg", "Config/video.cfg", "Config/video-integration.cfg"]

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
