"""editing xml files"""

import xml.etree.ElementTree as ET
from collections import OrderedDict

# from pybecc import *


def removedups(childs):
    """remove dups and retain order"""
    return list(OrderedDict.fromkeys(childs))


def getcontent(element):
    try:
        txt = element.text.strip()
    except AttributeError as e:
        txt = ""
    return txt


def getcontent1(xpath):
    childtags = removedups([item.tag for item in root.findall(xpath)])
    print(xpath)
    results.append(childtags)
    for childtag in childtags:
        nxpath = f"{xpath}{childtag}/"
        getchildtags(nxpath, results)


fname1 = "./resources/010012-SchSml-CECStd.xml"
# fname1 = "/Users/santosh/Dropbox/temp/190715_T24_00-post_open.xml"
# fname1 = "/Users/santoshphilip/Dropbox/temp/190715_T24_00-post_open.xml"
tree = ET.parse(fname1)
root = tree.getroot()

# print(getcontent(root))
xpath = "./Proj/"
found = root.findall(xpath)
childtags = removedups([item.tag for item in root.findall(xpath)])
# print(childtags)

xpath = "./Proj/Name"
found = root.findall(xpath)
# print(found[0])
print(getcontent(found[0]))
found[0].text = "Karamba"

xpath = "./Proj/Name"
found = root.findall(xpath)
# print(found[0])
print(getcontent(found[0]))

# tree.write(open("a.xml", 'w'), encoding='unicode')

# find xpath, **kwargs
xpath = "./Proj/Mat"
found = root.findall(xpath)
mats = [f for f in found if getcontent(f) == "Concrete - 140 lb/ft3 - 6 in."]
mats = [getcontent(f) for f in found]
childtags = removedups([item.tag for item in root.findall(xpath)])
print(childtags)

mats = [
    f for f in found if getcontent(f.find("./Name")) == "Concrete - 140 lb/ft3 - 6 in."
]

print(mats)

# find Mat, CodeCat="Insulation Board"

xpath = "./Proj/Mat/CodeCat"
found = root.findall(xpath)
mats = [
    f for f in found if getcontent(f.find("./Name")) == "Concrete - 140 lb/ft3 - 6 in."
]


# found = root.findall(xpath)
# subtag = "Name"
# childpath = f"{xpath}/{subtag}"
# print(childpath)
# for f in found:
#     childpath = f"./{childtag}"
#     f.find()
#
