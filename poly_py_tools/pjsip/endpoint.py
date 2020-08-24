import os

from xml.dom import minidom
from xml.etree import ElementTree

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

    def __init__(self, section):
        self.registrations = []
        self.authorizations = []
        self.addresses = []
        super().__init__(section)

    def use_proxy(self, proxy):
        self.sip_proxy = proxy

    def add_aor(self, aor):
        self.addresses.append(aor)

    def add_registration(self, registration: PolycomRegistration):
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
        my_aor_list = self.aors.split(",")
        my_aor_list = [s.strip() for s in my_aor_list]
        unsorted_aors = []

        for resource in resources:
            if not resource.type == 'aor':
                continue

            if resource.section_name in my_aor_list:
                resource.order = int(resource.order)
                unsorted_aors.append(resource)

        max_index = 0

        for aor in unsorted_aors:
            if aor.order > max_index:
                max_index = aor.order

        first_index = max_index
        for aor in unsorted_aors:
            if aor.order < first_index:
                first_index = aor.order

        for i in range(first_index, max_index+1):
            for aor in unsorted_aors:
                if aor.order == i:
                    self.addresses.append(aor)


    def load_auths(self, resources):
        # my_auth_list = self.auth.split(",")
        # my_auth_list = [s.strip() for s in my_auth_list]
        #
        # for resource in resources:
        #     if not resource.type == 'auth':
        #         continue
        #
        #     if resource.section_name in my_auth_list:
        #         self.authorizations.append(resource)

        if len(self.addresses) == 0:
            raise ValueError("No addresses (AORs) registered for endpoint. Be sure to run load_aors() first.")

        for aor in self.addresses:
            for resource in resources:
                if not resource.type == 'auth':
                    continue
                if resource.section_name == "auth{}".format(aor.section_name):
                    self.authorizations.append(resource)

    def hydrate_registrations(self):
        if len(self.authorizations) != len(self.addresses):
            raise ValueError("Authorization count and address count must be the same.")

        for x in range(0, len(self.authorizations)):
            auth = self.authorizations[x]
            aor = self.addresses[x]

            reg = PolycomRegistration()
            reg.set_sip_server(self.sip_proxy)
            reg.set_aor(aor)
            reg.set_auth(auth)
            reg.hydrate()
            self.registrations.append(reg)

    def basic_cfg_path(self, meta: ModelMeta, tftproot):
        return os.path.join(tftproot, "firmware/{}/Config/reg-basic.cfg".format(meta.get_firmware_version(self.model)))

    def basic_cfg(self, meta: ModelMeta, tftproot):
        xml = ElementTree.ElementTree()
        xml.parse(self.basic_cfg_path(meta, tftproot))
        root = xml.getroot()

        counter = 0
        attribs = {}

        for reg in self.registrations:
            counter = counter + 1

            tag = "reg.{}.address".format(counter)
            attribs[tag] = reg.registration_address

            tag = "reg.{}.auth.password".format(counter)
            attribs[tag] = reg.password

            tag = "reg.{}.auth.userId".format(counter)
            attribs[tag] = reg.auth.username

            tag = "reg.{}.label".format(counter)
            attribs[tag] = reg.label

        reg_node = root.find("reg")
        reg_node.attrib = attribs

        return ElementTree.tostring(root)

    def bootstrap_cfg_path(self, meta: ModelMeta, tftproot):
        return os.path.join(tftproot, "firmware/{}/000000000000.cfg".format(meta.get_firmware_version(self.model)))

    def bootstrap_cfg(self, meta: ModelMeta, tftproot):
        xml = ElementTree.ElementTree()
        xml.parse(self.bootstrap_cfg_path(meta, tftproot))
        root = xml.getroot()
        target_node = "APPLICATION_{}".format(self.model)
        node = root.find(target_node)

        if node is None:
            app_node = ElementTree.Element(target_node)
            root.append(app_node)

        attribs = {}
        attribs["APP_FILE_PATH_{}".format(self.model)] = "firmware/{}/{}.ld".format(meta.get_firmware_version(self.model), meta.get_part(self.model))
        attribs["CONFIG_FILES_{}".format(self.model)] = "{}/{}".format(self.template, self.mac)
        app_node.attrib = attribs

        return ElementTree.tostring(root, encoding="unicode", method='xml')

    def write_bootstrap(self, meta: ModelMeta, tftproot):
        target_file = os.path.join(tftproot, "{}.cfg".format(self.mac))
        element = ElementTree.fromstring(self.bootstrap_cfg(meta, tftproot))
        ET = ElementTree.ElementTree(element)
        ET.write(target_file, encoding="us-ascii", method="xml")

    def write_configs(self, meta: ModelMeta, tftproot):
        target_directory = os.path.join(tftproot, self.template)
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        target_file = os.path.join(target_directory, self.mac)
        element = ElementTree.fromstring(self.basic_cfg(meta, tftproot))
        ET = ElementTree.ElementTree(element)
        ET.write(target_file, encoding="us-ascii", method="xml")

    def render(self):
        buffer = []

        if self.template is None:
            buffer.append(self.section)
        else:
            buffer.append("[{}]({})".format(self.section_name, self.template))

        buffer.append("type=endpoint")
        buffer.append("context={}".format(self.context))
        buffer.append("disallow={}".format(self.disallow))
        buffer.append("allow={}".format(self.allow))
        buffer.append("transport={}".format(self.transport))

        auths=[]
        for auth in self.authorizations:
            auths.append(auth.section_name)

        buffer.append("auth={}".format(",".join(auths)))

        aors=[]
        for aor in self.addresses:
            aors.append(aor.section_name)

        buffer.append("aors={}".format(",".join(aors)))

        buffer.append(";mac={}".format(self.mac))
        buffer.append(";model={}".format(self.model))

        for auth in self.authorizations:
            buffer.append("")
            buffer.append(auth.render())


        for aor in self.addresses:
            buffer.append("")
            buffer.append(aor.render())

        return "\n".join(buffer)
