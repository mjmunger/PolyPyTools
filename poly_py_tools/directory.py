import os
import csv
from poly_py_tools.directory_item import DirectoryItem


class Directory:
    items = []
    mac_addr = None

    def __init__(self, mac_addr):
        self.items = []
        self.set_mac(mac_addr)

    def set_mac(self, mac):
        self.mac_addr = str(mac).replace(":", "").replace("-","").lower().strip()

    def add_item(self, item):
        self.items.append(item)

    def render(self):
        buffer = []
        count = 0
        for item in self.items:
            count = count + 1
            item.speed_dial = count
            buffer.append(item.render())

        buffer.insert(0, "  <item_list>")
        buffer.insert(0, "<directory>")
        buffer.append("  </item_list>")
        buffer.append("</directory>")

        return "\n".join(buffer)

    def read(self, path_to_csv):
        if not os.path.exists(path_to_csv):
            raise FileNotFoundError

        with open(path_to_csv) as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row[0] == "First" and row[1] == "Last" and row[2] == "Number":
                    continue

                item = DirectoryItem("SPIP670", row[1], row[0], row[2], "", "", "", "", 0, 0,
                                     1 if row[3] == "Yes" else 0, 0)

                self.items.append(item)

    def save(self, configs):
        tftp_root = configs['paths']['tftproot']
        target_filename = "{}-directory.xml".format(self.mac_addr)
        target_file = os.path.join(tftp_root, target_filename)

        f = open(target_file, 'w')
        f.write(self.render())
        f.close()

        print("Directory saved as: {}".format(target_file))

