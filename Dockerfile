# blackhole
FROM python:3.7-alpine3.9
LABEL maintainer="shawn <studyoo@foxmail.com>"

WORKDIR /app

COPY requirements.txt /app

RUN apk add --no-cache jpeg-dev \
                       zlib-dev \
                       freetype-dev \
                       lcms2-dev \
                       openjpeg-dev \
                       tiff-dev \
                       tk-dev \
                       tcl-dev \
                       harfbuzz-dev \
                       fribidi-dev \
                       gcc \
                       musl-dev \
    && echo "[global] \
index-url = http://pypi.tuna.tsinghua/simple \
trusted-host = pypi.tuna.tsinghua \
timeout = 120 \
" > /etc/pip.conf \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && mkdir output

COPY . /app

ENTRYPOINT ["python","blackhole.py"]


# docker build -f Dockerfile -t blackhole:0.0.1 .

# docker tag blackhole:0.0.1 game404/blackhole:0.0.1

# docker push game404/blackhole:0.0.1