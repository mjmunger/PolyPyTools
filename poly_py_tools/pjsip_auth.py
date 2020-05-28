from poly_py_tools.pjsip_resource import SipResource


class Auth(SipResource):
    auth_type = None
    nonce_lifetime = None
    md5_cred = None
    password = None
    realm = None
    type = None
    username = None

