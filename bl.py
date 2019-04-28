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
API_PATH = '/api/v2'

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
        BACKLOG_URL = add_schema_and_path(config[args.name]['base_url'])
        BACKLOG_API_KEY = config[args.name]['access_key']
    except KeyError:
        global conffile
        print('''
There seems no configuration `{name}`
Please make sure your configuration name is exists in the {conffile}.
        '''.format(name=args.name,conffile=conffile)
        )
    res = requests.get(BACKLOG_URL + '/wikis',
            params={
                'apiKey': BACKLOG_API_KEY,
                'projectIdOrKey': args.project
                }
            )
    return res.text

def command_wiki_list(args):
    print(get_wiki_list(args))

def add_schema_and_path(url):
    if not re.match(r"https?", url):
        url = f'https://{url}'
    if re.match(r"http:", url):
        url = re.sub('http:', 'https:', url)
    return url + API_PATH

def get_wiki_show(args):
    global DEFAULT
    global config
    if args.name is None:
        args.name = DEFAULT
    BACKLOG_URL = add_schema_and_path(config[args.name]['base_url'])
    BACKLOG_API_KEY = config[args.name]['access_key']
    res = requests.get(BACKLOG_URL + '/wikis/' + args.id,
            params={
                'apiKey': BACKLOG_API_KEY,
                }
            )
    return res.text

def command_wiki_show(args):
    print(get_wiki_show(args))

def get_projects_list(args):
    global DEFAULT
    global config
    if args.name is None:
        args.name = DEFAULT
    BACKLOG_URL = add_schema_and_path(config[args.name]['base_url'])
    BACKLOG_API_KEY = config[args.name]['access_key']
    archived = 'true' if args.archived else 'false'
    all_projects = 'true' if args.all else 'false'
    res = requests.get(BACKLOG_URL + '/projects',
            params={
                'apiKey': BACKLOG_API_KEY,
                'archived': archived,
                'all': all_projects,
                }
            )
    return res.text

def command_projects_list(args):
    print(get_projects_list(args))

def get_projects_show(args):
    global DEFAULT
    global config
    if args.name is None:
        args.name = DEFAULT
    BACKLOG_URL = add_schema_and_path(config[args.name]['base_url'])
    BACKLOG_API_KEY = config[args.name]['access_key']
    res = requests.get(BACKLOG_URL + '/projects/' + args.project,
            params={
                'apiKey': BACKLOG_API_KEY,
            }
    )
    return res.text

def command_projects_show(args):
    print(get_projects_show(args))

def get_projects_update(args):
    global DEFAULT
    global config
    if args.name is None:
        args.name = DEFAULT
    BACKLOG_URL = add_schema_and_path(config[args.name]['base_url'])
    BACKLOG_API_KEY = config[args.name]['access_key']
    data = {}
    keys = [
        'p_name',
        'p_key',
        'chartEnabled',
        'subtaskingEnabled',
        'projectLeaderCanEditProjectLeader',
        'textFormattingRule',
        'archived',
    ]
    for key in keys:
        if hasattr(args, key):
            key = re.sub(r'p_(.*)', r'\1', key)
            data[key] = getattr(args, key)
    res = requests.patch(BACKLOG_URL + '/projects/' + args.project,
            params={ 'apiKey': BACKLOG_API_KEY },
            data=data
    )
    return res.text

def command_projects_update(args):
    print(get_projects_update(args))

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
    parser.add_argument('-n', '--name',
            dest='name',
            help='Select which configuration you use. If NAME is not set, `default` would be selected.',
            metavar='NAME')

    subparsers = parser.add_subparsers()

    parser_configure = subparsers.add_parser('configure', help='see `configure -h`')
    parser_configure.add_argument('-o', '--output', dest='output',
            help='OUTPUT is output path of configuration file',
            metavar='OUTPUT')
    parser_configure.set_defaults(handler=command_configure)

    parser_wiki = subparsers.add_parser('wiki', help='see `wiki -h`')
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
    parser_wiki_show.set_defaults(handler=command_wiki_show)

    parser_help = subparsers.add_parser('help', help='see `help -h`')
    parser_help.add_argument('command', help='command name which help is shown')
    parser_help.set_defaults(handler=command_help)

    # project一覧取得
    parser_projects = subparsers.add_parser('projects', help='see `projects -h`')
    projects_subparsers = parser_projects.add_subparsers()
    parser_projects_list = projects_subparsers.add_parser('list', help='List projects')
    parser_projects_list.add_argument('-a', '--archived',
            action='store_true',
            dest='archived',
            help='Include archived project or not')
    parser_projects_list.add_argument('--all',
            action='store_true',
            dest='all',
            help="Include the project which you don't participated or not")
    parser_projects_list.set_defaults(handler=command_projects_list)

    # project情報取得
    parser_projects_show = projects_subparsers.add_parser('show', help='see `projects show -h`')
    parser_projects_show.add_argument('project',
            help='ProjectID or ProjectKey',
            metavar='PROJECT')
    parser_projects_show.set_defaults(handler=command_projects_show)

    # project更新
    parser_projects_update = projects_subparsers.add_parser('update', help='see `projects update -h`')
    parser_projects_update.add_argument('project',
            help='ProjectID or ProjectKey',
            metavar='PROJECT')
    parser_projects_update.set_defaults(handler=command_projects_update)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()

