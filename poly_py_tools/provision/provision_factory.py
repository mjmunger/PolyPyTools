from poly_py_tools.loggable import Loggable
from poly_py_tools.provision.provision_directory import ProvisionDirectory
from poly_py_tools.provision.provision_polycom import ProvisionPolycom
from poly_py_tools.provision.provision_lister import ProvisionLister


class ProvisionFactory(Loggable):

    def __init__(self):
        pass

    def get_runner(self, container):

        args = container['<args>']

        if args['polycom'] and args['<macaddress>']:
            return ProvisionPolycom(container)

        if args['list']:
            if args['endpoints'] is True:
                return ProvisionLister(container)

        if args['directory']:
            return ProvisionDirectory(container)

        raise ValueError("Unable to figure out what processor we need to use for this command.")

