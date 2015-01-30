import daTools, json, datetime, urllib2, socket, os, pprint




#print os.getcwd()

host='www.dataphorism.link'

#host='104.236.35.60'
"""
you had an issue, perhaps temporarily, where you were unable
to ping www.dataphorism.link, likely a DNS issue.  You updated
DNS settings in resolve.conf however it is possible such issues
will occur again which will be problematic for tracking uptime

Notes:
#{'sape': 4139, 'guido': 4127, 'jack': 4098}

"""

lclHost = socket.gethostname()
rDir = r'/var/www/data/js'
lclFileName = '/sw/up.json'
#upInterval is number of minutes between cronjobs that update server
upInterval = 15
timeInterval = (upInterval + 4)* 60 # in seconds

#load stored credentials from file:
daLogIn=json.loads(open('/pw/pw.json','r').read())[host]

#Load remote uptime file
rUpFile = r'http://www.dataphorism.link/data/js/up.json'

print 11
upFile = json.loads(urllib2.urlopen(rUpFile).read())
###upFile now contains a json/dictionary
#############################
try: #useful for entries in the right format...
    #print json.dumps(upFile, indent=4)

    #determine if this is first time since last update interval, add wiggle room

    #extract last uptime-start (note data stored as firstUp:lastUp)
    print 12
    tEntries = list(upFile[lclHost].keys())
    print 13
    tEntries.sort()
    tEntries.reverse()
    lastKey = tEntries[0]
    lastStart = datetime.datetime.strptime(upFile[lclHost][lastKey], '%Y-%m-%d %H:%M:%S.%f')
    #extract last uptime:
    lastUp = datetime.datetime.strptime(upFile[lclHost][lastKey], '%Y-%m-%d %H:%M:%S.%f')
    rightNow = datetime.datetime.now()
    timeDelta = rightNow - lastUp
    if timeDelta.seconds > timeInterval:
        #new entry!
        print 'System has not checked-in within specified time interval\ncreating new entry'
        upFile[lclHost][str(datetime.datetime.now())]=str(datetime.datetime.now())
        pass
    else:
        #update entry!
        print 'updating last entry'
        upFile[lclHost][lastKey]=str(datetime.datetime.now())
        timeDelta = lastUp - lastStart
    if timeDelta.seconds > timeInterval:
        #new entry!
        print 0
        upFile[lclHost]={str(datetime.datetime.now()):str(datetime.datetime.now())}
        pass
    else:
        #update entry!
        print 1
        upFile[lclHost][lastKey]=str(datetime.datetime.now())
        
        
    
except:
    upFile[lclHost]={str(datetime.datetime.now()):str(datetime.datetime.now())}
    #comment out error later...
    #raise('oops')




#dtTime = datetime.datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S.%f')

#raise('oops')

#############################
#update local host uptime entry


#save local copy of upFile as formated json file

lclFile = open(lclFileName,'w')
lclFile.write(json.dumps(upFile, indent=4, sort_keys=True))
lclFile.close()

#push local copy back to server

username = daLogIn['username']
pw = daLogIn['password']
#connect
ssh = daTools.SSHConnection(host, username, pw)

#push file
ssh.put(lclFileName, rDir+'/'+'up.json')

ssh.close()

print "done!"
