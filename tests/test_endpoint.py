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

    def test_add_registrations(self):
        target_endpoint = None
        target_mac = "0004f23a43bf"
        factory = SipResourceFactory()
        parser = PjSipSectionParser()
        parser.use_config(self.get_pconf())
        parser.use_factory(factory)
        parser.parse()
        target_endpoint = parser.get_endpoint(target_mac)

        self.assertIsNotNone(target_endpoint)
        self.assertIsInstance(target_endpoint, Endpoint)
        self.assertEqual(target_mac, target_endpoint.mac)

        self.assertEqual("6001,6003", target_endpoint.aors)
        target_endpoint.set_attributes()
        target_endpoint.load_aors(parser.resources)
        target_endpoint.load_auths(parser.resources)

        self.assertEqual(2, len(target_endpoint.authorizations), "target_endpoint should have 2 authorizations.")
        self.assertEqual(2, len(target_endpoint.addresses), "target_endpoint should have 2 addresses.")
        self.assertEqual(2, len(target_endpoint.authorizations))

        for aors_object in target_endpoint.addresses:
            self.assertIsInstance(aors_object, Aor)

        for auth_object in target_endpoint.authorizations:
            self.assertIsInstance(auth_object, Auth)

        target_endpoint.hydrate_registrations()

        self.assertEqual(2, len(target_endpoint.registrations))

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
            buffer.append("label={}".format(a['label']))
            if "order" in a:
                buffer.append("order={}".format(a['order']))

            aor = Aor(buffer)
            aor.label = a['label']
            if "order" in a:
                aor.order = a['order']
            aor.type = 'aor'
            aor.set_attributes()
            resources.append(aor)

        endpoint.load_aors(resources)

        self.assertTrue(len(endpoint.addresses) == 3,
                        "After loading AORs, you should have 3 addresses. There are {}".format(len(endpoint.addresses)))

        for expected_section in expected_order:
            aor = endpoint.addresses.pop(0)
            self.assertEqual(expected_section, aor.section_name)

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

        for aor in target_endpoint.addresses:
            test_auth = target_endpoint.authorizations.pop(0)
            self.assertTrue(aor.section_name in test_auth.section_name)

    provider_test_basic_cfg = lambda: (
        ('3.3.5.0247',),
        ('4.0.15.1009',),
        ('5.9.6.2327',),
        ('6.3.0.14929',),
    )

    @data_provider(provider_test_basic_cfg)
    def test_basic_cfg(self, version):
        factory = SipResourceFactory()
        parser = PjSipSectionParser()
        pconf = self.get_pconf()
        pconf.pjsip_path = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/pjsip/pjsip-multiple-registrations.conf"))
        parser.use_config(pconf)
        parser.use_factory(factory)
        parser.parse()

        target_mac = "0004f23a626f"
        sip_proxy = "33e9a719-de6e-4191-944f-601500b50b6e"
        expected_reg_1_address = '0004f23a626f102@33e9a719-de6e-4191-944f-601500b50b6e'
        expected_reg_1_password = 'CUzouRiNfNVRw'
        expected_reg_1_userId = '0004f23a626f102'
        expected_reg_1_label = "Line 2"

        expected_reg_2_address = "0004f23a626f101@33e9a719-de6e-4191-944f-601500b50b6e"
        expected_reg_2_password = "mHQFrPS"
        expected_reg_2_userId = "0004f23a626f101"
        expected_reg_2_label = "Line 1"

        # expected_dictionary = {
        #     "reg.1.address": expected_reg_1_address,
        #     "reg.1.auth.password": expected_reg_1_password,
        #     "reg.1.auth.userId": expected_reg_1_userId,
        #     "reg.1.label": expected_reg_1_label,
        #     "reg.1.extension": "",
        #     "reg.1.insertOBPAddressInRoute": "1",
        #     "reg.1.lineAddress": "",
        #     "reg.1.pin": "",
        #     "reg.1.outboundProxy.address": "",
        #     "reg.1.showRejectSoftKey": "1",
        #     "reg.1.useTelUriAsLineLabel": "1",
        #     "reg.1.server.1.pstnServerAuth.password": "",
        #     "reg.1.server.1.pstnServerAuth.userId": "",
        #     "reg.1.server.2.pstnServerAuth.password": "",
        #     "reg.1.server.2.pstnServerAuth.userId": "",
        #     "reg.2.address": expected_reg_2_address,
        #     "reg.2.auth.password": expected_reg_2_password,
        #     "reg.2.auth.userId": expected_reg_2_userId,
        #     "reg.2.label": expected_reg_2_label,
        #     "reg.2.extension": "",
        #     "reg.2.insertOBPAddressInRoute": "1",
        #     "reg.2.lineAddress": "",
        #     "reg.2.pin": "",
        #     "reg.2.showRejectSoftKey": "1",
        #     "reg.2.outboundProxy.address": "",
        #     "reg.2.useTelUriAsLineLabel": "1",
        #     "reg.2.server.1.pstnServerAuth.password": "",
        #     "reg.2.server.1.pstnServerAuth.userId": "",
        #     "reg.2.server.2.pstnServerAuth.password": "",
        #     "reg.2.server.2.pstnServerAuth.userId": ""
        # }

        registrations = []
        reg1 = {
            "reg.1.address": expected_reg_1_address,
            "reg.1.auth.password": expected_reg_1_password,
            "reg.1.auth.userId": expected_reg_1_userId,
            "reg.1.label": expected_reg_1_label
        }

        reg2 = {
            "reg.2.address": expected_reg_2_address,
            "reg.2.auth.password": expected_reg_2_password,
            "reg.2.auth.userId": expected_reg_2_userId,
            "reg.2.label": expected_reg_2_label,
        }

        registrations.append(reg1)
        registrations.append(reg2)

        endpoint = parser.get_endpoint(target_mac)
        self.assertIsInstance(endpoint, Endpoint)
        self.assertEqual(target_mac, endpoint.mac)
        self.assertEqual("SPIP670", endpoint.model)

        endpoint.set_attributes()
        endpoint.load_aors(parser.resources)
        endpoint.load_auths(parser.resources)
        endpoint.use_proxy(sip_proxy)
        endpoint.hydrate_registrations()

        self.assertEqual(2, len(endpoint.registrations))

        # Next test: confirm we are writing the XML properly.

        expected_xml_file = os.path.join(os.path.dirname(__file__),
                                         "fixtures/fs/firmware/{}/expected_xml.cfg".format(version))
        self.assertTrue(os.path.exists(expected_xml_file))

        expected_xml = minidom.parse(expected_xml_file)

        expected_config_node = expected_xml.getElementsByTagName('polycomConfig')[0]
        self.assertEqual("polycomConfig", expected_config_node.tagName)

        expected_reg_node = expected_config_node.getElementsByTagName('reg')[0]

        reg_basic_cfg_file = os.path.join(os.path.dirname(__file__),
                                          "fixtures/fs/firmware/{}/Config/reg-basic.cfg".format(version))
        self.assertTrue(os.path.exists(reg_basic_cfg_file))

        tftproot = reg_basic_cfg_file = os.path.join(os.path.dirname(__file__), "fixtures/fs/")
        meta = ModelMeta()
        meta.use_configs(pconf)
        actual_basic_cfg_xml = endpoint.basic_cfg(meta)
        actual_basic_cfg_node = ElementTree.fromstring(actual_basic_cfg_xml)

        for reg in registrations:
            for tag in reg:
                value = reg[tag]
                self.assertEqual(value, actual_basic_cfg_node.find('reg').attrib[tag])

    def test_basic_cfg_path(self):

        pconf = self.get_pconf()
        pconf.update_paths("tftproot", "/tmp/")
        pconf.update_paths("asterisk", os.path.join(os.path.dirname(__file__), "fixtures/pjsip/"))

        factory = SipResourceFactory()
        meta = ModelMeta()
        meta.use_configs(pconf)

        # meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware"))

        parser = PjSipSectionParser()
        parser.use_config(pconf)
        parser.use_factory(factory)
        parser.parse()

        target_mac = "0004f23a43bf"

        ep = parser.get_endpoint(target_mac)
        ep.set_attributes()
        ep.load_aors(parser.resources)
        ep.load_auths(parser.resources)
        ep.hydrate_registrations()

        expected_firmware_path = os.path.join(meta.get_firmware_dir(ep.model) , "Config/reg-basic.cfg")
        self.assertEqual(expected_firmware_path, ep.basic_cfg_path(meta))

    def test_bootstrap_cfg(self):

        factory = SipResourceFactory()

        pconf = PolypyConfig()
        pconf.add_search_path(os.path.join(os.path.dirname(__file__), 'fixtures/test_endpoint'))
        pconf.load()
        pconf.json['paths']['asterisk'] = os.path.join(os.path.dirname(__file__), "fixtures/pjsip/")

        meta = ModelMeta()
        meta.use_configs(pconf)

        parser = PjSipSectionParser()
        parser.use_config(pconf)
        parser.use_factory(factory)
        parser.parse()

        target_mac = "0004f23a43bf"

        ep = parser.get_endpoint(target_mac)
        ep.set_attributes()
        ep.model = "SSIP7000"
        ep.load_aors(parser.resources)
        ep.load_auths(parser.resources)
        ep.hydrate_registrations()

        expected_bootstrap_path = os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware/4.0.15.1009/expected_bootstrap.cfg")
        f = open(expected_bootstrap_path, 'r')
        buffer = f.read()
        f.close()
        expected_bootstrap = "".join(buffer)

        src_firmware_path = "/tmp/firmware/4.0.15.1009/"

        if not os.path.exists(src_firmware_path):
            os.makedirs(src_firmware_path)

        src_bootstrap_cfg = os.path.join(src_firmware_path, "000000000000.cfg")

        if not os.path.exists(src_bootstrap_cfg):
            original_source = os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware/4.0.15.1009/000000000000.cfg")
            shutil.copyfile(original_source, src_bootstrap_cfg)

        self.assertTrue(os.path.exists(src_bootstrap_cfg))
        meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware/"))
        actual_bootstrap_cfg_xml = ElementTree.fromstring(ep.bootstrap_cfg(meta))
        target_node = "APPLICATION_SSIP7000"
        application_node = actual_bootstrap_cfg_xml.find(target_node)

        self.assertFalse(application_node is None)
        self.assertTrue(application_node.tag, "APPLICATION_SSIP7000")
        self.assertEqual("firmware/4.0.15.1009/3111-40000-001.ld", application_node.attrib['APP_FILE_PATH_SSIP7000'])
        self.assertEqual("some-site-template/0004f23a43bf", application_node.attrib['CONFIG_FILES_SSIP7000'])

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

if __name__ == '__main__':
    unittest.main()
