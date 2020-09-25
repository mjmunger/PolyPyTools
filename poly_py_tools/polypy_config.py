import os
import json
import site
from shutil import copyfile


class PolypyConfig:
    json = None
    config_path = None
    search_paths = None
    polycom_files = None

    def __init__(self):
        self.json = {}
        self.search_paths = []
        self.add_search_path(os.getcwd())
        self.polycom_files = []

        self.polycom_files = ['000000000000.cfg', '000000000000-directory~.xml', "Config/applications.cfg",
                              "Config/device.cfg",
                              "Config/features.cfg", "Config/H323.cfg", "Config/polycomConfig.xsd",
                              "Config/reg-advanced.cfg",
                              "Config/reg-basic.cfg", "Config/region.cfg", "Config/sip-basic.cfg",
                              "Config/sip-interop.cfg",
                              "Config/site.cfg", "Config/video.cfg", "Config/video-integration.cfg"]

    def find(self):
        for path in self.search_paths:
            config_path = os.path.join(path, "polypy.conf")
            if os.path.exists(config_path):
                self.config_path = config_path
                return True

        return False

    def add_search_path(self, path):
        self.search_paths.append(path)

    def load(self):
        if not self.find():
            raise FileNotFoundError("Could not find polypy.conf. Perhaps you need to run set-defaults? Or polypy configure?")

        with open(self.config_path) as fp:
            self.json = json.load(fp)

    def write(self):
        try:
            with open(self.config_path, 'w') as fp:
                json.dump(self.json, fp)
        except PermissionError:
            print("Could not write config to {}. Perhaps you need to be root?".format(self.config_path))
            raise PermissionError

    def write_default_config(self, target_path):
        self.set_default_config(target_path)
        self.write()

    def set_default_config(self, target_path):
        self.config_path = target_path
        configs = {}
        # Setup default values:
        lib_path = '/var/lib/polypy'
        share_path = '/usr/share/polypy/'
        local_bin = '/usr/local/bin/'
        package_path = None
        paths = {}
        package_path = os.path.join(site.getsitepackages()[0], 'poly_py_tools')
        csv_header_matching_dictionary = {
            "first": ["first", "firstname", "first name"],
            "last": ["last", "lastname", "last name"],
            "exten": ["exten", "extension", "new extension"],
            "vm": ["vm", "voicemail"],
            "mac": ["mac", "macaddr", "mac address", "physical address"],
            "email": ["email"],
            "endpoint": ["device", "phone", "fax", "model"],
            "cid_number": ["cid", "cname", "callerid", "Caller-ID"],
            "priority": ["priority", "sort", "order by", "order"],
            "label": ["label"],
            "did": ["contact", "direct phone", "did", "number"],
            "group_dial": ["simul-ring", "group dial"],
            "site": ["site"]
        }
        paths["asterisk"] = "/etc/asterisk/"
        paths["tftproot"] = "/srv/tftp/"
        configs['lib_path'] = lib_path
        configs['share_path'] = share_path
        configs['config_path'] = self.config_path
        configs['package_path'] = package_path
        configs['paths'] = paths
        configs['server_addr'] = "127.0.0.1"
        configs['dictionary'] = csv_header_matching_dictionary
        configs['csvmap'] = {}
        self.json = configs
        return self.json

    def set_path(self, path, target_path):
        if target_path is ".":
            target_path = os.getcwd()

        if not str(target_path).startswith("/"):
            target_path = os.path.join(os.getcwd(), target_path)

        self.json['paths'][path] = target_path
        self.write()

    def set_server(self, server_addr):
        self.json['server_addr'] = server_addr
        self.write()

    def validate(self):
        state_report = {}
        state_report[self.json['paths']['asterisk']] = os.path.exists(
            os.path.join(self.json['paths']['asterisk'], "sip.conf"))
        state_report[self.json['paths']['tftproot']] = os.path.exists(self.json['paths']['tftproot'])

        for file in self.polycom_files:
            target_path = os.path.join(self.json['paths']['tftproot'], file)
            state_report[target_path] = os.path.exists(target_path)

        if False in state_report.values():
            print("The following files could not be found. Consider running copy-files to fix this.")
            for path in state_report:
                if state_report[path] == False:
                    print(path)
        else:
            print("Configuration looks good.")

        return state_report

    def copy_files(self, source_path):

        if not os.path.exists(source_path):
            print("Path %s does not exist. Quitting." % source_path)
            exit(1)

        missing_files = []

        for file in self.polycom_files:
            target_path = os.path.join(source_path, file)
            if not os.path.exists(target_path):
                missing_files.append(target_path)

        if len(missing_files) > 0:
            print("Some required files are missing from {}".format(source_path))
            for file in missing_files:
                print("- {}".format(file))

            exit(1)

        # Copy everything over.

        target_path = os.path.join(os.getcwd(), 'tftp')
        target_path = self.json['paths']['tftproot']

        if not os.path.exists(target_path):
            os.mkdir(target_path)

        target_config_path = os.path.join(target_path, "Config")
        if not os.path.exists(target_config_path):
            os.mkdir(target_config_path)

        for file in self.polycom_files:
            source_file = os.path.join(source_path, file)
            target_file = os.path.join(target_path, file)
            print("Copying: {} => {}".format(source_file, target_file))
            copyfile(source_file, target_file)

    def add_dictionary_alias(self, word, alias):
        word_list = list(self.json['dictionary'][word])
        word_list.append(alias)
        self.json['dictionary'][word] = word_list
        self.write()

    def del_dictionary_word(self, word, alias):
        word_list = list(self.json['dictionary'][word])
        word_list.remove(alias)
        self.json['dictionary'][word] = word_list
        self.write()

    def set_map(self, map):
        self.json['csvmap'] = map
        self.write()

    def __str__(self):
        buffer = []
        for attr, value in self.__dict__.items():
            buffer.append("{}: {}".format(attr,value))
        return "\n".join(buffer)

    def configs(self):
        return self.json

    def pjsip_path(self) -> str:
        """
        This facade is here so we can mock.patch it.
        :return:
        """
        return os.path.join(self.asterisk_path(), "pjsip.conf")

    def asterisk_path(self) -> str:
        return self.json['paths']['asterisk']

    def tftproot_path(self):
        return self.json['paths']['tftproot']

    def update_paths(self, path, value):
        self.json['paths'][path] = value

    def sip_proxy(self):
        return self.json['server_addr']
