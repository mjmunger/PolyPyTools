from typing import Dict

from poly_py_tools.site.site_configurator import SiteConfigurator


class SiteFactory(object):

    def create(self, container : Dict):
        args = container['<args>']

        if args['site']:
            if args['init']:
                return SiteConfigurator(container)

