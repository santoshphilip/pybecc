import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict

# from pybecc import *


def removedups(childs):
    """remove dups and retain order"""
    return list(OrderedDict.fromkeys(childs))


def structure(
    root,
    xpath=None,
    results=None,
    indent=0,
    uptoindent=None,
    afterindent=None,
    fromtag=None,
    thefile=None,
):
    if xpath is None:
        xpath = "./"
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
        structure(
            root,
            nxpath,
            results,
            indent=indent,
            uptoindent=uptoindent,
            afterindent=afterindent,
            fromtag=fromtag,
            thefile=thefile,
        )
        if breakhere:
            break


def structurepath(
    root,
    xpath=None,
    results=None,
    indent=0,
    uptoindent=None,
    afterindent=None,
    fromtag=None,
    thefile=None,
    pre=None,
):
    if xpath is None:
        xpath = "./"
    if results is None:
        results = list()
    if thefile is None:
        thefile = sys.stdout
    if fromtag:
        afterindent = 500
    if uptoindent:
        if indent > uptoindent:
            return
    if pre is None:
        pre = "."
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
        printthis = f"{pre}/{childtag}"
        if afterindent:
            if indent - 1 > afterindent:
                print(f"{tab}{indent - 1}.{i:003}. {printthis}", file=thefile)
        else:
            print(f"{tab}{indent - 1}.{i:003}. {printthis}", file=thefile)
        nxpath = f"{xpath}{childtag}/"
        structurepath(
            root,
            nxpath,
            results,
            indent=indent,
            uptoindent=uptoindent,
            afterindent=afterindent,
            fromtag=fromtag,
            thefile=thefile,
            pre=printthis,
        )
        if breakhere:
            break
