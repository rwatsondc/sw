"""

Simple python script to sort ssh log by IP address and save to file based
on IP name.

This is updated to handle multiple log sites in a list

"""
import os, datetime, difflib
"""
outDIR = r'/home/sshLogs/backup_auth.log'
bkupLog = r'/home/pyTest/tLog.txt'
liveLog = r'/home/pyTest/tLogNew.txt'
#inLog = r'/var/log/auth.log'
"""

bkupLog = r'/home/sshLogs/bkup_auth.log'
liveLog = r'/var/log/auth.log'

bkup_Lines = open(bkupLog,'r').readlines()
updateBackup = open(bkupLog,'a')
live_Lines = open(liveLog, 'r').readlines()

dif = difflib.Differ()

result = list(dif.compare(bkup_Lines, live_Lines))

updCount = 0
for line in result:
    if line[:2]=='+ ':
        updateBackup.write(line[2:])
        updCount = updCount + 1

updateBackup.close()

print 'Number of updated lines: '+str(updCount)




print "Done!"
