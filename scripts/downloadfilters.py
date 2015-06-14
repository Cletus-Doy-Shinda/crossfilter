"""downloadfilters.py - Finds all matches to a given Oil Filter part number
for a particular Brand"""


import sys
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


def _retrieve(filternumber, brand, ID, cursor):
    """Helper to retrieve all matches for <brand> <filternumber>.
    <cursor> is database cursor"""
    insert_stmt = "insert into matches values(%s, '%s', '%s');\n"

    with open(INSERT_SQL_FILE,'a') as out:
        for name, func in RETRIEVE_FUNCTIONS:
            if brand != name:
                filterString = func(filternumber, brand.upper())
                if filterString:
                    filters = filterString.split(',')
                    for f in filters:
                        f = f.strip()
                        try:
                            cursor.execute(insert_stmt % (ID, name, f))
                            out.write(insert_stmt % (ID, name, f))
                        except Exception:
                            out.write('Exception for %s, %s, %s\n' % (ID, name, f))
                            continue


def retrieve(filternumber, brand, ID):
    """Retrieve all matches for <brand> <filternumber>"""
    with dbcursor() as cursor:
        _retrieve(filternumber, brand, ID, cursor)


if __name__ == "__main__":
    retrieve(sys.argv[1], sys.argv[2], sys.argv[3])
