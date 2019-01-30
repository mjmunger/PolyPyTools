import re
import sys
from pprint import pprint


class Registration:
    verbosity = 0
    device_type = "device"

    disallow = []
    allow = []

    name = None
    type = None
    host = None
    context = None
    qualify = None
    callingpres = None
    permit = None
    deny = None
    secret = None
    md5secret = None
    remotesecret = None
    transport = None
    dtmfmode = None
    directmedia = None
    nat = None
    callgroup = None
    pickupgroup = None
    language = None
    autoframing = None
    insecure = None
    trustrpid = None
    trust_id_outbound = None
    progressinband = None
    promiscredir = None
    useclientcode = None
    accountcode = None
    setvar = None
    callerid = None
    amaflags = None
    callcounter = None
    busylevel = None
    allowoverlap = None
    allowsubscribe = None
    allowtransfer = None
    ignoresdpversion = None
    subscribecontext = None
    template = None
    videosupport = None
    maxcallbitrate = None
    rfc2833compensate = None
    mailbox = None
    session_timers = None
    session_expires = None
    session_minse = None
    session_refresher = None
    t38pt_usertpsource = None
    regexten = None
    fromdomain = None
    fromuser = None
    port = None
    defaultip = None
    defaultuser = None
    rtptimeout = None
    rtpholdtimeout = None
    sendrpid = None
    outboundproxy = None
    callbackextension = None
    timert1 = None
    timerb = None
    qualifyfreq = None
    contactpermit = None
    contactdeny = None
    directmediapermit = None
    directmediadeny = None
    unsolicited_mailbox = None
    use_q850_reason = None
    maxforwards = None
    encryption = None

    # Non-asterisk directives

    mac = None
    model = None
    site = None
    template = None
    email = None
    first_name = None
    last_name = None

    def __init__(self):
        self.type = "friend"

    def set_verbosity(self, level):
        self.verbosity = level

    def log(self, message, minimum_level=1):
        if self.verbosity < minimum_level:
            return True

        print("%s", message)

    def __str__(self):
        buffer = []
        buffer.append("============================================================")
        buffer.append(self.device_type.center(60," "))
        buffer.append("============================================================")
        buffer.append("Template: %s" % ("<unset>" if self.template is None else self.template))
        buffer.append("name: %s" % self.name)
        buffer.append("allow: %s" % (", ".join(self.allow)))
        buffer.append("disallow: %s" % (", ".join(self.disallow)))

        if self.name is not None or self.verbosity > 2:
            buffer.append("name: %s" % ("<unset>" if self.name is None else self.name))

        if self.type is not None or self.verbosity > 2:
            buffer.append("type: %s" % ("<unset>" if self.type is None else self.type))

        if self.host is not None or self.verbosity > 2:
            buffer.append("host: %s" % ("<unset>" if self.host is None else self.host))

        if self.context is not None or self.verbosity > 2:
            buffer.append("context: %s" % ("<unset>" if self.context is None else self.context))

        if self.qualify is not None or self.verbosity > 2:
            buffer.append("qualify: %s" % ("<unset>" if self.qualify is None else self.qualify))

        if self.callingpres is not None or self.verbosity > 2:
            buffer.append("callingpres: %s" % ("<unset>" if self.callingpres is None else self.callingpres))

        if self.permit is not None or self.verbosity > 2:
            buffer.append("permit: %s" % ("<unset>" if self.permit is None else self.permit))

        if self.deny is not None or self.verbosity > 2:
            buffer.append("deny: %s" % ("<unset>" if self.deny is None else self.deny))

        if self.secret is not None or self.verbosity > 2:
            buffer.append("secret: %s" % ("<unset>" if self.secret is None else self.secret))

        if self.md5secret is not None or self.verbosity > 2:
            buffer.append("md5secret: %s" % ("<unset>" if self.md5secret is None else self.md5secret))

        if self.remotesecret is not None or self.verbosity > 2:
            buffer.append("remotesecret: %s" % ("<unset>" if self.remotesecret is None else self.remotesecret))

        if self.transport is not None or self.verbosity > 2:
            buffer.append("transport: %s" % ("<unset>" if self.transport is None else self.transport))

        if self.dtmfmode is not None or self.verbosity > 2:
            buffer.append("dtmfmode: %s" % ("<unset>" if self.dtmfmode is None else self.dtmfmode))

        if self.directmedia is not None or self.verbosity > 2:
            buffer.append("directmedia: %s" % ("<unset>" if self.directmedia is None else self.directmedia))

        if self.nat is not None or self.verbosity > 2:
            buffer.append("nat: %s" % (("<unset>" if self.nat is None else self.nat)))

        if self.callgroup is not None or self.verbosity > 2:
            buffer.append("callgroup: %s" % ("<unset>" if self.callgroup is None else self.callgroup))

        if self.pickupgroup is not None or self.verbosity > 2:
            buffer.append("pickupgroup: %s" % ("<unset>" if self.pickupgroup is None else self.pickupgroup))

        if self.language is not None or self.verbosity > 2:
            buffer.append("language: %s" % ("<unset>" if self.language is None else self.language))

        if self.autoframing is not None or self.verbosity > 2:
            buffer.append("autoframing: %s" % ("<unset>" if self.autoframing is None else self.autoframing))

        if self.insecure is not None or self.verbosity > 2:
            buffer.append("insecure: %s" % ("<unset>" if self.insecure is None else self.insecure))

        if self.trustrpid is not None or self.verbosity > 2:
            buffer.append("trustrpid: %s" % ("<unset>" if self.trustrpid is None else self.trustrpid))

        if self.trust_id_outbound is not None or self.verbosity > 2:
            buffer.append("trust_id_outbound: %s" % ("<unset>" if self.trust_id_outbound is None else self.trust_id_outbound))

        if self.progressinband is not None or self.verbosity > 2:
            buffer.append("progressinband: %s" % ("<unset>" if self.progressinband is None else self.progressinband))

        if self.promiscredir is not None or self.verbosity > 2:
            buffer.append("promiscredir: %s" % ("<unset>" if self.promiscredir is None else self.promiscredir))

        if self.useclientcode is not None or self.verbosity > 2:
            buffer.append("useclientcode: %s" % ("<unset>" if self.useclientcode is None else self.useclientcode))

        if self.accountcode is not None or self.verbosity > 2:
            buffer.append("accountcode: %s" % ("<unset>" if self.accountcode is None else self.accountcode))

        if self.setvar is not None or self.verbosity > 2:
            buffer.append("setvar: %s" % ("<unset>" if self.setvar is None else self.setvar))

        if self.callerid is not None or self.verbosity > 2:
            buffer.append("callerid: %s" % ("<unset>" if self.callerid is None else self.callerid))

        if self.amaflags is not None or self.verbosity > 2:
            buffer.append("amaflags: %s" % ("<unset>" if self.amaflags is None else self.amaflags))

        if self.callcounter is not None or self.verbosity > 2:
            buffer.append("callcounter: %s" % ("<unset>" if self.callcounter is None else self.callcounter))

        if self.busylevel is not None or self.verbosity > 2:
            buffer.append("busylevel: %s" % ("<unset>" if self.busylevel is None else self.busylevel))

        if self.allowoverlap is not None or self.verbosity > 2:
            buffer.append("allowoverlap: %s" % ("<unset>" if self.allowoverlap is None else self.allowoverlap))

        if self.allowsubscribe is not None or self.verbosity > 2:
            buffer.append("allowsubscribe: %s" % ("<unset>" if self.allowsubscribe is None else self.allowsubscribe))

        if self.allowtransfer is not None or self.verbosity > 2:
            buffer.append("allowtransfer: %s" % ("<unset>" if self.allowtransfer is None else self.allowtransfer))

        if self.ignoresdpversion is not None or self.verbosity > 2:
            buffer.append("ignoresdpversion: %s" % ("<unset>" if self.ignoresdpversion is None else self.ignoresdpversion))

        if self.subscribecontext is not None or self.verbosity > 2:
            buffer.append("subscribecontext: %s" % ("<unset>" if self.subscribecontext is None else self.subscribecontext))

        if self.template is not None or self.verbosity > 2:
            buffer.append("template: %s" % ("<unset>" if self.template is None else self.template))

        if self.videosupport is not None or self.verbosity > 2:
            buffer.append("videosupport: %s" % ("<unset>" if self.videosupport is None else self.videosupport))

        if self.maxcallbitrate is not None or self.verbosity > 2:
            buffer.append("maxcallbitrate: %s" % ("<unset>" if self.maxcallbitrate is None else self.maxcallbitrate))

        if self.rfc2833compensate is not None or self.verbosity > 2:
            buffer.append("rfc2833compensate: %s" % ("<unset>" if self.rfc2833compensate is None else self.rfc2833compensate))

        if self.mailbox is not None or self.verbosity > 2:
            buffer.append("mailbox: %s" % ("<unset>" if self.mailbox is None else self.mailbox))

        if self.session_timers is not None or self.verbosity > 2:
            buffer.append("session_timers: %s" % ("<unset>" if self.session_timers is None else self.session_timers))

        if self.session_expires is not None or self.verbosity > 2:
            buffer.append("session_expires: %s" % ("<unset>" if self.session_expires is None else self.session_expires))

        if self.session_minse is not None or self.verbosity > 2:
            buffer.append("session_minse: %s" % ("<unset>" if self.session_minse is None else self.session_minse))

        if self.session_refresher is not None or self.verbosity > 2:
            buffer.append("session_refresher: %s" % ("<unset>" if self.session_refresher is None else self.session_refresher))

        if self.t38pt_usertpsource is not None or self.verbosity > 2:
            buffer.append("t38pt_usertpsource: %s" % ("<unset>" if self.t38pt_usertpsource is None else self.t38pt_usertpsource))

        if self.regexten is not None or self.verbosity > 2:
            buffer.append("regexten: %s" % ("<unset>" if self.regexten is None else self.regexten))

        if self.fromdomain is not None or self.verbosity > 2:
            buffer.append("fromdomain: %s" % ("<unset>" if self.fromdomain is None else self.fromdomain))

        if self.fromuser is not None or self.verbosity > 2:
            buffer.append("fromuser: %s" % ("<unset>" if self.fromuser is None else self.fromuser))

        if self.port is not None or self.verbosity > 2:
            buffer.append("port: %s" % ("<unset>" if self.port is None else self.port))

        if self.defaultip is not None or self.verbosity > 2:
            buffer.append("defaultip: %s" % ("<unset>" if self.defaultip is None else self.defaultip))

        if self.defaultuser is not None or self.verbosity > 2:
            buffer.append("defaultuser: %s" % ("<unset>" if self.defaultuser is None else self.defaultuser))

        if self.rtptimeout is not None or self.verbosity > 2:
            buffer.append("rtptimeout: %s" % ("<unset>" if self.rtptimeout is None else self.rtptimeout))

        if self.rtpholdtimeout is not None or self.verbosity > 2:
            buffer.append("rtpholdtimeout: %s" % ("<unset>" if self.rtpholdtimeout is None else self.rtpholdtimeout))

        if self.sendrpid is not None or self.verbosity > 2:
            buffer.append("sendrpid: %s" % ("<unset>" if self.sendrpid is None else self.sendrpid))

        if self.outboundproxy is not None or self.verbosity > 2:
            buffer.append("outboundproxy: %s" % ("<unset>" if self.outboundproxy is None else self.outboundproxy))

        if self.callbackextension is not None or self.verbosity > 2:
            buffer.append("callbackextension: %s" % ("<unset>" if self.callbackextension is None else self.callbackextension))

        if self.timert1 is not None or self.verbosity > 2:
            buffer.append("timert1: %s" % ("<unset>" if self.timert1 is None else self.timert1))

        if self.timerb is not None or self.verbosity > 2:
            buffer.append("timerb: %s" % ("<unset>" if self.timerb is None else self.timerb))

        if self.qualifyfreq is not None or self.verbosity > 2:
            buffer.append("qualifyfreq: %s" % ("<unset>" if self.qualifyfreq is None else self.qualifyfreq))

        if self.contactpermit is not None or self.verbosity > 2:
            buffer.append("contactpermit: %s" % ("<unset>" if self.contactpermit is None else self.contactpermit))

        if self.contactdeny is not None or self.verbosity > 2:
            buffer.append("contactdeny: %s" % ("<unset>" if self.contactdeny is None else self.contactdeny))

        if self.directmediapermit is not None or self.verbosity > 2:
            buffer.append("directmediapermit: %s" % ("<unset>" if self.directmediapermit is None else self.directmediapermit))

        if self.directmediadeny is not None or self.verbosity > 2:
            buffer.append("directmediadeny: %s" % ("<unset>" if self.directmediadeny is None else self.directmediadeny))

        if self.unsolicited_mailbox is not None or self.verbosity > 2:
            buffer.append("unsolicited_mailbox: %s" % ("<unset>" if self.unsolicited_mailbox is None else self.unsolicited_mailbox))

        if self.use_q850_reason is not None or self.verbosity > 2:
            buffer.append("use_q850_reason: %s" % ("<unset>" if self.use_q850_reason is None else self.use_q850_reason))

        if self.maxforwards is not None or self.verbosity > 2:
            buffer.append("maxforwards: %s" % ("<unset>" if self.maxforwards is None else self.maxforwards))

        if self.encryption is not None or self.verbosity > 2:
            buffer.append("encryption: %s" % ("<unset>" if self.encryption is None else self.encryption))

        if self.mac is not None or self.verbosity > 2:
            buffer.append("mac: %s" % ("<unset>" if self.mac is None else self.mac))

        if self.model is not None or self.verbosity > 2:
            buffer.append("model: %s" % ("<unset>" if self.model is None else self.model))

        return "\n".join(buffer)

    @staticmethod
    def implements_template(raw_device):
        template_pattern = r"^(\[[a-zA-Z0-9]+?\])(\([a-zA-Z0-9-]+?\){1})"

        match = re.search(template_pattern, raw_device[0])
        if match:
            return match.group(2).strip()
        return False

    def parse_registration(self, raw_device):

        if self.device_type == "device":
            pattern = r"^(\[[a-zA-Z0-9]+?\])(\([a-zA-Z0-9-]+?\)){0,}$"
            match = re.match(pattern, raw_device[0])
            self.name = match.group(1)[1:-1]

        for line in raw_device:
            line = line.strip()
            if "=" not in line:
                continue

            buff = line.split("=")
            if buff[0] == "allow":
                self.allow.append(buff[1])
                continue

            if buff[0] == "disallow":
                self.disallow.append(buff[1])
                continue

            directive = buff[0]
            if(directive[:1]) == ";":
                directive = directive[1:]

            setattr(self, directive, buff[1].strip())

    def valid_registration(self):

        if self.mac is None:
            print("ERROR: Mac address not set for %s. Cannot provision this device" % self.name)
            sys.exit(1)

    def import_template(self, template):
        self.type = template.type
        self.host = template.host
        self.context = template.context
        self.qualify = template.qualify
        self.callingpres = template.callingpres
        self.permit = template.permit
        self.deny = template.deny
        self.secret = template.secret
        self.md5secret = template.md5secret
        self.remotesecret = template.remotesecret
        self.transport = template.transport
        self.dtmfmode = template.dtmfmode
        self.directmedia = template.directmedia
        self.nat = template.nat
        self.callgroup = template.callgroup
        self.pickupgroup = template.pickupgroup
        self.language = template.language
        self.autoframing = template.autoframing
        self.insecure = template.insecure
        self.trustrpid = template.trustrpid
        self.trust_id_outbound = template.trust_id_outbound
        self.progressinband = template.progressinband
        self.promiscredir = template.promiscredir
        self.useclientcode = template.useclientcode
        self.accountcode = template.accountcode
        self.setvar = template.setvar
        self.callerid = template.callerid
        self.amaflags = template.amaflags
        self.callcounter = template.callcounter
        self.busylevel = template.busylevel
        self.allowoverlap = template.allowoverlap
        self.allowsubscribe = template.allowsubscribe
        self.allowtransfer = template.allowtransfer
        self.ignoresdpversion = template.ignoresdpversion
        self.subscribecontext = template.subscribecontext
        self.videosupport = template.videosupport
        self.maxcallbitrate = template.maxcallbitrate
        self.rfc2833compensate = template.rfc2833compensate
        self.mailbox = template.mailbox
        self.session_timers = template.session_timers
        self.session_expires = template.session_expires
        self.session_minse = template.session_minse
        self.session_refresher = template.session_refresher
        self.t38pt_usertpsource = template.t38pt_usertpsource
        self.regexten = template.regexten
        self.fromdomain = template.fromdomain
        self.fromuser = template.fromuser
        self.port = template.port
        self.defaultip = template.defaultip
        self.defaultuser = template.defaultuser
        self.rtptimeout = template.rtptimeout
        self.rtpholdtimeout = template.rtpholdtimeout
        self.sendrpid = template.sendrpid
        self.outboundproxy = template.outboundproxy
        self.callbackextension = template.callbackextension
        self.timert1 = template.timert1
        self.timerb = template.timerb
        self.qualifyfreq = template.qualifyfreq
        self.contactpermit = template.contactpermit
        self.contactdeny = template.contactdeny
        self.directmediapermit = template.directmediapermit
        self.directmediadeny = template.directmediadeny
        self.unsolicited_mailbox = template.unsolicited_mailbox
        self.use_q850_reason = template.use_q850_reason
        self.maxforwards = template.maxforwards
        self.encryption = template.encryption
        self.allow = template.allow
        self.disallow = template.disallow

    def import_csv_row(self, row, csv_config):

        try:
            self.name = row[csv_config.extension_column]
        except IndexError:
            print("The target csv file (%s) does not appear to have %s columns. Re-run polypy sip configure and check your file.")
            sys.exit(1)

        try:
            self.mac = row[csv_config.mac_column]
        except IndexError:
            print("The target csv file (%s) does not appear to have %s columns. Re-run polypy sip configure and check your file.")
            sys.exit(1)

        try:
            self.first_name = row[csv_config.first_name_column]
        except IndexError:
            print("The target csv file (%s) does not appear to have %s columns. Re-run polypy sip configure and check your file.")

        try:
            self.last_name = row[csv_config.last_name_column]
        except IndexError:
            print("The target csv file (%s) does not appear to have %s columns. Re-run polypy sip configure and check your file.")

        try:
            self.callerid = '"%s %s" <%s>' % (row[csv_config.first_name_column],
                                              row[csv_config.last_name_column],
                                              row[csv_config.cid_number])
        except IndexError:
            print("The target csv file (%s) does not appear to have %s columns. Re-run polypy sip configure and check your file.")
            sys.exit(1)

        if csv_config.voicemail_column is not None:
            self.mailbox = row[csv_config.voicemail_column]

        if csv_config.device_column is not None:
            self.model = row[csv_config.device_column]

        if csv_config.email_column is not None:
            self.email = row[csv_config.email_column]

    def get_device_definition(self):
        lines = []
        lines.append("\n")
        lines.append("[%s]" % self.name)
        lines.append(";mac=%s" % str(self.mac).lower())
        lines.append(";model=%s" % self.model)
        lines.append("type=%s" % self.type)
        lines.append("secret=%s" % self.secret)
        lines.append("callerid=%s" % self.callerid)
        lines.append("mailbox=%s" % self.mailbox)
        buffer = "\n".join(lines)
        return buffer

    def get_voicemail_definition(self):

        components = []
        components.append("%s => 1234" % self.name)
        if len(self.first_name.strip()) > 0 and len(self.last_name.strip()) > 0:
            components.append("%s %s" % (self.first_name, self.last_name))

        if len(self.email.strip()) > 0:
            components.append(self.email)

        line = ",".join(components)

        lines = []
        lines.append("\n")
        lines.append(line)
        buffer = "\n".join(lines)
        return buffer
