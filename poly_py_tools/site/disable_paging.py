from poly_py_tools.site.manage_paging import ManagePaging


class DisablePaging(ManagePaging):

    def paging_value(self):
        return "0"

