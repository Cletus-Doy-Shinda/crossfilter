import MySQLdb
import crossfilter.scripts.downloadfilters as df

from crossfilter.common.secure import get_mysql_credentials


user, passwd = get_mysql_credentials()
db = MySQLdb.connect(host='localhost', user=user, passwd=passwd, db='filters')
cursor = db.cursor()



def check_names_new_to_old(newbrand):
    """For every brand, test naming conventions for the
    new brand being added"""
    newbrand_filter_nums = set()
    query = 'select distinct brand from filters'
    cursor.execute(query)
    rows = cursor.fetchall()
    func = __import__(newbrand.strip())
    legit = {}

    def check_matches(brand, start, end):
        """prints the full output for <brand>"""
        legit[brand] = False
        print '============================================='
        print 'Checking %s matches for %s' % (newbrand, brand)
        print '============================================='
        query = "select filter from matches where brand = '%s' limit %s, %s" \
            % (brand, start, end)
        cursor.execute(query)
        match_rows = cursor.fetchall()
        for match_row in match_rows:
            filter_num = match_row[0]
            print '\tFull output for %s %s:' % (brand, filter_num)
            matched = func.getFilter(filter_num, brand, full=True)
            if matched:
                newbrand_filter_nums.add(matched)
                legit[brand] = True
                print '\tmatches: %s' % matched
                break
        print '\n\n\n'

    for row in rows:
        brand = row[0]
        check_matches(brand, 0, 1)

    found = {k: v for (k, v) in legit.items() if v}
    missing = {k: v for (k, v) in legit.items() if not v}
    if missing:
        print '\nstill having missing filters:'
        print ', '.join([k for k in missing.keys()])
        print 'trying again with larger range\n'
        for mis in missing.keys():
            check_matches(mis, 2, 3)

    found = {k: v for (k, v) in legit.items() if v}
    missing = {k: v for (k, v) in legit.items() if not v}
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Summary'.rjust(20)
    print 'Found'
    print '-----'
    for key, val in found.items():
        print ('%s' % key).ljust(20) + '%s' % val
    print '\nMissing'
    print '--------'
    for key, val in missing.items():
        print ('%s' % key).ljust(20) + '%s' % val

    return newbrand_filter_nums


def check_names_old_to_new(new_matches, brand):
    for string in new_matches:
        filter_nums = string.split(',')
        for filter_num in filter_nums:
            print '============================================='
            print 'Checking matches for %s %s' % (brand, filter_num)
            print '============================================='
            for name, func in df.RETRIEVE_FUNCTIONS:
                if name == brand.lower():
                    continue
                print '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                print '\tDebug output for %s:' % name
                matches = func(filter_num, brand, full=True)
                if matches:
                    print '\tmatches for %s: %s' % (name, matches)
            print '\n\n\n'


# new_brand = 'luberfiner'
# # new_matches = check_names_new_to_old(new_brand)
# new_matches = set()
# new_matches.add('PH2840')
# new_matches.add('PH47')
# new_matches.add('LFP4005')
# check_names_old_to_new(new_matches, new_brand)
