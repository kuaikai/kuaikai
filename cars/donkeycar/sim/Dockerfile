# docker build -t kuaikai/donkeycar-sim:latest -f Dockerfile .
#
# SCL <scott@rerobots.net>

FROM continuumio/miniconda3:latest

COPY build/donkey-master /root/extern/donkey-master/

WORKDIR /root/extern/donkey-master
RUN bash -c "conda create -n PY && source activate PY && pip install ."

WORKDIR /root
ENTRYPOINT ["/bin/bash"]
