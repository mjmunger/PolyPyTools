import unittest
import sys
import io
import os
from unittest.mock import MagicMock

from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta

from unittest_data_provider import data_provider


class TestModelMeta(unittest.TestCase):

    provider_unsupported_phones = lambda: (
        ('SPIP4000', ),
        ('SPIP301', ),
        ('SPIP501', ),
        ('SPIP600', ),
        ('SPIP601', ),
        ('SSDuo', ),
    )

    provider_test_get_part = lambda: (
        ('SPIP430', '2345-11402-001'),
        ('SPIP330', '2345-12200-001'),
        ('SPIP320', '2345-12200-002'),
        ('SPIP321', '2345-12360-001'),
        ('SPIP331', '2345-12365-001'),
        ('SPIP335', '2345-12375-001'),
        ('SPIP450', '2345-12450-001'),
        ('SPIP550', '2345-12500-001'),
        ('SPIP560', '2345-12560-001'),
        ('SPIP650', '2345-12600-001'),
        ('SPIP670', '2345-12670-001'),
        ('VVX1500', '2345-17960-001'),
        ('VVX1500', '2345-17960-001'),
        ('SSIP6000', '3111-15600-001'),
        ('VVXD60', '3111-17823-001'),
        ('SSIP5000', '3111-30900-001'),
        ('SSIP7000', '3111-40000-001'),
        ('VVX101', '3111-40250-001'),
        ('VVX201', '3111-40450-001'),
        ('VVX500', '3111-44500-001'),
        ('VVX600', '3111-44600-001'),
        ('VVX300', '3111-46135-002'),
        ('VVX400', '3111-46157-002'),
        ('VVX310', '3111-46161-001'),
        ('VVX410', '3111-46162-001'),
        ('VVX301', '3111-48300-001'),
        ('VVX311', '3111-48350-001'),
        ('VVX401', '3111-48400-001'),
        ('VVX411', '3111-48450-001'),
        ('VVX501', '3111-48500-001'),
        ('VVX601', '3111-48600-001'),
        ('VVX150', '3111-48810-001'),
        ('VVX250', '3111-48820-001'),
        ('VVX350', '3111-48830-001'),
        ('VVX450', '3111-48840-001'),
    )

    @data_provider(provider_unsupported_phones)
    def test_get_part_unsupported(self, model):
        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out

        meta = ModelMeta()
        part = meta.get_part(model)

        output = out.getvalue()

        self.assertEqual("The model you requested, {}, is unsupported. Legacy phones without a currently supported version of firmware are not supported.\n".format(model), output)

    @data_provider(provider_test_get_part)
    def test_get_part(self, model, expected_part):
        meta = ModelMeta()
        part = meta.get_part(model)
        self.assertEqual(expected_part, part,
                         "For model {} we are expecting {}, but we got {}".format(model, expected_part, part))

    provider_test_get_firmware_version = lambda: (
        ("SPIP320", "3.3.5.0247"),
        ("SPIP321", "4.0.15.1009"),
        ("SPIP330", "3.3.5.0247"),
        ("SPIP331", "4.0.15.1009"),
        ("SPIP335", "4.0.15.1009"),
        ("SPIP430", "3.2.7.0198"),
        ("SPIP450", "4.0.15.1009"),
        ("SSIP5000", "4.0.15.1009"),
        ("SPIP550", "4.0.15.1009"),
        ("SPIP560", "4.0.15.1009"),
        ("SPIP650", "4.0.15.1009"),
        ("SPIP670", "4.0.15.1009"),
        ("SSIP6000", "4.0.15.1009"),
        ("SSIP7000", "4.0.15.1009"),
        ("VVX101", "6.3.0.14929"),
        ("VVX150", "6.3.0.14929"),
        ("VVX1500", "5.9.6.2327"),
        ("VVX201", "6.3.0.14929"),
        ("VVX250", "6.3.0.14929"),
        ("VVX300", "5.9.6.2327"),
        ("VVX301", "5.9.6.2327"),
        ("VVX310", "5.9.6.2327"),
        ("VVX311", "5.9.6.2327"),
        ("VVX350", "6.3.0.14929"),
        ("VVX400", "5.9.6.2327"),
        ("VVX401", "6.3.0.14929"),
        ("VVX410", "5.9.6.2327"),
        ("VVX411", "6.3.0.14929"),
        ("VVX450", "6.3.0.14929"),
        ("VVX500", "5.9.6.2327"),
        ("VVX501", "6.3.0.14929"),
        ("VVX600", "5.9.6.2327"),
        ("VVX601", "6.3.0.14929"),
        ("VVXD60", "6.3.0.14929"),)

    @data_provider(provider_test_get_firmware_version)
    def test_get_firmware_version(self, model, expected_firmware_version):
        meta = ModelMeta()
        version = meta.get_firmware_version(model)
        self.assertEqual(expected_firmware_version, version,
                         "For model {} we are expecting {}, but we got {}".format(model, expected_firmware_version, version))

    def test_use_configs(self):
        pconf = PolypyConfig()

        meta = ModelMeta()
        meta.use_configs(pconf)
        self.assertEqual(pconf, meta.pconf)


    def test_firmware_base_dir(self):
        pconf = PolypyConfig()
        pconf.add_search_path(os.path.join(os.path.dirname(__file__), "fixtures/issue_31"))
        pconf.find()
        pconf.load()
        pconf.json['paths']['tftproot'] = "b3f2bf18-0f6f-4069-9ef0-44b30de2b477"
        meta = ModelMeta()
        meta.use_configs(pconf)

        self.assertEqual("b3f2bf18-0f6f-4069-9ef0-44b30de2b477/firmware", meta.get_firmware_base_dir())
        meta.get_firmware_base_dir = MagicMock(return_value="a8d3392d-0f5c-4804-920b-a04fa1edf1bd/firmware")
        self.assertEqual("a8d3392d-0f5c-4804-920b-a04fa1edf1bd/firmware", meta.get_firmware_base_dir())


if __name__ == '__main__':
    unittest.main()
