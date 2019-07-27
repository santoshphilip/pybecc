"""edit a file for real - using find and replace"""

from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from pybecc import cbecc_edit


fname = "/Users/santosh/Dropbox/temp/scratch/workingfile.cibd16x"
outfile1 = "/Users/santosh/Dropbox/temp/scratch/workingfile_out1.cibd16x"
outfile2 = "/Users/santosh/Dropbox/temp/scratch/workingfile_out2.cibd16x"


fname1 = "./resources/010012-SchSml-CECStd.xml"
# fname1 = "/Users/santosh/Dropbox/temp/190715_T24_00-post_open.xml"
# fname1 = "/Users/santoshphilip/Dropbox/temp/190715_T24_00-post_open.xml"
tree = ET.parse(fname)
root = tree.getroot()

ntree = ET.ElementTree(root)
ntree.write(open(outfile1, 'w'), encoding='unicode')


xpath = "./Proj/Bldg/ThrmlZn"
thermalzones = cbecc_edit.findelements(root, xpath) 

lines = ['428',
 '429',
 '430',
 '431',
 '432',
 '433',
 '434',
 '435',
 '436',
 '437',
 '438',
 '439',
 '440',
 '441',
 '442',
 '443',
 '444',
 '445',
 '446',
 '447',
 '448',
 '449',
 '450',
 '451',
 '452',
 '453',
 '454',
 '455',
 '456',
 '457',
 '458',
 '459',
 '460',
 '461',
 '462',
 '463',
 '464',
 '465',
 '466',
 '467',
 '468',
 '469',
 '470',
 '471',
 '472',
 '473',
 '474',
 '475',
 '476',
 '477',
 '478',
 '479',
 '480',
 '481',
 '482',
 '483',
 '484',
 '485',
 '486',
 '488',
 '489',
 '490']
 
ourzones = []
for thermalzone in thermalzones:
    # print(cbecc_edit.getfieldvalue(thermalzone, "Name"))
    for line in lines:
        if cbecc_edit.getfieldvalue(thermalzone, "Name").startswith(line):
            ourzones.append(thermalzone)

cbecc_edit.replacefield(ourzones, "PriAirCondgSysRef", after="- none -")
cbecc_edit.replacefield(ourzones, "VentSysRef", after="- none -")
                

tree = ET.ElementTree(root)
tree.write(outfile2)
# mydata = ET.tostring(root)
# myfile = open(outfile2, "w")
# myfile.write(mydata)
# ntree = ET.ElementTree(root)
# ntree.write(open(outfile2, 'w'), encoding='unicode')

# tree = ElementTree.ElementTree()
# tree._setroot(root)
# ntree.write(open(outfile2, 'w'), encoding='unicode')
# # tree.write("sample.xml")
# # # tree.write(open("a.xml", 'w'), encoding='unicode')
