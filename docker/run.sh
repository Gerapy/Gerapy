#!/bin/bash

cd /app
gerapy init
cd gerapy
gerapy migrate
gerapy initadmin
gerapy runserver 0.0.0.0:8000