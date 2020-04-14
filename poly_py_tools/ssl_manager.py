#!/usr/bin/env python3
"""
usage: polypy ssl [ -v ... ] [options] csr <macaddress> <commonname>
       polypy ssl [ -v ... ] [options] cert <macaddress> <certfile>

 Commands:
    csr            Generate a CSR for a phone
    cert           Import a signed certificate into the provisioning file for device with the given mac address.

options:
   -d             Debug mode
   -v             Be verbose
   -h, --help     Help
   -f, --force    Force.

"""

from pprint import pprint
from docopt import docopt
from poly_py_tools.polycom_config import PolycomConfig
from poly_py_tools.polypy_config_finder import ConfigFinder

args = docopt(__doc__)
pprint(args)
config_finder = ConfigFinder()
configs = config_finder.get_configs()

polycom_config = PolycomConfig(configs)

polycom_config.force = args['--force']
polycom_config.set_mac(args['<macaddress>'])

if args['csr']:
    polycom_config.set_cn(args['<commonname>'])
    polycom_config.generate_csr()

if args['cert']:
    polycom_config.set_certfile(args['<certfile>'])
    polycom_config.inject_cert()

print(polycom_config)