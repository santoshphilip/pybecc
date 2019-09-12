"""functions to edit a cbecc file"""

import xml.etree.ElementTree as ET


def printelement(element, filehandle=None):
    """print the element"""
    elementstr = element2str(element)
    print(elementstr, file=filehandle)


def element2str(element):
    """return the element as a string"""
    return ET.tostring(element, encoding="unicode")


def copyelement(element):
    """make a copy of the element"""
    elementstr = element2str(element)
    tree = ET.ElementTree(ET.fromstring(elementstr))
    return tree.getroot()


def getcontent(element):
    try:
        txt = element.text.strip()
    except AttributeError as e:
        txt = ""
    return txt


def setcontent(element, value):
    """set the content of that element to value"""
    try:
        element.text = value
    except AttributeError as e:
        raise AttributeError(f"no such element - cannot set value")


# TODO : we need functions for
# - delete elements
# - insert elements
# see the folowing functions to do this when needed
# - Element.remove(child)
# - element.append()
# - element.extend()
# - xml.etree.ElementTree.SubElement
# build this as needed.


def getfieldvalue(element, field):
    """return the value of the field in element"""
    return getcontent(element.find(f"./{field}"))


def setfieldvalue(element, field, value):
    """in element, set the value of the filed to 'value' """
    return setcontent(element.find(f"./{field}"), value)


def findelements(element, xpath=None, fieldvalues=None):
    """starting from element, find xpath elements and filter by fieldvalues"""
    if not fieldvalues:
        fieldvalues = list()
    if not xpath:
        xpath = "."
    filtered = element.findall(xpath)
    for field, value in fieldvalues:
        filtered = [
            item for item in filtered if getcontent(item.find(f"./{field}")) == value
        ]
    return filtered


def replacefield(elements, field, before=None, after=None):
    """replaces the value in field. 
    Replaces before with after.
    If before=None, replace all the before
    if after=None there are no changes"""
    if after == None:  # cannot use 'not after' -> maybe true for some values
        return elements
    subelements = [element.find(f"./{field}") for element in elements]
    subelements = [sub for sub in subelements if sub is not None]
    for subelement in subelements:
        presentvalue = getcontent(subelement)
        if before == None:  # cannot use 'not before' -> maybe true for some values
            subelement.text = after
        else:
            if presentvalue == before:
                subelement.text = after
    return elements


def removelement():
    """remove an element"""
    # see ../remove.py and code it here
    pass
