from poly_py_tools.polycom_provision import PolycomProvision
from poly_py_tools.provision.provision_lister import ProvisionLister


class ProvisionFactory:

    def __init__(self):
        pass

    def get_runner(self, args):

        if args['polycom'] and args['<macaddress>']:
            return PolycomProvision(args)

        if args['list']:
            if args['templates'] is True or args['endpoints'] is True or args['all'] is True:
                return ProvisionLister(args)
