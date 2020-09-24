from poly_py_tools.pjsip.pjsip_generator import PJSipGenerator
from poly_py_tools.pjsip.pjsip_column_mapper import PjSipColumnMapper


class PJSipFactory:

    def get_runner(self, args):

        if args['generate']:
            return PJSipGenerator(args)

        if args['guess']:
            return PjSipColumnMapper(args)
