from bs4 import BeautifulSoup
from crossfilter.common.util import get, format_brand


def getFilter(filterNumber, brand, full=False):
    brand_names, filterNumber = format_brand('wix',
                                             brand,
                                             filterNumber)
    address = 'http://www.wixfilters.com/Lookup/Exactmatch.aspx?PartNo=%s'
    address = address % filterNumber

    content = get(address)
    soup = BeautifulSoup(content, 'html.parser')

    rows = soup.find_all(bgcolor='#FFFBD6')
    rows = soup.find_all(bgcolor='White') + rows
    wixs = set()
    for row in rows:
        cells = row.find_all('td')
        if full:
            print ', '.join([cell.getText().strip() for cell in cells])

        comp_brand = cells[2].get_text().strip()
        comp_number = cells[1].getText().strip()
        comp_number = comp_number.replace(' Superseded by', '')
        wix_number = cells[4].getText().strip()

        if comp_brand in brand_names and comp_number == filterNumber:
            wixs.add(wix_number)

    return ','.join(wixs)
