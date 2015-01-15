from bs4 import BeautifulSoup
from crossfilter.common.util import get, format_brand


def getFilter(filterNumber, brand, full=False):
    brand_names, filterNumber = format_brand('fram',
                                             brand,
                                             filterNumber)
    address = "http://www.framcatalog.com/Competitor.aspx?b=F&pn=%s&em=True" % filterNumber

    content = get(address)
    if not content:
        return ''
    soup = BeautifulSoup(content)

    table = soup.find(id="G_ctl00xContentPlaceHolder1xUltraWebGrid1")
    frams = set()
    curr_brand = None
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if full:
                print ', '.join([cell.getText().strip() for cell in cells])
            if len(cells) == 3:
                comp_brand = cells[0].get_text().rstrip()
                curr_brand = comp_brand
                comp_number = cells[1].getText().strip()
                fram_brand = cells[2].find('a').getText().strip()
            else:
                comp_brand = curr_brand
                comp_number = cells[0].getText().strip()
                fram_brand = cells[1].find('a').getText().strip()
            if comp_brand in brand_names and comp_number == filterNumber:
                frams.add(fram_brand)

    return ','.join(frams)
