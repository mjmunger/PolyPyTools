import unittest
import os
import json
import shutil
from unittest.mock import MagicMock

from xml.dom import minidom
from xml.etree import ElementTree
from unittest_data_provider import data_provider

from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.auth import Auth
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta


class TestEndpoint(unittest.TestCase):

    def test_root(self):
        return os.path.join(os.path.dirname(__file__), 'fixtures/issue_36')

    def test_tftproot(self):
        return os.path.join(self.test_root(), 'tftproot')

    def test_asterisk(self):
        return os.path.join(self.test_root(), 'asterisk')

    def setUp(self) -> None:
        if not os.path.exists(self.test_tftproot()):
            os.mkdir(self.test_tftproot())

    def tearDown(self) -> None:
        if os.path.exists(self.test_tftproot()):
            shutil.rmtree(self.test_tftproot())

    provider_test_init = lambda: (
        # section                                                                                                                                                                                   expected_attributes
        (["[1234]", "model=SSIP7000", "mac=0004f23a43bf", "100rel=Jyl5aQ2zp0VCQwUA", "aggregate_mwi=uMuYIQnX",
          "allow=RadaiCnMtKfDef", "aors=nnj63k", "auth=RtK1MwZD6", "callerid=T9n", "callerid_privacy=tOeiVAvTp61mx",
          "callerid_tag=hjuHGReXzyMIBVqzeIf", "context=2NRpB", "direct_media_glare_mitigation=TXoZEhoqp5",
          "direct_media_method=ayF", "connected_line_method=VVe4GoxMG3ByJY5", "direct_media=zYEnS3aZwkwVM",
          "disable_direct_media_on_nat=6NClLUwI2OV9N", "disallow=3hgsB1YrOA2K9dgsAxer", "dtmf_mode=haJA4q9",
          "media_address=g4oHrspWAWOUAv", "force_rport=KL1BSA8sxIHEjIJrH", "ice_support=6EZ7K6M0f",
          "identify_by=sHT5LoSUL0JI96561Ym", "redirect_method=enBAGEH", "mailboxes=NPD", "moh_suggest=Ay800ZGIR4Sx3cn",
          "outbound_auth=BWmM9N1UynmWkYV4cwd2", "outbound_proxy=1KnxgfT", "rewrite_contact=kbyf1WV2x0B1Uew",
          "rtp_ipv6=rmIkmzMONfmA", "rtp_symmetric=eTYnUOegdnyJHk5", "send_diversion=9NATl", "send_pai=G4xN4a",
          "send_rpid=PnC5WqSWEQ6jsuPFN", "timers_min_se=sPP", "timers=0F38S2kevvIiyo", "timers_sess_expires=USNkosRLJ",
          "transport=wUufsy6C9FI7x", "trust_id_inbound=SmGFqxXpPT", "trust_id_outbound=TwEa5bzZPYsae9zuu", "type=mCP",
          "use_ptime=TaXY5GNLQhNa2I", "use_avpf=6YeQ16kd4", "force_avp=pVDffsVStBi", "media_use_received_transport=c1I",
          "media_encryption=DfgunEGr46MG", "inband_progress=oQD", "call_group=QzHz0t3X7Xgy5PaYV",
          "pickup_group=RYGg7aLIs6TJCifJf", "named_call_group=zPehn28V92sgS", "named_pickup_group=63dtH9FiDWQ4gn9cBmo",
          "device_state_busy_at=PpA9Zo0on5qquH", "t38_udptl=w280yj", "t38_udptl_ec=Q5g4Wk3u40GLC4",
          "t38_udptl_maxdatagram=h09FAJ3J", "fax_detect=CafruWUb9sdosqQnt", "t38_udptl_nat=qH0usAmG45BhicuA5G3",
          "t38_udptl_ipv6=ABRzOi0FCvg", "tone_zone=jOgC3Znh", "language=i5NsRW9wA", "one_touch_recording=rPVx",
          "record_on_feature=9UqyhzZL5Y3JGiGCI", "record_off_feature=L4LxqiSfWVbjtjFhTO",
          "rtp_engine=KuGAiiojWJq2SfLaBl", "allow_transfer=bmoLg9W6", "sdp_owner=kcw7z", "sdp_session=rsA6X",
          "tos_audio=o07hJCtWhiN8VzYVzVVy", "tos_video=rpTk1Slswv9", "cos_audio=MCe8aReDnGZ3KW8", "cos_video=oEAAk7bln",
          "allow_subscribe=nKlS3SzJf", "sub_min_expiry=ZuiLPJTaQy36Pgm9YgiQ", "from_user=XnjbEqf5Lc9",
          "mwi_from_user=KaZRECvQOtTnz", "from_domain=uGGZVBgzdQ", "dtls_verify=xFqxevOVHTWNGbY", "dtls_rekey=oS8ETR",
          "dtls_cert_file=XI1SGYC5", "dtls_private_key=lKs9zUzh50NJhuA6oE0", "dtls_cipher=bnvQRwE",
          "dtls_ca_file=1XMI9RB", "dtls_ca_path=LaLkcspFAcU", "dtls_setup=envEaRPuFwcX",
          "dtls_fingerprint=deRrBNCxnL0QAOrF", "srtp_tag_32=4qJ", "set_var=kN4ldR0gdk", "message_context=9WMjdjhs7pZm",
          "accountcode=weQrrYS4PAVg0yAd6uiw"],
         {"rel_100": "Jyl5aQ2zp0VCQwUA", "aggregate_mwi": "uMuYIQnX", "allow": "RadaiCnMtKfDef", "aors": "nnj63k",
          "auth": "RtK1MwZD6", "callerid": "T9n", "callerid_privacy": "tOeiVAvTp61mx",
          "callerid_tag": "hjuHGReXzyMIBVqzeIf", "context": "2NRpB", "direct_media_glare_mitigation": "TXoZEhoqp5",
          "direct_media_method": "ayF", "connected_line_method": "VVe4GoxMG3ByJY5", "direct_media": "zYEnS3aZwkwVM",
          "disable_direct_media_on_nat": "6NClLUwI2OV9N", "disallow": "3hgsB1YrOA2K9dgsAxer", "dtmf_mode": "haJA4q9",
          "media_address": "g4oHrspWAWOUAv", "force_rport": "KL1BSA8sxIHEjIJrH", "ice_support": "6EZ7K6M0f",
          "identify_by": "sHT5LoSUL0JI96561Ym", "redirect_method": "enBAGEH", "mailboxes": "NPD",
          "moh_suggest": "Ay800ZGIR4Sx3cn", "outbound_auth": "BWmM9N1UynmWkYV4cwd2", "outbound_proxy": "1KnxgfT",
          "rewrite_contact": "kbyf1WV2x0B1Uew", "rtp_ipv6": "rmIkmzMONfmA", "rtp_symmetric": "eTYnUOegdnyJHk5",
          "send_diversion": "9NATl", "send_pai": "G4xN4a", "send_rpid": "PnC5WqSWEQ6jsuPFN", "timers_min_se": "sPP",
          "timers": "0F38S2kevvIiyo", "timers_sess_expires": "USNkosRLJ", "transport": "wUufsy6C9FI7x",
          "trust_id_inbound": "SmGFqxXpPT", "trust_id_outbound": "TwEa5bzZPYsae9zuu", "type": "mCP",
          "use_ptime": "TaXY5GNLQhNa2I", "use_avpf": "6YeQ16kd4", "force_avp": "pVDffsVStBi",
          "media_use_received_transport": "c1I", "media_encryption": "DfgunEGr46MG", "inband_progress": "oQD",
          "call_group": "QzHz0t3X7Xgy5PaYV", "pickup_group": "RYGg7aLIs6TJCifJf", "named_call_group": "zPehn28V92sgS",
          "named_pickup_group": "63dtH9FiDWQ4gn9cBmo", "device_state_busy_at": "PpA9Zo0on5qquH", "t38_udptl": "w280yj",
          "t38_udptl_ec": "Q5g4Wk3u40GLC4", "t38_udptl_maxdatagram": "h09FAJ3J", "fax_detect": "CafruWUb9sdosqQnt",
          "t38_udptl_nat": "qH0usAmG45BhicuA5G3", "t38_udptl_ipv6": "ABRzOi0FCvg", "tone_zone": "jOgC3Znh",
          "language": "i5NsRW9wA", "one_touch_recording": "rPVx", "record_on_feature": "9UqyhzZL5Y3JGiGCI",
          "record_off_feature": "L4LxqiSfWVbjtjFhTO", "rtp_engine": "KuGAiiojWJq2SfLaBl", "allow_transfer": "bmoLg9W6",
          "sdp_owner": "kcw7z", "sdp_session": "rsA6X", "tos_audio": "o07hJCtWhiN8VzYVzVVy", "tos_video": "rpTk1Slswv9",
          "cos_audio": "MCe8aReDnGZ3KW8", "cos_video": "oEAAk7bln", "allow_subscribe": "nKlS3SzJf",
          "sub_min_expiry": "ZuiLPJTaQy36Pgm9YgiQ", "from_user": "XnjbEqf5Lc9", "mwi_from_user": "KaZRECvQOtTnz",
          "from_domain": "uGGZVBgzdQ", "dtls_verify": "xFqxevOVHTWNGbY", "dtls_rekey": "oS8ETR",
          "dtls_cert_file": "XI1SGYC5", "dtls_private_key": "lKs9zUzh50NJhuA6oE0", "dtls_cipher": "bnvQRwE",
          "dtls_ca_file": "1XMI9RB", "dtls_ca_path": "LaLkcspFAcU", "dtls_setup": "envEaRPuFwcX",
          "dtls_fingerprint": "deRrBNCxnL0QAOrF", "srtp_tag_32": "4qJ", "set_var": "kN4ldR0gdk",
          "message_context": "9WMjdjhs7pZm", "accountcode": "weQrrYS4PAVg0yAd6uiw", "mac": "0004f23a43bf",
          "model": "SSIP7000"}),
    )

    provider_test_process_exceptions = lambda: (
        (["[1234]", "100rel=Jyl5aQ2zp0VCQwUA", "aggregate_mwi=uMuYIQnX", "allow=RadaiCnMtKfDef", "aors=nnj63k",
          "auth=RtK1MwZD6", "callerid=T9n", "callerid_privacy=tOeiVAvTp61mx", "callerid_tag=hjuHGReXzyMIBVqzeIf",
          "context=2NRpB", "direct_media_glare_mitigation=TXoZEhoqp5", "direct_media_method=ayF",
          "connected_line_method=VVe4GoxMG3ByJY5", "direct_media=zYEnS3aZwkwVM",
          "disable_direct_media_on_nat=6NClLUwI2OV9N", "disallow=3hgsB1YrOA2K9dgsAxer", "dtmf_mode=haJA4q9",
          "media_address=g4oHrspWAWOUAv", "force_rport=KL1BSA8sxIHEjIJrH", "ice_support=6EZ7K6M0f",
          "identify_by=sHT5LoSUL0JI96561Ym", "redirect_method=enBAGEH", "mailboxes=NPD", "moh_suggest=Ay800ZGIR4Sx3cn",
          "outbound_auth=BWmM9N1UynmWkYV4cwd2", "outbound_proxy=1KnxgfT", "rewrite_contact=kbyf1WV2x0B1Uew",
          "rtp_ipv6=rmIkmzMONfmA", "rtp_symmetric=eTYnUOegdnyJHk5", "send_diversion=9NATl", "send_pai=G4xN4a",
          "send_rpid=PnC5WqSWEQ6jsuPFN", "timers_min_se=sPP", "timers=0F38S2kevvIiyo", "timers_sess_expires=USNkosRLJ",
          "transport=wUufsy6C9FI7x", "trust_id_inbound=SmGFqxXpPT", "trust_id_outbound=TwEa5bzZPYsae9zuu", "type=mCP",
          "use_ptime=TaXY5GNLQhNa2I", "use_avpf=6YeQ16kd4", "force_avp=pVDffsVStBi", "media_use_received_transport=c1I",
          "media_encryption=DfgunEGr46MG", "inband_progress=oQD", "call_group=QzHz0t3X7Xgy5PaYV",
          "pickup_group=RYGg7aLIs6TJCifJf", "named_call_group=zPehn28V92sgS", "named_pickup_group=63dtH9FiDWQ4gn9cBmo",
          "device_state_busy_at=PpA9Zo0on5qquH", "t38_udptl=w280yj", "t38_udptl_ec=Q5g4Wk3u40GLC4",
          "t38_udptl_maxdatagram=h09FAJ3J", "fax_detect=CafruWUb9sdosqQnt", "t38_udptl_nat=qH0usAmG45BhicuA5G3",
          "t38_udptl_ipv6=ABRzOi0FCvg", "tone_zone=jOgC3Znh", "language=i5NsRW9wA", "one_touch_recording=rPVx",
          "record_on_feature=9UqyhzZL5Y3JGiGCI", "record_off_feature=L4LxqiSfWVbjtjFhTO",
          "rtp_engine=KuGAiiojWJq2SfLaBl", "allow_transfer=bmoLg9W6", "sdp_owner=kcw7z", "sdp_session=rsA6X",
          "tos_audio=o07hJCtWhiN8VzYVzVVy", "tos_video=rpTk1Slswv9", "cos_audio=MCe8aReDnGZ3KW8", "cos_video=oEAAk7bln",
          "allow_subscribe=nKlS3SzJf", "sub_min_expiry=ZuiLPJTaQy36Pgm9YgiQ", "from_user=XnjbEqf5Lc9",
          "mwi_from_user=KaZRECvQOtTnz", "from_domain=uGGZVBgzdQ", "dtls_verify=xFqxevOVHTWNGbY", "dtls_rekey=oS8ETR",
          "dtls_cert_file=XI1SGYC5", "dtls_private_key=lKs9zUzh50NJhuA6oE0", "dtls_cipher=bnvQRwE",
          "dtls_ca_file=1XMI9RB", "dtls_ca_path=LaLkcspFAcU", "dtls_setup=envEaRPuFwcX",
          "dtls_fingerprint=deRrBNCxnL0QAOrF", "srtp_tag_32=4qJ", "set_var=kN4ldR0gdk", "message_context=9WMjdjhs7pZm",
          "accountcode=weQrrYS4PAVg0yAd6uiw"],
         ["[1234]", "rel_100=Jyl5aQ2zp0VCQwUA", "aggregate_mwi=uMuYIQnX", "allow=RadaiCnMtKfDef", "aors=nnj63k",
          "auth=RtK1MwZD6", "callerid=T9n", "callerid_privacy=tOeiVAvTp61mx", "callerid_tag=hjuHGReXzyMIBVqzeIf",
          "context=2NRpB", "direct_media_glare_mitigation=TXoZEhoqp5", "direct_media_method=ayF",
          "connected_line_method=VVe4GoxMG3ByJY5", "direct_media=zYEnS3aZwkwVM",
          "disable_direct_media_on_nat=6NClLUwI2OV9N", "disallow=3hgsB1YrOA2K9dgsAxer", "dtmf_mode=haJA4q9",
          "media_address=g4oHrspWAWOUAv", "force_rport=KL1BSA8sxIHEjIJrH", "ice_support=6EZ7K6M0f",
          "identify_by=sHT5LoSUL0JI96561Ym", "redirect_method=enBAGEH", "mailboxes=NPD", "moh_suggest=Ay800ZGIR4Sx3cn",
          "outbound_auth=BWmM9N1UynmWkYV4cwd2", "outbound_proxy=1KnxgfT", "rewrite_contact=kbyf1WV2x0B1Uew",
          "rtp_ipv6=rmIkmzMONfmA", "rtp_symmetric=eTYnUOegdnyJHk5", "send_diversion=9NATl", "send_pai=G4xN4a",
          "send_rpid=PnC5WqSWEQ6jsuPFN", "timers_min_se=sPP", "timers=0F38S2kevvIiyo", "timers_sess_expires=USNkosRLJ",
          "transport=wUufsy6C9FI7x", "trust_id_inbound=SmGFqxXpPT", "trust_id_outbound=TwEa5bzZPYsae9zuu", "type=mCP",
          "use_ptime=TaXY5GNLQhNa2I", "use_avpf=6YeQ16kd4", "force_avp=pVDffsVStBi", "media_use_received_transport=c1I",
          "media_encryption=DfgunEGr46MG", "inband_progress=oQD", "call_group=QzHz0t3X7Xgy5PaYV",
          "pickup_group=RYGg7aLIs6TJCifJf", "named_call_group=zPehn28V92sgS", "named_pickup_group=63dtH9FiDWQ4gn9cBmo",
          "device_state_busy_at=PpA9Zo0on5qquH", "t38_udptl=w280yj", "t38_udptl_ec=Q5g4Wk3u40GLC4",
          "t38_udptl_maxdatagram=h09FAJ3J", "fax_detect=CafruWUb9sdosqQnt", "t38_udptl_nat=qH0usAmG45BhicuA5G3",
          "t38_udptl_ipv6=ABRzOi0FCvg", "tone_zone=jOgC3Znh", "language=i5NsRW9wA", "one_touch_recording=rPVx",
          "record_on_feature=9UqyhzZL5Y3JGiGCI", "record_off_feature=L4LxqiSfWVbjtjFhTO",
          "rtp_engine=KuGAiiojWJq2SfLaBl", "allow_transfer=bmoLg9W6", "sdp_owner=kcw7z", "sdp_session=rsA6X",
          "tos_audio=o07hJCtWhiN8VzYVzVVy", "tos_video=rpTk1Slswv9", "cos_audio=MCe8aReDnGZ3KW8", "cos_video=oEAAk7bln",
          "allow_subscribe=nKlS3SzJf", "sub_min_expiry=ZuiLPJTaQy36Pgm9YgiQ", "from_user=XnjbEqf5Lc9",
          "mwi_from_user=KaZRECvQOtTnz", "from_domain=uGGZVBgzdQ", "dtls_verify=xFqxevOVHTWNGbY", "dtls_rekey=oS8ETR",
          "dtls_cert_file=XI1SGYC5", "dtls_private_key=lKs9zUzh50NJhuA6oE0", "dtls_cipher=bnvQRwE",
          "dtls_ca_file=1XMI9RB", "dtls_ca_path=LaLkcspFAcU", "dtls_setup=envEaRPuFwcX",
          "dtls_fingerprint=deRrBNCxnL0QAOrF", "srtp_tag_32=4qJ", "set_var=kN4ldR0gdk", "message_context=9WMjdjhs7pZm",
          "accountcode=weQrrYS4PAVg0yAd6uiw"]),
    )

    @data_provider(provider_test_process_exceptions)
    def test_process_exceptions(self, section, expected_result_section):
        endpoint = Endpoint(section)
        endpoint.process_exceptions()

        for i in range(1, len(expected_result_section)):
            self.assertEqual(expected_result_section[i], endpoint.section[i])

    @data_provider(provider_test_init)
    def test_init(self, section, expected_attributes):

        endpoint = Endpoint(section)
        self.assertEqual(section, endpoint.section)

        endpoint.set_attributes()

        for attribute in expected_attributes:
            expected_value = expected_attributes[attribute]
            actual_value = getattr(endpoint, attribute)
            self.assertEqual(expected_value, actual_value,
                             "endpoint.{} should be {}. Got {} instead.".format(attribute, expected_value,
                                                                                actual_value))

    provider_test_parse_templates = lambda: (
        [["[1001] (some-template)", "type=endpoint"], "some-template"],
        [["[1001] ( some-template)", "type=endpoint"], "some-template"],
        [["[1001] ( some-template )", "type=endpoint"], "some-template"],
        [["[1001] (some-template )", "type=endpoint"], "some-template"],
        [["[1001](some-template )", "type=endpoint"], "some-template"],
        [["[1001](some-template)", "type=endpoint"], "some-template"],
    )

    @data_provider(provider_test_parse_templates)
    def test_parse_template(self, section, expected_template):

        endpoint = Endpoint(section)
        endpoint.set_attributes()
        self.assertEqual(expected_template, endpoint.template)

    def get_pconf(self):
        pconf = PolypyConfig()
        pconf.add_search_path(os.path.join(os.path.dirname(__file__), "fixtures/test_endpoint"))
        pconf.find()
        pconf.load()
        pconf.update_paths('asterisk', os.path.join(os.path.dirname(__file__), "fixtures/pjsip/"))
        return pconf

    # def test_add_registrations(self):
    #     target_endpoint = None
    #     target_mac = "0004f23a43bf"
    #     factory = SipResourceFactory()
    #     parser = PjSipSectionParser()
    #     parser.use_config(self.get_pconf())
    #     parser.use_factory(factory)
    #     parser.parse()
    #     target_endpoint = parser.get_endpoint(target_mac)
    #
    #     self.assertIsNotNone(target_endpoint)
    #     self.assertIsInstance(target_endpoint, Endpoint)
    #     self.assertEqual(target_mac, target_endpoint.mac)
    #
    #     self.assertEqual("6001,6003", target_endpoint.aors)
    #     target_endpoint.set_attributes()
    #     target_endpoint.load_aors(parser.resources)
    #     target_endpoint.load_auths(parser.resources)
    #
    #     self.assertEqual(2, len(target_endpoint.authorizations), "target_endpoint should have 2 authorizations.")
    #     self.assertEqual(2, len(target_endpoint.addresses), "target_endpoint should have 2 addresses.")
    #     self.assertEqual(2, len(target_endpoint.authorizations))
    #
    #     for aors_object in target_endpoint.addresses:
    #         self.assertIsInstance(aors_object, Aor)
    #
    #     for auth_object in target_endpoint.authorizations:
    #         self.assertIsInstance(auth_object, Auth)
    #
    #     target_endpoint.hydrate_registrations()
    #
    #     self.assertEqual(2, len(target_endpoint.registrations))

    def test_get_firmware(self):
        section = ["[1001] (some-template)", "type=endpoint", "model=SPIP650"]
        endpoint = Endpoint(section)
        endpoint.set_attributes()
        expected_firmware_version = '75bd189a-6159-4aa4-b51f-40e36784a882'

    provider_test_load_aor = lambda: (
        ([{"section": "Section 1", "order": "1", "label": "Line 1"},
          {"section": "Section 2", "order": "2", "label": "Line 2"},
          {"section": "Section 3", "order": "3", "label": "Line 3"}], ["Section 1", "Section 2", "Section 3"],),
        ([{"section": "Section 1", "order": "3", "label": "Line 1"},
          {"section": "Section 2", "order": "2", "label": "Line 2"},
          {"section": "Section 3", "order": "1", "label": "Line 3"}], ["Section 3", "Section 2", "Section 1"],),
        ([{"section": "Section 1", "order": "3", "label": "Line 1"},
          {"section": "Section 2", "order": "1", "label": "Line 2"},
          {"section": "Section 3", "order": "2", "label": "Line 3"}], ["Section 2", "Section 3", "Section 1"],),
        ([{"section": "Section 1", "order": "33", "label": "Line 1"},
          {"section": "Section 2", "order": "10", "label": "Line 2"},
          {"section": "Section 3", "order": "27", "label": "Line 3"}], ["Section 2", "Section 3", "Section 1"],),
        ([{"section": "Section 1", "label": "Line 1"},
          {"section": "Section 2", "label": "Line 2"},
          {"section": "Section 3", "label": "Line 3"}], ["Section 1", "Section 2", "Section 3"],),
    )

    @data_provider(provider_test_load_aor)
    def test_load_aors(self, dict_test_data, expected_order):
        section = ["[1001] (some-template)", "type=endpoint", "model=SPIP650"]
        endpoint = Endpoint(section)
        endpoint.set_attributes()
        endpoint.aors = ",".join(expected_order)

        resources = []
        for a in dict_test_data:
            buffer = []
            buffer.append("[{}]".format(a['section']))
            # buffer.append("label={}".format(a['label']))
            # if "order" in a:
            #     buffer.append("order={}".format(a['order']))

            aor = Aor(buffer)
            # aor.label = a['label']
            # if "order" in a:
            #     aor.order = a['order']
            aor.type = 'aor'
            aor.set_attributes()
            resources.append(aor)

        endpoint.load_aors(resources)

        self.assertTrue(len(endpoint.addresses) == 3,
                        "After loading AORs, you should have 3 addresses. There are {}".format(len(endpoint.addresses)))

        # for expected_section in expected_order:
        #     aor = endpoint.addresses.pop(0)
        #     self.assertEqual(expected_section, aor.section_name)

    def test_load_auth(self):
        target_endpoint = None
        resources = []
        target_mac = "0004f23a43bf"
        factory = SipResourceFactory()
        parser = PjSipSectionParser()
        parser.use_config(self.get_pconf())
        parser.use_factory(factory)
        parser.parse()
        target_endpoint = parser.get_endpoint(target_mac)
        target_endpoint.load_aors(parser.resources)
        target_endpoint.load_auths(parser.resources)

        # for aor in target_endpoint.addresses:
        #     test_auth = target_endpoint.authorizations.pop(0)
        #     self.assertTrue(aor.section_name in test_auth.section_name)

    def test_render(self):


        endpoint = Endpoint("")
        endpoint.new_section("6001")
        endpoint.template = "some-site-template"
        endpoint.context = "default"
        endpoint.disallow = "all"
        endpoint.transport = "simpletrans"
        endpoint.mac = "0004f23a43bf"
        endpoint.model = "SSIP7000"
        endpoint.allow = "ulaw"

        aor1 = Aor("")
        aor1.new_section("6001")
        aor1.label = "Line 1"
        aor1.order = 2
        aor1.max_contacts = 1

        auth1 = Auth("")
        auth1.new_section("auth6001")
        auth1.auth_type = "userpass"
        auth1.password = "2034c37e"
        auth1.username = "dd341d078cfd"
        auth1.label = "Line 1"
        auth1.order = 2

        aor2 = Aor("")
        aor2.new_section("6003")
        aor2.label = "Line 2"
        aor2.order = 1
        aor2.max_contacts = 1

        auth2 = Auth("")
        auth2.new_section("auth6003")
        auth2.auth_type = "userpass"
        auth2.password = "d3fb5a6c69ee"
        auth2.username = "6c6499cf"
        auth2.label = "Line 2"
        auth2.order = 1

        endpoint.authorizations.append(auth1)
        endpoint.authorizations.append(auth2)
        endpoint.add_aor(aor1)
        endpoint.add_aor(aor2)

        f = open(os.path.join(os.path.dirname(__file__), "fixtures/pjsip/expected_rendered_endpoint_6001.conf"))
        buffer = f.read()
        f.close()

        expected_sections = "".join(buffer)
        self.assertEqual(expected_sections, endpoint.render())

    def test_add_auth(self):
        endpoint = Endpoint("[test-section]")
        auth = Auth("[test-auth]")
        endpoint.add_auth(auth)
        self.assertEqual(1, len(endpoint.authorizations))

    def test_get_resource(self):
        pconf = self.get_pconf()
        # Use the files from issue_36!
        pconf.set_path('tftproot', self.test_tftproot())
        pconf.set_path("asterisk", self.test_asterisk())

        factory = SipResourceFactory()
        meta = ModelMeta()
        meta.use_configs(pconf)

        meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware"))

        parser = PjSipSectionParser()
        parser.use_config(pconf)
        parser.use_factory(factory)
        parser.parse()

        tag = "0004f2e62aa4111"
        endpoint = parser.get_resource(tag, "endpoint")

        self.assertEqual("endpoint", endpoint.type)
        self.assertEqual(tag, endpoint.section_name)


    def test_get_label(self):
        pconf = self.get_pconf()
        # Use the files from issue_36!
        pconf.set_path('tftproot', self.test_tftproot())
        pconf.set_path("asterisk", self.test_asterisk())

        factory = SipResourceFactory()
        meta = ModelMeta()
        meta.use_configs(pconf)

        meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware"))

        parser = PjSipSectionParser()
        parser.use_config(pconf)
        parser.use_factory(factory)
        parser.parse()

        endpoint1 = parser.get_resource("0004f2e62aa4111", "endpoint")
        endpoint1.load_aors(parser.resources)
        endpoint1.load_auths(parser.resources)

        self.assertEqual("Line 1", endpoint1.get_label())

        endpoint2 = parser.get_resource("0004f2e62aa4104", "endpoint")
        endpoint2.load_aors(parser.resources)
        endpoint2.load_auths(parser.resources)
        self.assertEqual("Line 2", endpoint2.get_label())


    def test_get_auth(self):
        expected_auth = Auth(["[auth1234]", "type=auth"])
        endpoint = Endpoint(["[1234]", "type=endpoint"])
        endpoint.add_auth(expected_auth)

        self.assertEqual(expected_auth, endpoint.get_auth())

    def test_get_aor(self):
        expected_aor = Aor(["[1234]", "type=aor"])
        endpoint = Endpoint(["[1234]", "type=endpoint"])
        endpoint.add_aor(expected_aor)

        self.assertEqual(expected_aor, endpoint.get_aor())


if __name__ == '__main__':
    unittest.main()
