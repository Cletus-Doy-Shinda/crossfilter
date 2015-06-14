import crossfilter.scripts.servicechamp


def getFilter(filterNumber, brand, full=False):
    matches = crossfilter.scripts.servicechamp.getFilter(filterNumber, brand,
        full=full, supplier_name='VALVOLINE FILTERS', idval='69876V2')
    return matches.replace('-', '')
