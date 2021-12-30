import sys
from gerapy import version
from gerapy.server.core.utils import str2bool, str2str, str2json, str2body
import argparse

optional_title = 'Optional arguments'


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super(CapitalisedHelpFormatter, self).__init__(prog,
                                                       indent_increment=2,
                                                       max_help_position=30,
                                                       width=200)
        self._action_max_length = 20

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

    class _Section(object):

        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []

        def format_help(self):
            # format the indented section
            if self.parent is not None:
                self.formatter._indent()
            join = self.formatter._join_parts
            item_help = join([func(*args) for func, args in self.items])
            if self.parent is not None:
                self.formatter._dedent()

            # return nothing if the section was empty
            if not item_help:
                return ''

            # add the heading if the section was non-empty
            if self.heading is not argparse.SUPPRESS and self.heading is not None:
                current_indent = self.formatter._current_indent
                if self.heading == optional_title:
                    heading = '%*s%s:\n' % (current_indent, '', self.heading)
                else:
                    heading = '%*s%s:' % (current_indent, '', self.heading)
            else:
                heading = ''

            return join(['\n', heading, item_help])


parser = argparse.ArgumentParser(description='Gerapy %s - Distributed Crawler Management Framework' % version(),
                                 formatter_class=CapitalisedHelpFormatter, add_help=False)
parser._optionals.title = optional_title

parser.add_argument('-v', '--version', action='version',
                    version=version(), help='Get version of Gerapy')
parser.add_argument('-h', '--help', action='help',
                    help='Show this help message and exit')

subparsers = parser.add_subparsers(
    dest='command', title='Available commands', metavar='')

# init
parser_init = subparsers.add_parser(
    'init', help='Init workspace, default to gerapy')
parser_init.add_argument('folder', default='gerapy',
                         nargs='?', type=str, help='Initial workspace folder')

# init admin
parser_initadmin = subparsers.add_parser(
    'initadmin', help='Create default super user admin')

# runserver
parser_runserver = subparsers.add_parser(
    'runserver', help='Start Gerapy server')
parser_runserver.add_argument(
    'bind', default='127.0.0.1:8000', nargs='?', type=str, help='Host and port to bind')

# migrate
parser_migrate = subparsers.add_parser('migrate', help='Migrate database')

# create superuser
parser_createsuperuser = subparsers.add_parser(
    'createsuperuser', help='Create a custom superuser')

# makemigrations
parser_makemigrations = subparsers.add_parser(
    'makemigrations', help='Generate migrations for database')

# generate
parser_generate = subparsers.add_parser(
    'generate', help='Generate Scrapy code for configurable project')
parser_generate.add_argument('project', type=str, help='Project to generate')

# parse
parser_parse = subparsers.add_parser(
    'parse', help='Parse project for debugging')
parser_parse.add_argument('project', type=str, help='Target project')
parser_parse.add_argument('spider', type=str, help='Target spider')
parser_parse.add_argument('-d', '--dir', default='.',
                          type=str, help='Default workspace')
parser_parse.add_argument('-s', '--start', default=False, type=str2bool, nargs='?', const=True,
                          help='Parse start requests or not')
parser_parse.add_argument('-u', '--url', default='',
                          type=str, help='Url to parse')
parser_parse.add_argument(
    '-c', '--callback', default='parse', type=str2str, nargs='?', help='Callback')
parser_parse.add_argument('-m', '--method', default='GET',
                          type=str, help='Request method')
parser_parse.add_argument('-a', '--meta', default=None,
                          type=str2json, nargs='?', help='Extra meta info')
parser_parse.add_argument('-p', '--priority', default=0,
                          type=int, help='Request priority')
parser_parse.add_argument('-f', '--dont_filter', default=False,
                          type=str2bool, nargs='?', help='Do not filter')
parser_parse.add_argument('-b', '--body', default=None,
                          type=str2body, nargs='?', help='Request body')
parser_parse.add_argument('--headers', default=None,
                          type=str2json, nargs='?', help='Request headers')
parser_parse.add_argument('--cookies', default=None, type=str2json,
                          nargs='?', help='Request cookies, list or dict')

# loaddata
parser_loaddata = subparsers.add_parser(
    'loaddata', help='Load data from configs')
parser_loaddata.add_argument('source', type=str, help='Configs path')

# dumpdata
parser_dumpdata = subparsers.add_parser(
    'dumpdata', help='Dump data to configs')
parser_dumpdata.add_argument(
    'appname', default='core', nargs='?', type=str, help='Appname')

# show help info when no args
if len(sys.argv[1:]) == 0:
    parser.print_help()
    parser.exit()


def cmd():
    """
    run from cmd
    :return:
    """
    args = parser.parse_args()
    command = args.command
    # init workspace for gerapy
    if command == 'init':
        from gerapy.cmd.init import init
        init(args.folder)
    # generate code according to configuration
    elif command == 'generate':
        from gerapy.cmd.generate import generate
        generate(args.project)
    # debug parse for project
    elif command == 'parse':
        from gerapy.cmd.parse import parse
        parse(args)
    # init admin
    elif command == 'initadmin':
        from gerapy.cmd.initadmin import initadmin
        initadmin()
    else:
        from gerapy.server.manage import manage
        manage()


# for console debugger
if __name__ == '__main__':
    cmd()
