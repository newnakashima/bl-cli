#!/usr/bin/env python

import os
from os.path import expanduser
import sys
import configparser
import requests
from optparse import OptionParser
import argparse
import re

HOME = expanduser("~")
config = configparser.ConfigParser()
DEFAULT = 'default'

def command_configure(args):
    try:
        print("Please input your configuration name(default): ")
        config_name = input()
        global DEFAULT
        if config_name is '':
            config_name = DEFAULT
        global config

        print("Please input your backlog url: ")
        base_url = input()
        print("Please input your backlog access key: ")
        access_key = input()

        config[config_name] = {
            'base_url':base_url,
            'access_key': access_key,
        }

        global conffile
        with open(conffile, 'w') as f:
            config.write(f)
        with open(conffile, 'r') as f:
            print('''
Your configuration flie {filepath} is below.
            '''.format(filepath=conffile)
            )
            print(f.read())
            
    except KeyboardInterrupt:
        print("Configuration dialogue has stopped.")

def get_wiki_list(args):
    global DEFAULT
    global config
    if args.name is None:
        args.name = DEFAULT
    try:
        BACKLOG_URL = add_schema(config[args.name]['base_url'])
        BACKLOG_API_KEY = config[args.name]['access_key']
    except KeyError:
        global conffile
        print('''
There seems no configuration `{name}`
Please make sure your configuration name is exists in the {conffile}.
        '''.format(name=args.name,conffile=conffile)
        )
    res = requests.get(BACKLOG_URL + '/api/v2/wikis',
            params={
                'apiKey': BACKLOG_API_KEY,
                'projectIdOrKey': args.project
                }
            )
    return res.text

def command_wiki_list(args):
    print(get_wiki_list(args))

def add_schema(url):
    if not re.match(r"https?", url):
        url = f'https://{url}'
    if re.match(r"http:", url):
        url = re.sub('http:', 'https:', url)
    return url

def command_wiki_show(args):
    global DEFAULT
    global config
    if args.name is None:
        args.name = DEFAULT
    BACKLOG_URL = add_schema(config[args.name]['base_url'])
    BACKLOG_API_KEY = config[args.name]['access_key']
    res = requests.get(BACKLOG_URL + '/api/v2/wikis/' + args.id,
            params={
                'apiKey': BACKLOG_API_KEY,
                }
            )
    print(res.text)

def command_help(args):
    print(parser.parse_args([args.command, '--help']))

if __name__ == '__main__':
    path = HOME + '/.bl'
    conffile = path + '/credentials'
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.isdir(path):
        sys.exit(f'Path {path} is not a directory. Please make sure the path is a directory.')

    config.read(conffile)

    # 渡された引数やサブコマンドなどをパース
    parser = argparse.ArgumentParser(description='Backlog command line interface')
    subparsers = parser.add_subparsers()

    parser_configure = subparsers.add_parser('configure', help='see `configure -h`')
    parser_configure.add_argument('-o', '--output', dest='output',
            help='OUTPUT is output path of configuration file',
            metavar='OUTPUT')
    parser_configure.set_defaults(handler=command_configure)

    parser_wiki = subparsers.add_parser('wiki', help='see `wiki -h`')
    parser_wiki.add_argument('-n', '--name',
            dest='name',
            help='Select which configuration you use. If NAME is not set, `default` would be selected.',
            metavar='FILE')

    wiki_subparsers = parser_wiki.add_subparsers()

    # wikiページ一覧取得
    parser_wiki_list = wiki_subparsers.add_parser('list', help='List all wiki pages.')
    parser_wiki_list.add_argument('-p', '--project',
            dest='project',
            help='ProjectID or ProjectKey.',
            metavar='PROJECT',
            required=True)
    parser_wiki_list.set_defaults(handler=command_wiki_list)

    # wikiページ内容取得
    parser_wiki_show = wiki_subparsers.add_parser('show', help='Show a wiki page.')
    parser_wiki_show.add_argument('id')
    parser_wiki_show.add_argument('-n', '--name',
            dest='name',
            help='Select which configuration you use. If NAME is not set, `default` would be selected.',
            metavar='FILE')
    parser_wiki_show.set_defaults(handler=command_wiki_show)

    parser_help = subparsers.add_parser('help', help='see `help -h`')
    parser_help.add_argument('command', help='command name which help is shown')
    parser_help.set_defaults(handler=command_help)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()

