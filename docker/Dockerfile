FROM python:3.6
WORKDIR /app
COPY run.sh /app/run.sh
RUN pip3 install -U gerapy \
    && chmod a+x /app/run.sh
VOLUME /app/gerapy
ENTRYPOINT /app/run.sh