from bs4 import BeautifulSoup
from crossfilter.common.util import get, format_brand


def getFilter(filterNumber, brand, full=False):
    brand_names, filterNumber = format_brand('napa',
                                             brand,
                                             filterNumber)

    new_address = 'http://www.nfhconnect.com/Lookup/QuickSearch?q=%s'
    new_address = new_address % filterNumber

    content = get(new_address)
    soup = BeautifulSoup(content)

    napas = set()
    table = soup.find(class_='results-table partial table1')
    rows = table.find_all(class_='white-row')
    rows += table.find_all(class_='grey-row')
    for row in rows:
        compno = row.find(class_='col1').getText()
        compno = compno.replace(' Superseded by', '')
        compbrand = row.find(class_='col2').getText()
        napano = row.find(class_='col4')
        if not napano:
            continue
        else:
            napano = napano.getText().strip()
        if full:
            print compbrand, compno, napano
        if compno == filterNumber and compbrand in brand_names:
            napas.add(napano)

    return ','.join(napas)