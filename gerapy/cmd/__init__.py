"""
Usage:
  gerapy.py init
  gerapy.py migrate
  gerapy.py createsuperuser
  gerapy.py server [--port=<port>] [--host=<host>]
Options:
  -h --help
  -v --version
"""
from docopt import docopt
from gerapy import version

def cmd():
    arguments = docopt(__doc__, version=version())
    print(arguments)
