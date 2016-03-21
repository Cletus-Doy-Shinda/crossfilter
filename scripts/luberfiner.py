from bs4 import BeautifulSoup
from crossfilter.common.util import get, post, format_brand

# def getFilter(filter_number, brand, full=False):
#     brand_names, filter_number = format_brand('luberfiner',
#                                              brand,
#                                              filter_number)
#     address = 'http://www.luberfiner.com/catalog/CrossReference.aspx'
#     data = {'compno': filter_number,
#             'partkey': ''}

#     resp = post(address, data=data)
#     if resp.status_code != 200:
#         print 'Exception post to %s: status_code: %s' \
#               % (address, resp.status_code)

#     soup = BeautifulSoup(resp.text, 'html.parser')
#     table = soup.find(class_='showmetheparts_grid')
#     if not table:
#         return ''
#     rows = table.find_all('tr', class_='showmetheparts_view_gridrow')
#     rows += table.find_all('tr', class_='showmetheparts_view_gridrow_alt')
#     luberfiners = set()
#     for row in rows:
#         tds = row.find_all('td')
#         if tds:
#             luber_no = tds[0].getText()
#             filter_type = tds[1].getText()
#             compbrand = tds[2].getText()
#             compno = tds[3].getText()
#             # print compno
#             # print filter_number
#             # print compbrand
#             # print brand_names
#             if full:
#                 print luber_no, filter_type, compbrand, compno
#             if compno == filter_number and compbrand in brand_names:
#                 if 'Engine Oil' in filter_type:
#                     luberfiners.add(luber_no)

#     return ','.join(luberfiners)


def getFilter(filter_number, brand, full=False):
    brand_names, filter_number = format_brand('luberfiner',
                                             brand,
                                             filter_number)

    address = 'http://productguide.luber-finer.com/Home/PartInterchanges' \
              '?strForSearch=%s' % filter_number
    content = get(address)
    soup = BeautifulSoup(content, 'html.parser')

    luberfiners = set()
    table = soup.find(class_='display responsive')
    if not table:
        return ''

    rows = table.find('tbody').find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        matchnum = tds[1].getText()
        manufacturer = tds[2].getText()
        partnum = tds[3].getText().strip()
        if full:
            print matchnum, manufacturer, partnum
        if manufacturer in brand_names:
            luberfiners.add(partnum)

    return ','.join(luberfiners)
