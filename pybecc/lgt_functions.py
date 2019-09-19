"""functions that help to put lights into cbecc.com"""

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
    """create the lighting objects that go into IntLtgSys object"""
    elements = []
    if lcounts:
        elements.append(("Name", lgtobjname))
        elements.append({("LumRef", "LumCnt"): lcounts})
        elements.append(("DaylitAreaType", daylittype))
    return elements


def test_lcounts2elements():
    """py.test for lcounts2elements"""
    data = (
        (
            [("a", 1), ("b", 2)],
            "firstlight",
            "--none--",
            [
                ("Name", "firstlight"),
                {("LumRef", "LumCnt"): [("a", 1), ("b", 2)]},
                ("DaylitAreaType", "--none--"),
            ],
        ),  # lcounts, lgtobjname, daylittype, expected
    )
    for lcounts, lgtobjname, daylittype, expected in data:
        result = lcounts2elements(lcounts, lgtobjname, daylittype)
        assert result == expected


def splitlcounts(lcounts, lgtobjname, daylittype, maxlights=5):
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


def test_splitlcounts():
    """py.test for splitlcounts"""
    data = (
        (
            [("a", 1), ("b", 2)],
            "firstlight",
            "--none--",
            3,
            [
                [
                    ("Name", "firstlight"),
                    {("LumRef", "LumCnt"): [("a", 1), ("b", 2)]},
                    ("DaylitAreaType", "--none--"),
                ]
            ],
        ),  # lcounts, lgtobjname, daylittype, maxlights, expected
        (
            [("a", 1), ("b", 2), ("c", 3)],
            "firstlight",
            "--none--",
            2,
            [
                [
                    ("Name", "firstlight_1"),
                    {("LumRef", "LumCnt"): [("a", 1), ("b", 2)]},
                    ("DaylitAreaType", "--none--"),
                ],
                [
                    ("Name", "firstlight_2"),
                    {("LumRef", "LumCnt"): [("c", 3)]},
                    ("DaylitAreaType", "--none--"),
                ],
            ],
        ),  # lcounts, lgtobjname, daylittype, maxlights, expected
    )
    for lcounts, lgtobjname, daylittype, maxlights, expected in data:
        result = splitlcounts(lcounts, lgtobjname, daylittype, maxlights)
        # print(result)
        # print('-')
        # print(expected)
        # print('=')
        assert result == expected


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


def test_splitlist():
    """py.test for splitlist"""
    data = (
        ([1, 2, 3], 5, [[1, 2, 3]]),  # lst, chunk, expected
        ([1, 2, 3], 2, [[1, 2], [3]]),  # lst, chunk, expected
        ([1, 2, 3, 4], 2, [[1, 2], [3, 4]]),  # lst, chunk, expected
        ([1, 2, 3], 3, [[1, 2, 3]]),  # lst, chunk, expected
        ([], 5, [[]]),  # lst, chunk, expected
    )
    for lst, chunk, expected in data:
        result = splitlist(lst, chunk)
        assert result == expected


def space_lightrows(rows, headers=2):
    """convert rows to dict {spacename: lightrows, }
    The rows are assigned to each spacename"""
    spacelights = []
    for row in rows[headers:]:
        zname = row[0]
        if zname:
            # prev zname is complete
            if spacelights:
                yield znamenow, spacelights
                spacelights = []
            znamenow = zname
        spacelights.append(row)
    yield znamenow, spacelights


def test_space_lightrows():
    """py.test for space_lightrows"""
    data = (
        (
            [["header1"], ["Gumby", 1], ["", 2], ["Gumby1", 11], ["", 22]],
            1,
            [
                ("Gumby", [["Gumby", 1], ["", 2]]),
                ("Gumby1", [["Gumby1", 11], ["", 22]]),
            ],
        ),  # rows, headers, expected
    )
    for rows, headers, expected in data:
        result = list(space_lightrows(rows, headers))
        assert result == expected


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


def test_get_cbecc_lgt_dct():
    """py.test for get_cbecc_lgt_dct"""
    data = (
        (
            [
                [
                    "\ufeffMODEL ZONE NAMES",
                    "lighting Object Names",
                    "fixture type",
                    "Primary",
                    "Secondary",
                    "nonDaylit",
                    "",
                ],
                [
                    "",
                    "",
                    "",
                    "PrimarySidelit",
                    "SecondarySidelit",
                    "- none -",
                    "Daylit zone type",
                ],
                [
                    "S-180-1.01_1100 Large Hearing R",
                    "1.01_1100",
                    "A1",
                    "-",
                    "-",
                    "12",
                    "",
                ],
                ["", "", "B1", "", "", "2", ""],
                ["", "", "F_6FT", "", "", "6", "NonDaylit only (more than 5 types)"],
                ["", "", "D_8FT", "", "", "1", ""],
                ["", "", "C", "", "", "4", ""],
                ["", "", "D_26FT", "", "", "1", ""],
                [
                    "S-181-1.02_1100 Large Hearing R",
                    "1.02_1100",
                    "A1",
                    "7",
                    "13",
                    "",
                    "",
                ],
                ["", "", "B1", "1", "2", "", ""],
                ["", "", "F_6FT", "3", "6", "", "secondary+primary"],
                ["", "", "D_8FT", "", "1", "", ""],
                ["", "", "C", "2", "4", "", ""],
                [
                    "S-182-1.03_1100 Large Hearing R",
                    "1.03_1100",
                    "A1",
                    "10",
                    "",
                    "",
                    "",
                ],
                ["", "", "B1", "8", "", "", ""],
                ["", "", "D_24FT", "1", "", "", "primary only"],
                ["", "", "D_25FT", "1", "", "", ""],
                ["", "", "F_6FT", "4", "", "", ""],
                ["", "", "D_5FT", "1", "", "", ""],
                ["", "", "D_4FT", "1", "", "", ""],
                ["", "", "EX1", "9", "", "", ""],
                ["", "", "T", "1", "", "", ""],
                [
                    "S-183-1.04_1030 Circulation",
                    "1.04_1030",
                    "W",
                    "",
                    "",
                    "16",
                    "NonDaylit only (less than 5 types)",
                ],
                ["S-184-1.05_1041 Circulation", "1.05_1041", "W", "2", "", "4", ""],
                ["", "", "H1A", "", "1", "1", "primary+secondary+nonDaylit"],
            ],
            """S-180-1.01_1100 Large Hearing R
	 IntLtgSys
		 ('Name', '1.01_1100_nonDaylit_1')
		 {('LumRef', 'LumCnt'): [('A1', 12), ('B1', 2), ('F_6FT', 6), ('D_8FT', 1), ('C', 4)]}
		 ('DaylitAreaType', '- none -')

	 IntLtgSys
		 ('Name', '1.01_1100_nonDaylit_2')
		 {('LumRef', 'LumCnt'): [('D_26FT', 1)]}
		 ('DaylitAreaType', '- none -')


S-181-1.02_1100 Large Hearing R
	 IntLtgSys
		 ('Name', '1.02_1100_Primary')
		 {('LumRef', 'LumCnt'): [('A1', 7), ('B1', 1), ('F_6FT', 3), ('C', 2)]}
		 ('DaylitAreaType', 'PrimarySidelit')

	 IntLtgSys
		 ('Name', '1.02_1100_Secondary')
		 {('LumRef', 'LumCnt'): [('A1', 13), ('B1', 2), ('F_6FT', 6), ('D_8FT', 1), ('C', 4)]}
		 ('DaylitAreaType', 'SecondarySidelit')


S-182-1.03_1100 Large Hearing R
	 IntLtgSys
		 ('Name', '1.03_1100_Primary_1')
		 {('LumRef', 'LumCnt'): [('A1', 10), ('B1', 8), ('D_24FT', 1), ('D_25FT', 1), ('F_6FT', 4)]}
		 ('DaylitAreaType', 'PrimarySidelit')

	 IntLtgSys
		 ('Name', '1.03_1100_Primary_2')
		 {('LumRef', 'LumCnt'): [('D_5FT', 1), ('D_4FT', 1), ('EX1', 9), ('T', 1)]}
		 ('DaylitAreaType', 'PrimarySidelit')


S-183-1.04_1030 Circulation
	 IntLtgSys
		 ('Name', '1.04_1030_nonDaylit')
		 {('LumRef', 'LumCnt'): [('W', 16)]}
		 ('DaylitAreaType', '- none -')


S-184-1.05_1041 Circulation
	 IntLtgSys
		 ('Name', '1.05_1041_Primary')
		 {('LumRef', 'LumCnt'): [('W', 2)]}
		 ('DaylitAreaType', 'PrimarySidelit')

	 IntLtgSys
		 ('Name', '1.05_1041_Secondary')
		 {('LumRef', 'LumCnt'): [('H1A', 1)]}
		 ('DaylitAreaType', 'SecondarySidelit')

	 IntLtgSys
		 ('Name', '1.05_1041_nonDaylit')
		 {('LumRef', 'LumCnt'): [('W', 4), ('H1A', 1)]}
		 ('DaylitAreaType', '- none -')


""",
        ),  # rows, expected
    )
    for rows, expected in data:
        znames = [row[0] for row in rows[2:] if row[0].strip()]
        cbecc_lgt_dct = get_cbecc_lgt_dct(rows)
        result = StringIO()
        for zname in znames:
            print(zname, file=result)
            for manyelement in cbecc_lgt_dct[zname]:
                for elements in manyelement:
                    if elements:
                        print("\t", "IntLtgSys", file=result)
                        # insert the IntLtgSys here
                        for element in elements:
                            print("\t\t", element, file=result)
                        print(file=result)
            print(file=result)
        # for line1, line2 in zip(result.getvalue().splitlines(), expected.splitlines()):
        # print(line1)
        # print(line2)
        # assert line1 == line2
        assert result.getvalue() == expected
