import MySQLdb
import sys
import os
import time
import subprocess
import crossfilter.scripts.downloadfilters as df

from crossfilter.common.util import insert_new_filter, trycmd
from crossfilter.common.secure import get_mysql_credentials, get_braxas_credentials

user, passwd = get_mysql_credentials()
login_creds = get_braxas_credentials()

db = MySQLdb.connect(host='localhost', user=user, passwd=passwd, db='filters')
cursor = db.cursor()
PRODUCER_FILE = '/var/server/producer.php'
TEXT_DIR = '/home/abe/FilterApp/text/'
BRAXAS_LOG_FILE = os.path.join(TEXT_DIR, 'braxas_insert.sql')
REMOTE_BRAXAS_FILE = '/tmp/braxas_insert.sql'


def produce(filterNumber, brand, ID):
    """Acts like a producer - appends new filters to list"""
    with open(PRODUCER_FILE, 'a') as f:
        f.write('%s:%s:%s\n' % (ID, filterNumber, brand))


def start_consumer():
    """start the consumer.py function on braxas"""
    # clear contents of PRODUCER_FILE
    pfile = open(PRODUCER_FILE, 'w')
    pfile.close()

    # remove braxas insert sql file
    cmd = ['rm', '-rf', BRAXAS_LOG_FILE]
    trycmd(cmd)

    # start the consumer
    cmd = ['ssh', login_creds, 'screen', '-d', '-m',
           '/usr/bin/python', '/Users/Abe/crossfilter/scripts/consumer.py']
    trycmd(cmd)

    print 'consumer started'


def stop_consumer():
    """stop the consumer.py function on braxas"""
    # copy the remote sql file over
    cmd = ['scp', '%s:%s' % (login_creds, REMOTE_BRAXAS_FILE), '%s' % TEXT_DIR]
    trycmd(cmd)

    # shutdown consumer
    cmd = ['ssh', login_creds, '/usr/local/bin/pgrep', '-f', 'consumer.py']
    consumer_pids = subprocess.check_output(cmd)
    consumer_pids = consumer_pids.strip().split()
    cmd = ['ssh', login_creds, 'kill', ' '.join(consumer_pids)]
    subprocess.call(cmd)

    print 'consumer stopped'


def matches():
    with open(BRAXAS_LOG_FILE, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print line


def findNewBrandMatches(brand):
    """For every filter in the database, find all filters that match <brand>"""
    module = __import__(brand.strip())
    cursor.execute("select * from filters")

    rows = cursor.fetchall()

    insert_stmt = "insert into matches values(%s, '%s', '%s');\n"
    seen = set()
    with open('temp_out.sql', 'w') as out:
        for ID, db_brand, fltr in rows:
            print 'Getting %s matches for %s %s: %s' % (brand, ID, db_brand, fltr)
            try:
                filterString = module.getFilter(fltr, db_brand)
            except Exception as e:
                print 'Exception for %s:%s: %r' % (db_brand, fltr, e)
                filterString = ''
            if filterString:
                filters = filterString.split(',')
                for f in filters:
                    f = f.strip()
                    out.write(insert_stmt % (ID, brand, f))
                    cursor.execute(insert_stmt % (ID, brand, f))
                    if f not in seen:
                        seen.add(f)
                        new_id = insert_new_filter(brand, f, db, cursor)
                        produce(f, brand, new_id)

                db.commit()
            # Don't overload the remote server
            time.sleep(3)

    db.commit()


def insertNewBrandMatches(brand):
    """Pull all the unique filters for <brand> out of matches and insert them into filters table"""
    cursor.execute("select distinct brand, filter from matches where brand = '%s'" % brand)
    rows = cursor.fetchall()

    with open('temp_out2.sql', 'w') as out:
        for row in rows:
            new_brand = row[0]
            fltr = row[1]
            out.write("insert into filters(brand, filter) values('%s', '%s');\n" % (new_brand, fltr))
            cursor.execute("insert into filters(brand, filter) values('%s', '%s')" % (new_brand, fltr))

    db.commit()


def matchNewToOld(brand):
    """Query filters table for all filters of <brand> type and find matches"""
    cursor.execute("select * from filters where brand = '%s' and id > 4949 order by id" % brand)
    rows = cursor.fetchall()
    for row in rows:
        ID = row[0]
        new_brand = row[1]
        fltr = row[2]
        print 'Getting matches for %s %s:%s' % (str(ID), new_brand, fltr)
        df.retrieve(fltr, new_brand, ID)


def run(brand):
    """Kickstart the process of adding a new brand to the database"""
    start_consumer()
    findNewBrandMatches(brand)

    # Wait here to ensure consumer can catch up
    time.sleep(600)
    stop_consumer()
    print '\n\n\n\n\n\n\n\n\n'
    matches()
    # insertNewBrandMatches(brand)
    # matchNewToOld(brand)


if __name__ == "__main__":
    run(sys.argv[1])
