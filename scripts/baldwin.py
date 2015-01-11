import requests
from bs4 import BeautifulSoup
import sys


def getFilter(filterNumber, brand, full=False):
	brand = brand.upper()
	filterNumber = filterNumber.upper()

	if brand == 'HASTINGS':
		brand = 'HASTINGS PREMIUM FILTERS'

	address = "http://catalog.baldwinfilter.com/BaldwinDisplay.asp?URL=BaldwinOEM.asp&partnumber=%s=&optiontype=OEM"
	address = address % filterNumber
	
	page = requests.get(address)
	soup = BeautifulSoup(page.text)
	
	rows = soup.find_all("tr", class_="tblrow")
	bws = set()

	for row in rows:
		cells = row.find_all('td')
		comp_number = cells[0].getText().strip()
		comp_brand = cells[1].getText().strip()
		baldwin_filter = cells[2].getText().strip()
		if full:
			print ', '.join([cell.getText().strip() for cell in cells])

		if comp_brand == brand and comp_number == filterNumber:
			bws.add(baldwin_filter)

	return ','.join(bws)
