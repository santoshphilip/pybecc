"""functions that help to put lights into cbecc.com"""

import itertools
from io import StringIO


def getlightcounts(zrows, daytype_i, fixturetype_i=2):
    """get the light counts for a daylight type"""
    lightcount = []
    for zrow in zrows:
        try:
            num = int(zrow[daytype_i])
            fixture = zrow[fixturetype_i]
            lightcount.append((fixture.strip(), num))
        except (ValueError, IndexError) as e:
            pass
    return lightcount


def lcounts2elements(lcounts, lgtobjname, daylittype):
    """create the lighting objects that go into IntLtgSys object
    Dont use this. use splitcounts"""
    elements = []
    if lcounts:
        elements.append(("Name", lgtobjname))
        elements.append({("LumRef", "LumCnt"): lcounts})
        elements.append(("DaylitAreaType", daylittype))
    return elements


def splitlcounts(lcounts, lgtobjname, daylittype, maxlights=5):
    """does the same as lcounts2elements, but splits element if it has more
    than 5 fixtures. use this function instead of lcounts2elements"""
    lcounts_lst = splitlist(lcounts, maxlights)
    manyelements = list()
    for i, acounts in enumerate(lcounts_lst):
        if len(lcounts_lst) == 1:
            ii = ""
        else:
            ii = f"_{i + 1}"
        elements = lcounts2elements(acounts, f"{lgtobjname}{ii}", daylittype)
        manyelements.append(elements)
    return manyelements


def splitlist(lst, chunk):
    """split the list into pieces size of chunk"""
    if lst == []:
        return [lst]
    splits = []
    stop = len(lst)
    prev = None
    for i in range(0, len(lst), chunk):
        if prev is None:
            prev = i
            continue
        splits.append(lst[prev:i])
        prev = i
    if i < stop:
        splits.append(lst[i:stop])
    return splits


def space_lightrows(rows, headers=2):
    """convert rows to dict {spacename: lightrows, }
    The rows are assigned to each spacename"""
    rows = itertools.chain(rows)
    for i in range(headers):
        next(rows)
    spacelights = []
    for row in rows:
        zname = row[0]
        if zname:
            # prev zname is complete
            if spacelights:
                yield znamenow, spacelights
                spacelights = []
            znamenow = zname
        spacelights.append(row)
    yield znamenow, spacelights

    
def spaceroom_lightrows(rows, headers=2):
    """convert rows to dict {spacename: lightrows, }
    The rows are assigned to each spacename"""
    rows = itertools.chain(rows)
    for i in range(headers):
        next(rows)
    spacelights = []
    for row in rows:
        zname = row[0].strip()
        rname = row[1].strip()
        if rname:
            # prev zname and rname are complete
            if spacelights:
                yield (znamenow, rnamenow), spacelights
                spacelights = []
            if zname:
                znamenow = zname
            rnamenow = rname
        spacelights.append(row)
    yield (znamenow, rnamenow), spacelights


def get_cbecc_lgt_dct(rows):
    """return lighting dct for input into cbecc xml"""
    hrow1 = rows[0]
    hrow2 = rows[1]
    lgtobjname_i = 1
    fixturetype_i = 2
    primary_i = 3
    secondary_i = 4
    nondaylight_i = 5
    daytypes_i = [primary_i, secondary_i, nondaylight_i]
    cbecc_lgt_dct = dict()
    for zname, zrows in space_lightrows(rows):
        lgtobjname_preffix = zrows[0][lgtobjname_i]
        for daytype_i in daytypes_i:
            suffix = hrow1[daytype_i]
            lgtobjname = f"{lgtobjname_preffix}_{suffix}"
            daylittype = hrow2[daytype_i]
            elements = splitlcounts(
                getlightcounts(zrows, daytype_i), lgtobjname, daylittype
            )
            cbecc_lgt_dct.setdefault(zname, list()).append(elements)
    return cbecc_lgt_dct


def get_cbecc_lgt(rows, maxlights=5):
    """generator yielding (zonename, lightlist) for cbecc xml"""
    rows = itertools.chain(rows)  # allows me to use next() for list or generator
    hrow1 = next(rows)
    hrow2 = next(rows)
    lgtobjname_i = 1
    fixturetype_i = 2
    primary_i = 3
    secondary_i = 4
    nondaylight_i = 5
    daytypes_i = [primary_i, secondary_i, nondaylight_i]
    for zname, zrows in space_lightrows(rows, headers=0):
        lightlist = list()
        lgtobjname_preffix = zrows[0][lgtobjname_i]
        for daytype_i in daytypes_i:
            suffix = hrow1[daytype_i]
            lgtobjname = f"{lgtobjname_preffix}_{suffix}"
            daylittype = hrow2[daytype_i]
            elements = splitlcounts(
                getlightcounts(zrows, daytype_i),
                lgtobjname,
                daylittype,
                maxlights=maxlights,
            )
            lightlist.append(elements)
        yield zname, lightlist
