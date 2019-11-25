FROM python:3.6
WORKDIR /app
COPY . /app/source
COPY ./docker/run.sh /app/run.sh
RUN pip install . \
    && chmod a+x /app/run.sh
VOLUME /app/gerapy
CMD /bin/bash /app/run.sh