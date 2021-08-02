"""
-------------------------------------------------
   Description :
   Author :       Jing
   E-mail:        jliu4@heygears.com
   date：        2020/12/7 19:08

-------------------------------------------------
"""

import cv2
import os
import numpy as np
import time
import logging

current_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
logging.basicConfig(level=logging.DEBUG)
mylog =logging.getLogger(name='diff_test')
file_handler = logging.FileHandler(f'diff{current_time}.log')
mylog.addHandler(file_handler)
mylog.info('--start writing-----')

# def check_pixel(pix_without_diff, pix_with_diff, diff=0, threshold=80):
#     """ 以pix_without_diff为基准, 按规则计算加了diff后的值, 判断是否等于pix_with_diff"""


def compare(image_without_diff, image_with_diff, diff=0, threshold=80):
    img_g0 = cv2.imread(image_without_diff, cv2.COLOR_GRAY2BGR)
    img_gx = cv2.imread(image_with_diff, cv2.COLOR_GRAY2BGR)

    assert img_g0.shape == img_gx.shape  # 确保两张图片尺寸是一致的
    h, w = img_g0.shape
    print(h, w)
    try:
        for i in range(len(img_g0)):
            for j in range(len(img_g0[i])):
                after_diff_g0 = (img_g0[i][j] + diff)
                if img_g0[i][j] == 0 or img_g0[i][j] == 255:
                     continue
                if after_diff_g0 < 0:
                    after_diff_g0 = 0
                    assert after_diff_g0 == img_gx[i][j] , (i, j, after_diff_g0, img_gx[i][j])
                elif after_diff_g0 > 255:
                    after_diff_g0 = 255
                    assert abs(after_diff_g0 - img_gx[i][j]) < 2, (i, j, after_diff_g0, img_gx[i][j])
                elif after_diff_g0 < threshold:
                    after_diff_g0 = 0
                    assert after_diff_g0 == img_gx[i][j], (i, j, after_diff_g0, img_gx[i][j],"灰度未清零")

    # i, j, after_th_g0, img_g0[i][j], img_gx[i][j] == (x坐标，y坐标，整体灰度变化后的值a，a+边界处理或清零后的值，灰度设置后的值
                if after_diff_g0 >= 80 and after_diff_g0 < 255:
                    assert abs(after_diff_g0 - img_gx[i][j]) < 2, (i, j, after_diff_g0, img_gx[i][j], (img_gx[i][j]-after_diff_g0))
    except AssertionError:
        mylog.info((i, j, img_g0[i][j], after_diff_g0,  img_gx[i][j], (img_gx[i][j] - after_diff_g0)))


def list_images(img_dir: str):
    if not os.path.exists(img_dir):
        raise Exception('invalid path:', img_dir)
    images = {}
    for filename in os.listdir(img_dir):

        if filename.endswith(('.png', '.bmp', '.jpg', '.jpeg')):
            if "FillingImg" in filename:
                images[filename] = os.path.join(img_dir, filename).replace('\\', '/')
    print('found {} images in {}'.format(len(images), img_dir))
    return images


if __name__ == '__main__':

    image_dir0 = r'E:\diff 0'
    image_dir1 = r'E:\diff 30'
    diff_specify = -30
    # change_name(image_dir0)
    # change_name(image_dir1)
    for image_name, image_path in list_images(image_dir0).items():
            image_path_1 = os.path.join(image_dir1, image_name)
            print(image_name, image_path, image_path_1)
            mylog.info((image_name, image_path, image_path_1))
            compare(image_path, image_path_1, diff=diff_specify, threshold=80)
