import cv2
import numpy as np
import os


# 对图像调整亮度对比度


# 这是调整亮度对比度的函数,输入输出为灰度图
def contrast_img(img1, c, b):
    # b：亮度偏移量，c：对比度的放大倍数
    rows, cols = img1.shape
    blank = np.zeros([rows, cols], img1.dtype)
    dst = cv2.addWeighted(img1, c, blank, 1 - c, b)
    return dst


def img_contrast_batch(picpath, out_picpath):
    for name in os.listdir(picpath):
        imgname = os.path.join(picpath, name)
        img = cv2.imread(imgname, 0)

        img_alter = contrast_img(img, 2.2, -250)
        # 因为之前操作的是灰度图，这里扩展为为三通道
        img_alter = cv2.merge([img_alter, img_alter, img_alter])

        new_imgname = os.path.join(out_picpath, name)
        cv2.imwrite(new_imgname, img_alter)

        print("pic:" + new_imgname + ' saved')
