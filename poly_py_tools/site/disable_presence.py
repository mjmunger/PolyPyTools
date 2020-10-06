from poly_py_tools.site.manage_presence import ManagePresence


class DisablePresence(ManagePresence):

    def presence_value(self):
        return "0"
