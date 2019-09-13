"""py.test for cbecc_log"""

from io import StringIO
from pybecc import cbecc_log


def test_loglines_startswith():
    """py.test for loglines_startswith"""
    data = (
        (
            """2019-09-12 17:09:58 - Error:  The
2019-09-12 17:09:58 - Error:  The
2019-09-12 17:09:58 - thisline:  1
2019-09-12 17:09:58 - thisline:  2
2019-09-12 17:09:58 - Error:  The
2019-09-12 17:09:58 - thisline:  3
""",
            " - thisline",
            """2019-09-12 17:09:58 - thisline:  1
2019-09-12 17:09:58 - thisline:  2
2019-09-12 17:09:58 - thisline:  3""",
        ),  # logtxt, startswith, expected
    )
    for logtxt, startswith, expected in data:
        loghandle = StringIO(logtxt)
        thelines = cbecc_log.loglines_startswith(loghandle, startswith)
        thelines = list(thelines)
        result = "\n".join(thelines)
        assert result == expected


def test_termunit_cfm():
    """py.test for termunit_cfm"""
    data = (
        (
            "2019-09-12 17:09:58 - Error:  The min. primary flow of TrmlUnit '165-9.38_9002 Circulation-Trm' is 150 cfm, which is less than the minimum zone ventilation flow of 314 cfm. evaluating rule: Set CHECKCODE TrmlUnit:PriAirFlowMin  (72:'HVACSecondary-TerminalUnit-General.rule' line 739)",
            ("165-9.38_9002 Circulation-Trm", "150", "314"),
        ),  # theline, expected
    )
    for theline, expected in data:
        result = cbecc_log.termunit_cfm(theline)
        assert result == expected


def test_termunit_cfmdict():
    """py.test for termunit_cfmdict"""
    data = (
        (
            """2019-09-12 17:09:58 Other line
2019-09-12 17:09:58 - Error:  The min. primary flow of TrmlUnit 'Unit1' is 5 cfm, <snip> of 50 cfm. eval <snip> e 739)
2019-09-12 17:09:58 - Error:  The min. primary flow of TrmlUnit 'Unit2' is 10 cfm, <snip> of 100 cfm. eval <snip> e 739)
2019-09-12 17:09:58 Other line
2019-09-12 17:09:58 - Error:  The min. primary flow of TrmlUnit 'Unit3' is 15 cfm, <snip> of 150 cfm. eval <snip> e 739)
2019-09-12 17:09:58 - Error:  The min. primary flow of TrmlUnit 'Unit4' is 20 cfm, <snip> of 200 cfm. eval <snip> e 739)
2019-09-12 17:09:58 Other line""",
            dict(
                Unit1=("5", "50"),
                Unit2=("10", "100"),
                Unit3=("15", "150"),
                Unit4=("20", "200"),
            ),
        ),  # logtxt, expected
    )
    for logtxt, expected in data:
        fhandle = StringIO(logtxt)
        result = cbecc_log.termunit_cfmdict(fhandle)
        assert result == expected
