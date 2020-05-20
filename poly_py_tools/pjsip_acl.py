from poly_py_tools.pjsip_resource import SipResource


class Acl(SipResource):
    acl = None
    contact_acl = None
    contact_deny = None
    contact_permit = None
    deny = None
    permit = None