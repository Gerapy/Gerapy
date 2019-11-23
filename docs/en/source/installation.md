# Installation

Gerapy supports Python 3.x and does not support Python 2.

Installation command:

```
pip3 install -U gerapy
```

The gerapy command can be called directly after the installation is complete:

```
gerapy
```

If a similar output appears, the installation is successful:

```
Usage: gerapy [-v] [-h] ...

Gerapy 0.9.1 - Distributed Crawler Management Framework

Optional arguments:
  -v, --version Get version of Gerapy
  -h, --help Show this help message and exit

Available commands:
    Init Init workspace, default to gerapy
    Initadmin Create default super user admin
    Runserver Start Gerapy server
    Migrate Migrate database
    Createsuperuser Create a custom superuser
    Makemigrations Generate migrations for database
    Generate Generate Scrapy code for configurable project
    Parse parse project for debugging
    Loaddata Load data from configs
    Dumpdata Dump data to configs
```

If an error occurs, please go to [Gerapy Issues](https://github.com/Gerapy/Gerapy/issues) to search for a solution or issue a question, thank you for your support.