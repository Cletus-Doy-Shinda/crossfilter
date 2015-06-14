import xml.etree.ElementTree as ET

from crossfilter.common.util import get, format_brand


def getFilter(filternumber, brand, full=False):
    brand_names, filternumber = format_brand('fleetguard',
                                             brand,
                                             filternumber)
    address = 'http://catalog.cumminsfiltration.com/catalog/partsearch.do?req' \
              'Cmd=PartSearchResults&reqParts=%s' % filternumber
    cookies = 'FGD_CAT_REGION=FGUSA; WT_FPC=id=291462474b1e54dafe214033296083' \
              '83:lv=1403329616056:ss=1403329608383; __utma=66188348.14355021' \
              '74.1403326008.1403326008.1403326008.1; __utma=237773458.546691' \
              '331.1403368934.1403368934.1403580519.2; JSESSIONID=0000QkmygT6' \
              'BCTW9574NR7z4sZB:158pq8bk5'
    
    content = get(address, cookies=cookies)
    if not content:
        return ''
    
    tree = ET.fromstring(content)
    if tree is None:  # Can't do 'if not tree' - according to ET advisement
        return ''

    matches = set()

    for elem in tree.getiterator():
        if elem.tag == 'Manufacturer':
            mfs = elem.find('Name').text
            if mfs is None:
                return ''
            fleetguard = elem.find('Fleetguard-PartNumber')
            fleetguard_match = fleetguard.find('Name').text
            desc = fleetguard.find('Description').text
            if full:
                print mfs, fleetguard_match
            if mfs.upper() in brand_names and 'Lube' in desc:
                matches.add(fleetguard_match)

    return ','.join(matches)
