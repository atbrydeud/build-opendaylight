#!/bin/bash

#
# Opendaylight build script
#

set -e -x

CURRENT=`pwd`

cd src/odlparent
mvn clean install

cd ${CURRENT}
cd src/yangtools
mvn clean install

cd ${CURRENT}
cd src/controller
mvn clean install
