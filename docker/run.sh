#!/bin/bash

gerapy init
gerapy migrate
gerapy initadmin
gerapy runserver 0.0.0.0:8000
