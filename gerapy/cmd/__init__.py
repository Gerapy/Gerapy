"""
Usage:
  gerapy init [<folder>]
  gerapy migrate
  gerapy makemigrations
  gerapy createsuperuser
  gerapy runserver [<host:port>]
  gerapy generate [<project>]
  gerapy parse <project> <spider> [--start=<start>] [--url=<url>] [--callback=<callback>] [--method=<method>] [--dir=<dir>]
  gerapy loaddata <source>
  gerapy dumpdata [<appname>]
Options:
  -h --help
  -v --version
"""
from os.path import join
from docopt import docopt
from gerapy import version
from gerapy.cmd.init import init
from gerapy.cmd.server import server
from gerapy.cmd.generate import generate
from gerapy.server.core.parser import get_start_results, get_follow_results


def cmd():
    arguments = docopt(__doc__, version=version())
    print(arguments)
    if arguments.get('init'):
        # init folder
        init(arguments.get('<folder>'))
    if arguments.get('generate'):
        # generate code for project
        generate(arguments.get('<project>'))
    if arguments.get('parse'):
        project_path = join(arguments.get('--dir'), arguments.get('<project>'))
        spider_name = arguments.get('<spider>')
        if arguments.get('--start'):
            get_start_results(project_path, spider_name)
        else:
            url = arguments.get('--url')
            print('url', url)
            callback = arguments.get('--callback')
            print('callback', callback)
            get_follow_results(url, project_path, spider_name, callback)
    else:
        # call django cmd
        server()
