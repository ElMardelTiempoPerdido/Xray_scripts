import os
from math import atan, degrees, fabs
import cv2
from cal_vis_femoral_sacrum import x2orix, y2oriy


def get_sacrum_rec(txtname='txts/sacrum-retina.txt'):
    """返回每张图的[图片名，左上xy，右下xy]"""

    txtlines = []
    with open(txtname, 'r') as f:
        txtlines = f.readlines()
        f.close()

    res = []
    for l in txtlines:
        name, v, xmin, ymin, xmax, ymax = l.split()
        res.append([name, int(xmin), int(ymin), int(xmax), int(ymax)])
    print(res)
    return res


def get_femoral_rec(txtname = 'txts/femoralhead-retina.txt'):
    """返回每张图的[图片名，左上xy，右下xy]"""

    txtlines = []
    with open(txtname, 'r') as f:
        txtlines = f.readlines()
        f.close()
    res = []
    i = 0
    while i < len(txtlines):
        if i == len(txtlines) - 1:
            name, v, xmin, ymin, xmax, ymax = txtlines[i].split()
            res.append([name, int(xmin), int(ymin), int(xmax), int(ymax)])
            break

        name, v, xmin, ymin, xmax, ymax = txtlines[i].split()
        name_, v_, xmin_, ymin_, xmax_, ymax_ = txtlines[i + 1].split()

        if name == name_:  # 假如检测出两个股骨
            res.append([name, int(xmin), int(ymin), int(xmax), int(ymax)])
            res.append([name_, int(xmin_), int(ymin_), int(xmax_), int(ymax_)])
            i += 2
        else:  # 假如检测出一个股骨
            res.append([name, int(xmin), int(ymin), int(xmax), int(ymax)])
            i += 1
    return res


def vis_rec(picpath, outpicpath, coords,color):
    """用于可视化[图片名，左上xy，右下xy]这种格式的"""
    for l in coords:
        print('opening: ',os.path.join(picpath, l[0]+'.jpg'))
        img = cv2.imread(os.path.join(picpath, l[0]+'.jpg'))
        if img is None:
            continue
        h, w = img.shape[:2]
        h = int(h / 2)
        w = int(w / 2)

        xmin = x2orix(l[1], h)
        xmax = x2orix(l[3], h)
        ymin = y2oriy(l[2], h)
        ymax = y2oriy(l[4], h)

        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 5)
        midpoint = (int((xmin+xmax) / 2), int((ymin + ymax) / 2))
        cv2.circle(img, midpoint, 10, color, 15)

        cv2.imwrite(os.path.join(outpicpath, l[0]+'.jpg'), img)
        print(os.path.join(outpicpath, l[0]+'.jpg'), ' written')


def vis_fem_sac(picpath, outpicpath):
    fems = get_femoral_rec(txtname='txts/femoralhead-2-40.txt')
    #fems=get_sacrum_rec(txtname='txts/femoralhead_nas_filtered.txt')
    sacs = get_sacrum_rec(txtname='txts/sacrum_nas_filtered.txt')
    #vis_rec(picpath,outpicpath,sacs,(0,0,255))
    vis_rec(picpath,outpicpath,fems,(0,0,255))
