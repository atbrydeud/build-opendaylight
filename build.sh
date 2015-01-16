#!/bin/bash

#
# Opendaylight build script
#

#
# Notes: clean repo on each run
#        e.g. rm -rf repo/;mkdir repo;cd repo; repo init -u https://github.com/inocybe/odl-manifest.git;repo sync
#
#        Requires settings.xml in $HOME/.m2 for interaction with repo.inocybe.com

set -e -x

CURRENT=`pwd`
TRAIN_LABEL=$GO_PIPELINE_LABEL
REPOSITORY_LIST="odlparent yangtools controller openflowplugin openflowjava dlux l2switch"
DATESTAMP="true"

rm -rf pom.xml .m2repo
rm -rf /var/go/.m2/repository/org/opendaylight

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

cat <<EOF > pom-l2-dlux.xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.opendaylight.aggregators</groupId>
  <artifactId>l2-dlux-aggregator</artifactId>
  <version>1.0.0</version>
  <packaging>pom</packaging>
  <modules>
        <module>openflowplugin</module>
  	<module>l2switch</module>
  	<module>dlux</module>
  </modules>
</project>
EOF

cd src
export SUFFIX=${TRAIN_LABEL}
if [ "${NIGHTLY}" == "true" ]; then
   export DAY=`date +%d`
   export DAYMOD=`expr \( $DAY - 9 \) \% 7`
   export SUFFIX=${SUFFIX}-${DAYMOD}
fi
if [ "${DATESTAMP}" == "true" ]; then
   export SUFFIX=${SUFFIX}-`date -u +v%Y%m%d%H%M`
fi
echo $SUFFIX

# for PROJECT in ${REPOSITORY_LIST}
# do
#   echo "Checking out stable/helium for ${PROJECT}"
#   cd ${PROJECT};
#   git checkout stable/helium;
#   cd -
# done

echo "complete cherry pick temp changes"

for PROJECT in ${REPOSITORY_LIST}
do
  cd ${PROJECT}
  git tag ${SUFFIX} -a -m "Autorelease tag for ${SUFFIX}"
  echo ${PROJECT} `git rev-parse --verify HEAD` ${SUFFIX} >> ../taglist
  cd -
done

for PROJECT in ${REPOSITORY_LIST}
do
  cd ${PROJECT}
  $CURRENT/replaceDistMgmt.py ${PROJECT}
  cd -
done

# find . -type f -name "pom.xml" -exec perl -i -pe "s/SNAPSHOT/$SUFFIX/g" {} +
# find . -type f -name "features.xml" -exec perl -i -pe "s/SNAPSHOT/$SUFFIX/g" {} +

# Save the patches that differ from the commits in taglist
mkdir -p patches
for PROJECT in ${REPOSITORY_LIST}
do
  cd ${PROJECT}
  git diff > ../patches/${PROJECT}.patch
  cd -
done

# Monkey patching for odl-features-service



cd ${CURRENT}
cd src/odlparent
mvn clean install -DskipTests deploy
# mvn clean install -Dmaven.repo.local=$CURRENT/.m2repo -Dorg.ops4j.pax.url.mvn.localRepository=$CURRENT/.m2repo -DskipTests

cd ${CURRENT}
cd src/yangtools
mvn clean install -DskipTests deploy -DaltDeploymentRepository=repo.inocybe.com::default::http://repo.inocybe.com/repository/libs-snapshot-local
# mvn clean install -DskipTests deploy -DaltDeploymentRepository=repo.inocybe.com::default::http://repo.inocybe.com/repository/libs-release-local
# mvn clean install -Dmaven.repo.local=$CURRENT/.m2repo -Dorg.ops4j.pax.url.mvn.localRepository=$CURRENT/.m2repo -DskipTests

cd ${CURRENT}
cd src/controller
mvn clean install -DskipTests deploy -DaltDeploymentRepository=repo.inocybe.com::default::http://repo.inocybe.com/repository/libs-snapshot-local
# mvn clean install -DskipTests deploy -DaltDeploymentRepository=repo.inocybe.com::default::http://repo.inocybe.com/repository/libs-release-local
# mvn clean install -Dmaven.repo.local=$CURRENT/.m2repo -Dorg.ops4j.pax.url.mvn.localRepository=$CURRENT/.m2repo -DskipTests

cd ${CURRENT}
cd src/openflowplugin
mvn clean install -DskipTests deploy -DaltDeploymentRepository=repo.inocybe.com::default::http://repo.inocybe.com/repository/libs-snapshot-local

cd ${CURRENT}
cd src/openflowjava
mvn clean install -DskipTests deploy -DaltDeploymentRepository=repo.inocybe.com::default::http://repo.inocybe.com/repository/libs-snapshot-local

cd ${CURRENT}
cd src/dlux
mvn clean install -DskipTests deploy -DaltDeploymentRepository=repo.inocybe.com::default::http://repo.inocybe.com/repository/libs-snapshot-local

cd ${CURRENT}
cd src/l2switch
mvn clean install -DskipTests deploy -DaltDeploymentRepository=repo.inocybe.com::default::http://repo.inocybe.com/repository/libs-snapshot-local

# cd ${CURRENT}
# mvn clean install -f pom-l2-dlux.xml -Dmaven.repo.local=$CURRENT/.m2repo -Dorg.ops4j.pax.url.mvn.localRepository=$CURRENT/.m2repo -DskipTests


# cd ${CURRENT}
# mvn clean install -f pom.xml -Dmaven.repo.local=$CURRENT/.m2repo -Dorg.ops4j.pax.url.mvn.localRepository=$CURRENT/.m2repo -DskipTests
