#!/bin/sh -e
# Assume that the host is Ubuntu 16.04. This script might work on
# others without modification.
#
#
# SCL <scott@rerobots.net>
# 2018
set -e

sudo apt-get -y update && sudo apt-get -y dist-upgrade
sudo apt-get -y install fail2ban nginx postgresql rabbitmq-server

sudo /etc/init.d/rabbitmq-server stop
sudo cp -f etc/rabbitmq-env.conf /etc/rabbitmq/
sudo /etc/init.d/rabbitmq-server start

cd /var/lib/postgresql
sudo -u postgres createuser -D -R -S alice
sudo -u postgres createdb -O alice alicedb

sudo systemctl stop postgresql.service
