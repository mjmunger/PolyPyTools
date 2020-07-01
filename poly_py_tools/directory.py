import os
import csv
from poly_py_tools.directory_item import DirectoryItem


class Directory:
    items = None
    mac_addr = None
    csv_files = None

    def __init__(self, mac_addr):
        self.items = []
        self.csv_files = []
        self.set_mac(mac_addr)

    def add_csv(self, csv_file):
        if not os.path.exists(csv_file):
            raise FileNotFoundError("Cannot find: {}".format(csv_file))

        self.csv_files.append(csv_file)

    def set_mac(self, mac):
        self.mac_addr = str(mac).replace(":", "").replace("-", "").lower().strip()

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

    def read(self):
        for csv_file in self.csv_files:
            self.read_csv(csv_file)

    def read_csv(self, path_to_csv):
        if not os.path.exists(path_to_csv):
            raise FileNotFoundError

        with open(path_to_csv) as csvfile:
            csvfile.__next__()
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                row = [col.strip() for col in row]
                item = DirectoryItem("SPIP670", row[1], row[0], row[2], row[4], "", "", "", 0, 0,
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

