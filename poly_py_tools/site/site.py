#!/usr/bin/env python3
"""
Usage: polypy [ options ] site init <site> [<model>]
       polypy [ options ] site flush configs
       polypy [ options ] site setup sntp for <site> --offset=<gmtoffset> [--server=<ntp_server> ]
       polypy [ options ] site setup syslog for <site> [ --server=<syslog_server> ]
       polypy [ options ] site setup nat for <site> --keepalive=<interval> [--ip=<ip>] [ --mediaPortStart=<mediaPortStart> --signalPort=<signalPort> ]
       polypy [ options ] site setup password for <site> to <password>
       polypy [ options ] site setup digitmap for <site> add <pattern>
       polypy [ options ] site setup digitmap for <site> del <pattern>
       polypy [ options ] site setup voipprot for <site> --address=<address> [ --port=<port> ]
       polypy [ options ] site setup vlan for <site> [enable | disable ]
       polypy [ options ] site disable nat for <site>


  Commands:
      setup        Setup a site with basic settings.
      flush        Remove all the configured cfg files (but not the ones from the Config/ directory)
      fill         Copy files from Config/ to the tftproot, which do not yet exist so the configs are complete.
      disable      TBD. Will disable / reset settings to their defaults.

  Options:
    -d,            Debug mode
    -h, --help     Show this help.
    -v, --verbose  Be verbose
    -f, --force    Force the setting.

  Setup settings:
      sntp         Setup the time servers for a given <site>
      syslog       Setup syslog to use remote syslog to the specified server.
      nat          Setup NAT parameters:
                    - Keepalive is required, and you should probably use 30 as a default value.
                    - Only use --ip if you have a static IP address.
                    - Only use --mediaPortStart if the default (20,000) is not available.
                    - Only use --signalPort if ports udp/5060 and tcp/5060 are being blocked by the ISP.
      password     Reset a device password for a given site.
      digitmap     Add / remove digit maps to the phones for auto call initiation based on dial patterns.
      voipprot     Setup VoIP protocol specifications such as the server.
      vlan         Enable or disable vlan (for use with DHCP at a site where phones are on a vlan).

"""
import sys

from docopt import docopt
from poly_py_tools.site.site_factory import SiteFactory


class Site:

    container = None

    def __init__(self, container):
        self.container = container

    def pconf(self):
        return self.container['pconf']

    def run(self):
        factory = SiteFactory()
        runner = factory.create(self.container)
        runner.run()


if __name__ == '__main__':
    container = {}
    args = docopt(__doc__)
    container['<args>'] = args
    site = Site(container)
    site.run()
