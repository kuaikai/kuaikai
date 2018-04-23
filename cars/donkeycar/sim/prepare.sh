#!/bin/sh -e
# Prepare to build Docker image etc.
#
#
# SCL <scott@rerobots.net>
# 2018
set -e

mkdir -p extern
if [ ! -f extern/donkey-master.tar.gz ]
then
    echo "Fetching snapshot of donkey Python package..."
    curl -L -o extern/donkey-master.tar.gz https://github.com/wroscoe/donkey/archive/master.tar.gz
fi

rm -fv build
mkdir build
cd build

tar -xzf ../extern/donkey-master.tar.gz

echo "Ready"
