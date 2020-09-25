import unittest

from unittest_data_provider import data_provider

from poly_py_tools.container import Container
from poly_py_tools.polypy_config import PolypyConfig


class TestContainer(unittest.TestCase):
    provider_test_add = lambda : (
        ('poly_py_tools.polypy_config', "PolypyConfig", "c816533f5adce5144804245de30b5174", 1, None),
        ('poly_py_tools.polypy_config', "PolypyConfig", "c816533f5adce5144804245de30b5174", 1, Container()),
    )

    @data_provider(provider_test_add)
    def test_add(self, library, classname, expected_hash, expected_dict_length, expected_constructor):

        container = Container()
        if expected_constructor is None:
            container.add(library, classname)
        else:
            container.add(library, classname, expected_constructor)

        self.assertEqual(expected_dict_length, len(container.dict))

        key, classlist = container.dict.popitem()
        key, args = container.constructors.popitem()

        expected_classlist = [library, classname]

        self.assertEqual(expected_hash, key)
        self.assertEqual(expected_classlist, classlist)
        self.assertEqual(expected_constructor, args)

    provider_test_get = lambda : (
        ( "PolypyConfig", None, PolypyConfig),
    )

    @data_provider(provider_test_get)
    def test_get(self, expected_classname, constructor, expected_class_type):
        container = Container()
        container.add("poly_py_tools.polypy_config", "PolypyConfig", constructor)
        object = container.get("PolypyConfig")

        self.assertTrue(isinstance(object, expected_class_type))


if __name__ == '__main__':
    unittest.main()
