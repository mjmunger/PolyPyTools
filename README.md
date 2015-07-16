# PolyPyTools
Command line tools for provisioning Polycom Phones with Asterisk

# Getting Started

Clone this repo into /usr/src/, and then create symbolic links in /usr/local/bin for each of the tools you will use. The tools EXPECT to be run from the root directory (document root) where all the provisioning files will be kept. See polypy.conf.sample for more information on this as well as a template to install to /etc/polypy.conf, which is required for operation.

# Tool List
##configline.py - Generate Polycom config files for a given SIP entry.

This script reads the sip.conf file, and generates the appropriate configuration file for a given extension or group of extensions. Use configline.py -h for full help.

##gendir.py

This script generates local phone directories as well as the general directory for Polycom phones (in XML format). It creates the MAC-directory.xml files from the following files (if they exist):
1. users.csv - a CSV file of the extensions of users that you want to appear first in the directory. Gendir.py assumes that users here should have buddy watch enabled.
1. [user]-sd.csv - a comma separated list of numbers and people that should appear next as "speed dials"
1. [user]-personal.csv - a comma separated list of numbers and people that should appear as part of the "personal directory" for that phone's user. This can be completely omitted if you use user-sd.csv for all that data.

Using the -g swich will read a file called "mcdb.csv" and populate its contents into the 0000000000-directory.xml as the base directory for all phones at all sites.
