"""
Usage:
  gerapy init [<folder>]
  gerapy migrate
  gerapy makemigrations
  gerapy createsuperuser
  gerapy runserver [<host:port>]
  gerapy generate [<project>]
  gerapy loaddata <source>
  gerapy dumpdata [<appname>]
Options:
  -h --help
  -v --version
"""
from docopt import docopt
from gerapy import version
from gerapy.cmd.init import init
from gerapy.cmd.server import server
from gerapy.cmd.generate import generate


def cmd():
    arguments = docopt(__doc__, version=version())
    print(arguments)
    if arguments.get('init'):
        # init folder
        init(arguments.get('<folder>'))
    if arguments.get('generate'):
        # generate code for project
        generate(arguments.get('<project>'))
    else:
        # call django cmd
        server()
