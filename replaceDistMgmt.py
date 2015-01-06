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

    ## Testing ##
    ## To be removed ##
    # tree = ET.parse('test/test2/test3/pom.xml')
    # files = findPoms('test')

    # replaceDeps(tree)
    # replaceDistMgmt(tree)
    # replaceVersion(tree)
    # tree.write('newpom.xml')

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

    replaceDistMgmt(root)
    tree.write(pomFile)

def replaceDistMgmt(root):
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
    else:
        print "No distributionManagement to change for pom.xml of "+ root.find(getName('artifactId')).text

def printUsage():
    print "Usage:"
    print "./release.py [directory]"
    print "directory is the root directory to search\n"
