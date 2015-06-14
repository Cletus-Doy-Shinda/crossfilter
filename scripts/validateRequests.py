#!/usr/bin/python
"""validateRequests.py - Assesses and validates all filters
requested by Cross Filter in the filters database"""


import MySQLdb
import sys
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from crossfilter.scripts import downloadfilters as df
from crossfilter.common.secure import get_mysql_credentials
from crossfilter.common import util


def is_oil_filter(session, filter_number):
    """Determines if the <filter_number> is an oil filter"""
    if filter_number.endswith('FP'):
        return False
    address = "http://www.framcatalog.com/PartDetail.aspx?b=F&pn=%s"
    address = address % filter_number
    ret = session.get(address)
    soup = BeautifulSoup(ret.text)
    table = soup.find(id="G_ctl00xContentPlaceHolder1xUltraWebGridxAttributes")
    if table:
        rows = table.find_all('tr')
        if rows:
            for row in rows:
                tds = row.find_all('td')
                if tds:
                    description = tds[1].get_text()
                    return 'Lube' in description
    return False


def isvalidfram(session, filter_number):
    """Determines if the fram <filter_number> is a valid fram oil filter"""
    address = "http://www.framcatalog.com/Part.aspx?b=F&pn=*%s*&em=True"
    address = address % filter_number
    ret = session.get(address)
    soup = BeautifulSoup(ret.text)
    table = soup.find(id="G_ctl00xContentPlaceHolder1xUltraWebGrid1")
    valids = []
    if table:
        rows = table.find_all('tr')
        for row in rows:
            tds = row.find_all('td')
            description = tds[0].get_text()
            partnum = tds[1].find('a').get_text()
            if 'Lube' in description:
                valids.append(('fram', partnum))

    return valids


def valid(session, brand, fram_number):
    """Determines if the <brand> <filter_number> is a valid fram oil filter"""
    if brand.upper() == 'FRAM':
        return isvalidfram(session, fram_number)
    
    valids = set()
    valid_fram = set()
    seen = set()
    
    def _getinfo(fbrand, htmlrow, idx):
        """extract line info"""
        if fbrand.upper() == 'AC-DELCO':
            fbrand = 'ACDELCO'
        if fbrand not in util.BRANDS:
            return

        has_link = htmlrow[idx].find('a')
        if has_link:
            fram_number = has_link.get_text()
            if fram_number not in seen:
                if not any([fram_number.startswith(num) for num in seen]):
                    seen.add(fram_number)
                    if is_oil_filter(session, fram_number):
                        valid_fram.add(fram_number)
                        valids.add(('FRAM', fram_number))
                        valids.add((fbrand, htmlrow[idx - 1].get_text()))
            elif fram_number not in valid_fram:
                return
            else:
                valids.add((fbrand, htmlrow[idx - 1].get_text()))

    address = "http://www.framcatalog.com/Competitor.aspx?b=F&pn=*%s*&em=True"
    address = address % fram_number
    ret = session.get(address)
    soup = BeautifulSoup(ret.text)

    table = soup.find(id='G_ctl00xContentPlaceHolder1xUltraWebGrid1')
    prev_brand = None
    new_brand = ''
    
    if table:
        rows = table.find_all('tr')
        for row in rows:
            tds = row.find_all('td')
            if tds:
                if len(tds) != 3:
                    new_brand = prev_brand
                    _getinfo(new_brand, tds, 1)
                else:
                    new_brand = tds[0].get_text()
                    prev_brand = new_brand
                    _getinfo(new_brand, tds, 2)

    print ' ...%s valid filters' % len(valids)
    return valids


class Validator():
    def __init__(self):
        """initialize validator"""
        user, passwd = get_mysql_credentials()
        db = MySQLdb.connect(host='localhost', user=user,
                             passwd=passwd, db='filters')
        self.db = db
        self.cursor = db.cursor()


    def updateDB(self, brand, filter_number):
        """Set assessed = yes for <brand> <filter_number>"""
        update = "update requests set assessed = 'yes' " \
                  "where brand = '%s' and filter = '%s'"
        self.cursor.execute(update % (brand, filter_number))


    def updateValidDB(self, brand, filter_number):
        """Set valid = yes for <brand>, <filter_number>
        in requests table"""
        update = "update requests set valid = 'yes' " \
                  "where brand = '%s' and filter = '%s'"
        self.cursor.execute(update % (brand, filter_number))


    def alreadyhave(self, brand, filter_number):
        """Check if the filter is already in the database"""
        query = "select * from filters where brand = '%s' and filter = '%s'"
        self.cursor.execute(query  % (brand, filter_number))
        if self.cursor.fetchall():
            return True
        return False


    def insert_new_filter(self, new_brand, new_filter):
        """Insert <new_brand> <new_filter> in filters table in the database"""
        with open(util.INSERT_SQL_FILE, 'a', 1) as insert_file:
            ID = util.insert_new_filter(new_brand, new_filter,
                                        self.db, self.cursor)
            new_insert = "insert into filters(id, brand, filter) " \
                         "values(%d, '%s', '%s');\n" % \
                         (ID, new_brand, new_filter)
            insert_file.write(new_insert)
            return ID


    def run(self):
        """Process requested filters"""
        query = "select brand, filter from requests \
                where assessed = 'no' limit 5"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        validated = set()
        seen = set()

        # requests session - keep-alive, much fast :)
        session = requests.Session()

        for brand, filter_number in rows:
            sys.stdout.write('request: %s %s' % (brand, filter_number))
            self.updateDB(brand, filter_number)
            if filter_number not in seen:
                seen.add(filter_number)
                try:
                    valids = valid(session, brand, filter_number)
                    if (brand.upper(), filter_number) in valids:
                        self.updateValidDB(brand, filter_number)
                    validated = validated.union(valids)
                except Exception as e:
                    print str(e)
                    continue

        if not validated:
            self.db.commit()
            self.db.close()
            return

        with open(util.VALID_FILE, 'a') as out:
            dateformat = '%Y-%m-%d %H:%M:%S'
            now = datetime.strftime(datetime.today(), dateformat)
            print '*************************'
            print '** %s **' % now
            print '*************************'
            print 'number of validated filters: %s' % len(validated)
            for new_brand, new_filter in validated:
                if self.alreadyhave(new_brand, new_filter):
                    print 'already have %s %s' % (new_brand, new_filter)
                    continue

                print 'finding filters for %s %s' % (new_brand, new_filter)

                # Insert the new filter in the filter table and get it's ID
                new_brand = new_brand.lower()
                ID = self.insert_new_filter(new_brand, new_filter)

                # Find all the filters that match
                now = datetime.strftime(datetime.today(), dateformat)
                df._retrieve(new_filter, new_brand, ID, self.cursor)
                cmd = '{now}: {resp}'.format(now=now, resp=ID)
                out.write(cmd + '\n')
                self.db.commit()
        print '\n=========================\n'
        self.db.commit()
        self.db.close()


def main():
    validator = Validator()
    validator.run()


if __name__ == "__main__":
    main()

