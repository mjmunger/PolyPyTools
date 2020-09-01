from poly_py_tools.site.site_runner import SiteRunner


class SiteConfigurator(SiteRunner):

    container = None

    def __init__(self, container):
        self.container = container

    def run(self):
        """
        1.
        :return:
        """
