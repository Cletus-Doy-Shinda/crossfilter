import sys
from crossfilter.scripts.downloadfilters import RETRIEVE_FUNCTIONS


SQL_LOG_FILE = '/tmp/braxas_insert.sql'

def retrieve(filternumber, brand, dbid):
    """find all matches for <filternumber>"""
    insert_stmt = "insert into matches values(%s, '%s', '%s');\n"

    with open(SQL_LOG_FILE, 'a') as out:
        for name, func in RETRIEVE_FUNCTIONS:
            if brand != name:
                results = func(filternumber, brand.upper())
                if results:
                    filters = results.split(',')
                    for _filter in filters:
                        _filter = _filter.strip()
                        try:
                            out.write(insert_stmt % (dbid, name, _filter))
                        except Exception:
                            out.write('Exception for %s, %s, %s' \
                                      % (dbid, name, _filter))
                            continue


if __name__ == "__main__":
    retrieve(sys.argv[1], sys.argv[2], sys.argv[3])
