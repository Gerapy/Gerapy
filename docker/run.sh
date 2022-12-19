#!/bin/bash

cd /app || return
gerapy init
cd gerapy || return
gerapy migrate
gerapy initadmin
gerapy runserver 0.0.0.0:8000