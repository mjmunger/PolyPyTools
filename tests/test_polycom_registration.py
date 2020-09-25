import unittest

from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.auth import Auth
from poly_py_tools.provision.polycom_registration import PolycomRegistration


class TestPolycomRegistration(unittest.TestCase):

    def test_set_aor(self):
        pr = PolycomRegistration()
        aor = Aor("0004f23a626f102")
        aor.max_contacts = 1
        aor.type = "aor"

        pr.set_aor(aor)
        self.assertEqual(aor, pr.aor)

    def test_set_auth(self):
        pr = PolycomRegistration()

        auth = Auth("auth0004f23a626f102")
        auth.type = "auth"
        auth.auth_type = "userpass"
        auth.username = "0004f23a626f102"
        auth.password = "mHQFrPS"
        auth.label = "Label asdf"
        self.order = auth.order
        pr.set_auth(auth)

        self.assertEqual(pr.label, auth.label)
        self.assertEqual(auth, pr.auth)

    def test_set_proxy(self):
        pr = PolycomRegistration()
        pr.set_sip_server("128ba85c-c7fd-4943-a263-71a357087699")
        self.assertEqual("128ba85c-c7fd-4943-a263-71a357087699", pr.sip_server)

    def test_set_label(self):
        line_label = "ca141c69-7c18-4174-9b79-0ccf1065bfee"
        pr = PolycomRegistration()
        pr.set_label(line_label)
        self.assertEqual(line_label, pr.label)

    def test_hydrate(self):
        pr = PolycomRegistration()

        aor = Aor("0004f23a626f102")
        aor.max_contacts = 1
        aor.type = "aor"

        auth = Auth("auth0004f23a626f102")
        auth.type = "auth"
        auth.auth_type = "userpass"
        auth.username = "0004f23a626f102"
        auth.password = "mHQFrPS"
        auth.label = "Line 1"
        auth.order = 1

        sip_server = "a63d31a6-0b4a-49e8-9c67-02934706568c"

        pr.set_aor(aor)
        pr.set_auth(auth)
        pr.set_sip_server(sip_server)
        pr.hydrate()

        expected_address = "{}@{}".format(auth.username, sip_server)

        self.assertEqual(expected_address, pr.registration_address)
        self.assertEqual(auth.username, pr.userId)
        self.assertEqual(auth.password, pr.password)
        self.assertEqual(auth.label, pr.label)


if __name__ == '__main__':
    unittest.main()
