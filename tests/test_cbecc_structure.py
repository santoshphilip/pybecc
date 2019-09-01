"""py.test for cbecc_structure"""

from io import StringIO

import xml.etree.ElementTree as ET

from pybecc import cbecc_structure

def test_structure():
    """py.test for structure"""
    data = ((Tree().treetxt1,
    """0.000. country
  1.000. rank
  1.001. year
  1.002. gdppc
    2.000. inner_gdppc
      3.000. inner1_gdppc
        4.000. inner2_gdppc
          5.000. inner3_gdppc
            6.000. inner4_gdppc
    2.001. inner0_gdppc
      3.000. inner1_gdppc
        4.000. inner11_gdppc
          5.000. inner111_gdppc
  1.003. neighbor
  1.004. Month
"""
    ),  # treetxt, expected
    )
    for treetxt, expected in data:
        tree = ET.parse(StringIO(treetxt))
        root = tree.getroot()
        fhandle = StringIO()
        cbecc_structure.structure(root, thefile=fhandle)
        result = fhandle.getvalue()
        assert expected == result

def test_structurepath():
    """py.test for structurepath"""
    data = (
    (
    Tree().treetxt1,
    """0.000. ./country
  1.000. ./country/rank
  1.001. ./country/year
  1.002. ./country/gdppc
    2.000. ./country/gdppc/inner_gdppc
      3.000. ./country/gdppc/inner_gdppc/inner1_gdppc
        4.000. ./country/gdppc/inner_gdppc/inner1_gdppc/inner2_gdppc
          5.000. ./country/gdppc/inner_gdppc/inner1_gdppc/inner2_gdppc/inner3_gdppc
            6.000. ./country/gdppc/inner_gdppc/inner1_gdppc/inner2_gdppc/inner3_gdppc/inner4_gdppc
    2.001. ./country/gdppc/inner0_gdppc
      3.000. ./country/gdppc/inner0_gdppc/inner1_gdppc
        4.000. ./country/gdppc/inner0_gdppc/inner1_gdppc/inner11_gdppc
          5.000. ./country/gdppc/inner0_gdppc/inner1_gdppc/inner11_gdppc/inner111_gdppc
  1.003. ./country/neighbor
  1.004. ./country/Month
"""
    ), # treetxt, expected
    )
    for treetxt, expected in data:
        tree = ET.parse(StringIO(treetxt))
        root = tree.getroot()
        fhandle = StringIO()
        cbecc_structure.structurepath(root, thefile=fhandle)
        result = fhandle.getvalue()
        assert expected == result
    
        
class Tree(object):
    """holds the data for testing"""
    def __init__(self):
        self.treetxt1 = """<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>
            1300
        </gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>
            1300
            <inner_gdppc>13600</inner_gdppc>
        </gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <Month>January</Month>
        <gdppc>
            1300
            <inner_gdppc>
                13600
                <inner1_gdppc>
                    13600
                    <inner2_gdppc>
                        13600
                        <inner3_gdppc>
                            13600
                            <inner4_gdppc>
                                13600
                            </inner4_gdppc>
                        </inner3_gdppc>
                    </inner2_gdppc>
                </inner1_gdppc>
            </inner_gdppc>
        </gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <Month>January</Month>
        <gdppc>
            1300
            <inner0_gdppc>
                13600
                <inner1_gdppc>
                    13600
                    <inner11_gdppc>
                        13600
                        <inner111_gdppc>
                            13600
                        </inner111_gdppc>
                    </inner11_gdppc>
                </inner1_gdppc>
            </inner0_gdppc>
        </gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>    
    """