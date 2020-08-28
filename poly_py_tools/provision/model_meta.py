from poly_py_tools.polypy_config import PolypyConfig
import os

class ModelMeta(object):
    pconf = None


    polycom_dict = {
        "SPIP320": {"part": "2345-12200-002", "current_firmware_version": "3.3.5.0247"},
        "SPIP321": {"part": "2345-12360-001", "current_firmware_version": "4.0.15.1009"},
        "SPIP330": {"part": "2345-12200-001", "current_firmware_version": "3.3.5.0247"},
        "SPIP331": {"part": "2345-12365-001", "current_firmware_version": "4.0.15.1009"},
        "SPIP335": {"part": "2345-12375-001", "current_firmware_version": "4.0.15.1009"},
        "SPIP430": {"part": "2345-11402-001", "current_firmware_version": "3.2.7.0198"},
        "SPIP450": {"part": "2345-12450-001", "current_firmware_version": "4.0.15.1009"},
        "SSIP5000": {"part": "3111-30900-001", "current_firmware_version": "4.0.15.1009"},
        "SPIP550": {"part": "2345-12500-001", "current_firmware_version": "4.0.15.1009"},
        "SPIP560": {"part": "2345-12560-001", "current_firmware_version": "4.0.15.1009"},
        "SPIP650": {"part": "2345-12600-001", "current_firmware_version": "4.0.15.1009"},
        "SPIP670": {"part": "2345-12670-001", "current_firmware_version": "4.0.15.1009"},
        "SSIP6000": {"part": "3111-15600-001", "current_firmware_version": "4.0.15.1009"},
        "SSIP7000": {"part": "3111-40000-001", "current_firmware_version": "4.0.15.1009"},
        "VVX101": {"part": "3111-40250-001", "current_firmware_version": "6.3.0.14929"},
        "VVX150": {"part": "3111-48810-001", "current_firmware_version": "6.3.0.14929"},
        "VVX1500": {"part": "2345-17960-001", "current_firmware_version": "5.9.6.2327"},
        "VVX201": {"part": "3111-40450-001", "current_firmware_version": "6.3.0.14929"},
        "VVX250": {"part": "3111-48820-001", "current_firmware_version": "6.3.0.14929"},
        "VVX300": {"part": "3111-46135-002", "current_firmware_version": "5.9.6.2327"},
        "VVX301": {"part": "3111-48300-001", "current_firmware_version": "5.9.6.2327"},
        "VVX310": {"part": "3111-46161-001", "current_firmware_version": "5.9.6.2327"},
        "VVX311": {"part": "3111-48350-001", "current_firmware_version": "5.9.6.2327"},
        "VVX350": {"part": "3111-48830-001", "current_firmware_version": "6.3.0.14929"},
        "VVX400": {"part": "3111-46157-002", "current_firmware_version": "5.9.6.2327"},
        "VVX401": {"part": "3111-48400-001", "current_firmware_version": "6.3.0.14929"},
        "VVX410": {"part": "3111-46162-001", "current_firmware_version": "5.9.6.2327"},
        "VVX411": {"part": "3111-48450-001", "current_firmware_version": "6.3.0.14929"},
        "VVX450": {"part": "3111-48840-001", "current_firmware_version": "6.3.0.14929"},
        "VVX500": {"part": "3111-44500-001", "current_firmware_version": "5.9.6.2327"},
        "VVX501": {"part": "3111-48500-001", "current_firmware_version": "6.3.0.14929"},
        "VVX600": {"part": "3111-44600-001", "current_firmware_version": "5.9.6.2327"},
        "VVX601": {"part": "3111-48600-001", "current_firmware_version": "6.3.0.14929"},
        "VVXD60": {"part": "3111-17823-001", "current_firmware_version": "6.3.0.14929"},
    }

    def use_configs(self, pconf: PolypyConfig):
        self.pconf = pconf

    def get_requested_model(self, requested_model):
        for model in self.polycom_dict:
            if model == requested_model:
                return self.polycom_dict[model]
        print(
            "The model you requested, {}, is unsupported. Legacy phones without a currently supported version of firmware are not supported.".format(
                requested_model))
        return False

    def get_meta(self, requested_model, meta):
        model = self.get_requested_model(requested_model)
        if model is False:
            return False
        else:
            return model[meta]

    def get_part(self, requested_model):
        return self.get_meta(requested_model, 'part')

    def get_firmware_version(self, requested_model):
        return self.get_meta(requested_model, 'current_firmware_version')

    def get_firmware_base_dir(self):
        """
        This is here so we can mock.patch it and redirect for tests.
        :return:
        """
        return os.path.join(self.pconf.tftproot_path(), "firmware")

    def get_firmware_dir(self, requested_model):
        return os.path.join(self.get_firmware_base_dir(), self.get_firmware_version(requested_model))


