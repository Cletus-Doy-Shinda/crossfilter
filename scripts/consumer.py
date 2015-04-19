import braxas_retrieve as df
import requests
import time


def consume():
	"""Consumer grabbing new filters off the stack as they are created"""
	logfile = open(df.SQL_LOG_FILE, 'w')
	logfile.close()
	linesread = 0
	seen = set()
	curr_num = ''

	while True:
		try:
			page = requests.get('http://192.168.0.200/producer.php')
			lines = page.text.split('\n')
			for line in lines[linesread:]:
				if line:
					ID, filterNumber, brand = line.split(':')
					brand = brand.strip()
					if filterNumber not in seen:
						curr_num = filterNumber
						seen.add(filterNumber)
						print 'getting matches for %s %s' % (brand, filterNumber)
						df.retrieve(filterNumber, brand, ID)
					linesread += 1

			time.sleep(4)
		except:
			with open('/Users/Abe/crossfilter/text/mac_exceptions.log', 'a') as f:
				f.write('exception processing: mobil:%s\n' % curr_num)

			time.sleep(2)


consume()
