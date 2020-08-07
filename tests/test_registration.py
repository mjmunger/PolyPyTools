import unittest
from unittest_data_provider import data_provider
from poly_py_tools.pjsip.registration import Registration


class TestRegistration(unittest.TestCase):

    provider_test_init = lambda :(
        #section                                                                                                                                                                                   expected_attributes
        (["[sampleregistration]", "auth_rejection_permanent=guXSdpKW2wE", "client_uri=2mBnJnj6wgjCLuDI", "contact_user=YRVGCVzwXk4", "expiration=7ArVv0onh8O1", "max_retries=Y9pZ7klMRC9yzrIpdWyu", "outbound_auth=h6b8", "outbound_proxy=wuVq29s3uj", "retry_interval=voMjnDhmWWtYPu", "forbidden_retry_interval=VsGaPNxjtZAkf", "server_uri=fyfxqkMPF2", "transport=dYGExK0Shm0sZp6BBP", "type=7l4HhHJmIOiy5u3P", "support_path=pw9sKuNvamdb3hCJF"], {"auth_rejection_permanent":"guXSdpKW2wE", "client_uri":"2mBnJnj6wgjCLuDI", "contact_user":"YRVGCVzwXk4", "expiration":"7ArVv0onh8O1", "max_retries":"Y9pZ7klMRC9yzrIpdWyu", "outbound_auth":"h6b8", "outbound_proxy":"wuVq29s3uj", "retry_interval":"voMjnDhmWWtYPu", "forbidden_retry_interval":"VsGaPNxjtZAkf", "server_uri":"fyfxqkMPF2", "transport":"dYGExK0Shm0sZp6BBP", "type":"7l4HhHJmIOiy5u3P", "support_path":"pw9sKuNvamdb3hCJF"}),
    )

    @data_provider(provider_test_init)
    def test_init(self, section, expected_attributes):

        registration = Registration(section)
        self.assertEqual(section, registration.section)

        registration.set_attributes()

        for attribute in expected_attributes:
            expected_value = expected_attributes[attribute]
            actual_value = getattr(registration, attribute)
            self.assertEqual(expected_value, actual_value, "endpoint.{} should be {}. Got {} instead.".format(attribute, expected_value, actual_value))


if __name__ == '__main__':
    unittest.main()
