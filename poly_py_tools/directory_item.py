class DirectoryItem:
    model = None
    last_name = None
    first_name = None
    contact = None
    speed_dial = None
    protocol = None
    label = None
    ring_tone = None
    divert_contact = None
    auto_divert = None
    auto_reject = None
    buddy_watch = None
    buddy_block = None

    def __init__(self, model, last_name, first_name, contact, label, protocol, ring_tone, divert_contact,
                 auto_divert, auto_reject, buddy_watch, buddy_block):

        self.model = model
        self.last_name = last_name
        self.first_name = first_name
        self.contact = contact
        self.label = label
        self.protocol = protocol
        self.ring_tone = ring_tone
        self.divert_contact = divert_contact
        self.auto_divert = auto_divert
        self.auto_reject = auto_reject
        self.buddy_watch = buddy_watch
        self.buddy_block = buddy_block

    def render(self):
        buffer = []

        buffer.append("<ln>{}</ln>".format(self.last_name))
        buffer.append("<fn>{}</fn>".format(self.first_name))
        buffer.append("<ct>{}</ct>".format(self.contact))
        buffer.append("<sd>{}</sd>".format(self.speed_dial))
        buffer.append("<lb>{}</lb>".format(self.label))

        if self.model_uses_protocol():
            buffer.append("<pt>{}</pt>".format(self.protocol))

        buffer.append("<rt>{}</rt>".format(self.ring_tone))
        buffer.append("<dc>{}</dc>".format(self.divert_contact))
        buffer.append("<ad>{}</ad>".format(self.auto_divert))
        buffer.append("<ar>{}</ar>".format(self.auto_reject))
        buffer.append("<bw>{}</bw>".format(self.buddy_watch))
        buffer.append("<bb>{}</bb>".format(self.buddy_block))

        buffer = ["      {0}".format(i) for i in buffer]
        buffer.insert(0, "    <item>")
        buffer.append("    </item>")

        return "\n".join(buffer)

    def model_uses_protocol(self):
        if self.model in ["VVX1500", "VVX500", "VVX600"]:
            return True

    def __str__(self):
        buffer = []
        buffer.append("model: {} ".format(self.model))
        buffer.append("last_name: {} ".format(self.last_name))
        buffer.append("first_name: {} ".format(self.first_name))
        buffer.append("contact: {} ".format(self.contact))
        buffer.append("speed_dial: {} ".format(self.speed_dial))
        buffer.append("protocol: {} ".format(self.protocol))
        buffer.append("label: {} ".format(self.label))
        buffer.append("ring_tone: {} ".format(self.ring_tone))
        buffer.append("divert_contact: {} ".format(self.divert_contact))
        buffer.append("auto_divert: {} ".format(self.auto_divert))
        buffer.append("auto_reject: {} ".format(self.auto_reject))
        buffer.append("buddy_watch: {} ".format(self.buddy_watch))
        buffer.append("buddy_block: {} ".format(self.buddy_block))
        return "\n".join(buffer)
