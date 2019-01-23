#!/usr/bin/env python3
"""
usage: polypy validate [ asterisk | polycom ]
"""
from pprint import pprint
from docopt import docopt

if __name__ == "__main__":
    args = docopt(__doc__)
    pprint(args)

