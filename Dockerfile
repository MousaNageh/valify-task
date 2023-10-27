FROM python:3.11-alpine3.17


WORKDIR /app

COPY requirements.txt /app/

RUN apk add --update --no-cache \
    postgresql-client \
    libpng-dev \
    jpeg-dev \
    libwebp-dev \
    lcms2-dev \
    freetype-dev \
    libimagequant-dev \
    bash && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    gcc musl-dev \
    python3-dev \
    libffi-dev \
    postgresql \
    ca-certificates \
    build-base  \
    postgresql-dev \
    zlib \
    zlib-dev \
    libpq-dev \
    libpq \
    coreutils \
    dpkg-dev dpkg \
    make \
    openssl-dev \
    linux-headers && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt && \
    apk del .tmp-build-deps

ENV PATH="/py/bin:$PATH"

COPY . /app

