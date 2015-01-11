import servicechamp
import sys
from optparse import OptionParser


# This page can be modified and used to find other filter brands such as:
# Warner
# Mobile
# Mobile 1
# MileGuard


def getFilter(filterNumber, brand, full=False):
	return servicechamp.getFilter(filterNumber, brand,
		full=full, supplier_name='MOBIL 1')


def main():
	if len(sys.argv) < 2:
		print 'Error: not enough args'
		sys.exit(1)

	usage = 'usage: %prog [options] <filterNumber> <brand>'
	parser = OptionParser(usage=usage)
	parser.add_option('-f', '--full', dest='full',
					  action="store_true", default=False,
					  help='Output all matches for filterNumber and brand')

	(options, args) = parser.parse_args()
	filterNumber = str(args[0])
	brand = str(args[1])
	full = options.full

	print getFilter(filterNumber, brand, full=full)

if __name__ == "__main__":
	main()
