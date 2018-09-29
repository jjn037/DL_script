# -*- coding: utf-8 -*
import csv, os, json, re, cv2
import xml.etree.cElementTree as ET
import sys 
reload(sys) 
sys.setdefaultencoding( "utf-8" )

img_root = ""
output_dir = "./business_licence_crop3"
# csv_reader = csv.reader(open("business_licence1.csv"))
csv_file = "a.csv"

map_list = ["","key","value"] 

with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            imageFileName = row["file_key"]

            # if os.path.exists(imagePath) and len(lines) >= 10:
            #             print imageFileName
            root = ET.Element("annotation")
            ET.SubElement(root, "folder").text = "Business Licence"
            ET.SubElement(root, "filename").text = imageFileName

            source = ET.SubElement(root, "source")
            ET.SubElement(source, "dataset").text = "Business Licence 2018"
            # ET.SubElement(source, "id").text = data['image']['id']


            owner = ET.SubElement(root, "owner")
            ET.SubElement(owner, "name").text = "Di Di AI Labs"

            size = ET.SubElement(root, "size")

            img_path = os.path.join(img_root, )
            img = cv2.imread(img_path, imageFileName)

            height, width = img.shape[0], img.shape[1]
            
            ET.SubElement(size, "width").text = str(width)
            ET.SubElement(size, "height").text = str(height)
            ET.SubElement(size, "depth").text = '3'

            ET.SubElement(root, "segmented").text = '0'
            try:
                lines = json.loads(row["Result:label"])
            except:
                print(imageFileName)
                continue
            # print(len(lines))
            for line in lines:
                obj = ET.SubElement(root, "object")
                # index = re.search(r'\d+', line['label'])
                # index = int(re.findall('(\w*[0-9]+)\w*', line['label'])[0]) if len(re.findall('(\w*[0-9]+)\w*', line['label']))>0 else 0
                # print(index)
                # if index not in range(1,3):
                #     print(imageFileName)
                #     break

                # _label = map_list[index] if index in range(0,3) else ""
                _label = line['label']
                _i = _label.lower().strip()
                _i = ''.join(_i.split())
                if _i in ("kalue", "v","e", "xalue", "valuevalue","velue", "valeu","vaue", "vlue","valuev","vakue", "valye","valey","vslue","alue", "valur","vaalue"):
                    _i = "value"
                if _i in ("keykey", "key'", "keyv", "keye", "ey","keu","kley","kay"):
                    _i = "key"
                # print("label: {}".format(_label))
                # _label = _label.lower().strip()
                # _label = ''.join(_label.split())
                ET.SubElement(obj, "name").text = _i
                ET.SubElement(obj, "pose").text = 'Left'
                ET.SubElement(obj, "truncated").text = '1'
                ET.SubElement(obj, "difficult").text = '0'
                # ET.SubElement(obj, "content").text = line['attributes']['content']['value']

                box = ET.SubElement(obj, "bndbox")

                xmin = int(line['left']) if int(line['left'])>0 else 0
                ymin = int(line['top']) if int(line['top'])>0 else 0
                ET.SubElement(box, "xmin").text = xmin
                ET.SubElement(box, "ymin").text = ymin
                xmax = int(int(line['left']) + float(line['width']) * float(line['scaleX']))
                ymax = int(int(line['top']) + float(line['height']) * float(line['scaleY']))

                _xmax = xmax if xmax<width else width
                _ymax = ymax if ymax<height else height

                ET.SubElement(box, "xmax").text = str(_xmax)
                ET.SubElement(box, "ymax").text = str(_ymax)

            xmlFileName = imageFileName.split('.')[0] + ".xml"
            xmlPath = os.path.join(output_dir, xmlFileName)
            xml = ET.ElementTree(root)
            xml.write(xmlPath)