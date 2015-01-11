#!/usr/bin/python
"""feedback.py - Send daily stats emails"""


from datetime import date, datetime, timedelta
from crossfilter.common.contexts import dbcursor
from crossfilter.common.util import substring, sendmail


def email_feedback(cursor):
    """daily feedback email"""
    query = """select * from feedback where response = 'no'"""
    cursor.execute(query)
    rows = cursor.fetchall()

    emails = []
    suggestions = []
    for item in rows:
        suggestions.append(item[1])
        emails.append(item[2])

    if emails:
        receivers = emails
        message = """From: Cross Filter
Subject: Thank you for your feedback!

I appreciate you taking time to submit feedback to help improve Cross Filter. 
I will take your recommendations into consideration.

Thanks for using Cross Filter!
        """
        sendmail(receivers=receivers, message=message)

        update = "update feedback set response = 'yes' where response = 'no'"
        cursor.execute(update)

    if suggestions:
        receivers = ['abefriesen.af@gmail.com']

        message = """From: Cross Filter <crossfilterapp@gmail.com>
Subject: Daily Feedback

Suggestions:

%s


        """ % "\n==================================\n".join(suggestions)

        sendmail(receivers=receivers, message=message)


def email_access(cursor):
    """daily usage stats email"""
    file_ = open('/var/log/apache2/access.log','r')
    lines = file_.readlines()
    file_.close()
    file_ = open('/var/log/apache2/access.log.1','r')
    lines += file_.readlines()
    file_.close()

    yesterdate = str(date.today() - timedelta(1))
    yesterday = datetime.strptime(yesterdate, '%Y-%m-%d')
    total = 0

    def getlineinfo(line):
        """extract apache log line info"""
        date_pat = r'\d\d/\D{3}/\d{4}(:\d\d){3}'
        access_pat = r'POST /filter.php'
        dmatch = substring(date_pat, line)
        amatch = substring(access_pat, line)

        return dmatch, amatch

    for line in lines:
        linedate, access_type = getlineinfo(line)
        linedate = datetime.strptime(linedate, '%d/%b/%Y:%H:%M:%S')
        if not access_type:
            continue
        delta = linedate - yesterday
        if delta.days == 0:
            total += 1

    query = "select count(*) from requests where time like '%s%%'" % yesterdate
    cursor.execute(query)
    rows = cursor.fetchall()
    pretty_date = datetime.strftime(yesterday, '%b %d, %Y')
    misscount = int(rows[0][0])

    hitcount = total - misscount
    hitpercent = 0
    if total > 0:
        hitpercent = hitcount / float(total) * 100

    with open('/home/abe/FilterApp/python/hitrate.dat', 'a') as file_:
        file_.write('%s\t%d\t%d\n' % (yesterdate, hitcount, misscount))

    receivers = ['abefriesen.af@gmail.com']

    message = """From: Cross Filter <crossfilterapp@gmail.com>
Subject: Daily Access Count

Filter request data for %s:

Total requests:      %s
Request Hits:        %s
Request Misses:      %s
Hit Rate Percentage: %.2f

    """ % (pretty_date, total, hitcount, misscount, hitpercent)

    sendmail(receivers=receivers, message=message)


def run():
    """kick off the daily emails"""
    with dbcursor() as cursor:
        email_access(cursor)
        email_feedback(cursor)


run()
