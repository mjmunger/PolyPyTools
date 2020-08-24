from poly_py_tools.pjsip.resource import SipResource


class Auth(SipResource):
    auth_type = None
    nonce_lifetime = None
    md5_cred = None
    password = None
    realm = None
    type = None
    username = None

    def render(self):
        section = []
        section.append(self.section)
        section.append("type=auth")
        section.append("auth_type={}".format(self.auth_type))
        section.append("password={}".format(self.password))
        section.append("username={}".format(self.username))
        return "\n".join(section)