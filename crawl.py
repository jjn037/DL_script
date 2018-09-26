# -*- coding=utf-8 -*-
import requests as req
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os
from skimage import io
import numpy as np
import urllib
import cv2, csv


# url = 'https://img0.didiglobal.com/static/zhuancheimg/upload/rooster20180712/650910887310323920211ece10ba7a46840fa58ee3fa976/13b0a235b64031fc793d3cdc68c5c24e2cad1eef'
f_path = 'gouwei20180913171703.csv'

f = open(f_path) 
i=0

with open(f_path, "r") as f:
    reader = csv.reader(f)
    images = [row for row in reader]

print len(images)
if not os.path.exists("images"):
    os.mkdir("images")
for i in range(len(images)):
	if len(images[i]) == 0:
		print i,"empty"
		continue
	url = images[i][0]
	# print url
	if i<7989 :
		continue
	print (u"正在处理第%d张图片..." % (i+1))
	# img_src = img.get('src')
	# if img_src.startswith("http"):
	try:
		resp = urllib.urlopen(url)
		image = np.asarray(bytearray(resp.read()), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
		# try:
		w,h = image.shape[:2]
	except:
		print url
		continue
	# print(w,h)

	img_path = "images/" + str("%05d"%(i)) + ".jpg"
	i=i+1
	if w>=200 and h>200:
		cv2.imwrite(img_path, image)
		cv2.waitKey(3000)

    
print (u"处理完成")
file.close()