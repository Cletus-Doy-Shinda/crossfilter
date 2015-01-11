import urllib2
import sys
from bs4 import BeautifulSoup


def getFilter(filterNumber, brand, full=False):
	brand = brand.upper()
	filterNumber = filterNumber.upper()

	address = 'https://jdparts.deere.com/servlet/com.deere.u90.jdparts.view.servlets.searchcontroller.PartNumberSearch'
	form_data = 'userAction=exactSearch&browse=&screenName=partSearch&priceIdx=1&searchAppType=&searchType=exactSearch&partSearchNumber=%s&pageIndex=1&endPageIndex=1' % filterNumber

	page = urllib2.urlopen(address, data=form_data)
	soup = BeautifulSoup(page)

	if brand == 'ACDELCO':
		brand = 'AC'

	form = soup.find(attrs={'name':'partsearch'})
	if not form:
		return ''
	tables = form.find_all('table')

	table = tables[4]
	rows = table.find_all('tr')
	filters = set()
	for row in rows[2:]:
		cells = row.getText().split('\n')
		cells = [x for x in cells if x]
		_brand = cells[1]
		_filter = cells[0]
		fType = cells[4]
		match_filter = cells[2]
		if full:
			print _brand, _filter, fType, match_filter
		if brand == _brand.upper() and filterNumber == _filter.upper() and fType == 'Oil Filter':
			filters.add(match_filter)

	return ','.join(filters)
