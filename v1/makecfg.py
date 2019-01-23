#!/usr/bin/python
from xml.dom import minidom
xmldoc = minidom.parse('000000000000.cfg')
app = xmldoc.getElementsByTagName('APPLICATION')
site="l3atl"

# Assemble config file list
files = ['site.cfg', 'sip-interop.cfg', 'features.cfg', 'sip-basic.cfg', 'reg-advanced.cfg']
paths = []

for f in files:
    path = "%s/%s" % (site,files)
    paths.append(path)

# Add the last one.
config = "%s/%s" % (site,mac)
paths.append(config)

setting = ", ".join(paths)

app.attributes['CONFIG_FILES'] = setting

