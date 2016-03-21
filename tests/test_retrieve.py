"""test_retrieve.py - Unit test for getting matches for filters.
Checks the filters in the database match those returned by each
brand's website
"""


import random

from collections import defaultdict
from crossfilter.common.contexts import dbcursor
from crossfilter.common.util import BRANDS, add_filter


MODULE_DIR = 'crossfilter.scripts.%s'


def test_retrieve():
    """test retrieve functionality of brand websites"""
    with dbcursor() as cursor:

        for brnd in BRANDS:
            desc = 'check db filters for %s match those returned by website' \
                % brnd
            check_brand.description = desc
            yield check_brand, brnd, cursor


def check_brand(brnd, cursor):
    """check db filters for <brnd> match those returned by website"""
    db_filters = defaultdict(list)
    mismatches = []

    # find the max number of entries for brnd
    query = "select count(*) from filters " \
            "where brand = '%s'" % brnd
    cursor.execute(query)
    max_count = cursor.fetchall()[0][0]
    
    # choose random number betwen 0 and max_count
    rand_num = random.randint(1, int(max_count))
    query = "select id, filter from filters where brand = '%s' " \
            "order by id limit %s, %s" % (brnd, rand_num, rand_num + 1)
    cursor.execute(query)
    rows = cursor.fetchall()
    idnum, filternumber = rows[0]

    # get all the matches for said filter with idnum
    query = "select brand, filter from matches where id = %s" % idnum
    cursor.execute(query)
    rows = cursor.fetchall()

    # add all filters to list with brand as key in a dict
    for brand, filter_number in rows:
        brand = brand.lower().strip().replace(' ', '')
        db_filters[brand].append(filter_number)

    # now compare those values with what the website reports
    for key, value in db_filters.items():
        if key in ['carquest', 'purolator']:
            continue
        module_name = MODULE_DIR % key
        module = __import__(module_name, fromlist=['crossfilter.scripts'])
        results = module.getFilter(filternumber, brnd)
        results = results.split(',')
        
        # assert the filters are the same
        webset = set(results)
        dbset = set(value)
        if dbset != webset:
            # if the web reports more filters than we have in the db,
            # add those filters
            if len(results) > len(value):
                diff = webset - dbset
                mismatches.append('found more webfilters in %s for %s %s: %s' \
                    % (key, brnd, filternumber, ','.join(diff)))
                for diff_filter in diff:
                    add_filter(idnum, key, diff_filter)
            else:
                msg = 'mismatch in %s for %s %s:\ndb: %s\nweb: %s' % \
                    (key, brnd, filternumber, sorted(value), sorted(results))
                mismatches.append(msg)


    assert not mismatches, '\n'.join(mismatches)
