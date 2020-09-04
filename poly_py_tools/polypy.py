from docopt import docopt

from poly_py_tools.site.site import Site
from poly_py_tools.versionator import Versionator


class Polypy():

    args = None

    def __init__(self, args):
        self.args = args

    def run(self):
        argv = [self.args['<command>']] + self.args['<args>']
        container = {}

        if self.args['<command>'] == 'pjsip':
            from poly_py_tools.pjsip import pjsip
            docopt(pjsip.__doc__, argv=argv)
        elif self.args['<command>'] == 'configure':
            from poly_py_tools import polypy_configure
            docopt(polypy_configure.__doc__, argv=argv)

        elif self.args['<command>'] == 'provision':
            from poly_py_tools.provision import provision
            docopt(provision.__doc__, argv=argv)

        elif self.args['<command>'] == 'site':
            from poly_py_tools.site import site
            container['<args>'] = docopt(site.__doc__, argv=argv)
            site = Site(container)
            site.run()

        elif self.args['<command>'] == 'version':
            Versionator.show_version()
        else:
            print("Command '{}' not recognized. Use polypy --help".format(self.args['<command>']))
            raise SystemExit
