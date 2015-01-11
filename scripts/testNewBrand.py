import MySQLdb
import sys
import time
import downloadFilters3 as df
import acdelco, baldwin, carquest, donaldson
import napa, fram, wix, purolator, servicechamp, johndeere
import fleetguard, hastings

from crossfilter.common.secure import get_mysql_credentials


user, passwd = get_mysql_credentials()
db = MySQLdb.connect(host='localhost', user=user, passwd=passwd, db='filters')
cursor = db.cursor()
query = 'select distinct brand, filter from matches group by brand'

def check_names_new_to_old(newbrand):
	"""For every brand, test naming conventions for the
	new brand being added"""

	cursor.execute(query)
	rows = cursor.fetchall()
	func = __import__(newbrand.strip())
	for row in rows:
		brand = row[0]
		filterNumber = row[1].upper()

		print '======================================='
		print 'Full output for %s %s from %s' % (brand, filterNumber, newbrand)
		print '======================================='
		print 'matches: %s' % func.getFilter(filterNumber, brand, full=True)


def check_names_old_to_new(filterNumber, brand):
	for name, func in df.RETRIEVE_FUNCTIONS:
		if name == brand.lower():
			continue
		print 'checking %s for filters matching %s:%s' % (name, brand, filterNumber)
		print 'matches %s' % func(filterNumber, brand, full=False)

# check_names_new_to_old('mobil')
# check_names_old_to_new('MO111', 'mobil')

