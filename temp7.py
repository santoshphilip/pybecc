"""explore insert into a tree"""

from io import StringIO

import xml.etree.ElementTree as ET
from pybecc import cbecc_edit


fname = "./resources/010012-SchSml-CECStd.xml"
fname = "./resources/tree1.xml"

tree = ET.parse(fname)
print(f"read {fname}")
root = tree.getroot()
tree.write("a.txt")
spaces = cbecc_edit.findelements(root, "./Proj/Bldg/Story/Spc")
space = spaces[0]
ufloors = cbecc_edit.findelements(space, "./UndgrFlr")
ufloor = ufloors[0]
ufloorstr = str(ufloor)
# print(ET.tostring(ufloor, encoding='unicode'))
lastspace = spaces[-1]
lastspace.append(ufloor)

ufloors = cbecc_edit.findelements(lastspace, "./UndgrFlr")
ufloor = ufloors[-1]
cbecc_edit.setfieldvalue(ufloor, "Name", "Olive Oil")
tree.write("b.txt")


#
#
#
#
#
# print( ET.tostring(root, encoding='unicode'))
#
# s = StringIO('<year>2011</year>')
# tree1 = ET.parse(s)
# root1 = tree1.getroot()
# root.append(root1)
#
#
# print( ET.tostring(root, encoding='unicode'))
#
#

print(ET.tostring(country, encoding="unicode"))
