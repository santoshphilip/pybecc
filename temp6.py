"""find the systems that tthe ind. cond. zones are attached to"""

"""edit a file for real - using find and replace"""

from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from pybecc import cbecc_edit


fname = "/Users/santosh/Dropbox/temp/scratch/workingfile.cibd16x"
outfile1 = "/Users/santosh/Dropbox/temp/scratch/workingfile_out1.cibd16x"
outfile2 = "/Users/santosh/Dropbox/temp/scratch/workingfile_out2.cibd16x"
outfile3 = "/Users/santosh/Dropbox/temp/scratch/workingfile_out3.cibd16x"
outfile4 = "/Users/santosh/Dropbox/temp/scratch/workingfile_out4.cibd16x"
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

xpath = "./Proj/Bldg/ThrmlZn"
thermalzones = cbecc_edit.findelements(root, xpath) 


indzones = []
for thermalzone in thermalzones:
    fullzonename = cbecc_edit.getfieldvalue(thermalzone, "Name")
    zonename = fullzonename.split("-")[-1]
    if zonename.startswith("Ind"):
        indzones.append(thermalzone)

syszones = []
for zone in indzones:
    fullzonename = cbecc_edit.getfieldvalue(zone, "Name")
    sysname = cbecc_edit.getfieldvalue(zone, "PriAirCondgSysRef")
    # print(fullzonename, sysname)
    # print(f"{fullzonename:<35} {sysname:<15}")
    syszones.append((sysname, fullzonename))

syszones.sort()
for n1, n2 in syszones:
    print(f"{n2:<35} {n1:<15}")


# tree.write(outfile2)
# print(f"wrote: {outfile2}")


