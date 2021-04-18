import os
from math import atan, degrees, fabs
import cv2
from cal_vis_femoral_sacrum import get_sacrum, x2orix


def get_c7side():
    """返回每张图的[图片名，c7side中心点]"""
    txtname = 'txts/c7side-1231.txt'
    with open(txtname, 'r') as f:
        txtlines = f.readlines()
        f.close()
    res = []
    for l in txtlines:
        name, v, xmin, ymin, xmax, ymax = l.split()
        midx = (int(xmin) + int(xmax)) // 2
        midy = (int(ymin) + int(ymax)) // 2
        res.append([name, (midx, midy)])
    return res


def compute_sva(pupper, plower, resolution):
    """计算sva，单位：cm"""
    distance = fabs(pupper[0] - plower[0])
    distance /= resolution
    distance *= 2.54
    return distance


def vis_sva():
    """计算sva并可视化"""
    # 原尺寸图像的路径
    picpath = r'D:\pyth\PythonApplication9\PythonApplication9\res\xray-imgs\testset-48'
    # 输出绘制了参数的图像的路径
    outpath = r'D:\pyth\xray_preprocess_collection\res_sva'

    # 图像分辨率
    resolution = 96

    # 从txt中获得sac和c7side的关键点
    sac = get_sacrum()
    c7s = get_c7side()

    """total:[图片名，p0,p1]"""
    p0=[]
    p1=[]
    total = []
    for i in c7s:
        p0 = i[1]
        for j in sac:
            if j[0] == i[0]:
                p1 = j[3]
        total.append([i[0], p0, p1])

    for i in total:
        print('-------------------------------------------')
        print(os.path.join(picpath, i[0]+'.jpg'))
        img = cv2.imread(os.path.join(picpath, i[0]+'.jpg'))
        h, w = img.shape[:2]
        h = int(h / 2)
        w = int(w / 2)

        # c7side中心
        p0 = i[1]
        # sac上缘中心
        p1 = i[2]

        # 还原到原尺寸
        p0 = (x2orix(p0[0], h), x2orix(p0[1], h))
        p1 = (x2orix(p1[0], h), x2orix(p1[1], h))

        # 计算sva
        sva = round(compute_sva(p0, p1, resolution), 3)
        print('sva=', sva)

        # 在图片上绘制文字
        if img.shape[1] < 3000:
            cv2.putText(img, 'SVA=' + str(sva) + 'cm', (w, h), cv2.FONT_ITALIC, 4.0, (255, 255, 255), 8)
        else:
            cv2.putText(img, 'SVA=' + str(sva) + 'cm', (w, h), cv2.FONT_ITALIC, 6.0, (255, 255, 255), 8)

        # c7side中点
        cv2.circle(img, p0, 15, (0, 0, 255), 15)
        # sac上缘中点
        cv2.circle(img, p1, 15, (0, 0, 255), 15)

        # c7side铅垂线
        cv2.line(img, p0, (p0[0], p0[1] + 3000), (255, 0, 0), 8)
        # sac铅垂线
        cv2.line(img, p1, (p1[0], p1[1] - 3000), (255, 0, 0), 8)

        # 输出绘制了辅助线和参数数值的图片
        cv2.imwrite(os.path.join(outpath, i[0]+ '.jpg'), img)

        print(i[0], ' written')
