#!/usr/bin/python3

import xml.etree.ElementTree as ET
from xml.dom import minidom
import csv
import getopt
import sys
import os
import configparser
from pprint import pprint

options = "b:cdghlm:u:o:"
longopts = ['blacklist=', 'help', 'license', 'mac=', 'user=', 'discover=', 'show-configs', '--generate-basedirectory',
            'model']
optlist, args = getopt.getopt(sys.argv[1:], options, longopts)
themac = None
blacklist = None


def usage():
    print("""    
Usage: gendir.py [options]

FUNCTION SUMMARY
Parses several CSV files to build the contact directory, speed dials, and general directory for Polycom phones.

OPTION LIST

-b[...]  --blacklist[...]          Comma separated list of extensions NOT to include on this phone. Used to
                                     prevent your own number from being a speed dial / presence
-c       --show-configs            Show the current settings, which are kept in /etc/polypy.conf
-d       --discover                Display all the extensions that are found in sip.conf along with their
                                   mac addresses
-g       --generate-basedirectory  Generate the 000000000000-directory.xml from the directory.csv file
-m[...]  --mac[...]                Identify the mac address of the phone that will be using this directory.
-o[...]  --model[...]              Identify the model of the phone so the appropriate direcotry can be
                                     assigned to it. If unused, no directory will be appeneded to the speed
                                     dials.
-l       --license                 Display the license for this software
-h       --help                    Show this help.
-u       --user                    Phone's user. This is used to find the CSV files for that user.
    """)


def show_license():
    print("""
    Process multiple CSV files into Polycom directory configs.
    Copyright (C) 2015 High Powered Help, Inc. All Rights Reserved.
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """)


def discover(conf):
    blacklisted = ["general", "authentication", "!", "bandwidth"]

    print("Discovering %s" % conf)

    f = open(conf, 'r')
    for line in f:
        line = line.strip()
        if line.startswith("["):
            skip = False
            for banned in blacklisted:
                if banned in line:
                    skip = True

            if skip:
                continue

            # Find the closing ]
            pos = line.upper().find("]")
            extension = line[1:pos]
            meta = next(f)[1:].strip()

            if not "|" in meta:
                continue
                #raise ValueError("The first line after a device declaration should be ;NNNNNNNNNNNN|XXX where N is a mac and X is the model model. Got: " + meta )

            buf = meta.split('|')
            mac = buf[0]
            model = buf[1]

            cid = None
            buffer = None

            try:
                buffer = next(f).strip()
                while not len(buffer.strip()) == 0:
                    buffer = next(f).strip()
                    if buffer.startswith('callerid'):
                        data = buffer.split("=")
                        cid = data[1]
            except StopIteration as e:
                do = "nothing"
            print("Found a {} with extension: {} for MAC {} with cid of {}".format(model, extension, mac, cid))


def sanitize_number(number):
    if len(number) == 11:
        return number[1:]
    else:
        return number


def make_item(first, last, contact, counter, watch):
    item = ET.Element('item')

    ln = ET.Element('ln')
    ln.text = last

    fn = ET.Element('fn')
    fn.text = first

    ct = ET.Element('ct')
    ct.text = contact

    sd = ET.Element('sd')
    sd.text = "%s" % counter

    rt = ET.Element('rt')
    rt.text = "12"

    dc = ET.Element('dc')

    ad = ET.Element('ad')
    ad.text = "0"

    ar = ET.Element('ar')
    ar.text = "0"

    bw = ET.Element('bw')
    bw.text = "1" if watch == "Y" else "0"

    bb = ET.Element('bb')
    bb.text = "0"

    item.append(ln)
    item.append(fn)
    item.append(ct)
    item.append(sd)
    item.append(rt)
    item.append(dc)
    item.append(ad)
    item.append(ar)
    item.append(bw)
    item.append(bb)

    return item


def check_file(target_file):
    if not os.path.exists(target_file):
        print("WARNING! Could not find this directory file for this user (%s)" % target_file)
        print("    I assume that's because they don't use this feature??")
        return False
    else:
        return True


def gen_directory(theMac = '000000000000'):
    # Create XML
    header = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

    root = ET.Element("directory")
    item_list = ET.SubElement(root, 'item_list')

    counter = 0
    directory = {}

    outputfile = theMac + '-directory.xml'
    outputfile = os.path.join(rootPath, outputfile)

    with open('directory.csv', 'r') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in myreader:
            first = row[0]
            number = sanitize_number(row[2])
            last = row[1]
            # Skip the header
            if row[0] == "First":
                continue

            if len(number) > 0 and (len(last) > 0 or len(first) > 0):
                contact = number
                watch = row[3]
                pprint(watch)
                counter += 1

                directory[counter] = first + " " + last
                this_item = make_item(first, last, contact, counter, watch)
                item_list.append(this_item)

    print("Writing %s ..." % outputfile, )
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    with open("/tmp/asdf.xml",'w') as f:
        f.write(xmlstr)


# Start script

confFile = '/etc/polypy.conf'
if not os.path.exists(confFile):
    print("""
    You must setup /etc/polypy.conf!
    
    Example Contents:
    [polycom]
    root=/path/to/provisioning/root
    server=your.provisioning.server
    sip_path=/path/to/your/sip.conf
    """)

    sys.exit()

# Get settings
config = configparser.RawConfigParser()
config.read(confFile)

rootPath = config.get('polycom', 'root')
server = config.get('polycom', 'server')
sippath = config.get('polycom', 'sip_path')
# End Settings Get

for o, a in optlist:
    if o in ['-b', '--blacklist']:
        print("Blacklisting %s" % a)
        blacklist = a
    if o in ['-o', '--model']:
        print("Phone model set to: %s" % a)
        model = a
    if o in ['-m', '--mac']:
        print("Setting mac to: %s" % a)
        themac = a
    elif o in ['-g', '--generate-basedirectory']:
        gen_directory()
        sys.exit()
    elif o in ['-u', '--user']:
        print("Setting user to: %s" % a)
        theuser = a
    elif o in ['-h', '--help']:
        usage()
        sys.exit()
    elif o in ['-l', '--license']:
        show_license()
        sys.exit()
    elif o in ['-d', '--discover']:
        discover(sippath)
        sys.exit()
    elif o in ['-c', 'show-configs']:
        print("Current Config Settings:")
        print("Root: %s" % rootPath)
        print("Server: %s" % server)
        print("Sippath: %s" % sippath)
        sys.exit()

if themac == None or theuser == None:
    print("ERROR! You must specify the mac address of the phone that will use these configs as well as the user!")
    usage()
    sys.exit()

# Create XML
header = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

root = etree.Element('directory')
item_list = etree.Element('item_list')
counter = 0
directory = {}
numbers = []
duplicates = []

# Load up the office contacts
root.append(item_list)
with open('users.csv', 'rb') as csvfile:
    myreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in myreader:
        number = row[0]
        name = row[1]

        first = ""
        last = name
        contact = number
        watch = "1"

        counter += 1

        #  Skip this one if it is blacklisted.
        if not blacklist == None:
            if number in blacklist:
                continue

        item = make_item(first, last, contact, counter, watch)

        directory[counter] = first + " " + last
        item_list.append(item)

speedial = '%s-sd-%s.csv' % (theuser, model)

if check_file(speedial):

    print("INCLUDING: Speed Dial Direcotry (%s)" % speedial)
    with open(speedial, 'rb') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in myreader:
            number = sanitize_number(row[0])
            first = row[1].strip()
            last = row[2].strip()
            contact = number
            watch = row[3].strip()
            counter += 1

            directory[counter] = first + " " + last

            if number not in numbers:
                numbers.append(number)
                item = make_item(first, last, contact, counter, watch)
                item_list.append(item)
            else:
                t = [first, last, number]
                duplicates.append(t)

if model == '670':
    companyDirectory = 'master-670.csv'

elif model == '330':
    companyDirectory = 'master-330.csv'

if check_file(companyDirectory):
    print("INCLUDING: Company Direcotry (%s)" % companyDirectory)
    with open(companyDirectory, 'rb') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in myreader:
            number = sanitize_number(row[0])
            first = row[1].strip()
            last = row[2].strip()

            contact = number
            watch = "0"
            counter += 1

            directory[counter] = first + " " + last
            if number not in numbers:
                numbers.append(number)
                item = make_item(first, last, contact, counter, watch)
                item_list.append(item)
            else:
                t = [first, last, number]
                duplicates.append(t)

s = etree.tostring(root, pretty_print=True)
pprint(s)
outputfile = '%s-directory.xml' % themac
outputfile = os.path.join(rootPath, outputfile)
# If the output file already exists, delete it first.
if os.path.exists(outputfile):
    print("Directory already exists. Removing it!")
    os.remove(outputfile)

print("Writing %s ..." % outputfile, )
sm = open(outputfile, 'w')
sm.write(header + "\n")
sm.write(s)
sm.close

outputfile = '%s-list.txt' % themac
outputfile = os.path.join(rootPath, outputfile)
tl = open(outputfile, 'w')
for d in directory:
    line = str(d).ljust(5) + directory[d]
    tl.write(line + "\n")
    print(line)

if len(duplicates) > 0:
    for dupe in duplicates:
        print("Did not include this duplicate: %s" % dupe)
        tl.write("Did not include this duplicate: %s\n" % dupe)
else:
    tl.write("There were no duplicate numbers")
    print("There were no duplicate numbers")

tl.close
print("List saved in: %s" % outputfile)
print("Done.")
