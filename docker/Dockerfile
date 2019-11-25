FROM python:3.6
WORKDIR /app
COPY . /app/source
COPY ./docker/run.sh /app/run.sh
RUN cd /app/source \
    && pip install . \
    && chmod a+x /app/run.sh
VOLUME /app/gerapy
CMD /bin/bash /app/run.sh