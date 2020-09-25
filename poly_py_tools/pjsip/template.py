from poly_py_tools.dialplan_entry import Entry
from poly_py_tools.pjsip.endpoint import Endpoint


class Template:

    section = ""
    type = None
    context = None
    allow = None
    direct_media = None
    trust_id_outbound = None
    device_state_busy_at = None
    dtmf_mode = None
    force_rport = None
    rewrite_contact = None
    name = None

    def __init__(self):
        self.section = None
        self.type = "endpoint"
        self.allow = "!all,g722,ulaw"
        self.direct_media = "no"
        self.trust_id_outbound = "yes"
        self.device_state_busy_at = "1"
        self.dtmf_mode = "rfc4733"
        self.force_rport = "yes"
        self.rewrite_contact = "yes"
        self.name = None

    def from_entry(self, entry: Entry):
        site = str(entry.site).split(".")
        site.reverse()
        site = "-".join(site)
        self.name = site
        self.section = "[{}](!)".format(site)
        self.context = "{}-local-stations".format(site)

    def from_endpoint(self, endpoint: Endpoint):
        self.section = "[{}](!)".format(endpoint.section_name)
        self.context = endpoint.context
        self.name = endpoint.section_name

    def __str__(self):
        buffer = []
        buffer.append(self.section)
        buffer.append("type = {}".format(self.type))
        buffer.append("context = {}".format(self.context))
        buffer.append("allow = {}".format(self.allow))
        buffer.append("direct_media = {}".format(self.direct_media))
        buffer.append("trust_id_outbound = {}".format(self.trust_id_outbound))
        buffer.append("device_state_busy_at = {}".format(self.device_state_busy_at))
        buffer.append("dtmf_mode = {}".format(self.dtmf_mode))
        buffer.append("force_rport = {}".format(self.force_rport))
        buffer.append("rewrite_contact = {}".format(self.rewrite_contact))
        return "\n".join(buffer)

