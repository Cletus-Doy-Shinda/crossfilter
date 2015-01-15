from bs4 import BeautifulSoup
from crossfilter.common.util import get, format_brand


def getFilter(filternumber, brand, full=False):
    brand_names, filternumber = format_brand('hastings',
                                             brand,
                                             filternumber)
    filternumber = filternumber.upper().replace('-', '')
    address = 'http://catalog.hastingsfilter.com/BaldwinDisplay.asp?' \
              'partnumber=%s&optiontype=OEM' % filternumber
    content = get(address)
    if not content:
        return ''
    
    soup = BeautifulSoup(content)
    hastings = set()

    form = soup.find(id='BaldwinDisplay')
    if form:
        rows = form.find_all('tr', class_='tblrow')
        if rows:
            for row in rows:
                cells = row.find_all('td')
                comp_number = cells[0].getText()
                comp_brand = cells[1].getText()
                hastings_filter = cells[2].find('a').getText().strip()
                if full:
                    print ', '.join([cell.getText().strip() for cell in cells])
                if comp_brand in brand_names and comp_number == filternumber:
                    hastings_filter = hastings_filter.replace('**', '')
                    hastings.add(hastings_filter)

    return ','.join(hastings).strip()
