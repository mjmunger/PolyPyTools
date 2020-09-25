from poly_py_tools.pjsip.resource import SipResource


class Auth(SipResource):
    auth_type = None
    nonce_lifetime = None
    md5_cred = None
    password = None
    realm = None
    type = None
    username = None
    label = None
    order = None

    def render(self):
        section = []
        section.append("[{}]".format(self.section_name))
        if not self.label is None:
            section.append(";label={}".format(self.label))

        if not self.order is None:
            section.append(";order={}".format(self.order))

        section.append("type=auth")
        section.append("auth_type={}".format(self.auth_type))
        section.append("password={}".format(self.password))
        section.append("username={}".format(self.username))
        return "\n".join(section)
