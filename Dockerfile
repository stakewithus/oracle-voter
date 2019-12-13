FROM python:3.7.5-alpine3.10 AS build-deps

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev gmp-dev libressl libressl-dev

RUN mkdir -p /opt/pybuild/venv

WORKDIR /opt/pybuild

COPY requirements.txt .

RUN python3 -m venv /opt/pybuild/venv

ENV PATH="/opt/pybuild/venv/bin:$PATH"

RUN pip install -r requirements.txt


COPY oracle_voter oracle_voter

# WORKDIR /opt/pybuild/oracle_voter

COPY setup.py .

RUN python setup.py install

FROM python:3.7.5-alpine3.10

COPY --from=build-deps /opt/pybuild/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["python", "/opt/venv/bin/oracle_voter"]
