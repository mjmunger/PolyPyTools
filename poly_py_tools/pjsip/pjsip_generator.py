import os
from poly_py_tools.dialplan import Dialplan
from poly_py_tools.dialplan_entry import Entry
from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.auth import Auth
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.template import Template
from pwgen_secure.rpg import Rpg


class PJSipGenerator(object):

    container = None
    source_csv = None
    config = None
    rpg = None
    pconf = None
    endpoints = None
    templates = None

    def __init__(self, container):
        self.use(container)
        self.endpoints = []
        self.templates = {}

    def use(self, container):
        self.container = container

        if 'rpg' in container:
            self.rpg = container['rpg']

        if 'pconf' in container:
            self.pconf = container['pconf']

    def with_rpg(self, rpg):
        self.rpg = rpg

    def generate_from(self, csv):
        if not os.path.exists(csv):
            raise FileNotFoundError("Could not find {}".format(csv))

        self.source_csv = csv

    def parse_dialplan(self, dialplan: Dialplan):
        if self.pconf is None:
            raise ValueError("Polypy config (self.config) must be set before attempting to generate conf files. Try: generator.use('someconfig')")

        extension = self.container['args']['<extension>']

        for entry in dialplan.entries:

            if not extension == "all":
                if not entry.exten == extension:
                    continue

            template = Template()
            template.from_entry(entry)
            if not template.section in self.templates:
                self.templates[template.section] = template

            endpoint = Endpoint("[{}{}]({})".format(entry.mac, entry.exten, template.name))
            endpoint.mac = entry.mac
            endpoint.model = entry.endpoint
            endpoint.extension = entry.exten
            endpoint.callerid = "{} {}<{}>".format(entry.first, entry.last, entry.cid_number)

            aor = Aor("[{}{}]".format(endpoint.mac, entry.exten))
            aor.section_name = "{}{}".format(endpoint.mac, entry.exten)
            aor.max_contacts = "1"
            aor.mailboxes = entry.vm

            auth = Auth("[auth{}{}]".format(endpoint.mac, endpoint.extension))
            auth.section_name = "auth{}{}".format(endpoint.mac, endpoint.extension)
            auth.auth_type = "userpass"
            auth.username = "{}{}".format(endpoint.mac, endpoint.extension)
            auth.password = self.rpg.generate_password()

            endpoint.add_aor(aor)
            endpoint.add_auth(auth)

            self.endpoints.append(endpoint)

    def render_conf(self):
        buffer = []
        buffer.append(";Generated with polpypy pjsip generate")
        for t in self.templates:
            buffer.append("")
            buffer.append(str(self.templates[t]))
        for endpoint in self.endpoints:
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

        self.generate_from(self.container['args']['<file>'])
        dialplan = Dialplan(self.source_csv)
        dialplan.with_config(self.pconf)
        dialplan.parse()

        if self.container['args']['-a']:
            self.append_conf(dialplan)
        else:
            self.write_clean_conf(dialplan)

        print("Processed {} {}".format(len(self.endpoints), "entry" if len(self.endpoints)==1 else "entries"))

    def append_conf(self, dialplan: Dialplan):

        # Add in all the stuff that's already there.
        target_file = os.path.join(self.pconf.pjsip_path())
        parser = self.container['pjsipparser']
        parser.parse()

        # Get the templates
        for resource in parser.resources:
            if resource.type == "endpoint":
                if resource.is_template:
                    template = Template()
                    template.from_endpoint(resource)
                    self.templates[template.section] = template

        # Get the endpoints.
        for resource in parser.resources:
            if resource.type == "endpoint":
                if not resource.is_template:
                    resource.load_aors(parser.resources)
                    resource.load_auths(parser.resources)
                    self.endpoints.append(resource)

        # Get the things we want to append.
        self.parse_dialplan(dialplan)

        self.write_pjsip_conf()

    def write_clean_conf(self, dialplan: Dialplan):

        self.parse_dialplan(dialplan)
        self.write_pjsip_conf()

    def write_pjsip_conf(self):
        target_file = os.path.join(self.pconf.pjsip_path())
        f = open(target_file, 'w')
        f.write(self.render_conf())
        f.close()
        print("Saved to: {}".format(target_file))
