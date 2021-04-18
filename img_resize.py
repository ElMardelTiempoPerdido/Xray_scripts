import cv2
import os

def img_scale(picpath, out_picpath,scale):
    for name in os.listdir(picpath):
        imgname = os.path.join(picpath, name)
        img = cv2.imread(imgname)

        h, w = img.shape[:2]

        new_h = h // scale
        new_w = w // scale
        img_alter = cv2.resize(img, (new_w, new_h))

        new_imgname = os.path.join(out_picpath, name)
        cv2.imwrite(new_imgname, img_alter)
        print("pic:" + new_imgname + ' saved')

