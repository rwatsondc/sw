"""
This script is intended to provide suitable mapping
data based on summary results parsed from ssh and
apache logs and reference geo-data obtained via geocoder
"""
import os, csv, json, pprint


sshLogJSON = r'/data/summary/sumLog_sshAll.json'
apacheLogJSON = r'/data/summary/apacheHits_All.json'
geoLkUpJSON = r'/data/reference/geo/geoip.json'

outCSVfile = r'/data/summary/ip_ssh.csv'

#debug...
debugLoop = False
breakCount = 0
breakLimit = 20


outCSV = open(outCSVfile,'wb')
csvWriter = csv.writer(outCSV)



#out table format:
"""
IP Address
Lat
Lon
country
Type:{ssh, apache}
hits total
hits suspect
"""

testIP = '111.74.238.15'
#set up geoLkUp
geoLkUp = json.loads(open(geoLkUpJSON,'r').read())


#test geo lookups
lLat = geoLkUp[testIP]["lat"]
lLon = geoLkUp[testIP]["lng"]
lCountry = geoLkUp[testIP]["country"]

#map apache Logs, they're smaller...
apacheLog = json.loads(open(apacheLogJSON,'r').read())



#first round, group by date
print "[lclIp,lLat,lLon,gglStr,lCountry,sumHits, 'apache']"
print "\napache records\n"

header = ['ip_addr','lat','lon','xy_pair','country','hits','type']

csvWriter.writerow(header)


"""

for aplog in apacheLog:
    breakCount = breakCount + 1
    if breakCount%100==0:print "written", breakCount, "rows..."
    if breakCount > breakLimit and debugLoop:
        break
    #store geodata
    lclIp = aplog
    lLat = geoLkUp[aplog]["lat"]
    lLon = geoLkUp[aplog]["lng"]
    gglStr = str(geoLkUp[aplog]["lat"])+', '+str(geoLkUp[aplog]["lng"])
    lCountry = geoLkUp[aplog]["country"]
    sumHits = 0
    #store apache data
    for date in apacheLog[aplog].keys():
        sumHits = sumHits + apacheLog[aplog][date]["Hits"]
    outRow = [lclIp,lLat,lLon,gglStr,lCountry,sumHits, 'apache']
    outRow = [x.encode('ascii', 'ignore') if type(x)==type(u'str') else x for x in outRow]
    csvWriter.writerow(outRow)
    if debugLoop:print(str(outRow))

del apacheLog
"""
sshLog = json.loads(open(sshLogJSON,'r').read())

outCSV.flush()

print "\nssh records:\n"
if debugLoop:breakCount = 0

try:
    print sumHits
except:
    print "no sumHits..."

for ssh in sshLog:
    if breakCount%100==0:print "written", breakCount, "rows..."
    breakCount = breakCount + 1
    if breakCount > breakLimit and debugLoop:
        break
    #handle missing data...
    if u'status' in geoLkUp[ssh].keys():
        if geoLkUp[ssh]['status'] == u'ERROR - No results found':
            lLat = ''
            lLon = ''
            gglStr = ''
            lCountry = ''
        else:
            #store geodata
            lclIp = ssh
            lLat = geoLkUp[ssh]["lat"]
            lLon = geoLkUp[ssh]["lng"]
            gglStr = str(geoLkUp[ssh]["lat"])+', '+str(geoLkUp[ssh]["lng"])
            lCountry = geoLkUp[ssh]["country"]

    sumHits = 0
    if debugLoop:print sumHits
    #store ssh data:
    for date in sshLog[ssh].keys():
        if debugLoop:print sumHits
        sumHits = sumHits + sshLog[ssh][date]["Attempts"]
    outRow = [lclIp,lLat,lLon,gglStr,lCountry,sumHits, 'ssh']
    outRow = [x.encode('ascii', 'ignore') if type(x)==type(u'str') else x for x in outRow]
    csvWriter.writerow(outRow)
    if debugLoop:print(str(outRow))

outCSV.close()

print "Done!"
