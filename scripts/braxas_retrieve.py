import sys
import acdelco, baldwin, carquest, donaldson
import napa, fram, wix, purolator, servicechamp, johndeere
import fleetguard, hastings, mobil

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

SQL_LOG_FILE = '/tmp/braxas_insert.sql'

def retrieve(filterNumber, brand, ID, remote=False):
    """find all matches for <filterNumber>"""
    insert_stmt = "insert into matches values(%s, '%s', '%s');\n"

    with open(SQL_LOG_FILE, 'a') as out:
        for name, func in RETRIEVE_FUNCTIONS:
            if brand != name:
                filterString = func(filterNumber, brand.upper())
                if filterString:
                    filters = filterString.split(',')
                    for f in filters:
                        f = f.strip()
                        try:
                            out.write(insert_stmt % (ID, name, f))
                        except Exception:
                            out.write('Exception for %s, %s, %s' % (ID, name, f))
                            continue


if __name__ == "__main__":
    retrieve(sys.argv[1], sys.argv[2], sys.argv[3])
