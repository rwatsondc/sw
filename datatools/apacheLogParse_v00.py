import os, re, datetime, pprint, json

walkdir = r'/data/raw/apachelogs'
logwalk = os.walk(walkdir)

logList = []

for root, subs, files in logwalk:
    for fle in files:
        logList.append(os.path.join(root, fle))

"""
IP address:
    Date:
        Number of hits:#
        http codes:
            code:#

json example:

{
  "192.168.1.1":{
    "1-1-15":{
      "Hits":24,
      "http-codes":{
        "200":15,
        "304":7,
        "500":2
      }
    }
  }
  
}
"""
#re patterns
ipPat = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
#note - will need to remove trailing ":" from date results
datePat = r'\d*\/.*\/\d{4}:'
httpPat = r' \d{3} '

#date time conversion
#test = '16/Dec/2014'
#t1 = datetime.datetime.strptime(test, '%d/%b/%Y')
#str(t1.date())

logDict = {}

#used for debug
debugLoop = False
stopLoop = 3
breakCount = 0
printUpdate = 100

for log in logList:
    print "parsing", log
    breakCount = breakCount + 1
    if breakCount > stopLoop:
        if debugLoop:
            break
        else:
            pass
    lclip = re.findall(ipPat, log)[0]
    lclCount = 0
    if lclip not in logDict.keys():
        #init ip entry
        logDict[lclip]={}
    f = open(log,'r').readlines()
    lineCount = 0
    for line in f:
        lineCount = lineCount + 1
        if lineCount%printUpdate==0:print "parsed", lineCount, "lines..."
        lDateRaw = re.findall(datePat,line)[0][:-1]
        lDateTime = datetime.datetime.strptime(lDateRaw, '%d/%b/%Y')
        lDateNew = str(lDateTime.date())
        lCode = re.findall(httpPat,line)[0]
        #update dictionary
        if lDateNew not in logDict[lclip].keys():
            #init date entry
            logDict[lclip][lDateNew]={}
            logDict[lclip][lDateNew]["Hits"]=1
            logDict[lclip][lDateNew]["Codes"]={}
        else:
            logDict[lclip][lDateNew]["Hits"]=logDict[lclip][lDateNew]["Hits"]+1
        
        if lCode not in logDict[lclip][lDateNew]["Codes"].keys():
            #init new http code counter
            logDict[lclip][lDateNew]["Codes"][lCode]=1
        else:
            logDict[lclip][lDateNew]["Codes"][lCode]=logDict[lclip][lDateNew]["Codes"][lCode]+1
    #print out local results
    tDir = r'/data/summary/apachelogs'
    lclFileName = os.path.join(tDir, 'apacheHits_'+lclip+'.json')
    print "wriiting out file"
    lclFile = open(lclFileName,'w')
    lclFile.write(json.dumps(logDict, indent=4, sort_keys=True))
    lclFile.close()    
    #break

lclFileName = os.path.join(r'/data/summary', 'apacheHits_All.json')
print "wriiting out file"
lclFile = open(lclFileName,'w')
lclFile.write(json.dumps(logDict, indent=4, sort_keys=True))
lclFile.close()

print "Done!"
