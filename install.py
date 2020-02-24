#!/usr/bin/env python3
import os
import sys
import json
from shutil import copyfile
import subprocess

if os.getegid() != 0:
    print("You must run this as root. Cannot continue")
    sys.exit(1)

package_path = None
lib_path = '/var/lib/polypy'
config_path = '/etc/polypy/'
share_path = '/usr/share/polypy/'
local_bin = '/usr/local/bin/'

commands = []
commands.append("apt update".split(" "))
commands.append("apt -y upgrade".split(" "))
commands.append("pip3 install pip --upgrade".split(" "))
commands.append("pip3 install docopt".split(" "))
commands.append("pip3 install requests".split(" "))

for command in commands:
    print("Executing: {}".format(" ".join(command)))

    try:
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout= subprocess.PIPE)
    except subprocess.TimeoutExpired:
        proc.kill()
        print("Could not update system. Cannot install")
        outs, errs = proc.communicate()
        print(errs)
        sys.exit(1)

    outs, errs = proc.communicate()
    print(outs.decode("utf-8")).strip()

paths = [lib_path, config_path, share_path]

for path in sys.path:
    if '/usr/local/lib' in path:
        package_path = os.path.join(path, "poly_py_tools")

if not os.path.exists(package_path):
    os.mkdir(package_path)

for path in paths:
    if not os.path.exists(path):
        os.mkdir(path)

for root, dirs, files in os.walk(os.path.join(os.getcwd(), "poly_py_tools")):
    for file in files:
        src = os.path.join(root, file)
        copyfile(src, os.path.join(package_path, file))

copyfile("lib/10k-most-common.txt", os.path.join(lib_path, "10k-most-common.txt"))
copyfile("lib/csvguess.json", os.path.join(lib_path, "csvguess.json"))
copyfile("polypy.py", os.path.join('/usr/local/bin/', 'polypy'))
os.chmod(os.path.join('/usr/local/bin/', 'polypy'), 0o777)

configs = {}
configs['lib_path'] = lib_path
configs['share_path'] = share_path
configs['config_path'] = config_path
configs['package_path'] = package_path
configs['server_addr'] = None
configs['paths'] = None

f = open(os.path.join(config_path, 'polypy.conf'), 'w')
f.write(json.JSONEncoder().encode(configs))
f.close()

print("Setup complete.")