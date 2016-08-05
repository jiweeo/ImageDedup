#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import imagehash
from PIL import Image
import cv2
import os
def getKey(item):
    return item[0]

class processHash (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print "Starting thread "+str(self.threadID)
        index = self.threadID
        while index<img_num:
            if index%1000==0:
                print index
            path = imglist[index]
            error = False

            threadLock.acquire()  # get lock
            try:
                img = cv2.imread(path)
                cv2.imshow('img',img)
            except:
                error = True
            threadLock.release()  # release thread lock

            if not error:
                hash = int(str(imagehash.average_hash(Image.open(path))), 16)
                threadLock.acquire()  # get lock
                sorted_list.append([hash,index])
                threadLock.release()#release thread lock

            index+=Thread_Num


#input imglist
imglist = open('imglist', 'r').read().split('\n')
imglist.pop(-1)  # delete the last element
sorted_list = []
img_num = len(imglist)
#multi-threading
Thread_Num = 10
threadLock = threading.Lock()
threads = []
for i in range(Thread_Num):
    thread = processHash(i)
    threads.append(thread)
    thread.start()

# wait for all threads finishing
for t in threads:
    t.join()
print 'Hash finished'

sorted_list.sort(key=getKey)

if not (os.path.isdir('result')):
    os.mkdir('result')
count = 0
fnum = 1
os.mkdir('result/1')
print len(sorted_list)
for i in range(1,len(sorted_list)):
    if sorted_list[i][0]!=sorted_list[i-1][0]:
        path = imglist[sorted_list[i][1]]
        newpath = 'result/'+str(fnum)+'/'
        os.system('mv "'+path+'" ' +newpath)
        count+=1
        if count==1000:
            count = 0
            fnum+=1
            os.mkdir('result/'+str(fnum))



