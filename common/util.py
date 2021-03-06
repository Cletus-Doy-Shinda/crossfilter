"""util.py - Module for utility functions"""


import re
import requests
import smtplib
import base64
import traceback
import subprocess

from datetime import datetime
from crossfilter.common.contexts import dbcursor
from crossfilter.common.secure import get_email_credentials


ConnectionError = requests.ConnectionError
HTTPError = requests.HTTPError

INSERT_SQL_FILE = '/var/crossfilter/logs/insert.sql'
VALID_FILE = '/var/crossfilter/logs/validated.log'
EMAIL_LOG_FILE = '/var/crossfilter/logs/email.log'

BRANDS = ['ACDELCO', 'BALDWIN', 'CARQUEST', 'DONALDSON', 'FRAM',
          'NAPA', 'WIX', 'PUROLATOR', 'SERVICE CHAMP', 'JOHN DEERE',
          'FLEETGUARD', 'HASTINGS', 'MOBIL', 'VALVOLINE', 'LUBERFINER'
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
        'NAPA': ['NAPA', 'NAPA GOLD', 'NAPA PROSELECT'],
        'LUBERFINER': ['LUBER-FINER'],
        'CARQUEST': ['CARQUEST RED', 'CARQUEST']
    },
'carquest':
    {
        'ACDELCO': ['AC-DELCO'], # XXX Revert to AC DELCO
        'HASTINGS': ['HASTINGS FILTERS'],
    },
'caterpillar':
    {
        'BALDWIN': ['Baldwin'],
    },
'donaldson':
    {
        'ACDELCO': ['AC'],
        'MOBIL': ['MOBIL OIL'],
        'LUBERFINER': ['LUBER-FINER'],
    },
'fleetguard':
    {
        'ACDELCO': ['AC'],
    },
'fram':
    {
        'ACDELCO': ['AC-DELCO'],
        'LUBERFINER': ['LUBER-FINER'],
    },
'hastings':
    {
        'BALDWIN': ['BALDWIN FILTERS'],
        'NAPA': ['NAPA GOLD'],
        'LUBERFINER': ['LUBER-FINER'],
    },
'john deere':
    {
        'ACDELCO': ['AC'],
        'BALDWIN': ['Baldwin'],
        'CARQUEST': ['Carquest'],
        'DONALDSON': ['Donaldson'],
        'FLEETGUARD': ['Fleetguard'],
        'FRAM': ['Fram'],
        'HASTINGS': ['Hastings'],
        'LUBERFINER': ['Luberfiner (Champion)'],
        'MOBIL': ['Mobile'],
        'PUROLATOR': ['Purolator'],
        'VALVOLINE': ['Valvoline'],
    },
'luberfiner':
    {
        'ACDELCO': ['AC'],
        'NAPA': ['NAPA GOLD', 'NAPA PROSELECT'],
        'CARQUEST': ['CARQUEST', 'CARQUEST PREMIUM']
    },
'mobil':
    {
        'ACDELCO': ['AC'],
        'NAPA': ['NAPA', 'NAPA GOLD'],
        'LUBERFINER': ['LUBER-FINER'],
    },
'napa':
    {
        'ACDELCO': ['AC DELCO'],
        'HASTINGS': ['HASTINGS FILTERS'],
        'WIX': ['WIX', 'WIX XP'],
        'CARQUEST': ['CARQUEST', 'CARQUEST RED'],
        'LUBERFINER': ['LUBER-FINER', 'LUBERFINER'],
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
        'LUBERFINER': ['LUBER-FINER'],
    },
'valvoline filters':
    {
        'ACDELCO': ['AC-DELCO'],
        'NAPA': ['NAPA', 'NAPA GOLD'],
    },
'valvoline':
    {
        'ACDELCO': ['AC-DELCO'],
        'NAPA': ['NAPA', 'NAPA GOLD'],
    },
'wix':
    {
    'ACDELCO': ['AC DELCO'],
    'HASTINGS': ['HASTINGS FILTERS'],
    'NAPA': ['NAPA', 'NAPA GOLD', 'NAPA PROSELECT'],
    'CARQUEST': ['CARQUEST', 'CARQUEST RED'],
    }
}


def trycmd(cmd):
    """execute <cmd> and assert it was successful"""
    if not isinstance(cmd, list):
        cmd = shlex.split(cmd)
    retc = subprocess.call(cmd)
    assert retc == 0, '%s failed with retc: %s' % (' '.join(cmd), retc)


def add_request(filter_number, brand):
    """add <brand> <filternumber> to requests table"""
    with dbcursor() as cursor:
        _addrequest(filternumber, brand, cursor)
        

def _addrequest(filter_number, brand, cursor):
    """helper to add requests"""
    insert = "insert into requests(brand, filter) values('%s', '%s')"
    insert = insert % (brand, filter_number)
    cursor.execute(insert)


def add_filter(keyid, brand, filternumber):
    """add <brand>, <filternumber> to matches table"""
    with dbcursor() as cursor:
        add = "insert into matches(id, brand, filter) " \
              "values(%s, '%s', '%s')" % (keyid, brand, filternumber)
        cursor.execute(add)


def insert_new_filter(brand, filternumber, db, cursor):
    """insert <brand> <filternumber> into filters table"""
    new_insert = "insert into filters(brand, filter) " \
                 "values('%s', '%s')" % (brand, filternumber)
    cursor.execute(new_insert)
    return db.insert_id()


def get(url, cookies=None, fatal=False):
    """retrieve <url> conents, adding <cookies> if needed"""
    if cookies:
        cookies = dict(cookies_are=cookies)

    if not url.startswith('http://'):
        url = 'http://' + url
    try:
        page = requests.get(url, cookies=cookies)
        return page.text
    except requests.ConnectionError as e:
        print 'Exception trying to access %s:' % url
        if fatal:
            print traceback.format_exc()
            raise
        return None
    except requests.HTTPError as e:
        print 'debug HTTPError: %s'
        print traceback.format_exc()
        if fatal:
            raise
    


def post(url, cookies=None, data=dict, headers={}):
    """post <data> to <url>, adding <cookies> if needed. Returns
    http response code."""
    resp = requests.post(url, cookies=cookies, data=data, headers=headers)
    return resp


def substring(regex_pat, string):
    """returns substring matched by <regex_pat> in string"""
    match = re.search(regex_pat, string)
    return match.group(0) if match else ''


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

def replace(regex, replacement, string):
    """replace <regex> with <replacement> in <string>"""
    return re.sub(regex, replacement, string)



