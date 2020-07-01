from poly_py_tools.pjsip_resource import SipResource


class Endpoint(SipResource):
    rel_100 = None
    aggregate_mwi = None
    allow = None
    aors = None
    auth = None
    callerid = None
    callerid_privacy = None
    callerid_tag = None
    context = None
    direct_media_glare_mitigation = None
    direct_media_method = None
    connected_line_method = None
    direct_media = None
    disable_direct_media_on_nat = None
    disallow = None
    dtmf_mode = None
    media_address = None
    force_rport = None
    ice_support = None
    identify_by = None
    redirect_method = None
    mailboxes = None
    moh_suggest = None
    outbound_auth = None
    outbound_proxy = None
    rewrite_contact = None
    rtp_ipv6 = None
    rtp_symmetric = None
    send_diversion = None
    send_pai = None
    send_rpid = None
    timers_min_se = None
    timers = None
    timers_sess_expires = None
    transport = None
    trust_id_inbound = None
    trust_id_outbound = None
    type = None
    use_ptime = None
    use_avpf = None
    force_avp = None
    media_use_received_transport = None
    media_encryption = None
    inband_progress = None
    call_group = None
    pickup_group = None
    named_call_group = None
    named_pickup_group = None
    device_state_busy_at = None
    t38_udptl = None
    t38_udptl_ec = None
    t38_udptl_maxdatagram = None
    fax_detect = None
    t38_udptl_nat = None
    t38_udptl_ipv6 = None
    tone_zone = None
    language = None
    one_touch_recording = None
    record_on_feature = None
    record_off_feature = None
    rtp_engine = None
    allow_transfer = None
    sdp_owner = None
    sdp_session = None
    tos_audio = None
    tos_video = None
    cos_audio = None
    cos_video = None
    allow_subscribe = None
    sub_min_expiry = None
    from_user = None
    mwi_from_user = None
    from_domain = None
    dtls_verify = None
    dtls_rekey = None
    dtls_cert_file = None
    dtls_private_key = None
    dtls_cipher = None
    dtls_ca_file = None
    dtls_ca_path = None
    dtls_setup = None
    dtls_fingerprint = None
    srtp_tag_32 = None
    set_var = None
    message_context = None
    accountcode = None

    def set_attributes(self):
        self.process_exceptions()
        super().set_attributes()

    def process_exceptions(self):
        exceptions = {"100rel": "rel_100"}

        for exception in exceptions:
            self.section = [x.replace(exception, exceptions[exception]) for x in self.section]

