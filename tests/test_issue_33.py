import unittest
import os
import shutil

from pwgen_secure.rpg import Rpg

from poly_py_tools.pjsip.pjsip_factory import PJSipFactory
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy import Polypy
from poly_py_tools.polypy_config import PolypyConfig


class TestIssue33(unittest.TestCase):

    @staticmethod
    def issue_root():
        return os.path.join(os.path.dirname(__file__), "fixtures/issue_33")

    @staticmethod
    def asterisk_dir():
        return os.path.join(TestIssue33.issue_root(), "asterisk")

    def setUp(self) -> None:
        if not os.path.exists(TestIssue33.asterisk_dir()):
            os.mkdir(TestIssue33.asterisk_dir())

    # def tearDown(self) -> None:
    #     if os.path.exists(TestIssue33.asterisk_dir()):
    #         shutil.rmtree(TestIssue33.asterisk_dir())

    def test_issue_33(self):

        args = {'--force': False,
                 '-d': True,
                 '-v': 0,
                 '<column>': None,
                 '<extension>': '111',
                 '<file>': os.path.join(TestIssue33.issue_root(), 'DialPlanBuilder-L3_pbx_v1.csv'),
                 '<template>': None,
                 'assign': False,
                 'column': False,
                 'from': True,
                 'generate': True,
                 'pjsip': True,
                 'template': False,
                 'use': False,
                 'voicemail': False,
                 'with': False}

        # <Original pjsip.py content>
        pconf = PolypyConfig()
        pconf.add_search_path(TestIssue33.issue_root()) # was /etc/polypy
        pconf.find()
        pconf.load()

        # <mocks>
        pconf.update_paths("asterisk", TestIssue33.asterisk_dir())
        # <mocks>


        args['config'] = pconf
        args['<args>'] = args
        args['rpg'] = Rpg("strong", None)

        factory = PJSipFactory()
        runner = factory.get_runner(args)
        runner.run()
        # </Original pjsip.py content>

        parser = PjSipSectionParser()
        parser.use_config(pconf)
        parser.use_factory(SipResourceFactory())
        parser.parse()

        sections = {}
        for resource in parser.resources:
            if not resource.section_name in sections:
                sections[resource.section_name] = 1
            else:
                sections[resource.section_name] = sections[resource.section_name] + 1

        for section in sections:
            self.assertEqual(1, sections[section], "Section {} is duplicated, and will break asterisk".format(section))

        endpoint_count = 0
        for resource in parser.resources:
            if resource.type == 'endpoint':
                endpoint_count = endpoint_count + 1

        self.assertEqual(21, endpoint_count)

        ppc_phones = []
        rich = parser.get_endpoint("0004f23a3f53")
        ava = parser.get_endpoint("0004f23a5515")
        doris = parser.get_endpoint("0004f23a43bf")

        for phone in ppc_phones:
            self.assertEqual(2, len(phone.auth.split(",")))
            self.assertEqual(2, len(phone.aors.split(",")))









if __name__ == '__main__':
    unittest.main()
