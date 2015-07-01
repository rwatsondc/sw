import cv, time, datetime, sys
from Phidgets.Devices.GPS import GPS


saveDir='/data/tmpImg'

logFile = open('/data/tmpImg/runLog.txt','w')

gps = GPS()
gps.openPhidget()
gps.waitForAttach(10000)
gps_time = gps.getTime().toString()




capture = cv.CaptureFromCAM(0)
cv.SetCaptureProperty(capture, 3, 1280)
cv.SetCaptureProperty(capture, 4, 720)

header = 'imgName,curTime,elpTime,gps_time,gps_vel, gps_heading, gps_lon,gps_lat,gps_alt\n'
logFile.write(header)

for i in range(2000):
    #print 1
    curTime = str(datetime.datetime.now())
    imgName = 'testImg'+str(i).zfill(5)+'.jpg'
    img = cv.QueryFrame(capture)
    #print 2
    #cv.ShowImage("camera", img)
    cv.SaveImage(saveDir+'/'+imgName, img)
    #print 3
    #gps stuff...
    gps_time = gps.getTime().toString()
    gps_lat = gps.getLatitude()
    gps_lon = gps.getLongitude()
    gps_alt = gps.getAltitude()    
    gps_heading = gps.getHeading()
    gps_vel = gps.getVelocity()
    elpTime = str(datetime.datetime.now())
    outList = [imgName,curTime,elpTime,gps_time,gps_vel, gps_heading, gps_lon,gps_lat,gps_alt]
    outList = [str(x) for x in outList]
    outStr = ','.join(outList)+'\n'
    print 'Iteration:', i, str(curTime), gps_lon,gps_lat,gps_alt
    logFile.write(outStr)
    #time.sleep(0.1)
    
logFile.close()
    


print "Done"
