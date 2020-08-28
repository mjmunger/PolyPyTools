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
        (["[6001]", "type=endpoint"], "endpoint", Endpoint, False),
        (["[simpletrans]", "type=transport"], "transport", Transport, False),
        (["[auth6001]", "type=auth"], "auth", Auth, False),
        (["[6001]", "type=aor"], "aor", Aor, False),
        (["[mytrunk]", "type=registration"], "registration", Registration, False),
        (["[example2.com]", "type=domain_alias"], "domain_alias", DomainAlias, False),
        (["[acl]", "type=acl"], "acl", Acl, False),
        (["[6001](!)", "type=contact"], "contact", Contact, True),
        (["[6001](!)", "type=endpoint"], "endpoint", Endpoint, True),
        (["[simpletrans](!)", "type=transport"], "transport", Transport, True),
        (["[auth6001](!)", "type=auth"], "auth", Auth, True),
        (["[6001](!)", "type=aor"], "aor", Aor, True),
        (["[mytrunk](!)", "type=registration"], "registration", Registration, True),
        (["[example2.com](!)", "type=domain_alias"], "domain_alias", DomainAlias, True),
        (["[acl](!)", "type=acl"], "acl", Acl, True),
        (["[6001](!)", "type=contact"], "contact", Contact, True),
    )
    @data_provider(provider_section_meta)
    def test_extract_type(self, section, expected_type, expected_class, is_template):
        factory = SipResourceFactory()
        self.assertEqual(expected_type, factory.extract_type(section))

    @data_provider(provider_section_meta)
    def test_create(self, section, expected_type, expected_class, is_template):
        factory = SipResourceFactory()
        object = factory.create(section)
        object.set_attributes()
        self.assertTrue(isinstance(object, expected_class), "Object should have been of type {} for section {}.".format(expected_type, section[0]))
        self.assertEqual(expected_type, object.type, "Generated object {} should have the type ({}) set in itself.".format(expected_class, expected_type))
        self.assertEqual(is_template, object.is_template)

    provider_template_sections = lambda : (
        (["[com-l-3-office](!)", "type = endpoint", "context = com-l-3-office-local-stations", "allow = !all,g722,ulaw", "direct_media = no", "trust_id_outbound = yes", "device_state_busy_at = 1", "dtmf_mode = rfc4733"], True, Endpoint, "com-l-3-office" ),
        (["[0004f23a626f](com-l-3-office)", ";mac=0004f23a626f", ";model=670", ";extension=101", "auth=auth0004f23a626f101", "aors=0004f23a626f101", "callerid=Levine John<101>"], True, None, None),
    )

    @data_provider(provider_template_sections)
    def test_create_templates(self, section, is_template, expected_class, expected_template_name):
        factory = SipResourceFactory()
        object = factory.create_template(section)

        if not expected_class is None:
            self.assertEqual(is_template, isinstance(object, expected_class))
            self.assertEqual(expected_template_name, object.section_name)

    @staticmethod
    def provider_sections_with_templates_helper():
        section_templates = [
                                ['[com-l-3-office](!)', 'type = endpoint', 'context = com-l-3-office-local-stations',
                                 'allow = !all,g722,ulaw', 'direct_media = no', 'trust_id_outbound = yes', 'device_state_busy_at = 1',
                                 'dtmf_mode = rfc4733'],
                                ['[com-l-3-eastern](!)', 'type = endpoint', 'context = com-l-3-eastern-local-stations',
                                 'allow = !all,g722,ulaw', 'direct_media = no', 'trust_id_outbound = yes', 'device_state_busy_at = 1',
                                 'dtmf_mode = rfc4733'],
                                ['[com-l-3-central](!)', 'type = endpoint', 'context = com-l-3-central-local-stations',
                                 'allow = !all,g722,ulaw', 'direct_media = no', 'trust_id_outbound = yes', 'device_state_busy_at = 1',
                                 'dtmf_mode = rfc4733']
                            ]
        return (
        (section_templates, ['[0004f23a626f](com-l-3-office)', 'mac=0004f23a626f', 'model=SPIP670', 'auth=auth0004f23a626f101', 'aors=0004f23a626f101', 'callerid=Levine John<101>'], Endpoint),
        (section_templates, ['[0004f25fb5c3](com-l-3-central)', 'mac=0004f25fb5c3', 'model=SPIP670', 'auth=auth0004f25fb5c3118', 'aors=0004f25fb5c3118', 'callerid=Norrell Adam<118>'], Endpoint),
        (section_templates, ['[0004f23a5515](com-l-3-eastern)', 'mac=0004f23a5515', 'model=SPIP670', 'auth=auth0004f23a5515103', 'aors=0004f23a5515103', 'callerid=Maguire Ava<103>'], Endpoint),
    )

    provider_sections_with_templates = lambda : TestSipResourceFactory.provider_sections_with_templates_helper()

    @data_provider(provider_sections_with_templates)
    def test_template_entries(self, templates, section, expected_class):
        factory = SipResourceFactory()
        endpoint_templates = []
        for template in templates:
            endpoint_templates.append(factory.create_template(template))

        self.assertEqual(3, len(endpoint_templates))
        for ept in endpoint_templates:
            self.assertTrue(isinstance(ept, Endpoint))

        factory.use_templates(endpoint_templates)
        object = factory.create(section)
        self.assertTrue(isinstance(object, expected_class))


    def test_use_templates(self):
        factory = SipResourceFactory()
        template1 = Endpoint("section1")
        template2 = Endpoint("section2")
        template3 = Endpoint("section3")
        templates = [template1, template2, template3]
        factory.use_templates(templates)
        self.assertEqual(3, len(factory.templates))

    def test_get_template(self):
        factory = SipResourceFactory()

        template1 = Endpoint(["[section1](!)", "type=endpoint"])
        template1.set_attributes()

        template2 = Endpoint(["[section2](!)", "type=endpoint"])
        template2.set_attributes()

        template3 = Endpoint(["[section3](!)", "type=endpoint"])
        template3.set_attributes()

        templates = [template1, template2, template3]
        factory.use_templates(templates)
        template = factory.get_template_for_section("[example]( section1 )")
        self.assertIsNotNone(template, "Template should not be None!")
        self.assertEqual("section1", template.section_name)

if __name__ == '__main__':
    unittest.main()
