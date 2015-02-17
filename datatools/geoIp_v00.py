"""
#see http://geocoder.readthedocs.org/en/latest/providers/FreeGeoIP/
import geocoder

testIp = '69.255.132.71'

g = geocoder.freegeoip(testIp)

print "Done!"
"""

import os, re, geocoder, json

#gather up all IP addresses
rePat = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

ipSet = set()

sshwalk = os.walk(r'/data/summary/sshlogs')
print "walking ssh logs"
for root, subs, files in sshwalk:
    for fle in files:
        ipSet.add(re.findall(rePat,fle)[0])

apachewalk = os.walk(r'/data/raw/apachelogs')
print 'walking apache logs'
for root, subs, files in apachewalk:
    for fle in files:
        ipSet.add(re.findall(rePat,fle)[0])

print "number of IPs to geolocate:", len(ipSet)

outjson = r'/data/reference/geo/geoip.json'
geoDict = {}

print "geocoding IP addresses"

loopCount = 0

for ip in ipSet:
    loopCount = loopCount + 1
    if loopCount%20==0:print loopCount, "records geocoded..."
    g =geocoder.freegeoip(ip)
    geoDict[ip]=g.json
    #break

print "wriiting out file"
lclFile = open(outjson,'w')
lclFile.write(json.dumps(geoDict, indent=4, sort_keys=True))
lclFile.close()
    

print "Done!"
