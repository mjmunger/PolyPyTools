import unittest
from unittest_data_provider import data_provider
from poly_py_tools.directory_item import DirectoryItem

class TestDirectoryItem(unittest.TestCase):
    provider_test_render = lambda : (
        # model     last_name first_name, contact,      speed_dial, label,      protocol, ring_tone, divert_contact, auto_divert, auto_reject, buddy_watch, buddy_block, expected_item
        ("SPIP670", "Young",  "Eric",     "7704474556", 239,        "",         "",       12,        "",             0,           0,           0,           0,            "    <item>\n      <ln>Young</ln>\n      <fn>Eric</fn>\n      <ct>7704474556</ct>\n      <sd>239</sd>\n      <lb></lb>\n      <rt>12</rt>\n      <dc></dc>\n      <ad>0</ad>\n      <ar>0</ar>\n      <bw>0</bw>\n      <bb>0</bb>\n    </item>"),
        ("SPIP670", "Young",  "Eric",     "7704474556", 239,        "",         "ASDF",   12,        "",             0,           0,           0,           0,            "    <item>\n      <ln>Young</ln>\n      <fn>Eric</fn>\n      <ct>7704474556</ct>\n      <sd>239</sd>\n      <lb></lb>\n      <rt>12</rt>\n      <dc></dc>\n      <ad>0</ad>\n      <ar>0</ar>\n      <bw>0</bw>\n      <bb>0</bb>\n    </item>"),
        ("VVX1500", "Young",  "Eric",     "7704474556", 239,        "e323757f", "h.323",  12,        "",             0,           0,           0,           0,            "    <item>\n      <ln>Young</ln>\n      <fn>Eric</fn>\n      <ct>7704474556</ct>\n      <sd>239</sd>\n      <lb>e323757f</lb>\n      <pt>h.323</pt>\n      <rt>12</rt>\n      <dc></dc>\n      <ad>0</ad>\n      <ar>0</ar>\n      <bw>0</bw>\n      <bb>0</bb>\n    </item>"),
        ("VVX500",  "Young",  "Eric",     "7704474556", 239,        "38cb",     "h.323",  12,        "",             0,           0,           0,           0,            "    <item>\n      <ln>Young</ln>\n      <fn>Eric</fn>\n      <ct>7704474556</ct>\n      <sd>239</sd>\n      <lb>38cb</lb>\n      <pt>h.323</pt>\n      <rt>12</rt>\n      <dc></dc>\n      <ad>0</ad>\n      <ar>0</ar>\n      <bw>0</bw>\n      <bb>0</bb>\n    </item>"),
        ("VVX600",  "Young",  "Eric",     "7704474556", 239,        "44ef",     "h.323",  12,        "",             0,           0,           0,           0,            "    <item>\n      <ln>Young</ln>\n      <fn>Eric</fn>\n      <ct>7704474556</ct>\n      <sd>239</sd>\n      <lb>44ef</lb>\n      <pt>h.323</pt>\n      <rt>12</rt>\n      <dc></dc>\n      <ad>0</ad>\n      <ar>0</ar>\n      <bw>0</bw>\n      <bb>0</bb>\n    </item>"),
    )


    @data_provider(provider_test_render)
    def test_render(self, model, last_name, first_name, contact, speed_dial, label, protocol, ring_tone, divert_contact,
                    auto_divert, auto_reject, buddy_watch, buddy_block, expected_item):

        this_item = DirectoryItem(model, last_name, first_name, contact, label, protocol, ring_tone,
                                  divert_contact, auto_divert, auto_reject, buddy_watch, buddy_block)
        this_item.speed_dial = speed_dial

        self.assertEqual(expected_item, this_item.render())


if __name__ == '__main__':
    unittest.main()
