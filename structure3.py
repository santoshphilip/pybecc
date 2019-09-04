"""use the cbecc_sturcture library"""

import xml.etree.ElementTree as ET
from pybecc import cbecc_structure

fname1 = "./resources/010012-SchSml-CECStd.xml"
fname1 = "./resources/tree2.xml"
fname1 = "/Users/santoshphilip/Dropbox/coolshadow_dropbox/doe2eppystuff/eplusfiles/190729_T24_05_mech_process12_upprocess4.cibd16x"
fname1 = "/Users/santoshphilip/Dropbox/coolshadow_dropbox/doe2eppystuff/eplusfiles/190729_T24_05_mech_process12_upprocess4.cibd16x"
fname1 = "/Users/santosh/Documents/coolshadow/HOK_O_Street/simulation/O_street_working/T_24_models/cbecc_models/ibone/OST_T24/190902_T24_09_e5_nomech.cibd16x"
# fname1 = "/Users/santosh/Dropbox/temp/190715_T24_00-post_open.xml"
# fname1 = "/Users/santoshphilip/Dropbox/temp/190715_T24_00-post_open.xml"
# fname1 = "/Users/santosh/Dropbox/temp/scratch/workingfile.cibd16x"
tree = ET.parse(fname1)
root = tree.getroot()

xpath = "./"
res = list()
# getchildtags(xpath, res)
# getchildtags1(xpath, res)
# getchildtags2(xpath, res, uptoindent=1)
# res = getchildtags3(xpath, res, uptoindent=None, afterindent=3)
# res = getchildtags3(xpath, res, fromtag='Proj', uptoindent=None)
# res = getchildtags3(root, xpath, res, fromtag=None, uptoindent=None, thefile=None)


res = cbecc_structure.structure(root)
# res = cbecc_structure.structurepath(root)
