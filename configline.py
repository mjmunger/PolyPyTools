#!/usr/bin/python
from xml.dom import minidom
import os,sys, getopt, ConfigParser

config = ConfigParser.RawConfigParser()
config.read('/etc/polypy.conf')

options		  = "ace:hls:t:"
longopts	  = ['all','extension=','help','server=','site=','license','show-configs']
optlist, args = getopt.getopt(sys.argv[1:],options,longopts)

###
# Parses sip.conf entries to generate the sip-basic.cfg registrations.
# It's expecting an entry like the one below where:
# * The extension is in the brackets
# * The first line after the extension is a COMMENTED mac address for the phone / user.
# * The next line is the secret
# * The last line is the CID.
##
# Example
##
# [111](l3office)
# ;0004f2f957f9
# secret=shoonfa9s3k
# callerid="Conference Phone" <111>
###
def usage():
	print ""
	print "Usage: configline.py [options]"
	print ""
	print "FUNCTION SUMMARY"
	print "Parses sip.conf entries to generate the sip-basic.cfg registrations."
	print "It's expecting an entry like the one below where:"
	print "* The extension is in the brackets"
	print "* The first line after the extension is a COMMENTED mac address for the phone / user."
	print "* The next line is the secret"
	print "* The last line is the CID."
	print ""
	print "EXAMPLE"
	print ""
	print "[111](l3office)"
	print ";0004f2f957f9"
	print "secret=shoonfa9s3k"
	print 'callerid="Conference Phone" <111>'
	print ""
	print "NOTE: It's probably best to copy the extensions from sip.conf into a separate file before running this script. This way,"
	print "		 you can ensure the formatting is correct, and there will not be any erroneous files created from ther configs that"
	print "      which may match the patterns this script looks for."
	print ""
	print "OPTION LIST"
	print ""
	print "-a       --all             Process all extensions."
	print "-c       --show-configs    Show the configs for this app"
	print "-e[NNN]  --extension NNN   Process extension NNN only."
	print "-s[foo]  --site foo        Set the site name to bar. (This is the directory where the phone will look for configs under document root)"
	print "-l       --license         Display the license for this software"
	print ""

def showLicense():
	print "Process sip.conf into Polycom configs."
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

class Config:
	server		 = ""
	site		 = ""
	extension	 = ""
	secret		 = ""
	mac			 = ""
	registration = "1"

	def __init__(self,server,site,extension,secret,meta,root):

		try:
			buf = meta.split('|')
			mac = buf[0]
			model = buf[1]
		except Exception, e:
			print e
			sys.exit()

		self.server = server
		self.site = site
		self.extension = extension
		self.secret = secret
		self.mac = mac
		self.root = root

	def writeConfig(self):
		print "Writing Registration %s for %s" % (self.registration,self.mac)
		if self.registration == "1":
			xmldoc = minidom.parse('Config/reg-basic.cfg')
			itemlist = xmldoc.getElementsByTagName('reg')
			for s in itemlist:
				s.attributes['reg.1.address'] = '%s@%s' % (extension,server)
				s.attributes['reg.1.auth.password'] = secret
				s.attributes['reg.1.auth.userId'] = extension
				s.attributes['reg.1.label'] = extension
				# s.attributes['reg.1.outboundProxy.address']
		elif self.registration == "2":
			# This is the second registration, so we need to open up the first one, and add to that....
			xmldoc = minidom.parse(self.mac)
			itemlist = xmldoc.getElementsByTagName('reg')
			for s in itemlist:
				s.attributes['reg.2.address'] = '%s@%s' % (extension,server)
				s.attributes['reg.2.auth.password'] = secret
				s.attributes['reg.2.auth.userId'] = extension
				s.attributes['reg.2.label'] = "PPC"
				# s.attributes['reg.1.outboundProxy.address']
		output = xmldoc.toxml()
		print self.site
		print self.mac
		macfilePath = os.path.join(os.path.join(self.root,self.site),self.mac)
		print "Writing MAC file: %s" % macfilePath
		xp = open(macfilePath,'w')
		xp.write(output)
		xp.close()

		xmldoc = minidom.parse('Config/000000000000.cfg')
		app = xmldoc.getElementsByTagName('APPLICATION')

		# Assemble config file list
		files = ['site.cfg', 'sip-interop.cfg', 'features.cfg', 'sip-basic.cfg', 'reg-advanced.cfg']
		paths = []

		for f in files:
			path = "%s/%s" % (site,f)
			paths.append(path)

		# Add the last one.
		config = "%s/%s" % (site,self.mac)
		paths.append(config)

		setting = ", ".join(paths)

		for a in app:
			a.attributes['CONFIG_FILES'] = setting

		output =  xmldoc.toxml()
		configfile = os.path.join(self.root,self.mac+".cfg")
		print "Writing: %s" % configfile
		cp = open(configfile,"w")
		cp.write(output)
		cp.close()

site = None

root=config.get('polycom','root')
server=config.get('polycom','server')
sippath=config.get('polycom','sippath')

for o,a in optlist:
	if o in ["-s",'--site']:
		site = a
	elif o in ['-c','--show-configs']:
		print "Current Config Settings:"
		print "Root: %s" % root
		print "Server: %s" % server
		print "Sippath: %s" % sippath
		sys.exit()

# if site == None:
# 	print ""
# 	print "You must specify a site with -s"
# 	print ""
# 	usage()
# 	sys.exit()

fp = open('/home/asterisk/asterisk-bin/asterisk/sip.conf')

maclist = []
serverlist = {}
skiplist = ['[general]', '[authentication]']

reg1 = {}
reg2 = {}

for line in fp:
	buff = line.strip()
	if buff.startswith("["):

			#Don't process lines with bad keywords in them.
			if buff in skiplist:
				continue

			print "Processing: %s" % buff

			# OK, now we can process because this line should be "good"

			#Let's see if it's a template. If it is, we need to grab the server IP for this template.
			if "!" in buff:
				#It's a template! Parse the name, and find the server IP for this template
				#Get the location of "]"
				pos = buff.find("]")
				template = buff[1:pos]
				buff = fp.next().strip().split("=")
				server_uri = buff[1]
				serverlist[template] = server_uri
				#We're done here. Keep moving.
				continue

			# if not site in buff:
			# 	print "%s is not part of site %s. Skipping" % (buff,site)
			# 	continue
			extension = line[1:4]
			#Discover the template for this phone.
			pos1   = line.find("(") +1
			pos2   = line.find(")")
			site   = line[pos1:pos2]
			server = serverlist[site]


			buff = fp.next()
			mac = buff[1:].strip()
			buff = fp.next().split("=")
			secret = buff[1].strip()

			thisConfig = Config(server,site,extension,secret,mac,root)
			# print thisConfig.extension

			for o,a in optlist:
				if o in ["-h",'--help']:
					usage()
					sys.exit()
				elif o in ["-l",'--license']:
					showLicense()
					sys.exit()
				elif o in ['-a','--all']:
					print "Writing Config (all)"
					if not mac in maclist:
						maclist.append(mac)
						thisConfig.registration = "1"
						reg1[mac] = thisConfig.extension
					else:
						thisConfig.registration = "2"
						reg2[mac] = thisConfig.extension
					thisConfig.writeConfig()
				elif o in ['-e','--extension']:
					# print "does %s = %s?" % (a,thisConfig.extension)
					if a == thisConfig.extension:
						if not mac in maclist:
							maclist.append(mac)
							thisConfig.registration = "1"
						else:
							thisConfig.registration = "2"
						print "Writing Specific Extension: %s" % thisConfig.extension
						thisConfig.writeConfig()
print ""
print "REGISTRATION SUMMARY"
for mac in reg1:
	r1 = reg1[mac]
	r2 = reg2[mac]
	print  "%s has %s and %s" % (mac,r1,r2)
fp.close()
