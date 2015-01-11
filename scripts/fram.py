import requests
from bs4 import BeautifulSoup
import sys


def getFilter(filterNumber, brand, full=False):
	brand = brand.upper()
	filterNumber = filterNumber.upper()
	
	if brand == 'ACDELCO':
		brand = 'AC-DELCO'

	address = "http://www.framcatalog.com/Competitor.aspx?b=F&pn=%s&em=True" % filterNumber

	resp = requests.get(address) 
	soup = BeautifulSoup(resp.text)

	table = soup.find(id="G_ctl00xContentPlaceHolder1xUltraWebGrid1")
	frams = set()
	if table:
		rows = table.find_all('tr')
		for row in rows:
			cells = row.find_all('td')
			if full:
				print ', '.join([cell.getText().strip() for cell in cells])
			if len(cells) == 3:
				comp_brand = cells[0].get_text().rstrip()
				comp_number = cells[1].getText().strip()
				fram_brand = cells[2].find('a').getText().strip()
			if comp_brand == brand and comp_number == filterNumber:
				frams.add(fram_brand)

	return ','.join(frams)
