# from bs4 import BeautifulSoup


import valvoline
from crossfilter.common.contexts import dbcursor
from crossfilter.common.util import get, substring, _addrequest


with dbcursor() as cursor:
    query = "select filter from matches where brand = 'john deere' limit 30, 5`0"
    cursor.execute(query)
    rows = cursor.fetchall()
    for jd in rows:
        print 'trying %s' % jd[0]
        print valvoline.getFilter(jd[0], 'john deere', full=True)


