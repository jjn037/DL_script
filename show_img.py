import cv2
import os
import xml.etree.ElementTree as ET
import pdb

# for img in os.listdir("/home/mi/rotate/"):
#     a, b = os.path.splitext(img)
#     if b == ".jpg":
img = cv2.imread("/Users/didi/Desktop/rotate_imgs/63_60d.jpg")
tree = ET.parse("/Users/didi/Desktop/xmls/63_60d.xml")
# img = cv2.imread("/Users/didi/workspace/OCR/datas/business-licence/license/s1/63.jpg")
# tree = ET.parse("/Users/didi/Desktop/business_licence_anno1/63.xml")

root = tree.getroot()
for box in root.iter('bndbox'):
    x1 = float(box.find('xmin').text)
    y1 = float(box.find('ymin').text)
    x2 = float(box.find('xmax').text)
    y2 = float(box.find('ymax').text)

    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    cv2.rectangle(img, (x1, y1), (x2, y2), [0,255,0], 2)
    cv2.imwrite("test1.jpg", img)
# if 1 == cv2.waitKey(0):
#     pass