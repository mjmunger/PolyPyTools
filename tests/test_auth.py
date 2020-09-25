import unittest
import os
from unittest_data_provider import data_provider
from poly_py_tools.pjsip.auth import Auth


class TestAuth(unittest.TestCase):

    provider_test_init = lambda :(
        #section                                                                                                                                                                                   expected_attributes
        (["[authtest]", "auth_type = tEyO", "nonce_lifetime = qhY8jc", "md5_cred = YuqmdQ7CBCC0CBe5jew", "password = Z91Eboob", "realm = dYu6eW", "type = ut3DM6iplGwt9F2yC", "username = MO39W"], {"auth_type":"tEyO", "nonce_lifetime":"qhY8jc", "md5_cred":"YuqmdQ7CBCC0CBe5jew", "password":"Z91Eboob", "realm":"dYu6eW", "type":"ut3DM6iplGwt9F2yC", "username":"MO39W"}, 'authtest'),
    )

    @data_provider(provider_test_init)
    def test_init(self, section, expected_attributes, expected_section_name):

        auth = Auth(section)
        self.assertEqual(section, auth.section)

        auth.set_attributes()

        self.assertEqual(expected_section_name, auth.section_name)

        for attribute in expected_attributes:
            expected_value = expected_attributes[attribute]
            actual_value = getattr(auth, attribute)
            self.assertEqual(expected_value, actual_value, "auth.{} should be {}. Got {} instead.".format(attribute, expected_value, actual_value))

    def test_render(self):
        auth = Auth("")
        auth.new_section("auth6001")
        auth.auth_type = "userpass"
        auth.password = "2034c37e"
        auth.username = "dd341d078cfd"
        auth.label = "Line 1"
        auth.order = 2

        f = open(os.path.join(os.path.dirname(__file__), "fixtures/pjsip/expected_rendered_auth_6001.conf"), 'r')
        buffer = f.read()
        f.close()

        expected_section = "".join(buffer)

        self.assertEqual(expected_section, auth.render())

if __name__ == '__main__':
    unittest.main()
