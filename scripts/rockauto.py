import urllib2
from bs4 import BeautifulSoup

url = 'http://www.rockauto.com/catalog/x,carcode,%s,parttype,5340'
good = open('/home/abe/FilterApp/python/goodCars.txt','r')
lines = good.readlines()
good.close()

# def getCar(line):
# 	split = line.find('| ',0,len(line))
# 	return line[split+2:]

# cars = set()
# goodCars = open('C:/users/radio/filterapp/goodCars.txt','a')

# for line in lines:
# 	if(getCar(line) in cars):
# 		continue
# 	else:
# 		goodCars.write(line)
# 		cars.add(getCar(line))

# goodCars.close()
good = open('/home/abe/FilterApp/python/goodCars.txt','a')
out = open('/home/abe/FilterApp/python/carFilters.txt','a')

for line in range(2100500,2100600):
	print str(line)
	proxy = urllib2.ProxyHandler({'http': '54.224.82.100'})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	page = urllib2.urlopen(url % str(line))
	soup = BeautifulSoup(page)

	title = soup.find('title')
	titleString = title.getText()

	if(titleString.find('RockAuto Parts Catalog',0,len(titleString)) == -1):
		good.write(str(line) + ' | ' + titleString)
		tables = soup.find_all(class_='parts')
		for table in tables:
			close = table.find(class_="layout")
			td = close.find('td')
			string = td.getText()
			pound = string.find('# ',0,len(string))
			space = string.find(' ',pound+2,len(string))
			out.write((string[0:space]) + '\n')
		out.write('============================\n')
		print 'processed: ' + str(line)

# page = urllib2.urlopen('http://www.rockauto.com/catalog/x,carcode,1000012,parttype,5340')
# soup = BeautifulSoup(page)

# tables = soup.find_all(class_='parts')
# for table in tables:
# 	close = table.find(class_="layout")
# 	td = close.find('td')
# 	string = td.getText()
# 	bP = string.find(' More Info',0,len(string))

# 	print string[0:bP]
good.close()
out.close()

