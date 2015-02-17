"""
This is an experiment using matplotlib, the idea is to create
some interesting 'data driven art' for my web page derived from
some summary log information.

Variations on a Theme:
Try a non-cartographic map with algorithm controlled rendering.  i.e.
just plot lat/lon as xy and use hits/ip for color and size

create a network map:
multiple versions possible including
hierarchical clustering of networks
full permutation sets with rendering weghted by distance
non-geographic network, likely requires a python network rendering package


some thoughts:
size = hits
rgb color & aplha = scaled based on ip4
xy = lat/lon with possible scaling
"""

import matplotlib, csv

inApLog = r'/data/ip_apache.csv'

f = open(inApLog,'r').readlines()

header = {}
header["ip"]=0
header['y']=1
header["x"]=2
header['hits']=5

def rgbaPick(inString):
    r,g,b,a=[int(x) for x in inString.split('.')]


print "Done!"
