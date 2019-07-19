# -*- coding: utf-8 -*-

"""Main module."""

import xml.etree.ElementTree as ET
from collections import OrderedDict

def getroottag(tree):
    """get the root of the document"""
    root = tree.getroot()
    return root.tag
    
def getlevel1_tags(root):
    """get all tags for level below root without dups - maintain order"""
    childs = [child.tag for child in root]    
    # prunechilds = set(childs)
    # cant use set, since I want to preserve order
    l1tags = list(OrderedDict.fromkeys(childs))
    return l1tags
    
def getchildtags(element):
    """get tags at child level without dups - maintain order"""
    childs = [child.tag for child in element]    
    # prunechilds = set(childs)
    # cant use set, since I want to preserve order
    childtags = list(OrderedDict.fromkeys(childs))
    return childtags
    
def getallchildren(element):
    """get all the children of the element"""
    return [child for child in element]    

def findalltag_children(element, tag):
    """find all children that have this tag"""
    return element.findall(tag)
    
def get_tags_childrens_tags(element, tag):
    """get the tags of all the children that have this tag with no dups
    - retain the order"""
    # findalltag_children
    # for each in that:
    #     list.append its child tags
    # remove dups
    # return
    c_elements = findalltag_children(element, tag)
    alist = []
    for c_element in c_elements:
        for child in c_element:
            alist.append(child.tag)
    tags = list(OrderedDict.fromkeys(alist))
    return tags
    
        
        
    
# get_tags_childrens_tags -> get the tags of all the children that have this tag
# findalltag_children -> find all childred that have this tag
