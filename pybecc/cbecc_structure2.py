import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pybecc import *



def removedups(childs):
    """remove dups and retain order"""
    return list(OrderedDict.fromkeys(childs))
    

def getchildtags2(root, xpath, results=None, indent=0, uptoindent=None, thefile=None):
    if results is None:
        results = list()
    if thefile is None:
        thefile = sys.stdout
    if uptoindent:
        if indent > uptoindent:
            return
    childtags = removedups([item.tag for item in root.findall(xpath)])
    tab = "  " * indent
    # print(indent, xpath)
    indent += 1
    results.append(childtags)
    for i, childtag in enumerate(childtags):
        print(f"{tab}{indent - 1}.{i:003}. {childtag}", file=thefile)
        nxpath = f"{xpath}{childtag}/"
        getchildtags2(root, nxpath, results, indent=indent, uptoindent=uptoindent)

def structure(root, xpath=None, results=None, 
                  indent=0, uptoindent=None, 
                  afterindent=None, fromtag=None, thefile=None):
    if xpath is None:
        xpath = './'
    if results is None:
        results = list()
    if thefile is None:
        thefile = sys.stdout
    if fromtag:
        afterindent = 500
    if uptoindent:
        if indent > uptoindent:
            return
    childtags = removedups([item.tag for item in root.findall(xpath)])
    tab = "  " * indent
    # print(indent, xpath)
    indent += 1
    breakhere = False
    results.append(childtags)
    for i, childtag in enumerate(childtags):
        if childtag == fromtag:
            afterindent = indent - 2
            fromtag = None
            breakhere = True
        if afterindent:
            if indent - 1 > afterindent:
                print(f"{tab}{indent - 1}.{i:003}. {childtag}", file=thefile)
        else:
            print(f"{tab}{indent - 1}.{i:003}. {childtag}", file=thefile)
        nxpath = f"{xpath}{childtag}/"
        structure(root, nxpath, results, 
                      indent=indent, uptoindent=uptoindent,     
                      afterindent=afterindent, fromtag=fromtag)
        if breakhere:
            break



fname1 = "./resources/010012-SchSml-CECStd.xml"
fname1 = "./resources/tree2.xml"
# fname1 = "/Users/santosh/Dropbox/temp/190715_T24_00-post_open.xml"
# fname1 = "/Users/santoshphilip/Dropbox/temp/190715_T24_00-post_open.xml"
# fname1 = "/Users/santosh/Dropbox/temp/scratch/workingfile.cibd16x"
tree = ET.parse(fname1)
root = tree.getroot()

xpath = './'
res = list()
# getchildtags(xpath, res)
# getchildtags1(xpath, res)
# getchildtags2(xpath, res, uptoindent=1)
# res = getchildtags3(xpath, res, uptoindent=None, afterindent=3)
# res = getchildtags3(xpath, res, fromtag='Proj', uptoindent=None)
# res = getchildtags3(root, xpath, res, fromtag=None, uptoindent=None, thefile=None)
res = structure(root)
# print(res)
