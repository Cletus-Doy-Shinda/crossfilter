"""test_misc.py - Unit tests for misc sections of the code base"""

import traceback
from crossfilter.common import secure, util
from crossfilter.scripts import downloadfilters as df
from crossfilter.scripts.acdelco import name2id


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


def test_num_brands():
    """test all available brands are listed"""
    assert len(df.RETRIEVE_FUNCTIONS) == len(util.BRANDS)
    secure.test_num_brands(util.BRANDS)

def test_acdelco_name2id():
    """test all available brands are in acdelco module"""
    for key in util.BRANDS:
        if key != 'ACDELCO':
            assert key in name2id.keys(), '%s' % key
