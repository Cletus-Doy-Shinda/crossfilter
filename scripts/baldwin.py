from bs4 import BeautifulSoup
from crossfilter.common.util import get, format_brand, replace


def getFilter(filterNumber, brand, full=False):
    brand_names, filterNumber = format_brand('baldwin',
                                             brand,
                                             filterNumber)
    address = "http://catalog.baldwinfilter.com/BaldwinDisplay.asp?URL=BaldwinOEM.asp&partnumber=%s=&optiontype=OEM"
    address = address % filterNumber
    
    content = get(address)
    soup = BeautifulSoup(content)
    
    rows = soup.find_all("tr", class_="tblrow")
    bws = set()

    for row in rows:
        cells = row.find_all('td')
        comp_number = cells[0].getText().strip()
        comp_brand = cells[1].getText().strip()
        baldwin_filter = cells[2].getText().strip()
        if full:
            print ', '.join([cell.getText().strip() for cell in cells])

        if comp_brand in brand_names and comp_number == filterNumber:
            bws.add(replace(r'\[[0-9]+\] ', '', baldwin_filter))

    return ','.join(bws)
