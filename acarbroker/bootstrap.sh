#!/bin/sh -e
# Assume that the host is Ubuntu 16.04. This script might work on
# others without modification.
#
#
# SCL <scott@rerobots.net>
# 2018
set -e

sudo apt-get -y update && sudo apt-get -y dist-upgrade
sudo apt-get -y install fail2ban supervisor nginx postgresql rabbitmq-server memcached docker.io
sudo apt-get -y install python3-virtualenv

sudo nginx -s stop || true

sudo systemctl stop supervisor.service
sudo systemctl disable supervisor.service

sudo /etc/init.d/rabbitmq-server stop
sudo cp -f etc/rabbitmq-env.conf /etc/rabbitmq/
sudo /etc/init.d/rabbitmq-server start

sudo cp -f etc/nginx.conf /etc/nginx/

sudo cp -f etc/pg_hba.conf /etc/postgresql/9.5/main/

sudo systemctl start postgresql.service
CWD=`pwd`
cd /var/lib/postgresql
sudo -u postgres createuser -D -R -S acb
sudo -u postgres createdb -O acb acbdb
cd $CWD

if ! grep \^acb /etc/passwd; then
    sudo useradd -m -s /bin/bash -G docker -U acb
fi
sudo usermod -L acb
export HOME=/home/acb

sudo mv etc ${HOME}/
sudo chown -R acb:acb ${HOME}/etc

cd $HOME
sudo -u acb python3 -m virtualenv -p python3 PY
sudo -u acb bash -c "source ${HOME}/PY/bin/activate && pip install -U pip && pip install gunicorn django psycopg2 python-memcached celery requests pyjwt cryptography"
