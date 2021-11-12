FROM python:3.7-bullseye AS compile-image

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    LANG="C.UTF-8" \
    PYTHON_VERSION=3.7.12 \
    PYTHONUNBUFFERED=1 \
    WORKDIR=/srv/www/

WORKDIR $WORKDIR

COPY . .

RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc g++ curl unzip cmake && update-ca-certificates
RUN python -m venv venv && chmod 777 venv/bin/activate && ./venv/bin/activate
RUN venv/bin/pip install -U pip setuptools wheel && venv/bin/pip install -e .

EXPOSE 8090

ENTRYPOINT ["venv/bin/python", "bin/app/main.py", "--host", "0.0.0.0", "--port", "8090"]
