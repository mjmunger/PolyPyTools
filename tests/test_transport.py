import unittest
from unittest_data_provider import data_provider
from poly_py_tools.pjsip.transport import Transport


class TestTransport(unittest.TestCase):

    provider_test_init = lambda :(
        #section                                                                                                                                                                                   expected_attributes
        (["[sampletransport]", "async_operations=BwBCL4", "bind=5UIfQtXOX", "ca_list_file=mUMG8", "cert_file=4pSIS", "cipher=Q6w8SVxMMaNmyXMXI4iK", "domain=MPB", "external_media_address=7P9cAxJUBJJz66fHAXsA", "external_signaling_address=IcGKw", "external_signaling_port=egggXpOjpdGfqc1", "method=zAOasIGWr2GepUy4", "local_net=y9tJYJtVK", "password=L9mJD7RzIX", "priv_key_file=QFy6Rcnx1x5AvkIVom", "protocol=jA0JTSjqYFb0iLDs", "require_client_cert=DUdQlqZu5hUdpSXZ", "type=YIQjFDSXWfVku", "verify_client=4Ey2EjhN3XYbFD8ufl", "verify_server=XONxHpKl", "tos=Td2", "cos=kqBcmurbLzz", "websocket_write_timeout=U6PKOX7fAFCrrie2dF"], {"async_operations":"BwBCL4", "bind":"5UIfQtXOX", "ca_list_file":"mUMG8", "cert_file":"4pSIS", "cipher":"Q6w8SVxMMaNmyXMXI4iK", "domain":"MPB", "external_media_address":"7P9cAxJUBJJz66fHAXsA", "external_signaling_address":"IcGKw", "external_signaling_port":"egggXpOjpdGfqc1", "method":"zAOasIGWr2GepUy4", "local_net":"y9tJYJtVK", "password":"L9mJD7RzIX", "priv_key_file":"QFy6Rcnx1x5AvkIVom", "protocol":"jA0JTSjqYFb0iLDs", "require_client_cert":"DUdQlqZu5hUdpSXZ", "type":"YIQjFDSXWfVku", "verify_client":"4Ey2EjhN3XYbFD8ufl", "verify_server":"XONxHpKl", "tos":"Td2", "cos":"kqBcmurbLzz", "websocket_write_timeout":"U6PKOX7fAFCrrie2dF"}),
    )

    @data_provider(provider_test_init)
    def test_init(self, section, expected_attributes):

        transport = Transport(section)
        self.assertEqual(section, transport.section)

        transport.set_attributes()

        for attribute in expected_attributes:
            expected_value = expected_attributes[attribute]
            actual_value = getattr(transport, attribute)
            self.assertEqual(expected_value, actual_value, "endpoint.{} should be {}. Got {} instead.".format(attribute, expected_value, actual_value))


if __name__ == '__main__':
    unittest.main()
