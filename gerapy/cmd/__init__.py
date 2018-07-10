from gerapy import version
from gerapy.cmd.init import init
from gerapy.cmd.parse import parse
from gerapy.cmd.generate import generate
from gerapy.server.manage import manage
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--version', action='version', version=version(), help='get version')

subparsers = parser.add_subparsers(dest='command', title='available commands', metavar='')

# migrate
parser_migrate = subparsers.add_parser('migrate', help='migrate database')

# create superuser
parser_createsuperuser = subparsers.add_parser('createsuperuser', help='create superuser')

# makemigrations
parser_makemigrations = subparsers.add_parser('makemigrations', help='create superuser')

# runserver
parser_runserver = subparsers.add_parser('runserver', help='runserver')
parser_runserver.add_argument('bind', default='127.0.0.1:8000', nargs='?', type=str, help='host and port to bind')

# init
parser_init = subparsers.add_parser('init', help='init workspace')
parser_init.add_argument('folder', default='gerapy', nargs='?', type=str, help='initial workspace folder')

# generate
parser_generate = subparsers.add_parser('generate', help='generate code for project')
parser_generate.add_argument('project', type=str, help='project to generate')

# parse
parser_parse = subparsers.add_parser('parse', help='parse project for debugging')
parser_parse.add_argument('project', type=str, help='target project')
parser_parse.add_argument('spider', type=str, help='target spider')
parser_parse.add_argument('-d', '--dir', default='.', type=str, help='default workspace')
parser_parse.add_argument('-s', '--start', default=0, type=int, help='parse start requests or not')
parser_parse.add_argument('-u', '--url', default='', type=str, help='url to parse')
parser_parse.add_argument('-c', '--callback', default='parse', type=str, help='callback')
parser_parse.add_argument('-m', '--method', default='GET', type=str, help='method')
parser_parse.add_argument('-a', '--meta', default=None, type=str, help='meta')

# loaddata
# todo
parser_loaddata = subparsers.add_parser('loaddata', help='load data from configs')
parser_loaddata.add_argument('source', type=str, help='configs path')

# dumpdata
parser_dumpdata = subparsers.add_parser('dumpdata', help='dump data to configs')
parser_dumpdata.add_argument('appname', default='core', nargs='?', type=str, help='appname')


def cmd():
    args = parser.parse_args()
    command = args.command
    if command == 'init':
        init(args.folder)
    elif command == 'generate':
        generate(args.project)
    elif command == 'parse':
        parse(args)
    else:
        manage()
