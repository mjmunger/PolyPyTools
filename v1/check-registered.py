#!/usr/bin/python
import subprocess


class Peer:
    name = ''
    host = ''
    dyn = 'N'
    forcerprot = 'N'
    acl = ''
    port = ''
    status = ''

    def __init__(self, line):
        buffer = line.split(" ")


# checkcmd = 'sip notify polycom-check-cfg 192.168.10.%s' % x
checkcmd = 'sip show peers'
spcmd = ['asterisk', '-rx', checkcmd]
p = subprocess.Popen(spcmd, stdout=subprocess.PIPE)
for line in iter(p.stdout.readline, ''):
    # print line
    peer = Peer(line)
