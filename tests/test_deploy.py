import unittest
import os
from tempfile import NamedTemporaryFile, TemporaryDirectory
import json
from unittest_data_provider import data_provider
from poly_py_tools.deploy import Deploy
from poly_py_tools.dialplan import Dialplan
from poly_py_tools.dialplan_entry import Entry
from poly_py_tools.polypy_config import PolypyConfig


class TestDeploy(unittest.TestCase):

    def get_column_map(self):
        with open( os.path.join(os.path.dirname(__file__), "fixtures/csv_columns.map"), 'r') as fp:
            return json.load(fp)

    def get_csv_file(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/dialplanbuilder_sample.csv")

    provider_expected_filelist = lambda : (
        ("atl.example.org",
          "0004f23a626f\n0004f23a626f.cfg\n0004f23a626f-directory.xml\n0004f23a3f53\n0004f23a3f53.cfg\n0004f23a3f53-directory.xml\n0004f23a5515\n0004f23a5515.cfg\n0004f23a5515-directory.xml\n0004f23a3801\n0004f23a3801.cfg\n0004f23a3801-directory.xml\n0004f23a43bf\n0004f23a43bf.cfg\n0004f23a43bf-directory.xml\n0004f265ee1c\n0004f265ee1c.cfg\n0004f265ee1c-directory.xml\n0004f243f141\n0004f243f141.cfg\n0004f243f141-directory.xml\n0004f265ec84\n0004f265ec84.cfg\n0004f265ec84-directory.xml"),
         ("abq.example.org",
          "0004f23a380e\n0004f23a380e.cfg\n0004f23a380e-directory.xml\n0004f2f957f9\n0004f2f957f9.cfg\n0004f2f957f9-directory.xml\n0004f2687c95\n0004f2687c95.cfg\n0004f2687c95-directory.xml\n0004f24dc8ed\n0004f24dc8ed.cfg\n0004f24dc8ed-directory.xml\n0004f2327f13\n0004f2327f13.cfg\n0004f2327f13-directory.xml"),
         ("vegas.example.org",
          "0004f262f600\n0004f262f600.cfg\n0004f262f600-directory.xml\n0004f25fb5c3\n0004f25fb5c3.cfg\n0004f25fb5c3-directory.xml\n0004f23a611f\n0004f23a611f.cfg\n0004f23a611f-directory.xml"),
         ("nyc.example.org", "0004f24dc88f\n0004f24dc88f.cfg\n0004f24dc88f-directory.xml"),
         ("office.example.org",
          "0004f23a3f53\n0004f23a3f53.cfg\n0004f23a3f53-directory.xml\n0004f23a5515\n0004f23a5515.cfg\n0004f23a5515-directory.xml\n0004f23a43bf\n0004f23a43bf.cfg\n0004f23a43bf-directory.xml"),
    )

    @data_provider(provider_expected_filelist)
    def test_build_rsync_list(self, site_list_filename,  expected_filelist):
        with NamedTemporaryFile() as f:
            config = PolypyConfig()
            config.set_default_config(f.name)
            config.set_map(self.get_column_map())

            with TemporaryDirectory() as tftpdir:
                config.config['paths']['tftproot'] = tftpdir

                dialplan = Dialplan(self.get_csv_file())
                dialplan.with_config(config)
                deploy = Deploy(config, dialplan)
                deploy.build_rsync_lists()

                self.assertEqual(20, len(deploy.dialplan.entries))
                self.assertTrue(isinstance(dialplan, Dialplan))
                self.assertTrue(isinstance(config, PolypyConfig))
                self.assertEqual(dialplan, deploy.dialplan)
                self.assertEqual(config, deploy.config)

                self.assertEqual(5, len(deploy.rsync_lists))
                # expected_filelist = [os.path.join(tftpdir, file) for file in expected_filelist.split("\n")]
                self.assertEqual(expected_filelist, "\n".join(deploy.rsync_lists[site_list_filename]))

                deploy.write_scripts()

                for site in deploy.rsync_lists:
                    target_file = os.path.join(tftpdir, site + ".lst")
                    expected_rsync_list = target_file
                    self.assertTrue(os.path.exists(expected_rsync_list), "The file {} should exist, but does not.".format(target_file))

                target_file = os.path.join(tftpdir, site_list_filename + ".lst")
                with open(target_file, 'r') as infile:
                    self.assertEqual(expected_filelist.split("\n"), infile.read().split("\n"))

                run_file = os.path.join(tftpdir, "push.sh")
                self.assertTrue(os.path.exists(run_file))

                expected_bash_file_content = "#!/bin/bash\nrsync -avh --files-from='atl.example.org.lst' . root@pbx.hph.io:/var/www/html/io.hph.pbx/p/org.example.atl/\nrsync -avh --files-from='abq.example.org.lst' . root@pbx.hph.io:/var/www/html/io.hph.pbx/p/org.example.abq/\nrsync -avh --files-from='vegas.example.org.lst' . root@pbx.hph.io:/var/www/html/io.hph.pbx/p/org.example.vegas/\nrsync -avh --files-from='nyc.example.org.lst' . root@pbx.hph.io:/var/www/html/io.hph.pbx/p/org.example.nyc/\nrsync -avh --files-from='office.example.org.lst' . root@pbx.hph.io:/var/www/html/io.hph.pbx/p/org.example.office/\n".split("\n")

                with open(run_file, 'r') as fp_run_file:
                    buffer = fp_run_file.read().split("\n")
                    self.assertEqual(expected_bash_file_content, buffer)


if __name__ == '__main__':
    unittest.main()
