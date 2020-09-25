from poly_py_tools.pjsip.resource import SipResource


class Aor(SipResource):
    contact = None
    default_expiration = None
    mailboxes = None
    maximum_expiration = None
    max_contacts = None
    minimum_expiration = None
    remove_existing = None
    type = None
    qualify_frequency = None
    authenticate_qualify = None
    outbound_proxy = None
    support_path = None

    def render(self):
        section = []
        section.append("[{}]".format(self.section_name))
        section.append("type=aor")
        section.append("max_contacts={}".format(self.max_contacts))
        section.append("remove_existing=yes")
        if not self.mailboxes is None:
            section.append("mailboxes={}".format(self.mailboxes))
        return "\n".join(section)
