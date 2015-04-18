#!/usr/bin/python
"""x10login.py - Login into x10hosting site"""


import base64
import cookielib

from crossfilter.common.util import post, sendmail
from crossfilter.common.secure import get_x10_credentials


def login():
    """login into free hosting"""
    cookies = cookielib.CookieJar()
    
    # bad ascii characters if I need to dump out contents of html
    bad = [u'\xa0', u'\u221e', u'\u2122', u'\xae', u'\u2019']
    address = 'https://xo2.x10hosting.com:2083/login/'

    user, passwd = get_x10_credentials()

    login_data = {'login_theme': 'cpanel',
                    'user': user,
                    'pass': str(base64.b64decode(passwd)),
                    'failurl': 'https%3A%2F%2Fwww.x10hosting.com%2Fsso%2Fmain%2Fcaf'
                    }

    resp = post(address, cookies=cookies, data=login_data)
    if resp.status_code != 200:
        message = """From: Cross Filter
Subject: x10hosting login failure

Failed to login into x10hosting, better do it yourself asshole.
Status was: %s
    """ % resp.status_code

        sendmail(receivers=['abefriesen.af@gmail.com'], message=message)


login()
