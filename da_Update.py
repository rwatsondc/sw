import daTools, json, datetime, urllib2, socket, os, pprint

host='www.dataphorism.link'
lclHost = socket.gethostname()
print lclHost
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
    #determine if this is first time since last update interval, add wiggle room
    #extract last uptime-start (note data stored as firstUp:lastUp)
    tEntries = list(upFile[lclHost].keys())
    tEntries.sort()
    tEntries.reverse()
    lastKey = tEntries[0]
    lastStart = datetime.datetime.strptime(upFile[lclHost][lastKey], '%Y-%m-%d %H:%M:%S.%f')
    #extract last uptime:
    lastUp = datetime.datetime.strptime(upFile[lclHost][lastKey], '%Y-%m-%d %H:%M:%S.%f')
    rightNow = datetime.datetime.now()
    timeDelta = rightNow - lastUp
    print "time delta", timeDelta.seconds, '/', timeInterval

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

        
        
    
except:
    upFile[lclHost]={str(datetime.datetime.now()):str(datetime.datetime.now())}
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
