import xml.etree.ElementTree as ET

from crossfilter.common.util import get, format_brand

# This page can be modified and used to find other filter brands such as:
# Warner
# Mobile
# Mobile 1
# MileGuard
# Valvoline


def getFilter(filterNumber, brand, full=False, supplier_name='SERVICE CHAMP',
              idval=98757):
    brand_names, filterNumber = format_brand(supplier_name,
                                             brand,
                                             filterNumber)
    address = 'http://www.showmetheparts.com/bin/ShowMeConnect.exe?lookup=' \
              'complist&compno=%s&id=%s&storeid=&userid=' % (filterNumber, idval)

    content = get(address)
    tree = ET.fromstring(content)

    def match(mfg, supplier, mfg_number, part_type):
        if not part_type or not supplier:
            return False
        if supplier.upper() == supplier_name and mfg_number.upper() == filterNumber:
            if mfg.upper() in brand_names and 'Engine Oil' in part_type:
                return True
        return False

    champs = set()

    for result in tree.findall('interchangedata'):
        _mfg = result.find('mfg').text
        _supplier = result.find('supplier').text
        mfg_number = result.find('comp_no').text
        part_type = result.find('part_type').text
        if full:
            print _mfg, _supplier, mfg_number, part_type
        if match(_mfg, _supplier, mfg_number, part_type):
            champ_number = result.find('part_no').text
            champs.add(champ_number)

    return ','.join(champs)
