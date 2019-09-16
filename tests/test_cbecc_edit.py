"""py.test for cbecc_edit"""

from io import StringIO
import pytest
import xml.etree.ElementTree as ET
from pybecc import cbecc_edit


def test_printelement():
    """py.test for printelement"""
    data = (
        (
            Tree().treetxt1,
            "./country/rank",
            "<rank>0</rank>",
        ),  # treetxt, xpath, expected
    )
    for treetxt, xpath, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        element = root.find(xpath)
        fhandle = StringIO()
        cbecc_edit.printelement(element, filehandle=fhandle)
        result = fhandle.getvalue()
        assert result.strip() == expected


def test_element2str():
    """py.test for element2str"""
    data = (
        (
            Tree().treetxt1,
            "./country/rank",
            "<rank>0</rank>",
        ),  # treetxt, xpath, expected
    )
    for treetxt, xpath, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        element = root.find(xpath)
        result = cbecc_edit.element2str(element)
        assert result.strip() == expected


def test_copyelement():
    """py.test for copyelement"""
    data = (
        (
            Tree().treetxt1,
            "./country",
            """<country name="Liechtenstein">
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor direction="E" name="Austria" />
        <neighbor direction="W" name="Switzerland" />
    </country>""",
        ),  # treetxt, xpath, expected
    )
    for treetxt, xpath, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        element = root.find(xpath)
        copied = cbecc_edit.copyelement(element)
        result = cbecc_edit.element2str(copied)
        assert result.strip() == expected
        assert (
            cbecc_edit.element2str(copied).strip()
            == cbecc_edit.element2str(element).strip()
        )
        # make sure that is is a copy,
        cbecc_edit.setfieldvalue(copied, "year", "2009")
        assert (
            cbecc_edit.element2str(copied).strip()
            != cbecc_edit.element2str(element).strip()
        )


def test_getcontent():
    """py.test for getcontent"""
    data = (
        (Tree().treetxt1, "./country/rank", "0"),  # treetxt, xpath, expected
        (Tree().treetxt1, "./country/nothing", ""),  # treetxt, xpath, expected
    )
    for treetxt, xpath, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        element = root.find(xpath)
        result = cbecc_edit.getcontent(element)
        assert result == expected


def test_setcontent():
    """py.test for setcontent"""
    data = (
        (
            Tree().treetxt1,
            "./country/rank",
            "32",
            "32",
        ),  # treetxt, xpath, value, expected
    )
    for treetxt, xpath, value, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        element = root.find(xpath)
        cbecc_edit.setcontent(element, value)
        # get content and see then assert
        root = tree.getroot()
        element = root.find(xpath)
        result = cbecc_edit.getcontent(element)
        assert result == expected


def test_findelements():
    """py.test for findelements"""
    data = (
        (
            Tree().treetxt1,
            "./country",
            None,
            ["", "0", "4", "68"],
        ),  # treetxt, xpath, fieldvalues, expected
        (
            Tree().treetxt1,
            "./country",
            [("rank", "0")],
            ["0"],
        ),  # treetxt, xpath, fieldvalues, expected
        (
            Tree().treetxt1,
            "./country",
            [("year", "2011")],
            ["4", "68"],
        ),  # treetxt, xpath, fieldvalues, expected
        (
            Tree().treetxt1,
            "./country",
            [("year", "2011"), ("rank", "68")],
            ["68"],
        ),  # treetxt, xpath, fieldvalues, expected
        (Tree().treetxtm1, None, None, ["68"]),  # treetxt, xpath, fieldvalues, expected
    )
    for treetxt, xpath, fieldvalues, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        foundelements = cbecc_edit.findelements(root, xpath, fieldvalues)
        result = [cbecc_edit.getcontent(item.find("./rank")) for item in foundelements]
        assert result == expected


def test_replacefield():
    """py.test for replacefield"""
    data = (
        (
            Tree().treetxt1,
            "./country",
            "rank",
            None,
            "35",
            ["", "35", "35", "35"],
        ),  # treetxt, xpath, field, before, after, expected
        (
            Tree().treetxt1,
            "./country",
            "rank",
            "4",
            "35",
            ["", "0", "35", "68"],
        ),  # treetxt, xpath, field, before, after, expected
        (
            Tree().treetxt1,
            "./country",
            "rank",
            "4",
            None,
            ["", "0", "4", "68"],
        ),  # treetxt, xpath, field, before, after, expected
        (
            Tree().treetxt1,
            "./country",
            "rank",
            "0",
            "44",
            ["", "44", "4", "68"],
        ),  # treetxt, xpath, field, before, after, expected
        (
            Tree().treetxt1,
            "./country",
            "rank",
            "4",
            "",
            ["", "0", "", "68"],
        ),  # treetxt, xpath, field, before, after, expected
    )
    for treetxt, xpath, field, before, after, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        elements = root.findall(xpath)
        updatedelements = cbecc_edit.replacefield(elements, field, before, after)
        ranks = [element.find("./rank") for element in elements]
        result = [cbecc_edit.getcontent(rank) for rank in ranks]
        assert result == expected
    # -
    # replace a subset of the root  - maybe overkill
    data = (
        (
            Tree().treetxt1,
            "./country",
            "rank",
            None,
            "35",
            ["", "35", "35", "68"],
        ),  # treetxt, xpath, field, before, after, expected
    )
    for treetxt, xpath, field, before, after, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        elements = root.findall(xpath)
        elements = elements[1:3]
        updatedelements = cbecc_edit.replacefield(elements, field, before, after)
        # grab the elements again, just to make sure
        elements = root.findall(xpath)
        ranks = [element.find("./rank") for element in elements]
        result = [cbecc_edit.getcontent(rank) for rank in ranks]
        assert result == expected


def test_getfieldvalue():
    """py.test for getfieldvalue"""
    data = (
        (
            Tree().treetxt1,
            "./country",
            2,
            "rank",
            "4",
        ),  # treetxt, xpath, itemindex, field, expected
        (
            Tree().treetxt1,
            "./country",
            2,
            "year",
            "2011",
        ),  # treetxt, xpath, itemindex, field, expected
    )
    for treetxt, xpath, itemindex, field, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        elements = root.findall(xpath)
        element = elements[itemindex]
        result = cbecc_edit.getfieldvalue(element, field)
        assert result == expected


def test_setfieldvalue():
    """py.test for setfieldvalue"""
    data = (
        (
            Tree().treetxt1,
            "./country",
            2,
            "rank",
            "42",
            "42",
        ),  # treetxt, xpath, itemindex, field, value, expected
        (
            Tree().treetxt1,
            "./country",
            2,
            "year",
            "1969",
            "1969",
        ),  # treetxt, xpath, itemindex, field, value, expected
    )
    for treetxt, xpath, itemindex, field, value, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        elements = root.findall(xpath)
        element = elements[itemindex]
        cbecc_edit.setfieldvalue(element, field, value)
        # recover the value from root
        elements = root.findall(xpath)
        element = elements[itemindex]
        result = cbecc_edit.getfieldvalue(element, field)
        assert result == expected


def test_add_element():
    """py.test for add_element"""
    data = (
        (
            Tree().treetxt3,
            "./",
            ("Name", "Gumby"),
            """<data>
    <rank>68</rank>
<Name>Gumby</Name></data>""",
        ),  # treetxt, xpath, newelement, expected
        (
            Tree().treetxt3,
            "./",
            ("Name", "Gumby", {"index": "5"}),
            """<data>
    <rank>68</rank>
<Name index="5">Gumby</Name></data>""",
        ),  # treetxt, xpath, newelement, expected
    )
    for treetxt, xpath, newelement, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        cbecc_edit.add_element(root, newelement)
        result = cbecc_edit.element2str(root)
        # print(result)
        # print('-')
        # print(expected)
        # print('=')
        assert result == expected

def test_add_indexedelements():
    """py.test for add_indexedelements"""
    data = (
    (
    Tree().treetxt3,
    "./",
    {"Hr":["0.0", "1.0"]},
            """<data>
    <rank>68</rank>
<Hr index="1">0.0</Hr><Hr index="2">1.0</Hr></data>"""
    ), # treetxt, xpath, elementlist, expected
    (
    Tree().treetxt3,
    "./",
    {("LumRef", "LumCnt"):[("H", 1), ("F12", 4)]},
            """<data>
    <rank>68</rank>
<LumRef index="1">H</LumRef><LumRef index="2">F12</LumRef><LumCnt index="1">1</LumCnt><LumCnt index="2">4</LumCnt></data>"""    
    ), # treetxt, xpath, elementlist, expected
    )
    for treetxt, xpath, elementlist, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        cbecc_edit.add_indexedelements(root, elementlist)
        result = cbecc_edit.element2str(root)
        # print(result)
        # print('-')
        # print(expected)
        # print('=')
        assert result == expected
        

def test_add_elements():
    """py.test for add_elements"""
    data = (
        (
            Tree().treetxt3,
            "./",
            [("Name", "Gumby"), ],
            """<data>
    <rank>68</rank>
<Name>Gumby</Name></data>""",
        ),  # treetxt, xpath, newelements, expected
        (
            Tree().treetxt3,
            "./",
            [("Name", "Gumby"), ("Name2", "Gumby2", {"index":"52"}),],
            """<data>
    <rank>68</rank>
<Name>Gumby</Name><Name2 index="52">Gumby2</Name2></data>""",
        ),  # treetxt, xpath, newelements, expected
        (
            Tree().treetxt3,
            "./",
            [("Name", "Gumby"), {"Hr":["0.0", "1.0"]} ],
            """<data>
    <rank>68</rank>
<Name>Gumby</Name><Hr index="1">0.0</Hr><Hr index="2">1.0</Hr></data>""",
        ),  # treetxt, xpath, newelements, expected
        (
            Tree().treetxt3,
            "./",
            [("Name", "Gumby"), {("LumRef", "LumCnt"):[("H", 1), ("F12", 4)]}],
            """<data>
    <rank>68</rank>
<Name>Gumby</Name><LumRef index="1">H</LumRef><LumRef index="2">F12</LumRef><LumCnt index="1">1</LumCnt><LumCnt index="2">4</LumCnt></data>""",
        ),  # treetxt, xpath, newelements, expected
        (
            Tree().treetxt3,
            "./",
            [
                ("Name", "Gumby"), 
                {"Hr":["0.0", "1.0"]} ,
                {("LumRef", "LumCnt"):[("H", 1), ("F12", 4)]}
            ],
            """<data>
    <rank>68</rank>
<Name>Gumby</Name><Hr index="1">0.0</Hr><Hr index="2">1.0</Hr><LumRef index="1">H</LumRef><LumRef index="2">F12</LumRef><LumCnt index="1">1</LumCnt><LumCnt index="2">4</LumCnt></data>""",
        ),  # treetxt, xpath, newelements, expected
    )
    for treetxt, xpath, newelements, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        cbecc_edit.add_elements(root, newelements)
        result = cbecc_edit.element2str(root)
        # print(result)
        # print('-')
        # print(expected)
        # print('=')
        assert result == expected


class Tree(object):
    """holds tree fata for testing"""

    def __init__(self):
        self.treetxtm1 = """<?xml version="1.0"?>
<data>
    <rank>68</rank>:
</data>"""
        # -----------------------
        self.treetxt0 = """<?xml version="1.0"?>
<data>
    somedata
    <country name="Liechtenstein">
    </country>
    <country name="Singapore">
    </country>
    <country name="Panama">
    </country>
</data>"""
        # -----------------------
        self.treetxt1 = """<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Liechtenstein">
        <rank>0</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
        <capital>Panama City</capital>
    </country>
</data>"""
        # -----------------------
        self.treetxt2 = """<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <capital>Panama City</capital>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
    <city name="Chennai">
        <rank>681</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Kochi" direction="W"/>
        <neighbor name="Madurai" direction="S"/>
    </city>
</data>"""
        # -----------------------
        self.treetxt3 = """<?xml version="1.0"?>
<data>
    <rank>68</rank>
</data>"""
