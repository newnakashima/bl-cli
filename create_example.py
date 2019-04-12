import configparser
import os
from os.path import expanduser
import sys
from optparse import OptionParser

HOME = expanduser("~")
config = configparser.ConfigParser()

parser = OptionParser()
parser.add_option("-o", "--output", dest="output",
        help="OUTPUT is output path of configuration file",
        metavar="OUTPUT")
(options, args) = parser.parse_args()

try:
    print("Please input your backlog url: ")
    base_url = input()
    print("Please input your backlog access key: ")
    access_key = input()

    config['nksm'] = {
        'base_url':base_url,
        'access_key': access_key,
    }

    if options.output is None:
        path = HOME + '/.bl'
        conffile = path + '/credentials'
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.isdir(path):
            sys.exit(f'Path {path} is not a directory. Please make sure the path is a directory.')
    else:
        conffile = options.output
    with open(conffile, 'w') as configfile:
        config.write(configfile)
except KeyboardInterrupt:
    print("Configuration dialogue has stopped.")
