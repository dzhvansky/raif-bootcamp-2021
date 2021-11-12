FROM python:3.7-alpine AS compile-image

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    LANG="C.UTF-8" \
    PYTHON_VERSION=3.7.12 \
    PYTHONUNBUFFERED=1 \
    WORKDIR=/srv/www/

WORKDIR $WORKDIR

COPY . .

RUN apk update && apk upgrade && apk add gcc g++ curl unzip cmake && update-ca-certificates
RUN python -m venv venv && source venv/bin/activate && pip install -U pip setuptools wheel && pip install -e . && deactivate

EXPOSE 8090

ENTRYPOINT ["venv/bin/python", "bin/app/main.py", "--host", "0.0.0.0", "--port", "8090"]
