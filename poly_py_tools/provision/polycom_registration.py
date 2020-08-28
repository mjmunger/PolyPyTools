from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.auth import Auth


class PolycomRegistration:

    aor = None
    auth = None
    registration_address = None
    sip_server = None
    password = None
    label = None
    userId = None

    def __init__(self):
        self.aor = None
        self.auth = None
        self.registration_address = None
        self.sip_server = None
        self.password = None
        self.label = ""
        self.userId = None

    def set_label(self, label):
        self.label = label

    def set_aor(self, aor:Aor):
        self.aor = aor

    def set_auth(self, auth:Auth):
        self.auth = auth

    def set_sip_server(self, server):
        self.sip_server = server

    def hydrate(self):
        self.registration_address = "{}@{}".format(self.aor.section_name, self.sip_server)
        self.userId = self.auth.username
        self.password = self.auth.password
        self.label = self.aor.label

    def __str__(self):
        buffer = []
        for attr, value in self.__dict__.items():
            buffer.append("{}: {}".format(attr,value))
        return "\n".join(buffer)
