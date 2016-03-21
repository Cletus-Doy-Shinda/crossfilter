from bs4 import BeautifulSoup
from crossfilter.common.util import get, post, format_brand

address = 'http://www.catfiltercrossreference.com'

def getFilter(filterNumber, brand, full=False):
    brand_names, filterNumber = format_brand('caterpillar',
                                             brand,
                                             filterNumber)
    address = 'http://www.catfiltercrossreference.com/search.aspx'
    data = {'ctl00$MainContent$searchKey': filterNumber,
            'ctl00$MainContent$btnSearch2': 'Search'}

    content = get(address)
    soup = BeautifulSoup(content, 'html.parser')

    viewstate = soup.find(id='__VIEWSTATE')
    viewstate = viewstate['value']
    data['__VIEWSTATE'] = viewstate

    validate = soup.find(id='__EVENTVALIDATION')
    validate = validate['value']
    data['__EVENTVALIDATION'] = validate
    
    resp = post(address, data=data)
    if resp.status_code != 200:
        print 'Exception posting to %s: status code: %s' \
              % (address, resp.status_code)
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    results = soup.find_all(class_='search-result')
    cats = set()

    for result in results:
        comp_info = result.find(class_='search-result-part search-result-query-part')
        comp_part_num = comp_info.find(class_='search-result-part-number')

        # Hack to remove 'Part # ' at beginning of the text
        # because the second space is a unicode &nbsp
        comp_part_num = comp_part_num.getText().split(u'\xa0')[1]

        comp_part_info = comp_info.find(class_='search-result-part-type')
        comp_part_info = comp_part_info.getText()
        comp_brand = comp_part_info.split(u'\xa0')[0]
        filter_type = comp_part_info.split(u'\xa0')[1]

        if comp_part_num == filterNumber and comp_brand in brand_names:
            cat_filters = result.find_all(class_='search-result-part-number')
            for cat in cat_filters[1:]:
                cats.add(cat.getText().split(u'\xa0')[1])

    return ','.join(cats)
