#!/usr/bin/python
import sys, getopt
options = "ae:h"
longopts = ['all','extension','help']
optlist, args = getopt.getopt(sys.argv[1:],options,longopts)
print optlist