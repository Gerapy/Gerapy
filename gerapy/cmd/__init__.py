"""
Usage:
  gerapy init [--folder=<folder>]
  gerapy migrate
  gerapy makemigrations
  gerapy createsuperuser
  gerapy runserver [<host:port>]
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


def cmd():
    arguments = docopt(__doc__, version=version())
    
    if arguments.get('init'):
        # nit folder
        init(arguments.get('--folder'))
    else:
        # Call django cmd
        server()
