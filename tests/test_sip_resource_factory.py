import unittest
from unittest_data_provider import data_provider
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.transport import Transport
from poly_py_tools.pjsip.auth import Auth
from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.registration import Registration
from poly_py_tools.pjsip.domain_alias import DomainAlias
from poly_py_tools.pjsip.acl import Acl
from poly_py_tools.pjsip.contact import Contact
from poly_py_tools.pjsip.resource_factory import SipResourceFactory


class TestSipResourceFactory(unittest.TestCase):

    provider_section_meta = lambda : (
        (["[6001]", "type=endpoint"], "endpoint", Endpoint),
        (["[simpletrans]", "type=transport"], "transport", Transport),
        (["[auth6001]", "type=auth"], "auth", Auth),
        (["[6001]", "type=aor"], "aor", Aor),
        (["[mytrunk]", "type=registration"], "registration", Registration),
        (["[example2.com]", "type=domain_alias"], "domain_alias", DomainAlias),
        (["[acl]", "type=acl"], "acl", Acl),
        (["[6001]", "type=contact"], "contact", Contact),
    )

    @data_provider(provider_section_meta)
    def test_extract_type(self, section, expected_type, expected_class):
        factory = SipResourceFactory()
        self.assertEqual(expected_type, factory.extract_type(section))



    @data_provider(provider_section_meta)
    def test_create(self, section, expected_type, expected_class):
        factory = SipResourceFactory()
        object = factory.create(section)
        object.set_attributes()
        self.assertTrue(isinstance(object, expected_class), "Object should have been of type {} for section {}.".format(expected_type, section[0]))
        self.assertEqual(expected_type, object.type, "Generated object {} should have the type ({}) set in itself.".format(expected_class, expected_type))


if __name__ == '__main__':
    unittest.main()
