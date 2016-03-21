from bs4 import BeautifulSoup
from crossfilter.common.util import get, format_brand


# carquest website no longer active
def getFilter(filterNumber, brand, full=False):
    return ''

# def getFilter(filterNumber, brand, full=False):
#     brand_names, filterNumber = format_brand('carquest',
#                                              brand,
#                                              filterNumber)
#     address = 'http://www.cficonnect.com/filterlookup/results.asp?ExactMatch=0&PartNo1=%s&MakerCode1='
#     address = address % filterNumber

#     content = get(address)
#     if not content:
#         return ''
#     soup = BeautifulSoup(content, 'html.parser')

#     table_cells = soup.find_all("td", class_='bluemedium')
#     cqs = set()

#     def add_filter(row):
#         ref = row.find('a')
#         value = ref.getText().strip(' \n')
#         cqs.add(value)

#     for table_cell in table_cells:
#         row = table_cell.parent
#         cells = row.find_all('td')
#         match_number = cells[0].getText().strip()
#         match_brand = cells[1].getText().strip()
#         carquest_number = cells[3].getText().strip()

#         string = row.getText().strip(' \n')
#         if full:
#             print ', '.join([cell.getText().strip() for cell in cells])

#         if match_number == filterNumber and match_brand in brand_names:
#             cqs.add(carquest_number)
            
#     return ','.join(cqs).strip()


    # address = 'http://www.oilfilter-crossreference.com/convert/%s/%s' % (brand_names[0], filterNumber)
    # # print address
    # content = get(address)
    # soup = BeautifulSoup(content, 'html.parser')
    # # print soup.prettify()
    # result_table = soup.find(class_='left_details')
    # results = result_table.find_all('ul')
    # for result in results:
    #     print result.getText()