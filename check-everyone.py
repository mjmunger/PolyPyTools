#!/usr/bin/python
import subprocess

for x in range(1,254):
	checkcmd = 'sip notify polycom-check-cfg 192.168.10.%s' % x
	args = ['asterisk','-rx',checkcmd]
	subprocess.call(args)