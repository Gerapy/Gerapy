FROM python:3.10 AS build
ENV PATH="/root/.local/bin:$PATH"
RUN \
    curl -sSL https://install.python-poetry.org | python3 - &&\
    poetry --version

WORKDIR /app
COPY . /app

RUN \
    poetry install &&\
    poetry build --format wheel

# ---------------------------------------------
FROM python:3.10
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY ./docker/run.sh /app/run.sh
COPY --from=build /app/dist/gerapy-*.whl /app/
RUN \
    pip install /app/gerapy-*.whl &&\
    chmod a+x /app/run.sh
VOLUME /app/gerapy
CMD /bin/bash /app/run.sh