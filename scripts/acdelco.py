from bs4 import BeautifulSoup
from crossfilter.common.util import get, format_brand


def getFilter(filterNumber, brand, full=False):
    brand_names, filterNumber = format_brand('acdelco',
                                             brand,
                                             filterNumber)
    address = 'http://webcaps.ecomm.gm.com/canada/VehicleCompetitiveCrossRefPartDescription.jsp?autosel=A&part=%s&manfid=%s'
    address = address % (filterNumber, brand_names[0])

    content = get(address)
    soup = BeautifulSoup(content)

    rows = soup.find_all(attrs={'name':'part'})
    s = set()
    for row in rows:
        tr = row.parent.parent
        tds = tr.find_all('td')
        ac_filter = tds[2].getText().strip()
        filter_type = tds[3].getText().strip()

        if full:
            print ', '.join([td.getText().strip() for td in tds])

        if filter_type == 'FILTER,OIL':
            s.add(ac_filter)

    return ','.join(s)
