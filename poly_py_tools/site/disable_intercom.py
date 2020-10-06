from poly_py_tools.site.manage_intercom import ManageIntercom


class DisableIntercom(ManageIntercom):

    def alert_value(self):
        return ""

    def message(self):
        print("Intercom disabled for {}.".format(self.container['<args>']['<site>']))
