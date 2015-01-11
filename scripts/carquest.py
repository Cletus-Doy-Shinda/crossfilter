import requests
from bs4 import BeautifulSoup
import sys


def getFilter(filterNumber, brand, full=False):
	brand = brand.upper()
	filterNumber = filterNumber.upper()

	if brand == 'ACDELCO':
		brand = 'AC DELCO'
	if brand == 'HASTINGS':
		brand = 'HASTINGS FILTERS'

	address = 'http://www.cficonnect.com/filterlookup/results.asp?ExactMatch=0&PartNo1=%s&MakerCode1='
	address = address % filterNumber

	try:
		page = requests.get(address)
		soup = BeautifulSoup(page.text)
	except Exception:
		print 'Exception accessing carquest website'
		return ''

	table_cells = soup.find_all("td", class_='bluemedium')
	cqs = set()

	def add_filter(row):
		ref = row.find('a')
		value = ref.getText().strip(' \n')
		cqs.add(value)

	for table_cell in table_cells:
		row = table_cell.parent
		cells = row.find_all('td')
		match_number = cells[0].getText().strip()
		match_brand = cells[1].getText().strip()
		carquest_number = cells[3].getText().strip()

		string = row.getText().strip(' \n')
		if full:
			print ', '.join([cell.getText().strip() for cell in cells])

		if match_number == filterNumber and match_brand == brand:
			cqs.add(carquest_number)
			
	return ','.join(cqs).strip()
