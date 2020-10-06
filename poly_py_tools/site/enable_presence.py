from poly_py_tools.site.manage_presence import ManagePresence


class EnablePresence(ManagePresence):

    def presence_value(self):
        return "1"
