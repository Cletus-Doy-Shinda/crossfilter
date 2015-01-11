"""test_misc.py - Unit tests for misc sections of the code base"""


from crossfilter.common import secure


def test_hidden_functions():
    """test credentials in secure"""
    secure.test_secure()


