from docopt import docopt


class Polypy():

    args = None

    def __init__(self, args):
        self.args = args

    def run(self):
        argv = [self.args['<command>']] + self.args['<args>']

        if self.args['<command>'] == 'pjsip':
            from poly_py_tools.pjsip import pjsip
            docopt(pjsip.__doc__, argv=argv)

        if self.args['<command>'] == 'provision':
            from poly_py_tools.provision import provision
            docopt(provision.__doc__, argv=argv)

        if self.args['<command>'] == 'site':
            from poly_py_tools import polypy_site
            docopt(polypy_site.__doc__, argv=argv)
