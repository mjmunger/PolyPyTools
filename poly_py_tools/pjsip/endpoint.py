import os
from pprint import pprint

from xml.dom import minidom
from xml.etree import ElementTree

from poly_py_tools.pjsip.auth import Auth
from poly_py_tools.pjsip.resource import SipResource
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.polycom_registration import PolycomRegistration


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
    mac = None
    model = None
    template = None
    registrations = [] # This is an alternate shorthand for AORs because AORs are the registrations associated with an endpoint.
    authorizations = [] # Holds Auth objects for this endpoint.
    addresses = [] # Holds aors (Aor records) for this endpoint.
    sip_proxy = None
    extension = None

    def __init__(self, section):
        self.registrations = []
        self.authorizations = []
        self.addresses = []
        self.extension = None
        super().__init__(section)

    def use_proxy(self, proxy):
        self.sip_proxy = proxy

    def add_aor(self, aor):
        self.addresses.append(aor)

    def add_auth(self, auth : Auth):
        if not auth in self.authorizations:
            self.authorizations.append(auth)

    def add_registration(self, registration: PolycomRegistration):
        if registration.label is None:
            registration.label = ""

        self.registrations.append(registration)
        
    def set_attributes(self):
        self.process_exceptions()
        super().set_attributes()
        self.parse_template()

    def parse_template(self):
        for line in self.section:
            if not line.startswith("["):
                continue

            if not "(" in line or ")" not in line:
                continue

            line = str(line)
            start = line.find("(")
            stop = line.find(")")
            self.template = line[start + 1:stop].strip()

    def process_exceptions(self):
        exceptions = {"100rel": "rel_100"}

        for exception in exceptions:
            self.section = [x.replace(exception, exceptions[exception]) for x in self.section]

    def load_aors(self, resources):
        if "," in self.aors:
            my_aor_list = self.aors.split(",")
        else:
            my_aor_list = [self.aors]

        my_aor_list = [s.strip() for s in my_aor_list]

        for resource in resources:
            if not resource.type == 'aor':
                continue

            if not resource.section_name in my_aor_list:
                continue

            self.add_aor(resource)

        #     order = 0
        #     if resource.section_name in my_aor_list:
        #         if resource.order == None:
        #             order = order + 1
        #             resource.order = order
        #
        #         resource.order = int(resource.order)
        #         unsorted_aors.append(resource)
        #
        # max_index = 0

        # for aor in unsorted_aors:
        #     if aor.order > max_index:
        #         max_index = aor.order
        #
        # first_index = max_index
        # for aor in unsorted_aors:
        #     if aor.order < first_index:
        #         first_index = aor.order
        #
        # for i in range(first_index, max_index+1):
        #     for aor in unsorted_aors:
        #         if aor.order == i:
        #             self.addresses.append(aor)


    def load_auths(self, resources):
        if "," in self.auth:
            my_auth_list = self.auth.split(",")
        else:
            my_auth_list = [ self.auth ]

        my_auth_list = [s.strip() for s in my_auth_list]

        for resource in resources:
            if not resource.type == 'auth':
                continue

            if resource.section_name in my_auth_list:
                self.add_auth(resource)

        # if len(self.addresses) == 0:
        #     raise ValueError("No addresses (AORs) registered for endpoint. Be sure to run load_aors() first.")
        #
        # for aor in self.addresses:
        #     for resource in resources:
        #         if not resource.type == 'auth':
        #             continue
        #         if resource.section_name == "auth{}".format(aor.section_name):
        #             self.authorizations.append(resource)

    def hydrate_registrations(self):
        # if len(self.authorizations) != len(self.addresses):
        #     raise ValueError("Authorization count and address count must be the same.")

        for x in range(0, len(self.authorizations)):
            auth = self.authorizations[x]
            aor = self.addresses[x]

            reg = PolycomRegistration()
            reg.set_sip_server(self.sip_proxy)
            reg.set_aor(aor)
            reg.set_auth(auth)
            reg.hydrate()
            self.registrations.append(reg)

    def render(self):
        buffer = []

        if self.template is None:
            buffer.append(self.section)
        else:
            buffer.append("[{}]({})".format(self.section_name, self.template))

        buffer.append(";mac={}".format(self.mac))
        buffer.append(";model={}".format(self.model))
        if self.extension:
            buffer.append(";extension={}".format(self.extension))

        auths=[]
        for auth in self.authorizations:
            auths.append(auth.section_name)

        buffer.append("auth={}".format(",".join(auths)))

        aors=[]
        for aor in self.addresses:
            aors.append(aor.section_name)

        buffer.append("aors={}".format(",".join(aors)))

        if self.callerid:
            buffer.append("callerid={}".format(self.callerid))

        for auth in self.authorizations:
            buffer.append("")
            buffer.append(auth.render())


        for aor in self.addresses:
            buffer.append("")
            buffer.append(aor.render())

        # buffer.append("")

        return "\n".join(buffer)

    def get_label(self):
        """
        For now, we are only returning the label for the first authorization.
        :return:
        """

        auth = self.authorizations[0]
        return auth.label

    def get_auth(self):
        return self.authorizations[0]

    def get_aor(self):
        return self.addresses[0]
