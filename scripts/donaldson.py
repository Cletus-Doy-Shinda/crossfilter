from bs4 import BeautifulSoup
from crossfilter.common.util import get, format_brand


def getFilter(filterNumber, brand, full=False):
    brand_names, filterNumber = format_brand('donaldson',
                                             brand,
                                             filterNumber)
	address = 'http://www.michelecaroli.com/filter_cross_reference.asp?tpr=S2&f1=%s'
	address = address % filterNumber

	content = get(address)
	soup = BeautifulSoup(content)

	form = soup.find(id='forminvio')
	donaldsons = set()
	if form:
		rows = form.find_all('tr')
		for idx, row in enumerate(rows):
			cells = row.find_all('td')
			if full:
				if idx in [0, 1, 2, 4]:
					print ', '.join([cell.getText().strip() for cell in cells])
			text = row.get_text().strip()
			text = text.strip('\n')
			if 'Donaldson Part Number' in text:
				donaldson_filter = cells[1].get_text().strip()
				donaldson_filter = donaldson_filter.strip('\n')
				donaldsons.add(donaldson_filter)
		return ','.join(donaldsons)

	else:
		rows = soup.find_all('tr', class_='x1')			
		if(len(rows) != 0):
			for row in rows:
				cells = row.find_all('td')
				if full:
					print ', '.join([cell.getText().strip() for cell in cells])
				match_brand = cells[1].get_text().strip()
				match_brand = match_brand.strip('\n')
				if match_brand in brand_names:
					num = cells[0].get_text().strip()
					num = num.strip('\n')
					if(num == filterNumber):
						donaldson_filter = cells[2].get_text().strip(' \n')
						donaldsons.add(donaldson_filter)

	return ','.join(donaldsons)
