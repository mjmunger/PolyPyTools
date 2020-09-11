import io
import unittest
import os
import sys
import shutil
import xml.etree.ElementTree as ET

from docopt import docopt
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision_factory import ProvisionFactory


class TestIssue36(unittest.TestCase):

    debug = False

    def issue_tftproot(self):
        return os.path.join(self.issue_base(), 'tftproot')

    def issue_asterisk(self):
        return os.path.join(self.issue_base(), 'asterisk')

    def site_dir(self):
        return os.path.join(self.issue_tftproot(), "com-l-3-office")

    def setUp(self) -> None:

        if not os.path.exists(self.issue_tftproot()):
            os.mkdir(self.issue_tftproot())

        if not os.path.exists(self.issue_asterisk()):
            os.mkdir(self.issue_asterisk())

        src = os.path.join(self.issue_base(), 'pjsip.conf')
        dst = os.path.join(self.issue_asterisk(), 'pjsip.conf')

        shutil.copy(src, dst)

    def tearDown(self) -> None:
        if self.debug is True:
            return None

        if os.path.exists(self.issue_tftproot()):
            shutil.rmtree(self.issue_tftproot())

        if os.path.exists(self.issue_asterisk()):
            shutil.rmtree(self.issue_asterisk())

    def issue_base(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/issue_36")

    def test_issue_36(self):
        command = "polypy provision polycom 0004f2e62aa4"
        argv = command.split(" ")
        sys.argv = argv

        # Container is reset in site.py. This is so we can mock things.
        container = {}
        pconf = PolypyConfig()
        pconf.add_search_path(self.issue_base())
        pconf.find()
        pconf.load()
        pconf.json['paths']['tftproot'] = os.path.join(self.issue_base(), 'tftproot')

        container['pconf'] = pconf

        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out

        # Should match site.py's script. Mocking should go before here.
        from poly_py_tools.provision.provision import P
        args = docopt(provision.__doc__, argv=argv)
        container['<args>'] = args
        container['meta'] = ModelMeta()

        sip_resource_factory = SipResourceFactory()
        factory = ProvisionFactory()
        parser = PjSipSectionParser()
        parser.use_config(pconf)
        parser.use_factory(sip_resource_factory)

        args['pjsipsectionparser'] = parser
        args['pconf'] = pconf

        factory = ProvisionFactory()
        runner = factory.get_runner(args)


        # Do assertions for setup prior to run here
        # self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        runner.run()

        # Post run assertions
        output = out.getvalue()
        # self.assertEqual(expected_output, output)

        #Make sure we have <reg> entries in the output file.

        config_file = os.path.join(self.site_dir(), "0004f2e62aa4")

        self.assertTrue(os.path.exists(config_file))

        tree = ET.parse(config_filed)
        root = tree.getroot()
        print(root.tag)




if __name__ == '__main__':
    unittest.main()
