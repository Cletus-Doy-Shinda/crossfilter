"""downloadfilters.py - Finds all matches to a given Oil Filter part number
for a particular Brand"""


import sys
import acdelco, baldwin, carquest, donaldson
import napa, fram, wix, purolator, servicechamp, johndeere
import fleetguard, hastings, mobil

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
                      ('mobil', mobil.getFilter)
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
