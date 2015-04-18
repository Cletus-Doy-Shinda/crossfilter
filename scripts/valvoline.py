import servicechamp


def getFilter(filterNumber, brand, full=False):
    return servicechamp.getFilter(filterNumber, brand,
        full=full, supplier_name='VALVOLINE FILTERS', idval='69876V2')
