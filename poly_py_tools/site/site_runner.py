import os

class SiteRunner:

    container = None

    def __init__(self, container):
        self.container = container

    def site_cfg(self):
        return os.path.join(self.siteroot(), "site.cfg")

    def basic_cfg(self):
        return os.path.join(self.siteroot(), "sip-basic.cfg")

    def siteroot(self):
        if not "<site>" in self.container['<args>']:
            raise ValueError("<site> not set in this command. Cannot render site root.")

        domain = list(self.container['<args>']['<site>'].split("."))
        domain.reverse()
        return os.path.join(self.container['pconf'].tftproot_path(), "-".join(domain))

    def run(self):
        raise NotImplementedError("Run should be implemented in this class")
