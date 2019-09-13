"""functions to read the cbecc.com log files"""


def loglines_startswith(loghandle, swith):
    """generates lines that startswith 'swith' from log file
    the datestamp (19 chars) is clipped from start of the line"""
    # sampleline = "2019-09-12 17:09:58 - Error:  The min. primary flow of TrmlUnit '165-9.38_9002 Circulation-Trm' is 150 cfm, which is less than the minimum zone ventilation flow of 314 cfm. evaluating rule: Set CHECKCODE TrmlUnit:PriAirFlowMin  (72:'HVACSecondary-TerminalUnit-General.rule' line 739)"
    datestamp_i = 19  # clip the datestamp
    with loghandle as fhandle:
        for line in fhandle:
            line = line.strip()
            if line[datestamp_i:].startswith(swith):
                yield line


def termunit_cfm(theline):
    """return terminal unit name and the old and new cfms from the line"""
    cfms = theline.split("cfm")
    oldcfm = cfms[0].split()[-1]
    newcfm = cfms[1].split()[-1]
    trmname = cfms[0].split("'")[1]
    return trmname, oldcfm, newcfm


def termunit_cfmdict(fhandle):
    """return dict of terminal unit name and the old and new cfms"""
    swith = " - Error:  The min. primary flow of TrmlUnit"
    thedict = dict()
    dateend = 19
    for line in loglines_startswith(fhandle, swith):
        if line[dateend:].startswith(swith):
            trmname, oldcfm, newcfm = termunit_cfm(line)
            thedict[trmname] = (oldcfm, newcfm)
    return thedict
