import io
import sys
import unittest

from unittest_data_provider import data_provider

from poly_py_tools.loggable import Loggable


class TestLoggable(unittest.TestCase):
    def test_set_debug(self):
        loggable = Loggable()
        loggable.set_debug()
        self.assertTrue(loggable.debug_mode)
        self.assertEqual(10, loggable.verbosity)

    def test_set_verbosity(self):
        loggable = Loggable()
        self.assertEqual(0, loggable.verbosity)
        loggable.set_verbosity(7)
        self.assertEqual(7, loggable.verbosity)

    provder_test_log_message = lambda : (
        ( 0, 3, "5485f8cf-c496-4b27-9196-477ccbc5738a", ""),
        ( 3, 3, "2a12283e-56ad-47de-920c-bf1bed1c1ddd", "2a12283e-56ad-47de-920c-bf1bed1c1ddd\n"),
        ( 10, 3, "5638f987-236d-4b98-bc81-bd76b4072cad", "5638f987-236d-4b98-bc81-bd76b4072cad\n"),
    )

    @data_provider(provder_test_log_message)
    def test_log_message(self, current_verbosity, required_verbosity, message, expected_output):
        loggable = Loggable()
        loggable.set_verbosity(current_verbosity)

        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out

        loggable.log(message, required_verbosity)

        output = out.getvalue()
        self.assertEqual(expected_output, output)



if __name__ == '__main__':
    unittest.main()
