#!/usr/bin/env python
import os,random,sys,tempfile

def makePassword():
    buff = ''
    chars = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    for x in range(16):
        buff = buff + chars[random.randint(0,61)]

    return buff

def help():
    print "    "
    print "SUMMARY:"
    print "    This script reads a given file, and replaces #RND# with randomly "
    print "    generated passwords for use with phone authentication."
    print "    "
    print "SYNTAX:"
    print "    randomizepw.py /path/to/foo.conf"
    print "    "

def errorOut(message):
    print "================================================================================"
    print "ERROR: %s" % message
    print "================================================================================"
    help()
    exit(1)

def checkTarget(target):
    if os.path.exists(target) == False:
        errorOut("Specified target %s does not exist!" % target)
    return True

def process(line):
    line = line.strip()
    line = line.replace("#RND#",makePassword())
    return line

def setPasswords(target):

    outfd, outpath = tempfile.mkstemp()
    infile = open(target,'rb')
    outfile = open(outpath,'w')
    backupfile = open(target + ".backup",'w')

    for line in infile:
        backupfile.write(line)
        buff = process(line)
        outfile.write(buff + "\n")

    outfile.flush()

    fd = open(outpath,'r')
    
    infile.close()
    backupfile.close()

    infile = open(target,'w')
    for line in fd:
        infile.write(line)

    infile.close()
    outfile.close()

    os.remove(outpath)

    print "Done. A backup of the original file was created as %s.backup" % target


if len(sys.argv) == 1:
    errorOut("You must specify a target file to process!")

target=sys.argv[1]
checkTarget(target)
setPasswords(target)