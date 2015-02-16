import os, re, pprint, datetime, json

#raise('oops')

targetHost = 'wptest'

sshDir = r'/data/raw/sshlogs'

outDir = r'/data/summary/sshlogs'

walkssh = os.walk(sshDir)

fleList = []

for root, subs, files in walkssh:
    for fle in files:
        fleList.append(os.path.join(root,fle))
pass

#explore the data: how many distint IP addresses are hitting me?
#use re to look for pattern:
#Failed password for * from * port *
#regex pattern" 'Failed password for .* from .* port .*'

ipCount = {}
tempList = []

for fle in fleList:
    print "working on file", fle
    #load data
    #limit to first 10 lines for testing
    f = open(fle,'r').readlines()#[:1000]
    #sort with re
    for line in f:
        tMatch = re.findall('Failed password for .* from .* port .* ssh2',line)
        if len(tMatch)>0:
            tMatch=tMatch[0]
            tIp = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',tMatch)[0]
            if tIp not in ipCount.keys():
                ipCount[tIp]=1
            else:
                ipCount[tIp] = ipCount[tIp]+1



#Congrats, now you know how many times various IP addresses have tried to hack you!
"""
next it would be nice to know rough idea of when/how frequently you are getting hit
how about something like this:

IP Address:
    Date:mm/dd/yyyy
        Number of failed logon attempts:#
        usernames:[list of usernames]
        ports:[list of ports]
        
json format example:
https://www.jsoneditoronline.org/ helps format json/dictionaries properly

{
  "192.168.2.123":{
    "2-2-15":{
      "Attempts":23,
      "Users":["root","admin"],
      "Ports":[20,22,487]
    },
    "2-3-15":{
      "Attempts":23,
      "Users":["root","admin"],
      "Ports":[20,22,487]
      
    }
  },
  "192.168.2.122":{
    "1-23-15":{
      "Attempts":23,
      "Users":["root","admin"],
      "Ports":[20,22,487]      
    }
  }
}
"""

#collect prior processed ips and screen out before going on...
pastWorkDir = r'/data/summary/sshlogs'
skipIPs = []
walkWork = os.walk(pastWorkDir)
for root, subs, files in walkWork:
    for fle in files:
        skipIPs.append(re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', fle)[0])

setIpIn = set(ipCount.keys())
setIpDone = set(skipIPs)
ipDriver = list(setIpIn-setIpDone)

#cycles are cheap, you need practice, don't moddify working code...
#bootstrap existing code?

sshIp = {}
ipDate = {}
dateStats = {}


#raise('oops')

testOnly = ['81.149.31.54']

for ip in ipDriver:#ipCount.keys():
    print "working on IP address:", ip
    #init new ip entry:
    if ip not in sshIp.keys():sshIp[ip]={}
    
    for fle in fleList:
        f = open(fle,'r').readlines()
        for line in f:
            tMatch = re.findall('Failed password for .* from .* port .* ssh2',line)
            if len(tMatch)>0:
                tMatch=tMatch[0]
                #print tMatch
                #tIp = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',tMatch)[0]
                tUser = re.findall('for .* from', tMatch)[0][4:-5]
                tPort = re.findall('port \d*',tMatch)[0][5:]
                tDateTimeRaw = re.findall('.* '+targetHost,line)[0][:-1*(len(targetHost)+1)]
                #datetime.datetime.strptime(tDateTimeRaw+' 2015', '%b %d %H:%M:%S %Y')
                #assume logging starts in 2015
                tDateTime = datetime.datetime.strptime(tDateTimeRaw+' 2015', '%b %d %H:%M:%S %Y')
                sDate = str(tDateTime.date())
                #fill out dictionaries
                #check for date:
                if sDate not in sshIp[ip].keys():
                    #initialize
                    print "setting up first entry for ip-date"
                    sshIp[ip][sDate]={}
                    sshIp[ip][sDate]["Attempts"]=1
                    #uncomment out following lines to save verbose logs...
                    #sshIp[ip][sDate]["Users"]=set([tUser])
                    #sshIp[ip][sDate]["Ports"]=set([tPort])
                else:
                    #update
                    #print "updating IP"
                    sshIp[ip][sDate]["Attempts"]=sshIp[ip][sDate]["Attempts"]+1
                    #uncomment out following lines to save verbose logs...
                    #sshIp[ip][sDate]["Users"].add(tUser)
                    #sshIp[ip][sDate]["Ports"].add(tPort)
                    
    #consider saving output as an interim/debug step?
    lclFileName = os.path.join(outDir, 'sumLog_'+ip+'.json')
    print "wriiting out file"
    lclFile = open(lclFileName,'w')
    lclFile.write(json.dumps(sshIp[ip], indent=4, sort_keys=True))
    lclFile.close()
    
    #raise('oops')
lclFileName = os.path.join(r'/data/summary', 'sumLog_All.json')
print "wriiting out file"
lclFile = open(lclFileName,'w')
lclFile.write(json.dumps(sshIp, indent=4, sort_keys=True))
lclFile.close()


print "Done!"
