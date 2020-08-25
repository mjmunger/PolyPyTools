from poly_py_tools.pjsip.pjsip_generator import PJSipGenerator


class PJSipFactory:

    def get_runner(self, args):

        print(args)
        if args['<args>']:
            return PJSipGenerator(args)