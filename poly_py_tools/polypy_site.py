#!/usr/bin/env python3
"""
Usage: polypy site [ -v ... ] setup <site>

  Commands:
      setup        Setup a site with basic settings.

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

config_finder = ConfigFinder()
configs = config_finder.get_configs()

print(args)

writer = SiteWriter(configs)

if args['setup'] and args['site']:
    writer.set_site(args['<site>'])
    writer.setup_all()