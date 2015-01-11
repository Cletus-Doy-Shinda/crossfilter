import requests
from bs4 import BeautifulSoup
import sys


def getFilter(filterNumber, brand, full=False):
	brand = brand.upper()
	filterNumber = filterNumber.upper().replace('-', '')

	if brand == 'BALDWIN':
		brand = 'BALDWIN FILTERS'
	if brand == 'NAPA':
		brand = 'NAPA GOLD'

	address = 'http://catalog.hastingsfilter.com/BaldwinDisplay.asp?partnumber=%s&optiontype=OEM'
	address = address % filterNumber
	resp = requests.get(address)

	soup = BeautifulSoup(resp.text)

	hastings = set()

	form = soup.find(id='BaldwinDisplay')
	if form:
		rows = form.find_all('tr', class_='tblrow')
		if rows:
			for row in rows:
				cells = row.find_all('td')
				comp_number = cells[0].getText()
				comp_brand = cells[1].getText()
				hastings_filter = cells[2].getText().strip()
				if full:
					print ', '.join([cell.getText().strip() for cell in cells])
				if comp_brand == brand and comp_number == filterNumber:
					hastings.add(hastings_filter)

	return ','.join(hastings).strip()
