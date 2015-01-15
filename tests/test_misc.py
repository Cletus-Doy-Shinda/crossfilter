"""test_misc.py - Unit tests for misc sections of the code base"""

import traceback
from crossfilter.common import secure, util


def test_hidden_functions():
    """test credentials in secure"""
    secure.test_secure()


def test_bad_url():
    """test bad (non-existent) URL"""
    try:
        resp = util.get('http://www.asfassfjf.com', fatal=True)
        assert not resp
    except Exception as e:
        assert type(e) == util.ConnectionError


def test_malformed_url():
    """test url without http://"""
    resp = util.get('www.google.com')
    assert resp

