# -*- coding: utf-8 -*-
"" "  not for multy object"""
import numpy as np
import os
import cv2
import xml.etree.ElementTree as ET

save_path = "/nfs/project/jiangjianan/tf-faster-rcnn-master/data/err_img"
det_file_path = "/nfs/project/jiangjianan/OCR/dataset/results/LicenseTextDet/Main/comp4_1537324405877_det_test_value.txt"
img_path = "/nfs/project/jiangjianan/OCR/dataset/LicenseTextDet/JPEGImages"
xml_path = "/nfs/project/jiangjianan/OCR/dataset/LicenseTextDet/Annotations"
_label = "value"


def IoU(rec1, rec2):
    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

    # computing the sum_area
    sum_area = S_rec1 + S_rec2

    # find the each edge of intersect rectangle
    left_line = max(rec1[1], rec2[1])
    right_line = min(rec1[3], rec2[3])
    top_line = max(rec1[0], rec2[0])
    bottom_line = min(rec1[2], rec2[2])

    # judge if there is an intersect
    if left_line >= right_line or top_line >= bottom_line:
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        return intersect / (sum_area - intersect)


def GT_BOX(xml_path):
    tree = ET.parse(xml_path)
    # print(xml_path)
    objs = tree.findall('object')
    boxes = np.zeros(4, dtype=np.uint16)
    # Load object bounding boxes into a data frame.
    for ix, obj in enumerate(objs):
        _i = obj.find('name').text.lower().strip()
        # print(_i, type(_i))
        if _i in ("kalue", "v", "xalue"):
            _i = "value"
        if(_i==_label):
            bbox = obj.find('bndbox')
            # Make pixel indexes 0-based
            x1 = float(bbox.find('xmin').text)
            y1 = float(bbox.find('ymin').text)
            x2 = float(bbox.find('xmax').text)
            y2 = float(bbox.find('ymax').text)
            return np.array([x1, y1, x2, y2])
    return boxes


if __name__ == '__main__':
    det_file = open(det_file_path)
    err_imgs = []
    i=0
    for line in det_file.readlines():
        line = line.strip()
        l = line.split(" ")
        det_bbox = np.array([float(l[2]), float(l[3]), float(l[4]), float(l[5])])
        _img_path = os.path.join(img_path, l[0]+'.jpg')
        _xml_path = os.path.join(xml_path, l[0]+'.xml')
        print _xml_path
        gt_bbox = GT_BOX(_xml_path)
        # print(det_bbox,"+++++++=======++++++", gt_bbox)

        iou = IoU(det_bbox, gt_bbox)
        if(iou<0.7):
             err_imgs.append(_img_path)
             im = cv2.imread(_img_path)
             color = (255, 0, 0)
             cv2.rectangle(im, (int(det_bbox[0]), int(det_bbox[1])), (int(det_bbox[2]), int(det_bbox[3])), color, 2)
             color = (0, 255, 255)
             cv2.rectangle(im, (int(gt_bbox[0]), int(gt_bbox[1])), (int(gt_bbox[2]), int(gt_bbox[3])), color, 2)
             save_img_path = os.path.join('/nfs/project/jiangjianan/tf-faster-rcnn-master/data/err_img', l[0].split('/')[-1] + ".jpg")
             i+=1
             cv2.imwrite(save_img_path, im)
             print(save_img_path, iou)
             print(det_bbox, "=+++++++++++======++++++++", gt_bbox)

    # im = cv2.imread('/nfs/project/jiangjianan/tf-faster-rcnn-master/data/license/JPEGImages/s1/7150.jpg')
    # color = (255, 0, 0)
    # cv2.rectangle(im, (41, 991), (194, 1140), color, 2)
    # cv2.imwrite('/nfs/project/jiangjianan/tf-faster-rcnn-master/data/a.jpg', im)