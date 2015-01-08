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
    replaceRepositories(pomFile, root)
    replacePluginRepositories(pomFile, root)
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
    # else:
    #     print "No distributionManagement to change for pom.xml of "+ root.find(getName('artifactId')).text

def replaceRepositories(pomFile, root):
    repositories = root.find("./"+getName('repositories'))
    if repositories is not None:
        for child in list(repositories):
            repositories.remove(child)
        # release
        rel_rep_tag = ET.SubElement(repositories, getName('repository'))
        rel_rel_tag = ET.SubElement(rel_rep_tag, getName('releases'))
        rel_r_enabled_tag = ET.SubElement(rel_rel_tag, getName('enabled'))
        rel_r_enabled_tag.text = 'true'
        rel_snap_tag = ET.SubElement(rel_rep_tag, getName('snapshots'))
        rel_s_enabled_tag = ET.SubElement(rel_snap_tag, getName('enabled'))
        rel_s_enabled_tag.text = 'false'
        rel_id_tag = ET.SubElement(rel_rep_tag, getName('id'))
        rel_id_tag.text = 'repo.inocybe.com'
        rel_name_tag = ET.SubElement(rel_rep_tag, getName('name'))
        rel_name_tag.text = 'repo.inocybe.com-releases'
        rel_url_tag = ET.SubElement(rel_rep_tag, getName('url'))
        rel_url_tag.text = 'http://repo.inocybe.com/repository/libs-release-local'

        # snapshot
        snp_rep_tag = ET.SubElement(repositories, getName('repository'))
        snp_rel_tag = ET.SubElement(snp_rep_tag, getName('releases'))
        snp_r_enabled_tag = ET.SubElement(snp_rel_tag, getName('enabled'))
        snp_r_enabled_tag.text = 'false'
        snp_snap_tag = ET.SubElement(snp_rep_tag, getName('snapshots'))
        snp_s_enabled_tag = ET.SubElement(snp_snap_tag, getName('enabled'))
        snp_s_enabled_tag.text = 'true'
        snp_id_tag = ET.SubElement(snp_rep_tag, getName('id'))
        snp_id_tag.text = 'repo.inocybe.com'
        snp_name_tag = ET.SubElement(snp_rep_tag, getName('name'))
        snp_name_tag.text = 'repo.inocybe.com-snapshots'
        snp_url_tag = ET.SubElement(rel_rep_tag, getName('url'))
        snp_url_tag.text = 'http://repo.inocybe.com/repository/libs-snapshot-local'

        print "Changed repositories for :"+ root.find(getName('artifactId')).text
        print "at " + pomFile
    # else:
    #     print "No repositories to change for pom.xml of "+ root.find(getName('artifactId')).text

def replacePluginRepositories(pomFile, root):
    pluginRepositories = root.find("./"+getName('pluginRepositories'))
    if pluginRepositories is not None:
        for child in list(pluginRepositories):
            pluginRepositories.remove(child)
        # release
        rel_rep_tag = ET.SubElement(pluginRepositories, getName('pluginRepository'))
        rel_rel_tag = ET.SubElement(rel_rep_tag, getName('releases'))
        rel_r_enabled_tag = ET.SubElement(rel_rel_tag, getName('enabled'))
        rel_r_enabled_tag.text = 'true'
        rel_snap_tag = ET.SubElement(rel_rep_tag, getName('snapshots'))
        rel_s_enabled_tag = ET.SubElement(rel_snap_tag, getName('enabled'))
        rel_s_enabled_tag.text = 'false'
        rel_id_tag = ET.SubElement(rel_rep_tag, getName('id'))
        rel_id_tag.text = 'repo.inocybe.com'
        rel_name_tag = ET.SubElement(rel_rep_tag, getName('name'))
        rel_name_tag.text = 'repo.inocybe.com-releases'
        rel_url_tag = ET.SubElement(rel_rep_tag, getName('url'))
        rel_url_tag.text = 'http://repo.inocybe.com/repository/libs-release-local'

        # snapshot
        snp_rep_tag = ET.SubElement(pluginRepositories, getName('pluginRepository'))
        snp_rel_tag = ET.SubElement(snp_rep_tag, getName('releases'))
        snp_r_enabled_tag = ET.SubElement(snp_rel_tag, getName('enabled'))
        snp_r_enabled_tag.text = 'false'
        snp_snap_tag = ET.SubElement(snp_rep_tag, getName('snapshots'))
        snp_s_enabled_tag = ET.SubElement(snp_snap_tag, getName('enabled'))
        snp_s_enabled_tag.text = 'true'
        snp_id_tag = ET.SubElement(snp_rep_tag, getName('id'))
        snp_id_tag.text = 'repo.inocybe.com'
        snp_name_tag = ET.SubElement(snp_rep_tag, getName('name'))
        snp_name_tag.text = 'repo.inocybe.com-snapshots'
        snp_url_tag = ET.SubElement(rel_rep_tag, getName('url'))
        snp_url_tag.text = 'http://repo.inocybe.com/repository/libs-snapshot-local'

        print "Changed pluginRepositories for :"+ root.find(getName('artifactId')).text
        print "at " + pomFile
    # else:
    #     print "No repositories to change for pom.xml of "+ root.find(getName('artifactId')).text

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
