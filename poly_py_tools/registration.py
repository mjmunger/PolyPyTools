class Registration:

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

    def __init__(self):
        pass

    def __str__(self):
        buffer = []
        buffer.append("name: %s" % (self.name))
        buffer.append("allow: %s" % (", ".join(self.allow)))
        buffer.append("disallow: %s" % (", ".join(self.disallow)))
        buffer.append("name: %s" % ("<unset>" if self.name is None else self.name))
        buffer.append("type: %s" % ("<unset>" if self.type is None else self.type))
        buffer.append("host: %s" % ("<unset>" if self.host is None else self.host))
        buffer.append("context: %s" % ("<unset>" if self.context is None else self.context))
        buffer.append("qualify: %s" % ("<unset>" if self.qualify is None else self.qualify))
        buffer.append("callingpres: %s" % ("<unset>" if self.callingpres is None else self.callingpres))
        buffer.append("permit: %s" % ("<unset>" if self.permit is None else self.permit))
        buffer.append("deny: %s" % ("<unset>" if self.deny is None else self.deny))
        buffer.append("secret: %s" % ("<unset>" if self.secret is None else self.secret))
        buffer.append("md5secret: %s" % ("<unset>" if self.md5secret is None else self.md5secret))
        buffer.append("remotesecret: %s" % ("<unset>" if self.remotesecret is None else self.remotesecret))
        buffer.append("transport: %s" % ("<unset>" if self.transport is None else self.transport))
        buffer.append("dtmfmode: %s" % ("<unset>" if self.dtmfmode is None else self.dtmfmode))
        buffer.append("directmedia: %s" % ("<unset>" if self.directmedia is None else self.directmedia))
        buffer.append("nat: %s" % (("<unset>" if self.nat is None else self.nat)))
        buffer.append("callgroup: %s" % ("<unset>" if self.callgroup is None else self.callgroup))
        buffer.append("pickupgroup: %s" % ("<unset>" if self.pickupgroup is None else self.pickupgroup))
        buffer.append("language: %s" % ("<unset>" if self.language is None else self.language))
        buffer.append("autoframing: %s" % ("<unset>" if self.autoframing is None else self.autoframing))
        buffer.append("insecure: %s" % ("<unset>" if self.insecure is None else self.insecure))
        buffer.append("trustrpid: %s" % ("<unset>" if self.trustrpid is None else self.trustrpid))
        buffer.append("trust_id_outbound: %s" % ("<unset>" if self.trust_id_outbound is None else self.trust_id_outbound))
        buffer.append("progressinband: %s" % ("<unset>" if self.progressinband is None else self.progressinband))
        buffer.append("promiscredir: %s" % ("<unset>" if self.promiscredir is None else self.promiscredir))
        buffer.append("useclientcode: %s" % ("<unset>" if self.useclientcode is None else self.useclientcode))
        buffer.append("accountcode: %s" % ("<unset>" if self.accountcode is None else self.accountcode))
        buffer.append("setvar: %s" % ("<unset>" if self.setvar is None else self.setvar))
        buffer.append("callerid: %s" % ("<unset>" if self.callerid is None else self.callerid))
        buffer.append("amaflags: %s" % ("<unset>" if self.amaflags is None else self.amaflags))
        buffer.append("callcounter: %s" % ("<unset>" if self.callcounter is None else self.callcounter))
        buffer.append("busylevel: %s" % ("<unset>" if self.busylevel is None else self.busylevel))
        buffer.append("allowoverlap: %s" % ("<unset>" if self.allowoverlap is None else self.allowoverlap))
        buffer.append("allowsubscribe: %s" % ("<unset>" if self.allowsubscribe is None else self.allowsubscribe))
        buffer.append("allowtransfer: %s" % ("<unset>" if self.allowtransfer is None else self.allowtransfer))
        buffer.append("ignoresdpversion: %s" % ("<unset>" if self.ignoresdpversion is None else self.ignoresdpversion))
        buffer.append("subscribecontext: %s" % ("<unset>" if self.subscribecontext is None else self.subscribecontext))
        buffer.append("template: %s" % ("<unset>" if self.template is None else self.template))
        buffer.append("videosupport: %s" % ("<unset>" if self.videosupport is None else self.videosupport))
        buffer.append("maxcallbitrate: %s" % ("<unset>" if self.maxcallbitrate is None else self.maxcallbitrate))
        buffer.append("rfc2833compensate: %s" % ("<unset>" if self.rfc2833compensate is None else self.rfc2833compensate))
        buffer.append("mailbox: %s" % ("<unset>" if self.mailbox is None else self.mailbox))
        buffer.append("session_timers: %s" % ("<unset>" if self.session_timers is None else self.session_timers))
        buffer.append("session_expires: %s" % ("<unset>" if self.session_expires is None else self.session_expires))
        buffer.append("session_minse: %s" % ("<unset>" if self.session_minse is None else self.session_minse))
        buffer.append("session_refresher: %s" % ("<unset>" if self.session_refresher is None else self.session_refresher))
        buffer.append("t38pt_usertpsource: %s" % ("<unset>" if self.t38pt_usertpsource is None else self.t38pt_usertpsource))
        buffer.append("regexten: %s" % ("<unset>" if self.regexten is None else self.regexten))
        buffer.append("fromdomain: %s" % ("<unset>" if self.fromdomain is None else self.fromdomain))
        buffer.append("fromuser: %s" % ("<unset>" if self.fromuser is None else self.fromuser))
        buffer.append("port: %s" % ("<unset>" if self.port is None else self.port))
        buffer.append("defaultip: %s" % ("<unset>" if self.defaultip is None else self.defaultip))
        buffer.append("defaultuser: %s" % ("<unset>" if self.defaultuser is None else self.defaultuser))
        buffer.append("rtptimeout: %s" % ("<unset>" if self.rtptimeout is None else self.rtptimeout))
        buffer.append("rtpholdtimeout: %s" % ("<unset>" if self.rtpholdtimeout is None else self.rtpholdtimeout))
        buffer.append("sendrpid: %s" % ("<unset>" if self.sendrpid is None else self.sendrpid))
        buffer.append("outboundproxy: %s" % ("<unset>" if self.outboundproxy is None else self.outboundproxy))
        buffer.append("callbackextension: %s" % ("<unset>" if self.callbackextension is None else self.callbackextension))
        buffer.append("timert1: %s" % ("<unset>" if self.timert1 is None else self.timert1))
        buffer.append("timerb: %s" % ("<unset>" if self.timerb is None else self.timerb))
        buffer.append("qualifyfreq: %s" % ("<unset>" if self.qualifyfreq is None else self.qualifyfreq))
        buffer.append("contactpermit: %s" % ("<unset>" if self.contactpermit is None else self.contactpermit))
        buffer.append("contactdeny: %s" % ("<unset>" if self.contactdeny is None else self.contactdeny))
        buffer.append("directmediapermit: %s" % ("<unset>" if self.directmediapermit is None else self.directmediapermit))
        buffer.append("directmediadeny: %s" % ("<unset>" if self.directmediadeny is None else self.directmediadeny))
        buffer.append("unsolicited_mailbox: %s" % ("<unset>" if self.unsolicited_mailbox is None else self.unsolicited_mailbox))
        buffer.append("use_q850_reason: %s" % ("<unset>" if self.use_q850_reason is None else self.use_q850_reason))
        buffer.append("maxforwards: %s" % ("<unset>" if self.maxforwards is None else self.maxforwards))
        buffer.append("encryption: %s" % ("<unset>" if self.encryption is None else self.encryption))

        return "\n".join(buffer)

