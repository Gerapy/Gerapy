FROM python:3.6
WORKDIR /app
COPY run.sh /app/run.sh
RUN pip install -U gerapy \
    && chmod a+x /app/run.sh
VOLUME /app/gerapy
CMD /bin/bash /app/run.sh