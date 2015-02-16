import os

walkDIR = os.walk(r'/home/ipLogs')

fileList = []

for root, subs, files in walkDIR:
    for fle in files:
        fileList.append(os.path.join(root, fle))

