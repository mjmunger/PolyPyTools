import os
from poly_py_tools.dialplan import Dialplan
from poly_py_tools.dialplan_entry import Entry
from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.auth import Auth
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.template import Template
from pwgen_secure.rpg import Rpg


class PJSipGenerator(object):

    source_csv = None
    config = None
    rpg = None

    def __init__(self, args):
        self.args = args

        if 'rpg' in args:
            self.rpg = args['rpg']

        if 'config' in args:
            self.config = args['config']

    def use(self, config):
        self.config = config

    def with_rpg(self, rpg):
        self.rpg = rpg

    def generate_from(self, csv):
        if not os.path.exists(csv):
            raise FileNotFoundError("Could not find {}".format(csv))

        self.source_csv = csv

    def conf(self):
        if self.config is None:
            raise ValueError("Polypy config (self.config) must be set before attempting to generate conf files. Try: generator.use('someconfig')")

        dialplan = Dialplan(self.source_csv)
        dialplan.with_config(self.config)
        dialplan.parse()

        endpoints = []
        templates = {}

        for entry in dialplan.entries:
            template = Template()
            template.from_entry(entry)
            if not template.section in templates:
                templates[template.section] = template

            endpoint = Endpoint("[{}]({})".format(entry.mac, template.name))
            endpoint.mac = entry.mac
            endpoint.model = entry.endpoint
            endpoint.extension = entry.exten
            endpoint.callerid = "{} {}<{}>".format(entry.first, entry.last, entry.cid_number)

            aor = Aor("[{}{}]".format(endpoint.mac, endpoint.extension))
            aor.section_name = "{}{}".format(endpoint.mac, endpoint.extension)
            aor.max_contacts = "1"
            aor.mailboxes = entry.vm

            auth = Auth("[auth{}{}]".format(endpoint.mac, endpoint.extension))
            auth.section_name = "auth{}{}".format(endpoint.mac, endpoint.extension)
            auth.auth_type = "userpass"
            auth.username = "{}{}".format(endpoint.mac, endpoint.extension)
            auth.password = self.rpg.generate_password()

            endpoint.add_aor(aor)
            endpoint.add_auth(auth)

            endpoints.append(endpoint)

        buffer = []
        buffer.append(";Generated with polpypy pjsip generate")

        for t in templates:
            buffer.append("")
            buffer.append(str(templates[t]))

        for endpoint in endpoints:
            buffer.append("")
            buffer.append(endpoint.render())

            # for aor in endpoint.addresses:
            #     buffer.append("")
            #     buffer.append(aor.render())
            #
            # for auth in endpoint.authorizations:
            #     buffer.append("")
            #     buffer.append(auth.render())

        return "\n".join(buffer)

    def run(self):
        self.generate_from(self.args['<file>'])
        target_file = os.path.join(self.config.configs()['paths']['tftproot'], 'pjsip.conf')
        f = open(target_file, 'w')
        f.write(self.conf())
        f.close()
        print("Saved to: {}".format(target_file))
