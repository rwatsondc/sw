inNvm = '/data/GeoScene1.nvm'

outCsv = '/data/geoNvm.txt'


inData = open(inNvm,'r').readlines()
outData = open(outCsv,'w')

inCameras = inData[3:231]

inCloud = inData[240:700]

outData.write('Type,X,Y\n')
print 'Type,X,Y\n'
for i in inCameras:
    tI = i.split('\t')
    name = tI[0]
    data = tI[1].split(' ')
    outStr = ','.join(["camera",data[-6],data[-5]])+'\n'
    outData.write(outStr)
    #print outStr
    #break

for i in inCloud:
    tI = i.split(' ')
    outStr = ','.join(['cloud',tI[0],tI[1]])+'\n'
    outData.write(outStr)
    #print outStr
    #break

outData.close()
print "Done!"
