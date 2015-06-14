"""contexts.py - Custom contexts that are often used"""


import MySQLdb

from contextlib import contextmanager
from crossfilter.common.secure import get_mysql_credentials


@contextmanager
def dbcursor():
    """Cursor to MySQL Database 'Filters'"""
    user, passwd = get_mysql_credentials()
    db = MySQLdb.connect(host='localhost', user=user,
                         passwd=passwd, db='filters')
    cursor = db.cursor()
    yield cursor
    db.commit()
    db.close()
