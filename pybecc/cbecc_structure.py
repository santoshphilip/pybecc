
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pybecc import *



def removedups(childs):
    """remove dups and retain order"""
    return list(OrderedDict.fromkeys(childs))
    
def getchildtags(xpath, results):
    childtags = removedups([item.tag for item in root.findall(xpath)])
    print(xpath)
    results.append(childtags)
    for childtag in childtags:
        nxpath = f"{xpath}{childtag}/"
        getchildtags(nxpath, results)

def getchildtags1(xpath, results, indent=0):
    childtags = removedups([item.tag for item in root.findall(xpath)])
    tab = "  " * indent
    # print(indent, xpath)
    indent += 1
    results.append(childtags)
    for i, childtag in enumerate(childtags):
        print(f"{tab}{indent}.{i:003}. {childtag}")
        nxpath = f"{xpath}{childtag}/"
        getchildtags1(nxpath, results, indent=indent)
        
        

def getchildtags2(xpath, results, indent=0, uptoindent=None):
    if uptoindent:
        if indent > uptoindent:
            return
    childtags = removedups([item.tag for item in root.findall(xpath)])
    tab = "  " * indent
    # print(indent, xpath)
    indent += 1
    results.append(childtags)
    for i, childtag in enumerate(childtags):
        print(f"{tab}{indent - 1}.{i:003}. {childtag}")
        nxpath = f"{xpath}{childtag}/"
        getchildtags2(nxpath, results, indent=indent, uptoindent=uptoindent)

def getchildtags3(xpath, results, 
                  indent=0, uptoindent=None, 
                  afterindent=None, fromtag=None):
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
                print(f"{tab}{indent - 1}.{i:003}. {childtag}")
        else:
            print(f"{tab}{indent - 1}.{i:003}. {childtag}")
        nxpath = f"{xpath}{childtag}/"
        getchildtags3(nxpath, results, 
                      indent=indent, uptoindent=uptoindent,     
                      afterindent=afterindent, fromtag=fromtag)
        if breakhere:
            break



fname1 = "./resources/010012-SchSml-CECStd.xml"
# fname1 = "/Users/santosh/Dropbox/temp/190715_T24_00-post_open.xml"
fname1 = "/Users/santoshphilip/Dropbox/temp/190715_T24_00-post_open.xml"
tree = ET.parse(fname1)
root = tree.getroot()

xpath = './'
res = list()
# getchildtags(xpath, res)
# getchildtags1(xpath, res)
# getchildtags2(xpath, res, uptoindent=1)
# getchildtags3(xpath, res, uptoindent=None, afterindent=3)
getchildtags3(xpath, res, fromtag='Bldg', uptoindent=None)
