import unittest
from unittest import mock
from unittest.mock import Mock, MagicMock

from poly_py_tools.pjsip.template import Template
from poly_py_tools.dialplan_entry import Entry
from poly_py_tools.polypy_config import PolypyConfig


class TestTemplate(unittest.TestCase):
    def test_from_entry(self):
        config = PolypyConfig()
        config.config = {}
        config.config['csvmap'] = "none"
        config.__init__ = MagicMock(return_value=True)

        entry = Entry(config)
        entry.last = "Grune"
        entry.first = "Ike"
        entry.startrow = "212 - 555 - 1234"
        entry.exten = "1001"
        entry.vm = "2001"
        entry.did = "2001"
        entry.group_dial = "212 - 555 - 9955"
        entry.endpoint = "SPIP650"
        entry.mac = "e22908208d62"
        entry.email = "ike@example.org"
        entry.site = "atl.example.org"
        entry.cid_number = "1001"
        entry.label = "1001"
        entry.priority = "1"

        expected_template = "[org-example-atl](!)\ntype = endpoint\ncontext = org-example-atl-local-stations\nallow = !all,g722,ulaw\ndirect_media = no\ntrust_id_outbound = yes\ndevice_state_busy_at = 1\ndtmf_mode = rfc4733"

        template = Template()
        template.from_entry(entry)
        self.assertEqual(expected_template, str(template))



if __name__ == '__main__':
    unittest.main()
