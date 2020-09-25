import os
from xml.etree import ElementTree

from poly_py_tools.loggable import Loggable
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.polycom_registration import PolycomRegistration


class PolycomPhone(Loggable):
    endpoints = {}
    mac = None
    model = None
    pconf = None
    model_meta = None
    registrations = None
    site = None

    def __init__(self):
        self.endpoints = {}
        mac = ""
        pconf = None
        model_meta = None
        self.registrations = []
        self.site = None
        super().__init__()

    def is_model(self, model: str):
        self.model = model

    def sanitize_mac(self, mac):
        return str(mac).lower().replace(":", "").replace("-", "")

    def has_mac(self, mac: str):
        self.mac = self.sanitize_mac(mac)

    def add_endpoint(self, endpoint: Endpoint) :
        self.endpoints[endpoint.section_name] = endpoint

    def remove_endpoint(self, endpoint_name : str):
        del self.endpoints[endpoint_name]

    def bootstrap_cfg_path(self, meta: ModelMeta):
        return os.path.join(meta.get_firmware_dir(self.model), "000000000000.cfg")

    def use_configs(self, pconf: PolypyConfig):
        self.pconf = pconf

    def use_model_meta(self, meta: ModelMeta):
        self.model_meta = meta

    def is_located_at(self, site: str):
        self.site = site

    def bootstrap_cfg(self, meta: ModelMeta):
        xml = ElementTree.ElementTree()
        xml.parse(self.bootstrap_cfg_path(meta))
        root = xml.getroot()
        target_node = "APPLICATION_{}".format(self.model)
        node = root.find(target_node)

        if node is None:
            app_node = ElementTree.Element(target_node)
            root.append(app_node)

        files = ["site.cfg", "sip-interop.cfg", "features.cfg", "sip-basic.cfg", "reg-advanced.cfg"]
        files.append(self.mac)

        config_files = [ "{}/{}".format(self.site, file) for file in files ]

        attribs = {}
        attribs["APP_FILE_PATH_{}".format(self.model)] = "firmware/{}/{}.sip.ld".format(meta.get_firmware_version(self.model), meta.get_part(self.model))
        attribs["CONFIG_FILES_{}".format(self.model)] = ", ".join(config_files)
        app_node.attrib = attribs

        return ElementTree.tostring(root, encoding="unicode", method='xml')

    def write_bootstrap(self):
        tftproot = self.pconf.tftproot_path()
        target_file = os.path.join(tftproot, "{}.cfg".format(self.mac))
        element = ElementTree.fromstring(self.bootstrap_cfg(self.model_meta))
        ET = ElementTree.ElementTree(element)
        ET.write(target_file, encoding="us-ascii", method="xml")
        self.log("Bootstrap file for {} written to: {}".format(self.mac, target_file), 1)

    def write_configs(self):
        target_directory = self.configs_target_directory()
        print("target directory: {}".format(target_directory))
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        target_file = self.config_target_file_path()
        element = ElementTree.fromstring(self.basic_cfg())
        ET = ElementTree.ElementTree(element)
        ET.write(target_file, encoding="us-ascii", method="xml")
        self.log("Config file for {} written to: {}".format(self.mac, target_file),1)

    def config_target_file_path(self):
        return os.path.join(self.configs_target_directory(), self.mac)

    def configs_target_directory(self):
        return os.path.join(self.pconf.tftproot_path(), self.site)

    def basic_cfg_path(self):
        model_firmware_dir = self.model_meta.get_firmware_dir(self.model)
        return os.path.join(model_firmware_dir, "Config/reg-basic.cfg")

    def basic_cfg(self):
        xml = ElementTree.ElementTree()
        xml.parse(self.basic_cfg_path())
        root = xml.getroot()

        # if root is None:
        #     raise ValueError("Could not get root element for {}".format(self.basic_cfg_path(meta)))

        counter = 0
        attribs = {}

        for reg in self.registrations:

            counter = counter + 1

            if reg.order is None:
                reg.order = counter

            tag = "reg.{}.address".format(reg.order)
            attribs[tag] = reg.registration_address

            tag = "reg.{}.auth.password".format(reg.order)
            attribs[tag] = reg.password

            tag = "reg.{}.auth.userId".format(reg.order)
            attribs[tag] = reg.auth.username

            tag = "reg.{}.label".format(reg.order)
            attribs[tag] = reg.label if not reg.label is None else ""

        reg_node = root.find("reg")
        reg_node.attrib = attribs

        return ElementTree.tostring(root)

    def hydrate_registrations(self, resources):

        for tag in self.endpoints:
            ep = self.endpoints[tag]
            ep.load_aors(resources)
            ep.load_auths(resources)
            self.site = ep.template
            reg = PolycomRegistration()
            auth = ep.get_auth()
            aor = ep.get_aor()
            reg.set_auth(auth)
            reg.set_sip_server(self.pconf.sip_proxy())
            reg.set_aor(aor)
            reg.hydrate()
            self.registrations.append(reg)
