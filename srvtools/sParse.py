"""

Simple python script to sort apache log by IP address and save to file based
on IP name

"""
import os, datetime

outDIR = r'/home/ipLogs'
#inLog = r'/home/pyTest/tLog.txt'
inLog = r'/var/log/apache2/access2.log'

ipIn = open(inLog,'r')

ipList = []
outLogs = {}

for line in ipIn:
    ip = line.split(' ')[0]
    if ip not in ipList:
        ipList.append(ip)
        outLogs[ip]=open(outDIR+r'/'+ip+'.log','a')
    outLogs[ip].write(line)

#close all ip log writers
for i in outLogs.keys():
    outLogs[i].close()

#update copyLog
t = open(r'/home/copyLog.log','a')
outStr = 'sParse run on:' + str(datetime.datetime.now())+'\n'
t.write(outStr)
t.close()

#wipe inLog but not delete
t = open(inLog,'w')
t.close()

print "Done!"
