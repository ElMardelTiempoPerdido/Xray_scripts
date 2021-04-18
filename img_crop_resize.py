import cv2
import os

#图像裁剪掉一半并缩放


def img_crop_scale(picpath, out_picpath,scale):
    for name in os.listdir(picpath):
        imgname = os.path.join(picpath, name)
        img = cv2.imread(imgname)

        h, w = img.shape[:2]
        sub = int(h / 2)
        img_cut = img[sub:]
        new_h = int(h / (2 * scale))
        new_w = int(w / scale)
        img_alter = cv2.resize(img_cut, (new_w, new_h))

        new_imgname = os.path.join(out_picpath, name)
        cv2.imwrite(new_imgname, img_alter)
        print("pic:" + new_imgname + ' saved')

