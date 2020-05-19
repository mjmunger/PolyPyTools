import unittest
from unittest_data_provider import data_provider
from poly_py_tools.directory_item import DirectoryItem
from poly_py_tools.directory import Directory


class TestPhoneDirectory(unittest.TestCase):

    provider_test_directory_render = lambda: (
        # count, mac_addr,       model      last      first   contact      label,      protocol, ring_tone, divert_contact, auto_divert, auto_reject, buddy_watch, buddy_block, expected_item
        (1,      "bac58fc0b629", "SPIP670", "Young", "Eric", "7704474556", "e323757f", "",       12,        "",             0,           0,           0,           0,           "<directory>\n  <item_list>\n    <item>\n      <ln>Young</ln>\n      <fn>Eric</fn>\n      <ct>7704474556</ct>\n      <sd>1</sd>\n      <lb>e323757f</lb>\n      <rt>12</rt>\n      <dc></dc>\n      <ad>0</ad>\n      <ar>0</ar>\n      <bw>0</bw>\n      <bb>0</bb>\n    </item>\n  </item_list>\n</directory>"),
        (3,      "bac58fc0b629", "SPIP670", "Young", "Eric", "7704474556", "e323757f", "",       12,        "",             0,           0,           0,           0,           "<directory>\n  <item_list>\n    <item>\n      <ln>Young</ln>\n      <fn>Eric</fn>\n      <ct>7704474556</ct>\n      <sd>1</sd>\n      <lb>e323757f</lb>\n      <rt>12</rt>\n      <dc></dc>\n      <ad>0</ad>\n      <ar>0</ar>\n      <bw>0</bw>\n      <bb>0</bb>\n    </item>\n    <item>\n      <ln>Young</ln>\n      <fn>Eric</fn>\n      <ct>7704474556</ct>\n      <sd>2</sd>\n      <lb>e323757f</lb>\n      <rt>12</rt>\n      <dc></dc>\n      <ad>0</ad>\n      <ar>0</ar>\n      <bw>0</bw>\n      <bb>0</bb>\n    </item>\n    <item>\n      <ln>Young</ln>\n      <fn>Eric</fn>\n      <ct>7704474556</ct>\n      <sd>3</sd>\n      <lb>e323757f</lb>\n      <rt>12</rt>\n      <dc></dc>\n      <ad>0</ad>\n      <ar>0</ar>\n      <bw>0</bw>\n      <bb>0</bb>\n    </item>\n  </item_list>\n</directory>"),
        (2,      "bac58fc0b629", "SPIP670", "Young", "Eric", "7704474556", "e323757f", "", 12, "", 0, 0, 0, 0,
         "<directory>\n  <item_list>\n    <item>\n      <ln>Young</ln>\n      <fn>Eric</fn>\n      <ct>7704474556</ct>\n      <sd>1</sd>\n      <lb>e323757f</lb>\n      <rt>12</rt>\n      <dc></dc>\n      <ad>0</ad>\n      <ar>0</ar>\n      <bw>0</bw>\n      <bb>0</bb>\n    </item>\n    <item>\n      <ln>Young</ln>\n      <fn>Eric</fn>\n      <ct>7704474556</ct>\n      <sd>2</sd>\n      <lb>e323757f</lb>\n      <rt>12</rt>\n      <dc></dc>\n      <ad>0</ad>\n      <ar>0</ar>\n      <bw>0</bw>\n      <bb>0</bb>\n    </item>\n  </item_list>\n</directory>"),
    )

    @data_provider(provider_test_directory_render)
    def test_directory_render(self, count, mac_addr, model, last, first, contact, label, protocol, ring_tone, divert_contact,
                              auto_divert, auto_reject, buddy_watch, buddy_block, expected_item):

        directory = None
        directory_item = None
        directory = Directory(mac_addr)
        directory_item = DirectoryItem(model, last, first, contact, label, protocol, ring_tone, divert_contact,
                              auto_divert, auto_reject, buddy_watch, buddy_block)
        for i in range(1, count+1):
            directory.add_item(directory_item)

        self.assertEqual(count, len(directory.items))
        self.assertEqual(expected_item, directory.render())


if __name__ == '__main__':
    unittest.main()
