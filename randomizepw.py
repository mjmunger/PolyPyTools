#!/usr/bin/env python3
"""Read the specified file, generate passwords for use with phone authentication.

Usage: randomizepw (-e EXTENSION |--extension EXTENSION | -a|--all) <file> [-d | --debug]

Options:
    -e EXTENSION --extension EXTENSION   Randomize the password for the specified extension.
    -a, --all                            Randomize the password for ALL extensions
    -d, --debug                          Output debugging messages

"""
import os
import random
import sys
import tempfile
import shutil
from docopt import docopt
from pprint import pprint
from polypy.sipconf import Sipconf


def error_out(message):
    print(message)
    sys.exit(1)


def make_password():
    buff = ''
    chars = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    for x in range(16):
        buff = buff + chars[random.randint(0, 61)]

    return buff


def check_target(target):
    if not os.path.exists(target):
        error_out("Specified target %s does not exist!" % target)
    return True


def process(line):
    line = line.strip()
    line = line.replace("#RND#", make_password())
    return line


def backup_file(target):
    shutil.copy(target, target + ".backup")


def set_passwords(target):
    outfd, outpath = tempfile.mkstemp()
    infile = open(target, 'rb')
    outfile = open(outpath, 'w')
    backupfile = open(target + ".backup", 'w')

    for line in infile:
        backupfile.write(line)
        buff = process(line)
        outfile.write(buff + "\n")

    outfile.flush()

    fd = open(outpath, 'r')

    infile.close()
    backupfile.close()

    infile = open(target, 'w')
    for line in fd:
        infile.write(line)

    infile.close()
    outfile.close()

    os.remove(outpath)

    print("Done. A backup of the original file was created as %s.backup" % target)


def reset_all_passwords(file, debug):
    config = Sipconf('foo', file, 'bar')
    if debug:
        config.set_debug()

    config.parse()

    for reg in config.registrations:
        reset_single_password(file, reg.extension, debug)


def reset_single_password(target_file, extension, debug):
    fp = open(target_file, 'r')

    buffer = []
    for line in fp:
        line = line.strip()
        # print("Line starts with: %s: %s" % (extension, "YES" if line.startswith("[%s]" % extension) else "NO"))

        if not line.startswith("[%s]" % extension):
            buffer.append(line + "\n")
            continue

        if line.startswith("[%s]" % extension):
            if debug:
                print("Modifying extension: %s" % extension)

            buffer.append(line + "\n")
            line = next(fp)
            while not line.startswith("["):
                # print("Line starts with secret: %s" % ("YES" if line.startswith("secret") else "NO"))
                if line.startswith("secret"):
                    line = line.strip()
                    if debug:
                        print("Updating secret for extension %s" % extension)
                    # update the password
                    secret = line.split("=")
                    secret[1] = make_password()
                    new_secret = "=".join(secret)
                    if debug:
                        print("New secret line: %s " % new_secret)
                    buffer.append(new_secret + "\n")
                else:
                    buffer.append(line)
                line = next(fp)

            if line.startswith("["):
                buffer.append(line)

    fp.close()

    fp = open(target_file, 'w')
    fp.writelines(buffer)
    fp.close()



def check_file_exists(file):
    if not os.path.exists(file):
        error_out("%s does not exist." % file)


if __name__ == '__main__':
    args = docopt(__doc__)

    file = args['<file>']

    check_file_exists(file)
    backup_file(file)

    if args['--all']:
        reset_all_passwords(file, args['--debug'])

    elif args['--extension'].isnumeric():
        reset_single_password(file, args['--extension'], args['--debug'])