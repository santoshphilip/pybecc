"""print out the structure of the cbecc file"""
# copied from temp1.py
import xml.etree.ElementTree as ET
import pybecc.pybecc as pybecc


def printstuff(newtags, prevelement, ii, level, goto):
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
    print(tab * level, f"{level}.{ii:03d}", basetag)
    for i, tag, childtags in inbase:
        print(tab * (level + 1), f"{level+1}.{i:03d}", tag)
        for k, childtag in enumerate(childtags):
            printstuff(childtags, baseelement.find(tag), k, level + 2, goto)
    return lowertags, baseelement


fname1 = "/Users/santosh/Documents/coolshadow/github/pybecc/resources/010012-SchSml-CECStd.xml"
# fname1 = "/Users/santosh/Dropbox/temp/190715_T24_00-post_open.xml"
fname1 = "/Users/santosh/Documents/coolshadow/HOK_O_Street/simulation/O_street_working/T_24_models/cbecc_models/Abe/190729_T24_05_mech.cibd16x"
tree = ET.parse(fname1)
root = tree.getroot()
l1_tags = pybecc.getchildtags(root)

tab = "  "
level = 0
prevelement = root
basetag = l1_tags[1]
# --
baseelement = prevelement.find(basetag)
lowertags = pybecc.get_tags_childrens_tags(prevelement, basetag)
tags = lowertags
tagsinbase = [pybecc.get_tags_childrens_tags(baseelement, tag) for tag in tags]
inbase = [
    (i, tag, pybecc.get_tags_childrens_tags(baseelement, tag))
    for (i, tag) in enumerate(tags)
]
print(tab * level, f"{level}.{0}", basetag)
for i, tag, childtags in inbase:
    print(tab * (level + 1), f"{level+1}.{i}", tag)
    for k, childtag in enumerate(childtags):
        printstuff(childtags, baseelement.find(tag), k, level + 2, 1)
