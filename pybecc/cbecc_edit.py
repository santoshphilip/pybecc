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


def add_element(parent, newelement):
    """add a newelement int parent"""
    # ET.SubElement(doc, "field1", name="blah").text = "some value1"
    try:
        name, value, attrib = newelement
    except ValueError as e:
        name, value = newelement
        attrib = dict()
    ET.SubElement(parent, name, attrib).text = value


def add_indexedelements(parent, elementlist):
    """add a list of elements that have indexes"""
    # two type of inputs for elementlist
    # {("LumRef", "LumCnt"):[("H", 1), ("F12", 4), ("W 1x2", 0)]}
    # {"Hr":["0.0", "0.0", "0.75", "0.3", "0.0"]}
    dct = elementlist
    for key in dct:
        if isinstance(key, (list, tuple)):
            # dct = {("LumRef", "LumCnt"):[("H", 1), ("F12", 4), ("W 1x2", 0)]}
            for i, name in enumerate(key):
                for index, values in enumerate(dct[key]):
                    attrib = dict(index=str(index + 1))
                    value = str(values[i])
                    newelement = (name, value, attrib)
                    add_element(parent, newelement)

        else:
            # dct = {"Hr":["0.0", "0.0", "0.75", "0.3", "0.0"]}
            for index, value in enumerate(dct[key]):
                name = key
                attrib = dict(index=str(index + 1))
                newelement = (name, value, attrib)
                add_element(parent, newelement)


def add_elements(parent, newelements):
    """add new elements to parent"""
    for newelement in newelements:
        if isinstance(newelement, dict):
            add_indexedelements(parent, newelement)
        else:
            add_element(parent, newelement)


def removelement():
    """remove an element"""
    # see ../remove.py and code it here
    pass
