from docopt import docopt

class Polypy(object):

    args = None

    def __init__(self, args):
        self.args = args

    def run(self):
        argv = [self.args['<command>']] + self.args['<args>']

        if self.args['<command>'] == 'sip':
            from poly_py_tools import sip_manager
            docopt(sip_manager.__doc__, argv=argv)

        if self.args['<command>'] == 'provision':
            from poly_py_tools.provision import provision
            docopt(provision.__doc__, argv=argv)
