import crossfilter.scripts.servicechamp

# This page can be modified and used to find other filter brands such as:
# Warner
# Mobile
# Mobile 1
# MileGuard


def getFilter(filterNumber, brand, full=False):
    return crossfilter.scripts.servicechamp.getFilter(filterNumber, brand,
        full=full, supplier_name='MOBIL 1')
