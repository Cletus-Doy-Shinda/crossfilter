"""downloadfilters.py - Finds all matches to a given Oil Filter part number
for a particular Brand"""


import sys
from threading import Thread

import crossfilter.scripts.acdelco as acdelco
import crossfilter.scripts.baldwin as baldwin
import crossfilter.scripts.carquest as carquest
import crossfilter.scripts.donaldson as donaldson
import crossfilter.scripts.napa as napa
import crossfilter.scripts.fram as fram
import crossfilter.scripts.wix as wix
import crossfilter.scripts.purolator as purolator
import crossfilter.scripts.servicechamp as servicechamp
import crossfilter.scripts.johndeere as johndeere
import crossfilter.scripts.fleetguard as fleetguard
import crossfilter.scripts.hastings as hastings
import crossfilter.scripts.mobil as mobil
import crossfilter.scripts.valvoline as valvoline
import crossfilter.scripts.luberfiner as luberfiner

from crossfilter.common.util import INSERT_SQL_FILE
from crossfilter.common.contexts import dbcursor


RETRIEVE_FUNCTIONS = [('acdelco', acdelco.getFilter),
                      ('baldwin', baldwin.getFilter),
                      ('carquest', carquest.getFilter),
                      ('service champ', servicechamp.getFilter),
                      ('donaldson', donaldson.getFilter),
                      ('napa', napa.getFilter),
                      ('fram', fram.getFilter),
                      ('wix', wix.getFilter),
                      ('purolator', purolator.getFilter),
                      ('john deere', johndeere.getFilter),
                      ('fleetguard', fleetguard.getFilter),
                      ('hastings', hastings.getFilter),
                      ('mobil', mobil.getFilter),
                      ('valvoline', valvoline.getFilter),
                      ('luberfiner', luberfiner.getFilter),
                      ]
INSERT_STMT = "insert into matches values(%s, '%s', '%s');\n"


def async_retrieve(func, filternumber, brand, name, ID, results):
    """Called in a thread to download all matching filters for
    a specific <brand>"""
    result = func(filternumber, brand)
    if result:
        filters = result.split(',')
        for f in filters:
            stmt = INSERT_STMT % (ID, name, f)
            results.append(stmt)


def _retrieve(filternumber, brand, ID, cursor):
    """Helper to retrieve all matches for <brand> <filternumber>.
    <cursor> is database cursor"""
    results = []
    tp = []

    for name, func in RETRIEVE_FUNCTIONS:
        t = Thread(target=async_retrieve, name=name,
                   args=[func, filternumber, brand, name, ID, results])
        tp.append(t)
        t.start()

    for t in tp:
        t.join(30.0 * 60)  # 30 minutes
        if t.isAlive():
            print 'Thread %s is still going after 30 minutes' % t.name

    with open(INSERT_SQL_FILE, 'a') as out:
        for r in results:
            try:
                cursor.execute(r)
                out.write(r)
            except Exception as e:
                out.write('Exception executing "%s": %s' % (r, str(e)))


def retrieve(filternumber, brand, ID):
    """Retrieve all matches for <brand> <filternumber>"""
    with dbcursor() as cursor:
        _retrieve(filternumber, brand, ID, cursor)


if __name__ == "__main__":
    retrieve(sys.argv[1], sys.argv[2], sys.argv[3])
