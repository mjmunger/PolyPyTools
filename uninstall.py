#!/usr/bin/env python3
import sys
import os
from shutil import rmtree

if os.getegid() != 0:
    print("You must run this as root. Cannot continue")
    sys.exit(1)

print("Running uninstaller...")
package_path = None
lib_path = '/var/lib/polypy/'
config_path = '/etc/polypy/'
share_path = '/usr/share/polypy/'
symlink = '/usr/local/bin/polypy'

print("Uninstalling: %s" % lib_path)
rmtree(lib_path)
print("Uninstalling: %s" % share_path)
rmtree(share_path)
print("Unlinking: %s" % '/usr/local/bin/polypy')

try:
    os.unlink(symlink)
except:
    pass
