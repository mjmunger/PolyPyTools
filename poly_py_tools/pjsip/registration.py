from poly_py_tools.pjsip.resource import SipResource


class Registration(SipResource):
    auth_rejection_permanent = None
    client_uri = None
    contact_user = None
    expiration = None
    max_retries = None
    outbound_auth = None
    outbound_proxy = None
    retry_interval = None
    forbidden_retry_interval = None
    server_uri = None
    transport = None
    type = None
    support_path = None
