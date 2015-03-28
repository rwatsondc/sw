#step 1 demo a polar plot
"""
using
http://matplotlib.org/examples/pie_and_polar_charts/polar_bar_demo.html
as a starting point
"""
import json, urllib2, geocoder
import numpy as np
import matplotlib.pyplot as plt


inFile = r'/data/working/access2.master.log.json'

inData = json.loads(open(inFile,'r').read())

#grab your own IP address
resp = urllib2.urlopen('http://bot.whatismyipaddress.com/')
localIP = resp.read()

print localIP
g = geocoder.freegeoip(localIP)
localX = g.json['lng']
localY = g.json['lat']

#filter largest IP hits for testing

for ip in inData:
    if inData[ip]['count']>20:
        print ip, inData[ip]['count']
        print inData[ip]['x'],', ', inData[ip]['y']
        break

print "local", localX, localY

#define some trig functions
print "vector is ", inData[ip]['x']-localX, inData[ip]['y']-localY

v1 = [inData[ip]['x']-localX, inData[ip]['y']-localY]
#since graph naturally has 0 degrees (i.e. North) to the right, scale vector accordingly
v0 = [1,0]
#from http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle

print "angle is", angle_between(v0,v1)

#raise('oops')

"""
N = 15
theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
radii = 10 * np.random.rand(N)
width = np.pi / 4 * np.random.rand(N)

ax = plt.subplot(111, polar=True)
bars = ax.bar(theta, radii, width=width, bottom=0.0)

# Use custom colors and opacity
for r, bar in zip(radii, bars):
    bar.set_facecolor(plt.cm.jet(r / 10.))
    bar.set_alpha(0.5)
"""

degrees = [30, 60, 90, 180]
theta = [angle_between(v0,v1)]
radii = range(len(degrees))
width = 1

ax = plt.subplot(polar=True)
#bars = ax.bar(theta, radii, width=1, color='g')
#need to figure out how width impacts angle, it sweeps arond instead of being centered...
#width is probably in radians, so edit angle half with?

bars = ax.bar(theta,16, width=0.1, color='r',bottom=5)

#remove markup
#plt.axis('off')

plt.show()
