#!/bin/sh -e
# Assume that the host is Ubuntu 16.04. This script might work on
# others without modification.
#
#
# SCL <scott@rerobots.net>
# 2018
set -e

sudo apt-get -y update && sudo apt-get -y dist-upgrade
sudo apt-get -y install fail2ban supervisor nginx postgresql rabbitmq-server
sudo apt-get -y install python3-virtualenv

sudo nginx -s stop

sudo systemctl stop supervisor.service
sudo systemctl disable supervisor.service

sudo /etc/init.d/rabbitmq-server stop
sudo cp -f etc/rabbitmq-env.conf /etc/rabbitmq/
sudo /etc/init.d/rabbitmq-server start

cd /var/lib/postgresql
sudo -u postgres createuser -D -R -S acb
sudo -u postgres createdb -O acb acbdb

sudo systemctl stop postgresql.service

sudo cp -f etc/nginx.conf /etc/nginx/

if ! grep \^acb /etc/passwd; then
    sudo useradd -m -s /bin/bash -U acb
fi
sudo usermod -L acb
export HOME=/home/acb

cd $HOME
sudo -u acb python3 -m virtualenv PY
sudo -u acb bash -c "source ${HOME}/PY/bin/active && pip install -U && pip install gunicorn django python-memcached"
