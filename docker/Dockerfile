FROM python:latest
MAINTAINER thsheep
COPY requirements.txt /tmp/requirements.txt
COPY run.sh /usr/bin/run.sh
RUN mkdir /app \
    && pip3 install -r /tmp/requirements.txt \
    && chmod a+x /usr/bin/run.sh
WORKDIR /app
VOLUME ["/app/gerapy"]
ENTRYPOINT /usr/bin/run.sh