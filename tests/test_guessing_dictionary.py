import unittest
from unittest_data_provider import data_provider


class TestGuessingDictionary(unittest.TestCase):

    def test__init(self):
        dictionary = Dictionary()
        dictionary.use_config(config)

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
