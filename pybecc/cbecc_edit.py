"""functions to edit a cbecc file"""



def getcontent(element):
    try:
        txt = element.text.strip()
    except AttributeError as e:
        txt = ""
    return txt


def getfieldvalue(element, field):
    """rerurn the value of the field"""
    return getcontent(element.find(f"./{field}"))

def findelements(element, xpath=None, fieldvalues=None):
    """starting from element, find xpath elements and filter by fieldvalues"""
    if not fieldvalues:
        fieldvalues = list()
    if not xpath:
        xpath = "."
    filtered = element.findall(xpath)
    for field, value in fieldvalues:
        filtered = [item for item in filtered if getcontent(item.find(f"./{field}")) == value]
    return filtered
        

def replacefield(elements, field, before=None, after=None):
    """replaces the value in field. 
    Replaces before with after.
    If before=None, replace all the before
    if after=None there are no changes"""
    # TODO : test fi filed eists
    # print(field, before, after)
    if after == None:  # cannot use 'not after' -> maybe true for some values
        return elements
    subelements = [element.find(f"./{field}") for element in elements]
    for subelement in subelements:
        if subelement:
            presentvalue = getcontent(subelement)
            if before == None:  # cannot use 'not before' -> maybe true for some values
                subelement.text = after
            else:
                if presentvalue == before:
                    subelement.text = after
    return elements