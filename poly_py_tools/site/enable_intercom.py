from poly_py_tools.site.manage_intercom import ManageIntercom


class EnableIntercom(ManageIntercom):

    def alert_value(self):
        return "Auto Answer"

    def message(self):
        print("Intercom enabled for {}.\n\nYou must add SIPAddHeader(Alert-Info: Auto Answer) in your dialplan to use it.".format(self.container['<args>']['<site>']))
