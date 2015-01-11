from bs4 import BeautifulSoup
from crossfilter.common.util import get, format_brand


def getFilter(filterNumber, brand, full=False):
    brand_names, filterNumber = format_brand('napa',
                                             brand,
                                             filterNumber)
    address = 'http://www.nfhconnect.com/lookup/results.asp?PartNo=%s&Submit=Search'
    address = address % filterNumber

    content = get(address)
    soup = BeautifulSoup(content)

    table_cells = soup.find_all("td", class_='blackmedium', valign='top')
    napas = set()
    for table_cell in table_cells:
        row = table_cell.parent
        cells = row.find_all('td')
        match_number = cells[1].getText().strip()
        match_brand = cells[2].getText().strip()
        napa_number = cells[3].getText().strip()

        if full:
            print ', '.join([cell.getText().strip() for cell in cells])

        if match_number == filterNumber and match_brand in brand_names:
            napas.add(napa_number)

    return ','.join(napas)
