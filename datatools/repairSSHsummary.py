#rebuild master summary json file from component parts
#save as alternate file name

import os, csv, json, pprint, re

reIpPat = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

walkdir = os.walk(r'/data/summary/sshlogs')

ipList = []
logList = []

for root, subs, files in walkdir:
    for fle in files:
        logList.append(os.path.join(root, fle))

rebuildDict = {}

for jsonFile in logList:
    print "rebuilding", jsonFile
    ip = re.findall(reIpPat, jsonFile)[0]
    stage = open(jsonFile,'r').read()
    rebuildDict[ip]=json.loads(stage)
    
lclFileName = os.path.join(r'/data/summary', 'sumLog_sshAll.json')
print "wriiting out file"
lclFile = open(lclFileName,'w')
lclFile.write(json.dumps(rebuildDict, indent=4, sort_keys=True))
lclFile.close()    
        
