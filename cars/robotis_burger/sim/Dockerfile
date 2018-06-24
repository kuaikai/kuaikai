# Docker image for simulation evaluation of TurtleBot 3 Burger targets
#
# To build,
#
#     ./prepare.sh
#     docker build -t kuaikai/turtlebot3burger-sim:latest -f Dockerfile .
#
#
# SCL <scott@rerobots.net>

FROM ubuntu:xenial

RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list' \
    && apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116 \
    && apt-get update \
    && apt-get -y install \
       ros-kinetic-ros-base \
       ros-kinetic-xacro \
       ros-kinetic-robot-state-publisher \
       ros-kinetic-turtlebot3-simulations

WORKDIR /root
ENTRYPOINT ["/bin/bash"]
