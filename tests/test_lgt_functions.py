"""py.test for lgt_functions.py"""

from io import StringIO
from operator import itemgetter, attrgetter   

from pybecc import lgt_functions


def test_getlightcounts():
    """py.test for getlightcounts"""
    data = (
        (
            [["zone1", "objname1", "fixturetype1", "1"], ["", "", "fixturetype2", "2"]],
            3,
            2,
            [("fixturetype1", 1), ("fixturetype2", 2)],
        ),  # zrows, daytype_i, fixturetype_i, expected
        (
            [
                ["zone1", "objname1", "fixturetype1", "1"],
                ["", "", "fixturetype2", "2", "3"],
            ],
            4,
            2,
            [("fixturetype2", 3)],
        ),  # zrows, daytype_i, fixturetype_i, expected
    )
    for zrows, daytype_i, fixturetype_i, expected in data:
        result = lgt_functions.getlightcounts(zrows, daytype_i, fixturetype_i)
        # print(result)
        # print('-')
        # print(expected)
        # print('=')
        assert result == expected


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
        result = lgt_functions.lcounts2elements(lcounts, lgtobjname, daylittype)
        assert result == expected


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
        result = lgt_functions.splitlcounts(lcounts, lgtobjname, daylittype, maxlights)
        # print(result)
        # print('-')
        # print(expected)
        # print('=')
        assert result == expected


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
        result = lgt_functions.splitlist(lst, chunk)
        assert result == expected


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
        result = list(lgt_functions.space_lightrows(rows, headers))
        assert result == expected


def test_spaceroom_lightrows():
    """py.test for spaceroom_lightrows"""
    data = (
        (
            [
                ["header1"],
                ["Gumby", "room1", 0],
                ["", "", 2],
                ["", "", 11],
                ["", "", 22],
            ],
            1,
            [
                (
                    ("Gumby", "room1"),
                    [["Gumby", "room1", 0], ["", "", 2], ["", "", 11], ["", "", 22]],
                )
            ],
        ),  # rows, headers, expected
        (
            [
                ["header1"],
                ["Gumby", "room1", 0],
                ["", "", 2],
                ["", "room2", 11],
                ["", "", 22],
            ],
            1,
            [
                (("Gumby", "room1"), [["Gumby", "room1", 0], ["", "", 2]]),
                (("Gumby", "room2"), [["", "room2", 11], ["", "", 22]]),
            ],
        ),  # rows, headers, expected
        (
            [
                ["header1"],
                ["Gumby", "room1", 0],
                ["", "", 2],
                ["", "room2", 11],
                ["", "", 22],
                ["Gumby1", "room11", 0],
                ["", "", 2],
                ["", "room22", 11],
                ["", "", 22],
            ],
            1,
            [
                (("Gumby", "room1"), [["Gumby", "room1", 0], ["", "", 2]]),
                (("Gumby", "room2"), [["", "room2", 11], ["", "", 22]]),
                (("Gumby1", "room11"), [["Gumby1", "room11", 0], ["", "", 2]]),
                (("Gumby1", "room22"), [["", "room22", 11], ["", "", 22]]),
            ],
        ),  # rows, headers, expected
        (
            [
                ["header1"],
                ["Gumby", "room1", 0],
                ["", "room2", 2],
                ["", "room3", 11],
                ["", "", 22],
                ["Gumby1", "room11", 0],
                ["", "", 2],
                ["", "room22", 11],
                ["", "room33", 22],
            ],
            1,
            [
                (("Gumby", "room1"), [["Gumby", "room1", 0],]),
                (("Gumby", "room2"), [["", "room2", 2], ]),
                (("Gumby", "room3"), [["", "room3", 11], ["", "", 22]]),
                (("Gumby1", "room11"), [["Gumby1", "room11", 0], ["", "", 2]]),
                (("Gumby1", "room22"), [["", "room22", 11], ]),
                (("Gumby1", "room33"), [["", "room33", 22], ]),
            ],
        ),  # rows, headers, expected
    )
    for rows, headers, expected in data:
        result = list(lgt_functions.spaceroom_lightrows(rows, headers))
        # print(result)
        # print("-")
        # print(expected)
        # print("=")
        assert result == expected


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
        (
[['\ufeffMODEL ZONE NAMES',
  'lighting Object Names',
  'fixture type',
  'Primary',
  'Secondary',
  'nonDaylit',
  ''],
 ['',
  '',
  '',
  'PrimarySidelit',
  'SecondarySidelit',
  '- none -',
  'Daylit zone type'],
 ['S-180-1.01_1100 Large Hearing R', '1.01_1100', 'A1', '-', '-', '12', ''],
 ['', '', 'B1', '', '', '2', ''],
 ['', '', 'F_6FT', '', '', '6', 'NonDaylit only (more than 5 types)'],
 ['', '1.01_XXXX', 'D_8FT', '', '', '1', ''],
 ['', '', 'C', '', '', '4', ''],
 ['S-181-1.02_1100 Large Hearing R', '1.02_1100', 'A1', '7', '13', '', ''],
 ['', '', 'B1', '1', '2', '', ''],
 ['', '', 'F_6FT', '3', '6', '', 'secondary+primary'],
 ['', '', 'D_8FT', '', '1', '', ''],
 ['', '', 'C', '2', '4', '', '']],
  """S-180-1.01_1100 Large Hearing R
	 IntLtgSys
		 ('Name', '1.01_1100_nonDaylit')
		 {('LumRef', 'LumCnt'): [('A1', 12), ('B1', 2), ('F_6FT', 6)]}
		 ('DaylitAreaType', '- none -')


S-180-1.01_1100 Large Hearing R
	 IntLtgSys
		 ('Name', '1.01_XXXX_nonDaylit')
		 {('LumRef', 'LumCnt'): [('D_8FT', 1), ('C', 4)]}
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


""",
        ),  # rows, expected
    )
    for rows, expected in data:
        znames = [row[0] for row in rows[2:] if row[0].strip()]
        cbecc_lgt_dct = lgt_functions.get_cbecc_lgt_dct(rows)
        okeys = cbecc_lgt_dct.keys()
        keys = sorted(okeys, key= lambda x: znames.index(itemgetter(0)(x))) # sort in the order of znames
        result = StringIO()
        for zname, rname in keys:
            print(zname, file=result)
            for manyelement in cbecc_lgt_dct[(zname, rname)]:
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


def test_get_cbecc_lgt():
    """py.test for get_cbecc_lgt"""
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
        (
[['\ufeffMODEL ZONE NAMES',
  'lighting Object Names',
  'fixture type',
  'Primary',
  'Secondary',
  'nonDaylit',
  ''],
 ['',
  '',
  '',
  'PrimarySidelit',
  'SecondarySidelit',
  '- none -',
  'Daylit zone type'],
 ['S-180-1.01_1100 Large Hearing R', '1.01_1100', 'A1', '-', '-', '12', ''],
 ['', '', 'B1', '', '', '2', ''],
 ['', '', 'F_6FT', '', '', '6', 'NonDaylit only (more than 5 types)'],
 ['', '1.01_XXXX', 'D_8FT', '', '', '1', ''],
 ['', '', 'C', '', '', '4', ''],
 ['S-181-1.02_1100 Large Hearing R', '1.02_1100', 'A1', '7', '13', '', ''],
 ['', '', 'B1', '1', '2', '', ''],
 ['', '', 'F_6FT', '3', '6', '', 'secondary+primary'],
 ['', '', 'D_8FT', '', '1', '', ''],
 ['', '', 'C', '2', '4', '', '']],
  """S-180-1.01_1100 Large Hearing R
	 IntLtgSys
		 ('Name', '1.01_1100_nonDaylit')
		 {('LumRef', 'LumCnt'): [('A1', 12), ('B1', 2), ('F_6FT', 6)]}
		 ('DaylitAreaType', '- none -')


S-180-1.01_1100 Large Hearing R
	 IntLtgSys
		 ('Name', '1.01_XXXX_nonDaylit')
		 {('LumRef', 'LumCnt'): [('D_8FT', 1), ('C', 4)]}
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


""",
        ),  # rows, expected
    )
    # rows is a list
    for rows, expected in data:
        # import csv
        # csv_writer = csv.writer(open('a1.csv', 'w'))
        # for row in rows:
        #     csv_writer.writerow(row)
        cbecc_lgt_gen = lgt_functions.get_cbecc_lgt(rows)
        result = StringIO()
        for zname, lightlist in cbecc_lgt_gen:
            print(zname, file=result)
            for manyelement in lightlist:
                for elements in manyelement:
                    if elements:
                        print("\t", "IntLtgSys", file=result)
                        # insert the IntLtgSys here
                        for element in elements:
                            print("\t\t", element, file=result)
                        print(file=result)
            print(file=result)
        # for line1, line2 in zip(result.getvalue().splitlines(), expected.splitlines()):
        #     print(line1)
        #     print(line2)
        #     assert line1 == line2
        assert result.getvalue() == expected
    # ----
    # rows as a generator
    for rows, expected in data:
        row_generator = (row for row in rows)
        cbecc_lgt_gen = lgt_functions.get_cbecc_lgt(row_generator)
        result = StringIO()
        for zname, lightlist in cbecc_lgt_gen:
            print(zname, file=result)
            for manyelement in lightlist:
                for elements in manyelement:
                    if elements:
                        print("\t", "IntLtgSys", file=result)
                        # insert the IntLtgSys here
                        for element in elements:
                            print("\t\t", element, file=result)
                        print(file=result)
            print(file=result)
        # for line1, line2 in zip(result.getvalue().splitlines(), expected.splitlines()):
        #     print(line1)
        #     print(line2)
        #     assert line1 == line2
        assert result.getvalue() == expected
