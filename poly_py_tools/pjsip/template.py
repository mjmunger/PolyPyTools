from poly_py_tools.dialplan_entry import Entry

class Template:

    section = ""
    type = None
    context = None
    allow = None
    direct_media = None
    trust_id_outbound = None
    device_state_busy_at = None
    dtmf_mode = None

    def __init__(self):
        self.section = None
        self.type = "endpoint"
        self.allow = "!all,g722,ulaw"
        self.direct_media = "no"
        self.trust_id_outbound = "yes"
        self.device_state_busy_at = "1"
        self.dtmf_mode = "rfc4733"

    def from_entry(self, entry: Entry):
        site = str(entry.site).split(".")
        site.reverse()
        site = "-".join(site)
        self.section = "[{}](!)".format(site)
        self.context = "{}-local-stations".format(site)

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
        return "\n".join(buffer)

