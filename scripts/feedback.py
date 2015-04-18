#!/usr/bin/python
"""feedback.py - Send daily stats emails"""

import subprocess

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
    access_log_1 = '/var/log/apache2/access.log'
    access_log_2 = '/var/log/apache2/access.log.1'
    
    yesterdate = date.today() - timedelta(1)
    pretty_date = datetime.strftime(yesterdate, '%d/%b/%Y')

    query = "select count(*) from requests where time like '%s%%'" % yesterdate
    cursor.execute(query)
    rows = cursor.fetchall()
    misscount = int(rows[0][0])
    
    cmd = "grep -E '%s.*(POST|GET.*filter.php)' %s %s | wc -l" \
        % (pretty_date, access_log_1, access_log_2)
    cmdargs = ['bash', '-c', cmd]
    total = int(subprocess.check_output(cmdargs))

    cmd = "grep -E '%s.*(POST|GET.*filter.php).*(237|308)' %s %s | wc -l" \
        % (pretty_date, access_log_1, access_log_2)
    cmdargs = ['bash', '-c', cmd]

    misscount = int(subprocess.check_output(cmdargs))
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
