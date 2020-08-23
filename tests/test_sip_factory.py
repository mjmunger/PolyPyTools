import unittest

from unittest_data_provider import data_provider


class TestSipFactory(unittest.TestCase):

    provider_test_get_runner = lambda : (
        ([], []),
    )

    @data_provider(provider_test_get_runner)
    def test_get_runner(self, args, expected_class):
        self.skipTest("Not developed yet.")


if __name__ == '__main__':
    unittest.main()
