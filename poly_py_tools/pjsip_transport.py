from poly_py_tools.pjsip_resource import SipResource


class Transport(SipResource):
    async_operations = None
    bind = None
    ca_list_file = None
    cert_file = None
    cipher = None
    domain = None
    external_media_address = None
    external_signaling_address = None
    external_signaling_port = None
    method = None
    local_net = None
    password = None
    priv_key_file = None
    protocol = None
    require_client_cert = None
    type = None
    verify_client = None
    verify_server = None
    tos = None
    cos = None
    websocket_write_timeout = None