import os
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.dialplan import Dialplan
from poly_py_tools.payload import Payload


class Deploy:

    config = None
    dialplan = None
    rsync_lists = None

    def __init__(self, config: PolypyConfig, dialplan: Dialplan):
        self.config = config
        self.dialplan = dialplan
        self.rsync_lists = {}

    def build_rsync_lists(self):
        buffer = {}
        self.dialplan.parse()

        for entry in self.dialplan.entries:

            if not entry.site in buffer:
                buffer[entry.site] = []

            payload = Payload(self.config, entry)
            for source in payload.sources:
                buffer[entry.site].append(os.path.basename(source))

        self.rsync_lists = buffer

    def write_scripts(self):
        run_script = os.path.join(self.config.config['paths']['tftproot'], "push.sh")

        with open(run_script, 'w') as script_file:
            script_file.write("#!/bin/bash\n")

            for site in self.rsync_lists:
                if site is None:
                    continue
                buffer = site.split(".")
                buffer.reverse()
                target_directory = ".".join(buffer)
                target_file = os.path.join(self.config.config['paths']['tftproot'], site + ".lst")
                # print("target file: {}".format(target_file))
                # print("\n".join(self.rsync_lists[site]))

                with open(target_file, 'w') as outfile:
                    outfile.writelines("\n".join(self.rsync_lists[site]))

                outfile.close()
                # print("File {} exists={}".format(target_file, "Yes" if os.path.exists(target_file) else "No"))
                script_file.write("rsync -avh --files-from='{}' . root@pbx.hph.io:/var/www/html/io.hph.pbx/p/{}/\n".format(os.path.basename(target_file), target_directory))
