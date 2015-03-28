import json, urllib2, geocoder, datetime
import numpy as np
import matplotlib.pyplot as plt

#from http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle
#SO code ends here

def simpVector(origin, dest):
    return [dest[0]-origin[0], dest[1]-origin[1]]

inFile = r'/data/working/access2.master.log.date.json'

inData = json.loads(open(inFile,'r').read())

#grab your own IP address
resp = urllib2.urlopen('http://bot.whatismyipaddress.com/')
localIP = resp.read()

print localIP

g = geocoder.freegeoip(localIP)
localX = g.json['lng']
localY = g.json['lat']

originPnt = [localX, localY]

#Now you're ready to graph

loopEnd = 500000
loopCount = 0
filter = 0

#programatically determine max count, later...
maxCount = 200
#colorPlot{"200":'g',}


#set up plot area...
ax = plt.subplot(polar=True)

for key in inData:
    #skip your own IP address...
    if key.split(':')[0]==localIP:
        pass
        #continue
    if inData[key]['count']>filter:
        loopCount = loopCount + 1
        if loopCount > loopEnd:
            pass
            #break
        #construct dest vector
        destPnt = [inData[key]['x'],inData[key]['y']]
        destVector = simpVector(originPnt, destPnt)
        #correct for right-northed bias of matplotlib graph
        v0 = [1.0,0.0]
        v1 = destVector
        #direction of location from you
        curTheta = angle_between(v0, v1)
        #convert count to angular width, start in degrees
        degWidth = np.interp(inData[key]['count'],[0,maxCount],[5,90])
        thWidth = np.deg2rad(degWidth/2.0)
        #account for 'sweep' of width
        curTheta = curTheta + thWidth
        """
        print np.rad2deg(curTheta)
        print destVector
        print destPnt[1],',',destPnt[0]
        """
        #next figure out bottom, radius from time
        minTime = datetime.datetime.strptime(inData[key]['minTime'],"%Y-%m-%d %H:%M:%S")
        maxTime = datetime.datetime.strptime(inData[key]['maxTime'],"%Y-%m-%d %H:%M:%S")
        curTime = datetime.datetime.now()
        print minTime, maxTime
        
        #radius logic
        """
radius = 0 is now
curTime - maxTme = bottom
curTime - minTime = radius
        """
        #color logic:
        if inData[key]['code'][:2]=='20':
            color='g'
        elif inData[key]['code'][:2]=='30':
            color = 'y'
        elif inData[key]['code'][:2]=='40':
            color='r'
        else:
            color='b'
            
        bottom = (curTime-maxTime).days -1.5
        #radius is measure from bottom, not center, set to 1 for 1 day
        radius = 3
        print bottom, radius
        
        print "new plot segment"
        bars = ax.bar(curTheta,radius, width=thWidth, linewidth=0, color=color,bottom=bottom, alpha=0.6)
        #break
#plt.axis('off')
#bars = ax.bar(curTheta,5,bottom=5, alpha=0.6)

plt.show()



print "Done!"
