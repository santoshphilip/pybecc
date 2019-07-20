#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pybecc` package."""

import pytest
import xml.etree.ElementTree as ET
from io import StringIO
from collections import OrderedDict as od

from pybecc import pybecc



def test_getroot():
    """py.test for getroot"""
    data = ((Tree().treetxt1, "data"),  # treetxt, expected
    )
    for treetxt, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        result = pybecc.getroottag(tree)
        assert result == expected
        
def test_getlevel1_tags():
    """py.test for getlevel1_tags"""
    data = (
        (Tree().treetxt1, ['country']),  # treetxt, expected
        (Tree().treetxt2, ['country', 'city']),  # treetxt, expected
    )
    for treetxt, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        result = pybecc.getlevel1_tags(root)
        assert result == expected

def test_getchildtags():
    """py.test for getchildtags"""
    data = ((Tree().treetxt1, ['rank', 'year', 'gdppc', 'neighbor']),  # treetxt, expected
    )
    for treetxt, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        element = root.find('country')
        result = pybecc.getchildtags(element)
        assert result == expected
        
def test_getallchildren():
    """py.test for getallchildren"""
    data = (
    (Tree().treetxt1, ['country', 'country', 'country']),  # treetxt, expected
    )        
    for treetxt, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        element = tree.getroot()
        result = pybecc.getallchildren(element)
        assert [item.tag for item in result] == expected
        

def test_findalltag_children():
    """py.test for findalltag_children"""
    data = (
    (Tree().treetxt1, 'country', 
    ['country', 'country', 'country']),  
    # treetxt, tag, expected
    (Tree().treetxt2, 'country', 
    ['country', 'country', 'country']),  
    # treetxt, tag, expected
    )
    for treetxt, tag, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        element = root
        result = pybecc.findalltag_children(element, tag)
        assert [item.tag for item in result] == expected

def test_get_tags_childrens_tags():
    """py.test for get_tags_childrens_tags"""
    data = (
    (Tree().treetxt1, 'country', 
    ['rank', 'year', 'gdppc', 'neighbor', 'capital']),  
    # treetxt, tag, expected
    (Tree().treetxt2, 'country', 
    ['rank', 'year', 'gdppc', 'neighbor', 'capital']),  
    # treetxt, tag, expected
    )
    for treetxt, tag, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        element = root
        result = pybecc.get_tags_childrens_tags(element, tag)
        assert result == expected
    data = (
    (Tree().treetxt1, 'data', 
    ['country']),  
    # treetxt, tag, expected
    # (Tree().treetxt2, 'country',
    # ['rank', 'year', 'gdppc', 'neighbor', 'capital']),
    # # treetxt, tag, expected
    )
    for treetxt, tag, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        element = root
        result = pybecc.get_tags_childrens_tags(element, tag)
        assert result == expected


def test_get_cbeccdicts():
    """py.test for get_cbeccdicts"""
    data = (
    (Tree().treetxt0,
    od([('data', 
            od([('country',  None)])
        )])
    ),  # treetxt, expected
    # (Tree().treetxt1,
    # od([('data',
    #         od([('country',
    #             od([('rank', None), ('year',  None), ('neighbor',  None), ('capital',  None)])
    #         )])
    #     )])
    # ),  # treetxt, expected
    )
    for treetxt, expected in data:
        tree = ET.ElementTree(ET.fromstring(treetxt))
        root = tree.getroot()
        element = root
        result = pybecc.get_cbeccdicts(element)
        # print(result)
        # print(expected)
        assert result == expected
    
        
class Tree(object):
    """holds tree fata for testing"""
    def __init__(self):
        self.treetxt0 = """<?xml version="1.0"?>
<data>
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