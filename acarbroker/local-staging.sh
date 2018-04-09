#!/bin/sh -e
#
# SCL <scott@rerobots.net>
# 2018
set -e

# etc/rabbitmq-env.conf should be installed before running this. E.g.,
# sudo cp etc/rabbitmq-env.conf /etc/rabbitmq/
sudo -u rabbitmq rabbitmq-server
