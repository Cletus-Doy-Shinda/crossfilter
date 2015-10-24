from bs4 import BeautifulSoup
import re
from crossfilter.common.util import get, post, format_brand

name2id = {
    'BALDWIN': 136,
    'CARQUEST': 253,
    'DONALDSON': 2016,
    'FLEETGUARD': 2097,
    'FRAM': 489,
    'HASTINGS': 553,
    'JOHN DEERE': 2251,
    'LUBERFINER': 2320,
    'MOBIL': 785,
    'MOBIL1': 4583,
    'NAPA': 821,
    'PUROLATOR': 995,
    'SERVICE CHAMP': 1697,
    'VALVOLINE': 2704,
    'WIX': 1312,
}


def isoilfilter(string):
    if 'Engine Oil Filter' in string:
        return True
    if 'FILTER,OIL' in string:
        return True
    return False


def getFilter(filterNumber, brand, full=False):
    brand_names, filterNumber = format_brand('acdelco',
                                             brand,
                                             filterNumber)
    address = 'http://parts-catalog.acdelco.com/catalog/interchange.php'
    catid = name2id.get(brand.upper(), None)
    if not catid:
        return ''
    data = {
        'interchange_part': filterNumber,
        'prev_interchange_part': filterNumber,
        'prev_catalogid': '',
        'catalogid': catid,
        'prev_parttypeid': 2614,
        'parttypeid': 2614,
        'prev_applicationid': '',
        'applicationid': 5559,
    }
    resp = post(address, data=data)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text)
    else:
        return ''

    matches = set()
    results = soup.find_all(class_='nxp_item_view')
    if not results:
        return ''
    for result in results:
        table = result.find('table')
        for row in table.find_all('tr'):
            tds = row.find_all('td')
            ftype = tds[2].find(class_='partname').getText()
            data = tds[2].getText().strip()
            lines = data.split('\n')
            if full:
                print lines[1]
            if isoilfilter(ftype):
                pn = lines[1].strip()
                pn = pn.replace(u'\xa0', ' ')
                val = re.sub(r'Part Number:\s+', '', pn)
                matches.add(val)

    return ','.join(matches)
