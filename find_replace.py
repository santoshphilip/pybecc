"""edit a file for real - using find and replace"""

from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from pybecc import cbecc_edit


fname = "/Users/santosh/Dropbox/temp/scratch/workingfile.cibd16x"
fname = "/Users/santosh/Documents/coolshadow/HOK_O_Street/simulation/O_street_working/T_24_models/cbecc_models/Abe/190729_T24_05_mech.cibd16x"
outfile1 = "/Users/santosh/Dropbox/temp/scratch/workingfile_out1.cibd16x"
outfile2 = "/Users/santosh/Dropbox/temp/scratch/workingfile_out2.cibd16x"
outfile3 = "/Users/santosh/Dropbox/temp/scratch/workingfile_out3.cibd16x"
outfile4 = "/Users/santosh/Dropbox/temp/scratch/workingfile_out4.cibd16x"
finalfile = "/Users/santosh/Documents/coolshadow/HOK_O_Street/simulation/O_street_working/T_24_models/cbecc_models/Abe/190729_T24_05_mech_recept085.cibd16x"
# -
# fname = "/Users/santoshphilip/Dropbox/temp/scratch/workingfile.cibd16x"
# outfile1 = "/Users/santoshphilip/Dropbox/temp/scratch/workingfile_out1.cibd16x"
# outfile2 = "/Users/santoshphilip/Dropbox/temp/scratch/workingfile_out2.cibd16x"


# fname1 = "./resources/010012-SchSml-CECStd.xml"
# fname1 = "/Users/santosh/Dropbox/temp/190715_T24_00-post_open.xml"
# fname1 = "/Users/santoshphilip/Dropbox/temp/190715_T24_00-post_open.xml"
tree = ET.parse(fname)
print(f"read {fname}")
root = tree.getroot()

ntree = ET.ElementTree(root)
ntree.write(open(outfile1, "w"), encoding="unicode")
print(f"wrote: {outfile1}")


xpath = "./Proj/Bldg/ThrmlZn"
xpath = "./Proj/Bldg/Story/Spc"
spaces = cbecc_edit.findelements(root, xpath)


# cbecc_edit.replacefield(thermalzones, "PriAirCondgSysRef", after="- none -")
# cbecc_edit.replacefield(spaces, "RecptPwrDens", before="3.5", after="0.85")
cbecc_edit.replacefield(spaces, "ProcElecPwrDens", after="1.21")


tree.write(outfile2)
print(f"wrote: {outfile2}")

tree.write(finalfile)
print(f"wrote: {finalfile}")
