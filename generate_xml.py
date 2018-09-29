# coding=utf-8
import os,sys
import glob
import json
import numpy as np
import xml.etree.cElementTree as ET

reload(sys) 
sys.setdefaultencoding("utf8")

# label_dir = "/Users/lairf/Documents/RefineData/OcrTestLabelElse/"
# image_dir = "/Users/lairf/Documents/RefineData/OcrTestDataElse/"
# output_dir = "/Users/lairf/Documents/RefineData/xml/"

label_dir = "/home/Myproject/tf-faster-rcnn/data/Detection2017/label/"
image_dir = "/home/Myproject/tf-faster-rcnn/data/Detection2017/Detect2017/JPEGImages/"
output_dir = "/home/Myproject/tf-faster-rcnn/data/Detection2017/Detect2017/Annotations/"
global enumerate
num=0
in_path = label_dir +  "*.json"
for json_file in glob.glob(in_path):
    with open(json_file) as file:
        text = file.read().decode("utf-8").strip()
        data = json.loads(text)
        imageFileName = data['image']['rawFilename']
        imagePath = image_dir + imageFileName
        try:
            lines = data['objects']['ocr'][0]['polygonList']
            if os.path.exists(imagePath) and len(lines) >= 1:
                #print imageFileName
                num+=1
                if num%1000==0:
                    print(num)

                root = ET.Element("annotation")
                ET.SubElement(root, "folder").text = "Detect2017"
                ET.SubElement(root, "filename").text = imageFileName

                source = ET.SubElement(root, "source")
                ET.SubElement(source, "dataset").text = "Detection 2017"
                ET.SubElement(source, "id").text = data['image']['id']


                owner = ET.SubElement(root, "owner")
                ET.SubElement(owner, "name").text = "Linkface"

                size = ET.SubElement(root, "size")
                ET.SubElement(size, "width").text = str(data['image']['width'])
                ET.SubElement(size, "height").text = str(data['image']['height'])
                ET.SubElement(size, "depth").text = '3'

                ET.SubElement(root, "segmented").text = '0'

                #f0 = Res['objects']['ocr'][0]['polygonList']
                for line in lines:
                    obj = ET.SubElement(root, "object")
                    ET.SubElement(obj, "name").text = 'text'
                    ET.SubElement(obj, "pose").text = 'Left'
                    ET.SubElement(obj, "truncated").text = '1'
                    ET.SubElement(obj, "difficult").text = '0'
                    # ET.SubElement(obj, "content").text = line['attributes']['content']['value']

                    box = ET.SubElement(obj, "bndbox")
                    x0 = line[0]['x']
                    y0 = line[0]['y']
                    x1 = line[1]['x']
                    y1 = line[1]['y']
                    x2 = line[2]['x']
                    y2 = line[2]['y']
                    x3 = line[3]['x']
                    y3 = line[3]['y']
                    pts = np.array([[x0, y0], [x1, y1], [x2, y2], [x3, y3]], np.int32)
                    xmin = min(pts[:, 0])
                    xmax = max(pts[:, 0])
                    ymin = min(pts[:, 1])
                    ymax = max(pts[:, 1])

                    ET.SubElement(box, "xmin").text = str(xmin)
                    ET.SubElement(box, "ymin").text = str(ymin)
                    ET.SubElement(box, "xmax").text = str(xmax)
                    ET.SubElement(box, "ymax").text = str(ymax)

                xmlFileName = imageFileName[:-3] + "xml"
                xmlPath = output_dir + xmlFileName
                xml = ET.ElementTree(root)
                xml.write(xmlPath)
        except:
            os.remove(imagePath)
            os.remove(json_file)
