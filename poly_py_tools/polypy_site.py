#!/usr/bin/env python3
"""
Usage: polypy site [ options ] setup sntp for <site> --offset=<gmtoffset> [--server=<ntp_server> ]
       polypy site [ options ] setup syslog for <site> [ --server=<syslog_server> ]
       polypy site [ options ] setup nat for <site> --ip=<ip> [ --mediaPortStart=<mediaPortStart> --signalPort=<signalPort> ]
       polypy site [ options ] setup password for <site> to <password>
       polypy site [ options ] setup digitmap for <site> add <pattern>
       polypy site [ options ] setup digitmap for <site> del <pattern>
       polypy site [ options ] setup voipprot for <site> --address=<address> [ --port=<port> ]
       polypy site [ options ] configs flush
       polypy site [ options ] configs fill

  Commands:
      setup        Setup a site with basic settings.
      flush        Remove all the configured cfg files (but not the ones from the Config/ directory)

  Options:
    -d,            Debug mode
    -h, --help     Show this help.
    -v, --verbose  Be verbose
    -f, --force    Force the setting.
    -w FILE        Write these site settings to a file FILE.

"""

from pprint import pprint
from docopt import docopt
import sys
import os
import json
from poly_py_tools.polypy_config_finder import ConfigFinder
from poly_py_tools.site_writer import SiteWriter
from shutil import copyfile

args = docopt(__doc__)

if args['-d']:
    print("-----DEBUG MODE-----")
    print(args)

config_finder = ConfigFinder()
configs = config_finder.get_configs()

writer = SiteWriter(configs)
writer.debug_mode = args['-d']
writer.set_site(args['<site>'])

if args['setup'] and args['syslog']:
    writer.syslog_server = "pbx.hph.io" if args['--server'] is None else args['--server']
    writer.setup_syslog()

if args['setup'] and args['sntp']:
    writer.set_gmt_offset(args['--offset'])
    writer.ntp_server = "0.north-america.pool.ntp.org" if args['--server'] is None else args['--server']
    writer.setup_sntp()

if args['setup'] and args['nat']:
    writer.nat_ip = args['--ip']
    writer.nat_media_start_port = "20000" if args['--mediaPortStart'] is None else args['--mediaPortStart']
    writer.nat_signal_port = "5060" if args['--signalPort'] is None else args['--signalPort']
    writer.setup_nat()

if args['setup'] and args['password']:
    writer.setup_local_admin_password(args['<password>'])

if args['setup'] and args['digitmap'] and args['add']:
    writer.add_digitmap(args['<pattern>'])

if args['setup'] and args['digitmap'] and args['del']:
    writer.del_digitmap(args['<pattern>'])

if args['setup'] and args['voipprot']:
    writer.setup_voipprot(args['--address'], "5060" if args['--port'] is None else args['--port'])

if args['configs'] and args['flush']:
    writer.flush_cfgs()

if args['configs'] and args['fill']:
    writer.fill_cfgs()