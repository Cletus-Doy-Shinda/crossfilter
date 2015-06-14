from bs4 import BeautifulSoup
from crossfilter.common.util import get, format_brand


def getFilter(filternumber, brand, full=False):
    brand_names, filternumber = format_brand('purolator',
                                             brand,
                                             filternumber)
    address = 'http://ca-en.purolatorautofilters.net/enen/ca/resources/Pages' \
              '/InterchangeGuideResults.aspx?partnr=%s&page=1' % filternumber
    content = get(address)
    soup = BeautifulSoup(content)

    table = soup.find(id='results')
    if not table:
        return ''

    def format_string(string):
        s = string.strip(' Availability limited to existing inventory.')
        s = s.strip(' May not be a direct cross - check applications catalog.')
        return s

    rows = table.find_all('tr')
    purolators = set()
    for row in rows:
        cells = row.find_all(class_='interchangeguidecolumn')
        if cells:
            _brand = cells[0].getText()
            _number = cells[1].getText().replace('-', '')
            purolator_match = cells[2].getText()
            fType = cells[3].getText()
            if full:
                print _brand, _number, purolator_match, fType
            if _brand in brand_names and fType.lower() == 'oil' \
                and _number.upper() == filternumber.upper():
                purolators.add(format_string(purolator_match))
    return ','.join(purolators)
