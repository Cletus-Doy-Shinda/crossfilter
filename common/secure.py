INFO_FILE = '/var/crossfilter/info'

def get_mysql_credentials():
	"""get user and passwd for MySQL access"""
	with open(INFO_FILE, 'r') as file_:
		data = file_.read()
		user, passwd = data.split(':')

	return user, passwd.strip()


def get_email_credentials():
	"""get sender and password for sending emails"""
	password = 'Y3Jvc3NmaWx0ZXI1MTcx'
	sender = 'crossfilterapp@gmail.com'
	return sender, password


def get_braxas_credentials():
	"""return user and hostname of braxas machine"""
	return 'abe@braxas.local'


def get_x10_credentials():
	"""return user and password for x10 login"""
	return ('crossfi3', 'cmVhZHlvcm5vdDE=')


def test_secure():
	"""test hidden functions"""
	user, password = get_x10_credentials()
	assert user == 'crossfi3'
	assert password == 'cmVhZHlvcm5vdDE='

	creds = get_braxas_credentials()
	assert creds == 'abe@braxas.local'

	sender, password = get_email_credentials()
	assert sender == 'crossfilterapp@gmail.com'
	assert password == 'Y3Jvc3NmaWx0ZXI1MTcx'
