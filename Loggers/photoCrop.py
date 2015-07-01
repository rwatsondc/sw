import os
from PIL import Image


inDir = '/data/tmpImg'
outDir = '/data/ManyTurnsImagery'

testFile = '/data/tmpImg/testImg00340.jpg'


allFiles = os.listdir(inDir)
iFiles = [x for x in allFiles if x[-4:]=='.jpg']

for imFile in iFiles:
    im = Image.open(inDir+'/'+imFile)
    w, h = im.size
    im.crop((342,0,w,h)).save(outDir+'/'+imFile)
    #break
    #im.show()

print "Done!"
