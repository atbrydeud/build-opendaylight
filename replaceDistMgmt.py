#!/usr/bin/env python

import xml.etree.ElementTree as ET
import os
import sys
import fnmatch
import re

XML_NAMESPACE = 'http://maven.apache.org/POM/4.0.0'
ET.register_namespace('', XML_NAMESPACE)

def main() :
    if len(sys.argv) < 2:
        printUsage()
    else:
        if not os.path.isdir(sys.argv[1]):
            printUsage()
        else:
            files = findPoms(sys.argv[1])
            for pomFile in files:
                process(pomFile)

def process(pomFile):
    print "Processing : " + pomFile
    try:
        tree = ET.parse(pomFile)
        root = tree.getroot()
    except ET.ParseError as parseError:
        # Remove first line of file before parsing
        # This is because some pom.xml have #set( $dollar = '$' )
        # as their first line
        with open (pomFile, "r") as rPFile:
            pomString = rPFile.read()
            nPomString = '\n'.join(pomString.split('\n')[1:])
            # write string to a temporary file to get the tree
            newPomFile = open ('tempPomFile.xml', 'w+')
            newPomFile.write(nPomString)
            newPomFile.close()
            newPomFile = open ('tempPomFile.xml', 'r')
            tree = ET.parse(newPomFile)
            root = tree.getroot()
            os.remove('tempPomFile.xml')

    replaceDistMgmt(pomFile, root)
    tree.write(pomFile)

def replaceDistMgmt(pomFile, root):
    dist_mgmt = root.find("./"+getName('distributionManagement'))
    if dist_mgmt is not None:
        # print "tag : " + dist_mgmt.tag
        # print "text: " + dist_mgmt.text
        for child in list(dist_mgmt):
            # print child
            dist_mgmt.remove(child)
        rep_tag = ET.SubElement(dist_mgmt, getName('repository'))
        id_tag = ET.SubElement(rep_tag, getName('id'))
        id_tag.text = 'repo.inocybe.com'
        name_tag = ET.SubElement(rep_tag, getName('name'))
        name_tag.text = 'repo.inocybe.com-releases'
        url_tag = ET.SubElement(rep_tag, getName('url'))
        url_tag.text = 'http://repo.inocybe.com/repository/libs-release-local'
        print "Changed distributionManagement for :"+ root.find(getName('artifactId')).text
        print "at " + pomFile
    else:
        #print "No distributionManagement to change for pom.xml of "+ root.find(getName('artifactId')).text

def getName(tag):
    return '{'+XML_NAMESPACE+'}'+tag

def findPoms(rootdir):
    matches = []
    for root, dirnames, filenames in os.walk(rootdir):
        for filename in fnmatch.filter(filenames, 'pom.xml'):
            matches.append(os.path.join(root, filename))
    return matches

def printUsage():
    print "Usage:"
    print "./release.py [directory]"
    print "directory is the root directory to search\n"

if __name__ == "__main__":
    main()
