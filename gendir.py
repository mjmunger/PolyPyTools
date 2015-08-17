#!/usr/bin/python
from lxml import etree
import csv
import getopt, sys, os, ConfigParser

options = "b:cdghlm:u:"
longopts = ['blacklist=','help','license','mac=','user=','discover=','show-configs','--generate-basedirectory']
optlist, args = getopt.getopt(sys.argv[1:],options,longopts)
themac = None
blacklist = None

def usage():
	print ""
	print "Usage: gendir.py [options]"
	print ""
	print "FUNCTION SUMMARY"
	print "Parses several CSV files to build the contact directory, speed dials, and general directory for Polycom phones."
	print ""
	print "OPTION LIST"
	print ""
	print "-b[...]  --blacklist[...]          Comma separated list of extensions NOT to include on this phone. Used to prevent your own number from being a speed dial / presence"
	print "-c       --show-configs            Show the current settings, which are kept in /etc/polypy.conf"
	print "-d       --discover                Display all the extensions that are found in sip.conf along with their mac addresses"
	print "-g       --generate-basedirectory  Generate the 000000000000-directory.xml from the mcdb.csv file"
	print "-m[...]  --mac[...]                Identify the mac address of the phone that will be using this directory."
	print "-l       --license                 Display the license for this software"
	print "-h       --help                    Show this help."
	print "-u       --user                    The user that uses this phone. This is used to find the CSV files for that user."
	print ""

def showLicense():
	print "Process multiple CSV files into Polycom directory configs."
	print "Copyright (C) 2015 High Powered Help, Inc. All Rights Reserved."
	print ""
	print "This program is free software: you can redistribute it and/or modify"
	print "it under the terms of the GNU General Public License as published by"
	print "the Free Software Foundation, either version 3 of the License, or"
	print "(at your option) any later version."
	print ""
	print "This program is distributed in the hope that it will be useful,"
	print "but WITHOUT ANY WARRANTY; without even the implied warranty of"
	print "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
	print "GNU General Public License for more details."
	print ""
	print "You should have received a copy of the GNU General Public License"
	print "along with this program.  If not, see <http://www.gnu.org/licenses/>."
	print ""

def discover(conf):
	print "Discovering %s" % conf
	f = open(conf,'rb')
	for line in f:
		line = line.strip()
		if line.startswith("["):
			if not "general" in line and not "authentication" in line and not "!" in line:
				#Find the closing ]
				pos = line.upper().find("]")
				extension = line[1:pos]
				mac = f.next()[1:].strip()
				CID=None
				buffer=None
				try:
					buffer = f.next().strip()
					while not len(buffer.strip()) == 0:
						buffer = f.next().strip()
						if buffer.startswith('callerid'):
							data = buffer.split("=")
							CID = data[1]
				except StopIteration, e:
					do="nothing"
				print "Found extension: %s for MAC %s with CID of %s" % (extension,mac,CID)


def sanitize_number(number):
	if len(number) == 11:
		return number[1:]
	else:
		return number

def make_item(first,last,contact,counter,watch):
	item = etree.Element('item')
		
	ln = etree.Element('ln')
	ln.text = last

	fn = etree.Element('fn')
	fn.text=first

	ct = etree.Element('ct')
	ct.text = contact

	sd=etree.Element('sd')
	sd.text = "%s" % counter

	rt=etree.Element('rt')
	rt.text = "12"

	dc=etree.Element('dc')

	ad=etree.Element('ad')
	ad.text = "0"

	ar=etree.Element('ar')
	ar.text = "0"

	bw=etree.Element('bw')
	bw.text = watch

	bb=etree.Element('bb')
	bb.text="0"

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

def check_file(theFile):
	if not os.path.exists(theFile):
		print "WARNING! Could not find this directory file for this user (%s)" % theFile
		print "\tI assume that's because they don't use this feature??"
		return False
	else:
		return True

def gen_general_directory():
	# Create XML
	header = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
	
	root = etree.Element('directory')
	item_list = etree.Element('item_list')
	counter = 0
	directory = {}

	with open('mcdb.csv','rb') as csvfile:
		myreader = csv.reader(csvfile,delimiter=',',quotechar='"')
		for row in myreader:
			first = ""
			last = ""
			number = sanitize_number(row[0])
			last = row[1]
			if len(number) > 0 and len(last)> 0:
				contact = number
				watch = "0"
				counter += 1
				
				directory[counter] = first + " " + last
				item = make_item(first,last,contact,counter,watch)
				item_list.append(item)

	root.append(item_list)
	s = etree.tostring(root,pretty_print=True)
	outputfile = '000000000000-directory.xml'
	outputfile = os.path.join(rootPath,outputfile)
	print "Writing %s ..." % outputfile,
	sm = open(outputfile,'w')
	sm.write(header + "\n")
	sm.write(s)
	sm.close

#Start script

confFile = '/etc/polypy.conf'
if not os.path.exists(confFile):
	print "You must setup /etc/polypy.conf!"
	print ""
	print "Example Contents:"
	print "[polycom]"
	print "root=/path/to/provisioning/root"
	print "server=your.provisioning.server"
	print "sippath=/path/to/your/sip.conf"
	print ""
	sys.exit()

#Get settings
config = ConfigParser.RawConfigParser()
config.read(confFile)

rootPath=config.get('polycom','root')
server=config.get('polycom','server')
sippath=config.get('polycom','sippath')
#End Settings Get

for o,a in optlist:
	if o in ['-b','--blacklist']:
		print "Blacklisting %s" % a
		blacklist = a
	if o in ['-m','--mac']:
		print "Setting mac to: %s" % a
		themac = a
	elif o in ['-g','--generate-basedirectory']:
		gen_general_directory()
		sys.exit()
	elif o in ['-u','--user']:
		print "Setting user to: %s" % a
		theuser = a
	elif o in ['-h','--help']:
		usage()
		sys.exit()
	elif o in ['-l','--license']:
		showLicense()
		sys.exit()
	elif o in ['-d','--discover']:
		discover(sippath)
		sys.exit()
	elif o in ['-c','show-configs']:
		print "Current Config Settings:"
		print "Root: %s" % rootPath
		print "Server: %s" % server
		print "Sippath: %s" % sippath
		sys.exit()			
		
		
if themac == None or theuser == None:
	print "ERROR! You must specify the mac address of the phone that will use these configs as well as the user!"
	usage()
	sys.exit()

# Create XML
header = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

root = etree.Element('directory')
item_list = etree.Element('item_list')
counter = 0
directory = {}

# Load up the office contacts
root.append(item_list)
with open('users.csv','rb') as csvfile:
	myreader = csv.reader(csvfile,delimiter=',',quotechar='"')
	for row in myreader:
		number =  row[0]
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

		item = make_item(first,last,contact,counter,watch)

		directory[counter] = first + " " + last
		item_list.append(item)

speedial = '%s-sd.csv' % theuser

if check_file(speedial):

	print "INCLUDING: Speed Dial Direcotry (%s)" % speedial
	with open(speedial,'rb') as csvfile:
		myreader = csv.reader(csvfile,delimiter=',',quotechar='"')
		for row in myreader:
			first = ""
			last = ""
			number = sanitize_number(row[0])
			col2 = row[1]
			if " " in col2:
				buffer = col2.split(" ")
				first = buffer[0]
				last = buffer[1]
			else:
				first = col2
				last = ""

			contact = number
			watch = "0"
			counter += 1
			
			directory[counter] = first + " " + last
			item = make_item(first,last,contact,counter,watch)

			item_list.append(item)

companyDirectory = 'mcdb.csv'

if check_file(companyDirectory):
	print "INCLUDING: Company Direcotry (%s)" % companyDirectory
	with open(companyDirectory,'rb') as csvfile:
		myreader = csv.reader(csvfile,delimiter=',',quotechar='"')
		for row in myreader:
			print row
			first = ""
			last = row[1]
			number = sanitize_number(row[0])

			contact = number
			watch = "0"
			counter += 1
			
			directory[counter] = first + " " + last
			item = make_item(first,last,contact,counter,watch)

			item_list.append(item)

s = etree.tostring(root,pretty_print=True)
outputfile = '%s-directory.xml' % themac
outputfile = os.path.join(rootPath,outputfile)
print "Writing %s ..." % outputfile,
sm = open(outputfile,'w')
sm.write(header + "\n")
sm.write(s)
sm.close

outputfile = '%s-list.txt' % themac
outputfile = os.path.join(rootPath,outputfile)
tl = open(outputfile,'w')
for d in directory:
	line = str(d).ljust(5) + directory[d]
	tl.write(line + "\n")
	print line
tl.close
print "List saved in: %s" % outputfile
print "Done."
