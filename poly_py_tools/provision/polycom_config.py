import os
import subprocess
from pprint import pprint
from xml.dom import minidom


class PolycomConfig:

    path = None
    mac = None
    cn = None
    configs = None
    private_key_path = None
    csr_path = None
    force = False
    cert_file_path = None
    polycom_config_file = None

    def __init__(self, configs):
        self.configs = configs

    def set_path(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError

        self.path = path

    def set_mac(self, mac):
        self.mac = mac

    def set_cn(self, cn):
        self.cn = cn

    def __str__(self):
        buffer = []
        buffer.append("Mac: {}".format(self.mac))
        buffer.append("Common Name: {}".format(self.cn))
        return "\n".join(buffer)

    def check_export_path(self):
        if not os.path.exists(self.configs['paths']['tftproot']):
            raise FileNotFoundError("TFTP Root ({}) could not be found. Provision a phone first.".format(self.configs['paths']['tftproot']))

        target_cfg_file = os.path.join(self.configs['paths']['tftproot'], self.mac + ".cfg")
        if not os.path.exists(target_cfg_file):
            raise FileNotFoundError("{} has not been generated or could not be found. Provision this phone before trying to secure it with TLS/SSL".format( target_cfg_file))

    def generate_private_key(self):
        target_key_file = os.path.join(self.configs['paths']['tftproot'], self.cn + ".key")
        if os.path.exists(target_key_file) and self.force is False:
            raise FileExistsError("{} exists. Use --force to regenerate".format(target_key_file))

        cmd = "openssl|genrsa|-out|{}|2048".format(target_key_file).split("|")
        subprocess.call(cmd)

        if os.path.exists(target_key_file):
            self.private_key_path = target_key_file
        else:
            raise FileNotFoundError("The file {} should have just been created, but I could not find it. Error!".format(target_key_file))

    def generate_csr(self):
        self.check_export_path()
        self.generate_private_key()

        self.csr_path = os.path.join(os.path.dirname(self.private_key_path), "{}.csr".format(self.cn))
        expected_crt_file = os.path.join(os.path.dirname(self.private_key_path), "{}.crt".format(self.csr_path))

        cmd = "openssl|req|-new|-sha256|-key|{}|-out|{}|-subj|/CN={}".format(self.private_key_path, self.csr_path, self.cn).split("|")
        pprint(cmd)
        subprocess.call(cmd)

        print("CSR generated: {}".format(self.csr_path))
        print("Submit this to your CA and get it signed, then import the resulting cert with polypy ssl cert {} {}".format(expected_crt_file, self.mac))
        print("Done")

    def set_certfile(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError
        self.cert_file_path = file_path

    def find_base_config(self):
        target_file = os.path.join(self.configs['paths']['tftproot'], self.mac + ".cfg")
        if not os.path.exists(target_file):
            raise FileNotFoundError("Cannot find the base config for the phone: {}".format(target_file))
        return target_file

    def find_full_config(self, base_config):
        xmldoc = minidom.parse(base_config)
        app = xmldoc.getElementsByTagName('APPLICATION')[0]
        for file in app.attributes['CONFIG_FILES'].value.split(","):
            if self.mac in file:
                target_file = file.strip()
                target_path = os.path.join(self.configs['paths']['tftproot'], target_file)
        print("Target file: {}".format(target_file))
        print("Target path: {}".format(target_path))
        self.polycom_config_file = target_path

        if not os.path.exists(self.polycom_config_file):
            raise FileNotFoundError("Cannot find full config for this phone. It should be here: {}", self.polycom_config_file)

        return minidom.parse(self.polycom_config_file)

    def inject_cert(self):
        if self.cert_file_path is None:
            raise Exception("Cert file path not set. Please specify a cert file path.")

        if not os.path.exists(self.cert_file_path):
            raise FileNotFoundError("Cannot find {}".format(self.cert_file_path))

        polycom_xml = self.find_full_config(self.find_base_config())
        pprint(polycom_xml.toprettyxml())
