import daTools, json, datetime, urllib2, socket, os

#print os.getcwd()

host='www.dataphorism.link'

#host='104.236.35.60'
"""
you had an issue, perhaps temporarily, where you were unable
to ping www.dataphorism.link, likely a DNS issue.  You updated
DNS settings in resolve.conf however it is possible such issues
will occur again which will be problematic for tracking uptime
"""

lclHost = socket.gethostname()
rDir = r'/var/www/data/js'
lclFileName = '/sw/up.json'

#load stored credentials from file:
daLogIn=json.loads(open('/sw/pw.json','r').read())[host]

#Load remote uptime file
rUpFile = r'http://www.dataphorism.link/data/js/up.json'

upFile = json.loads(urllib2.urlopen(rUpFile).read())
#update local host uptime entry
upFile[lclHost] = str(datetime.datetime.now())

#save local copy of upFile as formated json file

lclFile = open(lclFileName,'w')
lclFile.write(json.dumps(upFile, indent=4))
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
