# author:Jiang Yi
# delete duplicate images by averge_hash

import imagehash
from PIL import Image


def getKey(item):
    return item[0]


imglist = open('imglist', 'r').read().split('\n')
output = open('deduplist', 'w')

imglist.pop(-1)  # delete the last element

num = len(imglist)
remove = [False] * num
sorted_list = []
for i in range(num):
    path = imglist[i]
    hash = int(str(imagehash.average_hash(Image.open(path))), 16)
    sorted_list.append([hash,i])
    if i%10000==0:
        print i

sorted_list.sort(key=getKey)


output.write(imglist[sorted_list[0][1]]+'\n')
for i in range(1,num):
    if sorted_list[i][0] != sorted_list[i-1][0]:
        output.write(imglist[sorted_list[i][1]]+'\n')
