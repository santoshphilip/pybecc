"""print out the structure of the cbecc file
Gives the full pathname - usefil for getting elements or objects

does not find nested structure if the it is below the first layer
and is not within the first element
This needs to be rethought"""


# copied from structure1.py

import xml.etree.ElementTree as ET
import pybecc.pybecc as pybecc


def printstuff1(newtags, prevelement, ii, level, goto, pre):
    if level > goto + 2:
        return None, None
    basetag = newtags[ii]
    tab = "  "
    baseelement = prevelement.find(basetag)
    lowertags = pybecc.get_tags_childrens_tags(prevelement, basetag)
    tags = lowertags
    tagsinbase = [pybecc.get_tags_childrens_tags(baseelement, tag) for tag in tags]
    inbase = [
        (i, tag, pybecc.get_tags_childrens_tags(baseelement, tag))
        for (i, tag) in enumerate(tags)
    ]
    printthis = f"{pre}/{basetag}"
    length = len(printthis.split("/")) - 1
    print(tab * level, f"{level}.{ii:03d}", printthis, length, end="  --out\n")
    fullpath = pre
    for i, tag, childtags in inbase:
        printhis = f"{pre}/{basetag}/{tag}"
        length = len(printthis.split("/")) - 1
        print(
            tab * (level + 1), f"{level+1}.{i:03d}", printthis, length, end="  --in\n"
        )
        fullpath = printthis
        for k, childtag in enumerate(childtags):
            printstuff(childtags, baseelement.find(tag), k, level + 2, goto, fullpath)
    pre = fullpath
    return lowertags, baseelement


def printstuff(newtags, prevelement, ii, level, goto, pre):
    if level > goto + 2:
        return None, None
    basetag = newtags[ii]
    tab = "  "
    baseelement = prevelement.find(basetag)
    lowertags = pybecc.get_tags_childrens_tags(prevelement, basetag)
    tags = lowertags
    tagsinbase = [pybecc.get_tags_childrens_tags(baseelement, tag) for tag in tags]
    inbase = [
        (i, tag, pybecc.get_tags_childrens_tags(baseelement, tag))
        for (i, tag) in enumerate(tags)
    ]
    printthis = f"{pre}/{basetag}"
    length = len(printthis.split("/")) - 1
    print(tab * level, f"{level}.{ii:03d}", printthis, length)
    for i, tag, childtags in inbase:
        printthis = f"{pre}/{basetag}/{tag}"
        length = len(printthis.split("/")) - 1
        print(tab * (level + 1), f"{level+1}.{i:03d}", printthis, length)
        for k, childtag in enumerate(childtags):
            printstuff(
                childtags,
                baseelement.find(tag),
                k,
                level + 2,
                goto,
                f"{pre}/{basetag}/{tag}",
            )
    return lowertags, baseelement


fname1 = "/Users/santosh/Documents/coolshadow/github/pybecc/resources/010012-SchSml-CECStd.xml"
# fname1 = "/Users/santosh/Dropbox/temp/190715_T24_00-post_open.xml"
fname1 = "/Users/santosh/Documents/coolshadow/HOK_O_Street/simulation/O_street_working/T_24_models/cbecc_models/Abe/190729_T24_05_mech.cibd16x"
fname1 = "/Users/santoshphilip/Dropbox/coolshadow_dropbox/doe2eppystuff/eplusfiles/190729_T24_05_mech_process12_upprocess4.cibd16x"
fname1 = "./resources/tree2.xml"
tree = ET.parse(fname1)
root = tree.getroot()
l1_tags = pybecc.getchildtags(root)

tab = "  "
level = 0
# prevelement = root
# maintag = l1_tags[1]
# # # --
# baseelement = prevelement.find(basetag)

baseelement = root
# baseelement = root.find(maintag)
basetag = baseelement.tag
# lowertags = pybecc.get_tags_childrens_tags(prevelement, basetag)
lowertags = pybecc.getchildtags(baseelement)
tags = lowertags
# tagsinbase = [pybecc.get_tags_childrens_tags(baseelement, tag) for tag in tags]
inbase = [
    (i, tag, pybecc.get_tags_childrens_tags(baseelement, tag))
    for (i, tag) in enumerate(tags)
]
print(tab * level, f"{level}.{0}", basetag)
for i, tag, childtags in inbase:
    pre = f"{basetag}/{tag}"
    pre = f"./{tag}"
    # print(pre, "\n", end="")
    printthis = pre
    length = len(printthis.split("/")) - 1
    print(tab * (level + 1), f"{level+1}.{i}", printthis, length)
    for k, childtag in enumerate(childtags):
        printstuff(childtags, baseelement.find(tag), k, level + 2, 10, pre)
