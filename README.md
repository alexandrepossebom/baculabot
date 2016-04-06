# baculabot
Simple Bacula bot to notify when backup ends
Based in Wanderlei Huttel bash script


```
pip install pymysql
```


You need create a bot, to do this:

Add BotFather to your telegram :
https://telegram.me/BotFather

send /newbot

Choose a name

at end it will return the http API token.

put it in telegram.py variable BOT_ID

To get chat id

Add you new bot to your telegram and start message something with him.

Uncomment these lines in telegram.py:

#result = urllib2.urlopen("https://api.telegram.org/bot" + BOT_ID + "/getUpdates").read()
#print result
#sys.exit(0)

Run the telegram.py it will return CHAT_ID put it in your telegram.py.

delete or comment lines you have uncommented.


### Change your bacula-dir.conf Default Job to like this:

```
JobDefs {
  Name = "DefaultJob"
  Type = Backup
  Level = Differential
  Client = tralha-fd
  FileSet = "Full Set"
  Schedule = "WeeklySchedule"
  Storage = LTO6-Library
  Messages = Standard
  Pool = Daily
  SpoolAttributes = yes
  Priority = 10
  Write Bootstrap = "/var/lib/bacula/%c.bsr"
  RunScript {
     Command = "/etc/bacula/scripts/telegram.py %i"
     FailJobOnError = no
     RunsWhen = After
     RunsOnFailure = yes
     RunsOnClient = no
     RunsOnSuccess = yes
  }
}
```
