# baculabot
Simple Bacula bot to notify when backup ends
Based in Wanderlei Huttel bash script


# Change your bacula-dir.conf Default Job to like this:
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
