"""util.py - Module for utility functions"""


import re
import requests
import smtplib
import base64

from datetime import datetime
from crossfilter.common.contexts import dbcursor
from crossfilter.common.secure import get_email_credentials


INSERT_SQL_FILE = '/var/crossfilter/logs/insert.sql'
VALID_FILE = '/var/crossfilter/logs/validated.log'
EMAIL_LOG_FILE = '/var/crossfilter/logs/email.log'

BRANDS = ['ACDELCO', 'BALDWIN', 'CARQUEST', 'DONALDSON', 'FRAM',
          'NAPA', 'WIX', 'PUROLATOR', 'SERVICE CHAMP', 'JOHN DEERE',
          'FLEETGUARD', 'HASTINGS', 'MOBIL'
        ]

NAME_MAP = {
'acdelco':
    {
        'JOHN DEERE': ['JOHN+DEERE'],
        'SERVICE CHAMP': ['SERVICE+CHAMP'],
        'WIX': ['WIX+CORPORATION'],
    },
'baldwin':
    {
        'HASTINGS': ['HASTINGS PREMIUM FILTERS'],
    },
'carquest':
    {
        'ACDELCO': ['AC DELCO'],
        'HASTINGS': ['HASTINGS FILTERS'],
    },
'donaldson':
    {
        'ACDELCO': ['AC'],
        'MOBIL': ['MOBIL OIL'],
    },
'fram':
    {
        'ACDELCO': ['AC-DELCO'],
    },
'hastings':
    {
        'BALDWIN': ['BALDWIN FILTERS'],
        'NAPA': ['NAPA GOLD'],
    },
'john deere':
    {
        'ACDELCO': ['AC'],
    },
'mobil':
    {
        'ACDELCO': ['AC'],
        'NAPA': ['NAPA', 'NAPA GOLD'],
    },
'napa':
    {
        'ACDELCO': ['AC DELCO'],
        'HASTINGS': ['HASTINGS FILTERS'],
    },
'purolator':
    {
        'ACDELCO': ['AC-DELCO'],
        'NAPA': ['NAPA GOLD'],
    },
'service champ':
    {
        'ACDELCO': ['AC'],
        'NAPA': ['NAPA', 'NAPA GOLD'],
    },
'wix':
    {
    'ACDELCO': ['AC DELCO'],
    'HASTINGS': ['HASTINGS FILTERS'],
    }
}


def add_request(filter_number, brand):
    """add <brand> <filternumber> to requests table"""
    with dbcursor() as cursor:
        insert = "insert into requests(brand, filter) values('%s', '%s')"
        insert = insert % (brand, filter_number)
        cursor.execute(insert)


def get(url, cookies=None):
    """retrieve <url> conents, adding <cookies> if needed"""
    if cookies:
        cookies = dict(cookies_are=cookies)

    try:
        page = requests.get(url, cookies=cookies)
        return page.text
    except Exception as e:
        print 'Exception trying to access %s: %s' % (url, str(e))
        return None


def post(url, cookies=None, data=dict):
    """post <data> to <url>, adding <cookies> if needed. Returns
    http response code."""
    resp = requests.post(url, cookies=cookies, data=data)
    return resp.status_code


def substring(regex_pat, string):
    """returns substring matched by <regex_pat> in string"""
    match = re.search(regex_pat, string)
    return match.group(0) if matche else ''


def sendmail(receivers=[str], message=str):
    """send <message> to <receivers"""
    sender, password = get_email_credentials()
    
    with open(EMAIL_LOG_FILE, 'a') as out:
        try:
            session = smtplib.SMTP('smtp.gmail.com',587)
            session.ehlo()
            session.starttls()
            session.ehlo()
            session.login(sender, base64.b64decode(password))
            session.sendmail(sender, receivers, message)
            session.quit()
        except smtplib.SMTPException as e:
            out.write(str(datetime.now()) + ': Error writing email: %s\n' % str(e))


def format_brand(modulename, brand, filternumber):
    """Return list of brand names unique to <modulename>"""
    filternumber = filternumber.upper()
    brand = brand.upper()
    modulename = modulename.lower()

    alias_map = NAME_MAP.get(modulename, None)
    if not alias_map:
        return [brand], filternumber
    alias_list = alias_map.get(brand, None)
    if not alias_list:
        return [brand], filternumber
    return alias_list, filternumber


# for brand in BRANDS:
#     brnds, fnum = format_brand(brand.lower(), 'acdelco', 'pf47')
#     print '%s: %s %s' % (brand, brnds, fnum)