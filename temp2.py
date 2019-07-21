import xml.etree.ElementTree as ET
from collections import OrderedDict
# from pybecc import *

def morechild(child):
    try:
        txt = child.text.strip()
    except AttributeError as e:
        txt = ""
    print(f"{child.tag:<20} = {txt}")
    for grandchild in child:
        morechild(grandchild)

def morechild1(child, ii=0, indent=0):
    tab = "  " * indent
    try:
        txt = child.text.strip()
    except AttributeError as e:
        txt = ""
    print(f"{tab}{indent}.{ii}. {child.tag:<20} = {txt}")
    indent += 1
    for i, grandchild in enumerate(child):
        morechild1(grandchild, i, indent=indent)

def morechild2(child, ii=0, indent=0, uptoindent=None):
    if uptoindent:
        if indent > uptoindent:
            return
    tab = "  " * indent
    try:
        txt = child.text.strip()
    except AttributeError as e:
        txt = ""
    print(f"{tab}{indent}.{ii}. {child.tag:<20} = {txt}")
    indent += 1
    for i, grandchild in enumerate(child):
        morechild2(grandchild, i, indent=indent, uptoindent=uptoindent)


fname1 = "./resources/010012-SchSml-CECStd.xml"
# fname1 = "/Users/santosh/Dropbox/temp/190715_T24_00-post_open.xml"
# fname1 = "/Users/santoshphilip/Dropbox/temp/190715_T24_00-post_open.xml"
tree = ET.parse(fname1)
root = tree.getroot()


# morechild(root)
# morechild1(root)
morechild2(root, uptoindent=2)