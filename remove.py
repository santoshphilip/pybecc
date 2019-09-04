"""remove an element from the tree"""
# Get this into the cbecc_edit


import xml.etree.ElementTree as ET


fname = "/Users/santosh/Documents/coolshadow/HOK_O_Street/simulation/O_street_working/T_24_models/cbecc_models/ibone/OST_T24/190902_T24_09_e5_nomech.cibd16x"
outfile = "a.xml"
finalfile = "final.xml"

tree = ET.parse(fname)
tree.write(outfile)
root = tree.getroot()

xpath = "./Proj/Bldg/Story/Spc"
spaces = root.findall(xpath)
for space in spaces:
    lpath = "./IntLtgSys"
    lights = space.findall(lpath)

    for light in lights:
        space.remove(light)

tree.write(finalfile)

