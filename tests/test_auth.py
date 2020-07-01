import unittest
from unittest_data_provider import data_provider
from poly_py_tools.pjsip_auth import Auth


class TestAuth(unittest.TestCase):

    provider_test_init = lambda :(
        #section                                                                                                                                                                                   expected_attributes
        (["[authtest]", "auth_type = tEyO", "nonce_lifetime = qhY8jc", "md5_cred = YuqmdQ7CBCC0CBe5jew", "password = Z91Eboob", "realm = dYu6eW", "type = ut3DM6iplGwt9F2yC", "username = MO39W"], {"auth_type":"tEyO", "nonce_lifetime":"qhY8jc", "md5_cred":"YuqmdQ7CBCC0CBe5jew", "password":"Z91Eboob", "realm":"dYu6eW", "type":"ut3DM6iplGwt9F2yC", "username":"MO39W"}),
    )

    @data_provider(provider_test_init)
    def test_init(self, section, expected_attributes):

        auth = Auth(section)
        self.assertEqual(section, auth.section)

        auth.set_attributes()

        for attribute in expected_attributes:
            expected_value = expected_attributes[attribute]
            actual_value = getattr(auth, attribute)
            self.assertEqual(expected_value, actual_value, "auth.{} should be {}. Got {} instead.".format(attribute, expected_value, actual_value))


if __name__ == '__main__':
    unittest.main()
