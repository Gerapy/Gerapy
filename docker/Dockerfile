FROM python:3.6
WORKDIR /app
RUN pip3 install gerapy \
    & cd /app \
    & gerapy init \
    & cd gerapy \
    & gerapy migrate \
    & gerapy initadmin
VOLUME /app/gerapy
CMD ['gerapy', 'runserver']