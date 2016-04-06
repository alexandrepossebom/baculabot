#!/usr/bin/python
# Based in Wanderlei Huttel shell script

import sys
import urllib2
import urllib
import pymysql


try:
    connection = pymysql.connect(host='localhost',
                                 user='bacula',
                                 password='',
                                 db='bacula',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
except:
    sys.exit(1)

#Fill with your data
BOT_ID = ""
CHAT_ID = ""

def human_readable(size, precision=2):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffixindex = 0
    while size > 1024 and suffixindex < 4:
        suffixindex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f%s"%(precision, size, suffixes[suffixindex])

cursor = connection.cursor()

#result = urllib2.urlopen("https://api.telegram.org/bot" + BOT_ID + "/getUpdates").read()
#print result
#sys.exit(0)

try:
    jobid = int(sys.argv[1])
except:
    sys.exit(0)

sql = ("SELECT "
       "j.name as jobname, c.name as client, "
       "j.jobbytes as jobbytes, j.jobfiles as jobfiles, "
       "j.jobstatus as jobstatus, "
       "case when j.level = 'F' then 'Full' when j.level = 'I' "
       "then 'Incremental' when j.level = 'D' then 'Differential' end as level, "
       "p.name as pool, "
       "j.starttime as starttime, j.endtime as endtime, "
       "SEC_TO_TIME(TIMESTAMPDIFF(SECOND, starttime, endtime)) as duration, "
       "m.mediatype as mediatype, s.name as storage, "
       "st.jobstatuslong as status "
       "FROM Job as j "
       "INNER JOIN Pool as p on p.poolid = j.poolid "
       "INNER JOIN Client as c on c.clientid = j.clientid "
       "INNER JOIN JobMedia as jm on jm.jobid = j.jobid "
       "INNER JOIN Media as m on jm.mediaid = m.mediaid "
       "INNER JOIN Storage as s on m.storageid = s.storageid "
       "INNER JOIN Status as st on st.jobstatus = j.jobstatus "
       "where j.jobid = %d") % jobid

cursor.execute(sql)
message = ""

data = cursor.fetchone()

if not data:
    sys.exit(0)

if data["jobstatus"] == "T":
    message += '* BACKUP OK [%s] *\n' % data["client"]
else:
    message += '* BACKUP ERROR [%s] *\n' % data["client"]

message += "JobName = %s\n" % data["jobname"]
message += "JobId = %s\n" % jobid
message += "Client = %s\n" % data["client"]
message += "JobBytes = %s\n" % human_readable(data["jobbytes"])
message += "JobFiles = %d\n" % data["jobfiles"]
message += "Level = %s\n" % data["level"]
message += "Pool = %s\n" % data["pool"]
message += "Storage = %s\n" % data["storage"]
message += "StartTime = %s\n" % data["starttime"].strftime("%d/%m/%y %H:%M:%S")
message += "EndTime = %s\n" % data["endtime"].strftime("%d/%m/%y %H:%M:%S")
message += "Duration  = %s\n" % data["duration"]
message += "JobStatus = %s\n" % data["jobstatus"]
message += "Status = %s\n" % data["status"]

connection.close()

try:
    TLMESSAGE = urllib.urlencode({"chat_id": CHAT_ID, "text": message})
    urllib2.urlopen("https://api.telegram.org/bot" + BOT_ID + "/sendMessage", TLMESSAGE).read()
except:
    sys.exit(0)
