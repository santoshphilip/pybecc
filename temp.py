
import xml.etree.ElementTree as ET
from pybecc.pybecc import *


fname1 = "./resources/010012-SchSml-CECStd.xml"
# fname1 = "/Users/santosh/Dropbox/temp/190715_T24_00-post_open.xml"
tree = ET.parse(fname1)
root = tree.getroot()
l1_tags = getchildtags(root)
l1_childtags = [(tag, get_tags_childrens_tags(root, tag)) for tag in l1_tags]



prevelement = root
basetag = l1_tags[1]
# --
baseelement = prevelement.find(basetag)
lowertags = get_tags_childrens_tags(prevelement, basetag)
tags = lowertags
tagsinbase = [get_tags_childrens_tags(baseelement, tag) for tag in tags]
inbase = [(i, tag, get_tags_childrens_tags(baseelement, tag)) for (i, tag) in enumerate(tags)]



# newtags = lowertags
# prevelement = baseelement
# level = 1
# # --
# i = 25
# # i += 1
# basetag = newtags[i]
# # --
# tab = "    "
# baseelement = prevelement.find(basetag)
# lowertags = get_tags_childrens_tags(prevelement, basetag)
# tags = lowertags
# tagsinbase = [get_tags_childrens_tags(baseelement, tag) for tag in tags]
# inbase = [(i, tag, get_tags_childrens_tags(baseelement, tag)) for (i, tag) in enumerate(tags)]
# print(i, basetag)
# for i, tag, childtags in inbase:
#     print(i, tag)
#     if not childtags:
#         print(tab * level, "no more")
#     for childtag in childtags:
#         print(tab * level, childtag)

# ------------------

def printstuff(newtags, prevelement, ii, level, goto):
    if level > goto+1:
        return None, None
    basetag = newtags[ii]
    tab = "  "
    baseelement = prevelement.find(basetag)
    lowertags = get_tags_childrens_tags(prevelement, basetag)
    tags = lowertags
    tagsinbase = [get_tags_childrens_tags(baseelement, tag) for tag in tags]
    inbase = [(i, tag, get_tags_childrens_tags(baseelement, tag)) for (i, tag) in enumerate(tags)]
    print(tab * level, f"{level}.{ii}", basetag)
    for i, tag, childtags in inbase:
        print(tab * (level+1), f"{level+1}.{i}", tag)
        for k, childtag in enumerate(childtags):
            printstuff(childtags, baseelement.find(tag), k, level+2, goto)
    return lowertags, baseelement


newtags = lowertags
prevelement = baseelement
level = 1
# # --
# i = 25
# lowertags, baseelement = printstuff(newtags, prevelement, i, level)

for i in range(0, len(lowertags)): 
    lowertags, baseelement = printstuff(newtags, prevelement, i, level, 1)
    # print("=" * 23)

# printstuff
#
# In [100]: inproj
# Out[100]:
# [(0, 'Name', []),
#  (1, 'BldgEngyModelVersion', []),
#  (2, 'CreateDate', []),
#  (3, 'ModDate', []),
#  (4, 'RunDate', []),
#  (5, 'ZipCode', []),
#  (6, 'DDWeatherFile', []),
#  (7, 'AnnualWeatherFile', []),
#  (8, 'ExcptCondNoClgSys', []),
#  (9, 'ExcptCondRtdCap', []),
#  (10, 'ExcptCondNarrative', []),
#  (11, 'AutoHardSize', []),
#  (12, 'AutoEffInput', []),
#  (13, 'DefaultDayltgCtrls', []),
#  (14, 'CompOptNew', []),
#  (15, 'SoftwareVersion', []),
#  (16, 'ProjFileName', []),
#  (17, 'ResultsCurrentMessage', []),
#  (18,
#   'ConsAssm',
#   ['Name',
#    'CompatibleSurfType',
#    'SlabType',
#    'MatRef',
#    'CRRCInitialRefl',
#    'CRRCAgedRefl',
#    'CRRCInitialEmit',
#    'CRRCAgedEmit',
#    'CRRCProdID']),
#  (19, 'Mat', ['Name', 'CodeCat', 'CodeItem']),
#  (20,
#   'FenCons',
#   ['Name',
#    'FenType',
#    'FenProdType',
#    'AssmContext',
#    'CertificationMthd',
#    'SHGC',
#    'UFactor',
#    'VT']),
#  (21, 'SchDay', ['Name', 'Type', 'Hr']),
#  (22,
#   'SchWeek',
#   ['Name',
#    'Type',
#    'SchDayWDRef',
#    'SchDaySunRef',
#    'SchDaySatRef',
#    'SchDayAllRef',
#    'SchDayMonRef',
#    'SchDayTueRef',
#    'SchDayWedRef',
#    'SchDayThuRef',
#    'SchDayFriRef',
#    'SchDayHolRef',
#    'SchDayClgDDRef',
#    'SchDayHtgDDRef']),
#  (23, 'Sch', ['Name', 'Type', 'SchWeekRef', 'EndMonth', 'EndDay']),
#  (24, 'Lum', ['Name', 'Pwr']),
#  (25,
#   'Bldg',
#   ['Name', 'TotStoryCnt', 'AboveGrdStoryCnt', 'Story', 'AirSys', 'ThrmlZn']),
#  (26, 'FluidSys', ['Name', 'Type', 'FluidSeg', 'WtrHtr', 'Blr']),
#  (27,
#   'SpcFuncDefaults',
#   ['Name',
#    'SpcFunc',
#    'OccSchRef',
#    'IntLtgRegSchRef',
#    'RecptSchRef',
#    'ProcElecSchRef',
#    'CommRfrgEqpSchRef',
#    'ElevSchRef',
#    'ProcGasSchRef',
#    'HotWtrHtgSchRef',
#    'InfSchRef']),
#  (28,
#   'EUseSummary',
#   ['Name',
#    'Title1',
#    'Title2',
#    'Title3',
#    'Enduse1',
#    'Enduse2',
#    'Enduse3',
#    'Enduse4',
#    'Enduse5',
#    'Enduse6',
#    'Enduse7',
#    'Enduse8',
#    'Enduse9',
#    'Enduse10',
#    'Enduse11',
#    'Enduse12',
#    'Enduse13',
#    'ZoneUMLHsLoaded',
#    'ZoneUMLHs',
#    'SimSummary',
#    'PassFail',
#    'PctSavingsTDV',
#    'PctSavingsCmpTDV',
#    'PctSavTDVLbl',
#    'PctSavCmpTDVLbl',
#    'MarginkW'])]
#
# In [101]:
# # ====================
#
# newtags = lowertags
# prevelement = baseelement
# # --
# i = 4
# # i += 1
# basetag = newtags[i]
# # --
# tab = "    "
# baseelement = prevelement.find(basetag)
# lowertags = get_tags_childrens_tags(prevelement, basetag)
# tags = lowertags
# tagsinbase = [get_tags_childrens_tags(baseelement, tag) for tag in tags]
# inbase = [(i, tag, get_tags_childrens_tags(baseelement, tag)) for (i, tag) in enumerate(tags)]
# print(i, basetag)
# for i, tag, childtags in inbase:
#     print(i, tag)
#     if not childtags:
#         print(tab * level, "no more")
#     for childtag in childtags:
#         print(tab * level, childtag)
#
#
# 25 Bldg
#
# In [47]: inbase
# Out[47]:
# [(0, 'Name', []),
#  (1, 'TotStoryCnt', []),
#  (2, 'AboveGrdStoryCnt', []),
#  (3, 'Story', ['Name', 'Spc']),
#  (4,
#   'AirSys',
#   ['Name',
#    'Type',
#    'CtrlSysType',
#    'AvailSchRef',
#    'ReheatCtrlMthd',
#    'OptStart',
#    'ClRstSupHi',
#    'ClRstSupLow',
#    'AirSeg',
#    'OACtrl',
#    'TrmlUnit']),
#  (5,
#   'ThrmlZn',
#   ['Name',
#    'Type',
#    'PriAirCondgSysRef',
#    'ClgTstatSchRef',
#    'HtgTstatSchRef',
#    'HVACZnCnt',
#    'VentCtrlMthd'])]
# # ========================
# 26 FluidSys
#
# In [51]: inbase
# Out[51]:
# [(0, 'Name', []),
#  (1, 'Type', []),
#  (2, 'FluidSeg', ['Name', 'Type', 'Src']),
#  (3, 'WtrHtr', ['Name', 'FluidSegOutRef', 'FluidSegMakeupRef', 'EF']),
#  (4, 'Blr', [])]
#
