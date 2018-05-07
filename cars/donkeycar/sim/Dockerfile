# docker build -t kuaikai/donkeycar-sim:latest -f Dockerfile .
#
# SCL <scott@rerobots.net>

FROM continuumio/miniconda3:latest

RUN bash -c "conda create -n PY && pip install -U pip"

COPY Adafruit_PCA9685-pkg /root/extern/Adafruit_PCA9685-pkg/
WORKDIR /root/extern/Adafruit_PCA9685-pkg
RUN bash -c "source activate PY && pip install ."

COPY picamera-pkg /root/extern/picamera-pkg/
WORKDIR /root/extern/picamera-pkg
RUN bash -c "source activate PY && pip install ."

COPY build/donkey-master /root/extern/donkey-master/
WORKDIR /root/extern/donkey-master
RUN bash -c "source activate PY && pip install .[pi]"

WORKDIR /root
ENTRYPOINT ["/bin/bash"]
