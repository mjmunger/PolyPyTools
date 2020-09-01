import unittest

from poly_py_tools.polypy_config import PolypyConfig


class TestIssue35(unittest.TestCase):
    def test_setup_sntp(self):

        args = {'--force': False,
                 '-d': False,
                 '-v': 0,
                 '<csvfile>': [],
                 '<macaddress>': '0004F2E62AA4',
                 'directory': False,
                 'endpoints': False,
                 'for': False,
                 'list': False,
                 'polycom': True,
                 'provision': True,
                 'using': False}

        pconf = PolypyConfig()
        pconf.add_search_path(self.issue_base())
        pconf.find()
        pconf.load()

        # Redirect output, etc... to issue_31 tmp directory
        pconf.update_paths("tftproot", os.path.join(self.issue_base(), "tftproot"))

        args['pconf'] = pconf
        args['<args>'] = args

        factory = ProvisionFactory()
        parser = PjSipSectionParser()
        parser.use_config(pconf)
        parser.use_factory(sip_resource_factory)

        args['pjsipsectionparser'] = parser
        runner = factory.get_runner(args)
        runner.run()

        tree = ET.parse(os.path.join(pconf.tftproot_path(), "com-l-3-office/0004f2e62aa4"))
        root = tree.getroot()

        self.assertEqual("polycomConfig", root.tag)

        reg = root.find("reg")
        addr = reg.attrib['reg.1.address']
        buffer = addr.split("@")
        self.assertEqual(buffer[1], "pbx.example.org", "reg.1.address should have pbx.hph.io as the server, found '{}' instead.".format(buffer[1]))

    def issue_base(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/issue_31")

if __name__ == '__main__':
    unittest.main()
