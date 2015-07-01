"""
This is a scripting sandbox for determining best methods for
linking async gps coorindates to photos based on log files
and using sysTime as a common key.
"""

import os, datetime, calendar, bisect
from matplotlib import pyplot as plt

def str2Time(inStr):
    #datetime format:
    #datetime.datetime.strptime(tTimeStr, "%Y-%m-%d %H:%M:%S.%f")
    inStr = inStr.lstrip()
    inStr = inStr.rstrip()
    return datetime.datetime.strptime(inStr, "%Y-%m-%d %H:%M:%S.%f")

def unix2Datetime(d):
    return calendar.timegm(d.timetuple())

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0


#use data logged after or during run5, all previous data is pre-linked or not worth it

inFolder = r"/data/geoPhotos/run5/imgs_6_27_2015_0"

newLookUp = r'/data/geoPhotos/run5/data.txt'
outData = open(newLookUp,'w')


inGpsPath = os.path.join(inFolder, "Gps.log")
inCamPath0 = os.path.join(inFolder, "Cam0.log")
inCamPath1 = os.path.join(inFolder, "Cam1.log")

inGps = [x[:-1].split(',') for x in open(inGpsPath,'r').readlines()]
inCam0 = [x[:-1].split(',') for x in open(inCamPath0,'r').readlines()]
inCam1 = [x[:-1].split(',') for x in open(inCamPath1,'r').readlines()]

#make a graph to figure out relationship between cameras and gps times


#need to account for corupt abrubt data errors

#pntsGps = [unix_time(str2Time(x[0]))for x in inGps[1:]]
pntsGps = []
for x in inGps[1:]:
    try:
        pntsGps.append(unix_time(str2Time(x[0])))
    except:
        break

#pntsCam0 = [unix_time(str2Time(x[1])) for x in inCam0]
pntsCam0 = []
for x in inCam0:
    try:
        pntsCam0.append(unix_time(str2Time(x[1])))
    except:
        break
    
#pntsCam1 = [unix_time(str2Time(x[1])) for x in inCam1]
pntsCam1 = []
for x in inCam1:
    try:
        pntsCam1.append(unix_time(str2Time(x[1])))
    except:
        break

#use bisect to match cam points to gps points?
#http://stackoverflow.com/questions/8162379/python-locating-the-closest-timestamp
#bisect.bisect_left(pntsGps, pntsCam0[55])
#should return 150, what that really means is pntsGps[149] is the closest value to the input!

#test matching cam0 to gps
"""
def testFuncl(value, inList):
    lIdx = bisect.bisect_left(inList, value)
    #rIdx = bisect.bisect_right(inList, value)
    return inList[lIdx]

def testFuncr(value, inList):
    #lIdx = bisect.bisect_left(inList, value)
    rIdx = bisect.bisect_right(inList, value)
    return inList[rIdx]
"""
def minDiff(value, inList):
    idx = bisect.bisect_right(inList, value)
    #check 2 below, 2 after, and the actual value
    testVals = {}
    for i in range(idx-2, idx+3):
        testVals[abs(inList[i]-value)]=i
    #return inList[testVals[min(testVals.keys())]]
    return testVals[min(testVals.keys())]
    

#now do the hard work...

gpsHeader = inGps[0]
#strip spaces from header
gpsHeader = [x.strip() for x in gpsHeader]
#add image name to index
gpsHeader.append('imgName\n')
workGps = inGps[1:] #1 to 1 with values in pntsGps
photoSets = [inCam0,inCam1] #1 to 1 with v alues in [pntsCam1, pntsCam0]

#write out header
outData.write(','.join(gpsHeader))
counter1 = 0

#work based on range index...
for i in range(len(pntsCam0)):
    counter1 = counter1+1
    if counter1%100==0:
        print counter1, "points processed"
    lclTime = pntsCam0[i]
    lclPhoto = inCam0[i]
    #get index from minDiff
    gpsIndex = minDiff(lclTime, pntsGps)
    outRow = list(workGps[gpsIndex])
    outRow.append(lclPhoto[0]+'\n')
    
    #write outRow
    outData.write(','.join(outRow))
    
outData.flush()

#now do second set...
for i in range(len(pntsCam1)):
    counter1 = counter1+1
    if counter1%100==0:
        print counter1, "points processed"
    lclTime = pntsCam1[i]
    lclPhoto = inCam1[i]
    #get index from minDiff
    gpsIndex = minDiff(lclTime, pntsGps)
    outRow = list(workGps[gpsIndex])
    outRow.append(lclPhoto[0]+'\n')
    
    #write outRow
    outData.write(','.join(outRow))

outData.close()
print "total photos linked:", counter1


"""
cam0testl = [testFuncl(x,pntsGps) for x in pntsCam0]
cam0testr = [testFuncr(x,pntsGps) for x in pntsCam0]
"""
#cam0min = [minDiff(x,pntsGps) for x in pntsCam0]

#test for double-ups using dict counter

##dictTest = {}
##
##for i in pntsCam0:
##    lVal = testFunc(i, pntsGps)
##    if lVal not in dictTest.keys():
##        dictTest[lVal]= 1
##    else:
##        dictTest[lVal]= dictTest[lVal]+1



"""
#plot work...

fig, ax = plt.subplots()

#ax.convert_yunits(

#gps systime
plt.scatter([0 for x in pntsGps], pntsGps, c='blue')

#cam0 systime
plt.scatter([1 for x in pntsCam0], pntsCam0,c='blue')
plt.scatter([0.5 for x in cam0testl], cam0testl,c='red')
plt.scatter([0.75 for x in cam0testr], cam0testr,c='red')
plt.scatter([0.625 for x in cam0min], cam0min,c='green')

#cam1.systime
plt.scatter([2 for x in pntsCam1], pntsCam1,c='blue')

#handle tick labels?

#yLabels = ax.get_yticks().tolist()
#ax.set_yticklabels([str(datetime.datetime.fromtimestamp(x)) for x in yLabels])



plt.show()
plt.close()

print "this should let you map async values from cam time to gps's sys-time"
print "note, you need to add some smarts to double-check that a neighboring value isn't closer, bisect left/right doesn't round"
"""
print "Done!"

