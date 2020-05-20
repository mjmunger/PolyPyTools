import unittest
from unittest_data_provider import data_provider
from poly_py_tools.deploy import Deploy


class TestDeploy(unittest.TestCase):

    provider_test_init = lambda : (
        # customer               expected_directory
        ("masseyautomotive.com", "com-masseyautomotive"),
    )

    @data_provider(provider_test_init)
    def test_init(self, customer_domain, expected_directory):
        deploy = Deploy(customer_domain)
        self.assertEqual(deploy.customer_domain, customer_domain)
        self.assertEqual(deploy.provisioned_directory, expected_directory)


if __name__ == '__main__':
    unittest.main()
