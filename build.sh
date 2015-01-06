#!/bin/bash

#
# Opendaylight build script
#

set -e -x

CURRENT=`pwd`

cat << EOF > pom.xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.opendaylight.aggregators</groupId>
  <artifactId>controller-aaa-aggregator</artifactId>
  <version>1.0.0</version>
  <packaging>pom</packaging>
  <modules>
  	<module>controller</module>
  	<module>aaa</module>
  </modules>
</project>
EOF

cd src/odlparent
mvn clean install -Dmaven.repo.local=$CURRENT/.m2repo -Dorg.ops4j.pax.url.mvn.localRepository=$CURRENT/.m2repo

cd ${CURRENT}
cd src/yangtools
mvn clean install -Dmaven.repo.local=$CURRENT/.m2repo -Dorg.ops4j.pax.url.mvn.localRepository=$CURRENT/.m2repo

cd ${CURRENT}
cd src/controller
mvn clean install -Dmaven.repo.local=$CURRENT/.m2repo -Dorg.ops4j.pax.url.mvn.localRepository=$CURRENT/.m2repo
