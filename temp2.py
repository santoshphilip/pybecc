
import xml.etree.ElementTree as ET
from pybecc.pybecc import *


def getchildtags(xpath, results):
    childtags = list(set([item.tag for item in root.findall(xpath)]))
    print(xpath)
    results.append(childtags)
    for childtag in childtags:
        nxpath = f"{xpath}{childtag}/"
        getchildtags(nxpath, results)



fname1 = "./resources/010012-SchSml-CECStd.xml"
# fname1 = "/Users/santosh/Dropbox/temp/190715_T24_00-post_open.xml"
tree = ET.parse(fname1)
root = tree.getroot()

xpath = './'
res = list()
getchildtags(xpath, res)
# childs = list(set([item.tag for item in root.findall(xpath)]))

# xpath = f"{xpath}{child}/"
# childs = list(set([item.tag for item in root.findall(xpath)]))

def find_rec(node, element):
    def _find_rec(node, element, result):
        for el in node.getchildren():
            _find_rec(el, element, result)
        if node.tag == element:
            result.append(node)
    res = list()
    _find_rec(node, element, res)
    return res