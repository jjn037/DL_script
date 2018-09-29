#coding=utf-8
import xml.etree.cElementTree as et
import cv2
import numpy as np

img = cv2.imread('1.jpg')

tree=et.parse("business_licence_anno1/1.xml")
root=tree.getroot()

filename=root.find('filename').text
print (filename)
i=0
for Object in root.findall('object'):
    name=Object.find('name').text
    print (name)
    bndbox=Object.find('bndbox')
    pts = list()
    xmin =  bndbox.find('xmin').text
    ymin =  bndbox.find('ymin').text
    xmax=  bndbox.find('xmax').text
    ymax =  bndbox.find('ymax').text
    # pt = bndbox.find('pt')
    cv2.rectangle(img, (int((xmin)), int((ymin))), (int((xmax)), int((ymax))), (0,255,0), 2)
    cv2.imshow('src',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # if(i==2):
    #     break
    # i+=1
cv2.imwrite('image.jpg',img)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite('bb.jpg', img)