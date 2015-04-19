from crossfilter.common.util import get


lines = []
donaldson_have = set()
donaldson_need = set()
with open('temp.txt', 'r') as f:
	lines = f.readlines()
	for line in lines:
		address = 'http://crossfilterapp.ddns.net/filter.php?brand=%s&filter=%s'
		donaldson, carquest = line.split(':')
		have = get(address % ('donaldson', donaldson))
		# have = get(address % ('donaldson', 'P166375'))
		if have:
			print have
