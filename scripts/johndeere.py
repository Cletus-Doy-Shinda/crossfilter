import urllib2
from crossfilter.common.util import format_brand
from bs4 import BeautifulSoup


def getFilter(filter_number, brand, full=False):
    brand_names, filter_number = format_brand('john deere',
                                              brand,
                                              filter_number)

    address = 'https://jdparts.deere.com/servlet/com.deere.u90.jdparts.view.servlets.searchcontroller.PartNumberSearch'
    form_data = 'userAction=exactSearch&browse=&screenName=partSearch&priceIdx=1&searchAppType=&searchType=exactSearch&partSearchNumber=%s&pageIndex=1&endPageIndex=1' % filter_number

    page = urllib2.urlopen(address, data=form_data)
    soup = BeautifulSoup(page, 'html.parser')

    form = soup.find(attrs={'name':'partsearch'})
    if not form:
        return ''
    tables = form.find_all('table')

    table = tables[4]
    rows = table.find_all('tr')
    filters = set()
    for row in rows[2:]:
        cells = row.getText().split('\n')
        cells = [x for x in cells if x]
        _brand = cells[1]
        _filter = cells[0]
        fType = cells[4]
        match_filter = cells[2]
        if full:
            print _brand, _filter, fType, match_filter
        if _brand in brand_names and filter_number == _filter.upper() and fType == 'Oil Filter':
            filters.add(match_filter)

    return ','.join(filters)
