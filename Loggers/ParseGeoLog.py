inFile = '/data/tmpImg/runLog.txt'

outFile = '/data/tmpImg/geoPhoto_gcp.gcp'

f = open(inFile,'r').readlines()

of = open(outFile,'w')

newLines = f[1:]

for line in newLines:
    temp = line[:-1].split(',')
    outStr = temp[0]+' '+temp[-3][:9]+' '+temp[-2][:10]+' '+temp[-1]+'\n'
    #print outStr
    of.write(outStr)
    #break
of.close()

print "Done!"
