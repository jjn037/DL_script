# -*- coding: utf-8 -*-
#######################
# Author: Du XiaoGang #
# Date: 2017.10.16    #
#######################
import subprocess
import os
import shutil
import csv
import json
import argparse
import sys
import cv2
import codecs
import numpy as np

reload(sys)
sys.setdefaultencoding('utf8')
font = cv2.FONT_HERSHEY_SIMPLEX
csv_file = './csv/plateno_point_2018-08-08_03-24-18.csv'
images_dir = './src'
dst_images_dir = './images'
dst_txts_dir = './txts'
dst_vis_dir = './vis'


def load_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='gen the xml')

    parser.add_argument('--csv_file', help='csv data file ',
                        default=csv_file, type=str)
    parser.add_argument('--images_dir', help='image directory',
                        default=images_dir, type=str)

    parser.add_argument('--dst_images_dir', help='dst images directory',
                        default=dst_images_dir, type=str)
    parser.add_argument('--dst_txts_dir', help='dst xmls directory',
                        default=dst_txts_dir, type=str)

    #    if len(sys.argv) < 3:
    #        parser.print_help()
    #        sys.exit(1)

    args = parser.parse_args()
    return args


def fetch_size(image_path):
    img = cv2.imread(image_path)
    return img.shape, img


def corner_valid(x, y, image_size):
    if x < 0:
        x = 0
    else:
        if x > image_size[1]:
            x = image_size[1] - 1

    if y < 0:
        y = 0
    else:
        if y > image_size[0]:
            y = image_size[0] - 1

    return x, y


def is_json(rects_str):
    try:
        json.loads(rects_str)
    except ValueError:
        return False

    return True


if __name__ == "__main__":
    args = load_args()

    with open(args.csv_file, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_file = row['plateno_point']
            cmd = 'wget -P {} {}'
            subprocess.call(cmd.format(images_dir, image_file), shell=True)
            image_name = os.path.split(image_file)[1]
            name_list = os.path.splitext(image_name)

            src_image_file = os.path.join(args.images_dir, image_name)
            dst_image_file = os.path.join(args.dst_images_dir, image_name)

            if not os.path.exists(src_image_file):
                continue

            corners_info = row['Result:1']
            if corners_info == "":
                continue

            image_size, src_image = fetch_size(src_image_file)

            if not is_json(corners_info):
                continue

            corners_list = json.loads(corners_info)
            is_save = False
            corner_result = []
            if len(corners_list) >= 4:
                is_save = True
                vis_image = src_image.copy()
                corner_result = []
                num_bbox = len(corners_list) // 4
                for i in range(num_bbox):
                    oriented_box = []
                    for j in range(i * 4, (i + 1) * 4, 1):
                        corner_idx = int(corners_list[j]['index'])
                        xc = float(corners_list[j]['center_x'])
                        yc = float(corners_list[j]['center_y'])
                        xc = int(xc)
                        yc = int(yc)
                        xc, yc = corner_valid(xc, yc, image_size)
                        corner_result.append((corner_idx, xc, yc))
                        oriented_box.append(xc)
                        oriented_box.append(yc)
                        # vis corner
                        cv2.circle(vis_image, (xc, yc), 2, (0, 255, 0), 2)
                        cv2.putText(vis_image, str(corner_idx), (xc, yc), font, 1.2, (255, 0, 0))
                    # draw bbox
                    oriented_box = np.asarray(oriented_box)
                    xs = oriented_box.reshape(4, 2)[:, 0]
                    ys = oriented_box.reshape(4, 2)[:, 1]
                    xmin = xs.min()
                    xmax = xs.max()
                    ymin = ys.min()
                    ymax = ys.max()
                    cv2.rectangle(vis_image, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)

            if is_save:
                vis_path = os.path.join(dst_vis_dir, '{}.jpg'.format(name_list[0]))
                txt_dst_path = os.path.join(args.dst_txts_dir, \
                                            '{}.txt'.format(name_list[0]))
                with codecs.open(txt_dst_path, 'w', 'utf-8') as label_file:
                    for idx, corner in enumerate(corner_result):
                        # label_file.write(str(corner[0]))
                        # label_file.write(',')
                        label_file.write(str(corner[1]))
                        label_file.write(',')
                        label_file.write(str(corner[2]))
                        if (idx + 1) % 4 == 0:
                            label_file.write('\n')
                        else:
                            label_file.write(',')

                # shutil.copy(src_image_file, dst_image_file)
                cv2.imwrite(dst_image_file, src_image)
                cv2.imwrite(vis_path, vis_image)
