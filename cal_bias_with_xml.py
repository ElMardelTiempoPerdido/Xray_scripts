"""计算三个骨盆参数和真实值的误差"""

import numpy as np
import os
from math import atan, degrees
import cv2
import xml.dom.minidom
import math

"""通过两个txt计算骨盆参数
txt1：sacrum.txt,每张图片记录一组xmin,ymin,xmax,ymax
得到p0:(xmin,ymin)
得到p1:(xmax,ymax)
得到p3:((xmin+xmax)/2,(ymin+ymax)/2)

----------------------------------------------------------
txt2：femoralhead.txt,每张图片记录2组xmin,ymin,xmax,ymax
得到两个股骨中心((xmin1+xmax1)/2,(ymin1+ymax1)/2)
             ((xmin2+xmax2)/2,(ymin2+ymax2)/2)
得到两个股骨中心连线的中心：（(xmin1+xmax1)/2+((xmin2+xmax2)/2）/2,
算屁呢，直接全都相加除以四

得到股骨连线中心p2((xmin1+xmax1+xmin2+xmax2)/4,(ymin1+ymax1+ymin2+ymax2)/4)
下面函数计算这个
"""

res_txt_path = r'D:\pyth\PythonApplication9\PythonApplication9\res\sacrum+femoralhead\efficentdet-d3-att+gelu-0903'


def get_sacrum():
    """返回每张图的[图片名，p0,p1,p3]"""
    txtname = os.path.join(res_txt_path, 'sacrum.txt')
    txtlines = []
    with open(txtname, 'r') as f:
        txtlines = f.readlines()
        f.close()

    res = []
    for l in txtlines:
        name, v, xmin, ymin, xmax, ymax = l.split()
        res.append([name, (int(xmin), int(ymin)), (int(xmax), int(ymax)),
                    (int((int(xmin) + int(xmax)) / 2), int((int(ymin) + int(ymax)) / 2))])
    print(res)
    return res


def get_femoral():
    """返回每张图的[图片名，p2,股骨中心1，股骨中心2]"""
    txtname = os.path.join(res_txt_path, 'femoralhead.txt')
    txtlines = []
    with open(txtname, 'r') as f:
        txtlines = f.readlines()
        f.close()

    res = []
    # for i in range(0,len(txtlines)-1,2):
    i = 0
    while i < len(txtlines):
        if i == len(txtlines) - 1:
            name, v, xmin, ymin, xmax, ymax = txtlines[i].split()
            res.append([name, (int((int(xmin) + int(xmax) + int(xmin) + int(xmax)) / 4),
                               int((int(ymin) + int(ymax) + int(ymin) + int(ymax)) / 4)),
                        (int((int(xmin) + int(xmax)) / 2), int((int(ymin) + int(ymax)) / 2)),
                        (int((int(xmin) + int(xmax)) / 2), int((int(ymin) + int(ymax)) / 2))])
            break

        name, v, xmin, ymin, xmax, ymax = txtlines[i].split()
        name_, v_, xmin_, ymin_, xmax_, ymax_ = txtlines[i + 1].split()
        print(name, v, xmin, ymin, xmax, ymax)
        print(name_, v_, xmin_, ymin_, xmax_, ymax_)

        if name == name_:  # 假如检测出两个股骨
            res.append([name, (int((int(xmin) + int(xmax) + int(xmin_) + int(xmax_)) / 4),
                               int((int(ymin) + int(ymax) + int(ymin_) + int(ymax_)) / 4)),
                        (int((int(xmin) + int(xmax)) / 2), int((int(ymin) + int(ymax)) / 2)),
                        (int((int(xmin_) + int(xmax_)) / 2), int((int(ymin_) + int(ymax_)) / 2))])
            i += 2
        else:  # 假如检测出一个股骨
            res.append([name, (int((int(xmin) + int(xmax) + int(xmin) + int(xmax)) / 4),
                               int((int(ymin) + int(ymax) + int(ymin) + int(ymax)) / 4)),
                        (int((int(xmin) + int(xmax)) / 2), int((int(ymin) + int(ymax)) / 2)),
                        (int((int(xmin) + int(xmax)) / 2), int((int(ymin) + int(ymax)) / 2))])
            i += 1
    print(res)
    return res


'''
对一张图片，检测结果包含如下数据：
骶骨上边缘线，用两个坐标表示：p0(x0，y0),p1(x1,y1)
股骨中心坐标：p2(x2,y2)
得到骶骨上边缘中心为((x0+x1)/2,(y0+y1)/2),记为p3(x3,y3)
--------------------------------------------------------------------
ss参数：表示骶骨上边缘线与水平方向夹角
ss=arctan((y1-y0)/(x1-x0))

pt参数：表示（骶骨上边缘中心与股骨中心连线）与（竖直方向）的夹角
pt=90-arctan((y3-y2)/(x3-x2))

pi参数：表示（骶骨上边缘中心与股骨中心连线）与(骶骨上边缘线的垂线)的夹角
=ss+pt
pi=ss+pt
'''


def compute_ss(p0, p1):
    # 传入p0[x0,y0],p1[x1,y1]
    return degrees(atan((p1[1] - p0[1]) / (p1[0] - p0[0])))


def compute_pt(p0, p1, p2):
    # 传入p0[x0,y0],p1[x1,y1],p2[x2,y2]
    p3 = [(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2]
    return 90.0 - degrees(atan((p3[1] - p2[1]) / (p3[0] - p2[0])))


def compute_pi(ss, pt):
    # 传入计算过的ss和pt
    return ss + pt


scale = 5


def x2orix(x, half_h):
    return scale * x


def y2oriy(y, half_h):
    return scale * y + half_h


picpath = r'D:\pyth\PythonApplication9\PythonApplication9\res\alter_pic_added'

xmlpath = r'D:\pyth\PythonApplication9\PythonApplication9\res\xml_added_orignal'


def get_params_from_xml(picname):
    dom = xml.dom.minidom.parse(os.path.join(xmlpath, picname + '.xml'))
    root = dom.documentElement
    # 获取标签对之间的值
    labelname = root.getElementsByTagName('name')
    xmin = root.getElementsByTagName('xmin')
    ymin = root.getElementsByTagName('ymin')
    xmax = root.getElementsByTagName('xmax')
    ymax = root.getElementsByTagName('ymax')

    sac = []
    fem = []

    for i in range(len(labelname)):
        '''

        print(labelname[i].firstChild.data)
        print(xmin[i].firstChild.data)
        print(xmax[i].firstChild.data)
        print(ymin[i].firstChild.data)
        print(ymax[i].firstChild.data)
        '''
        if labelname[i].firstChild.data == 'sacrum':
            sac.append(int(xmin[i].firstChild.data))
            sac.append(int(ymin[i].firstChild.data))
            sac.append(int(xmax[i].firstChild.data))
            sac.append(int(ymax[i].firstChild.data))
        elif labelname[i].firstChild.data == 'femoralhead':
            f = [int(xmin[i].firstChild.data), int(ymin[i].firstChild.data),
                 int(xmax[i].firstChild.data), int(ymax[i].firstChild.data)]
            fem.append(f)

    if len(sac) == 0 or len(fem) == 0:
        return None

    elif len(fem) == 1:
        fem.append(fem[0])

    p0 = [sac[0], sac[1]]
    p1 = [sac[2], sac[3]]
    p3 = [int((sac[0] + sac[2]) / 2), int((sac[1] + sac[3]) / 2)]

    p4 = [int((fem[0][0] + fem[0][2]) / 2), int((fem[0][1] + fem[0][3]) / 2)]
    p5 = [int((fem[1][0] + fem[1][2]) / 2), int((fem[1][1] + fem[1][3]) / 2)]

    p2 = [int((p4[0] + p5[0]) / 2), int((p4[1] + p5[1]) / 2)]

    ss = compute_ss(p0, p1)
    pt = compute_pt(p0, p1, p2)
    pi = compute_pi(ss, pt)
    print('ss:' + str(ss))
    print('pt:' + str(pt))
    print('pi:' + str(pi))
    return [ss, pt, pi]


def get_mse(records_real, records_predict):
    """
    均方误差 估计值与真值 偏差
    """
    if len(records_real) == len(records_predict):
        return sum([(x - y) ** 2 for x, y in zip(records_real, records_predict)]) / len(records_real)
    else:
        return None


def get_rmse(records_real, records_predict):
    """
    均方根误差：是均方误差的算术平方根
    """
    mse = get_mse(records_real, records_predict)
    if mse:
        return math.sqrt(mse)
    else:
        return None


def mape(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean(np.abs((y_pred - y_true) / y_true)) * 100


def smape(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return 2.0 * np.mean(np.abs(y_pred - y_true) / (np.abs(y_pred) + np.abs(y_true))) * 100


def main():
    ss_bias_t = []
    pt_bias_t = []
    pi_bias_t = []
    ss_truth = []
    pi_truth = []
    pt_truth = []
    ss_pre = []
    pt_pre = []
    pi_pre = []

    sac = get_sacrum()
    fem = get_femoral()
    print('sacrums:')
    print(sac)
    print('femorals:')
    print(fem)

    """total:[图片名，p0,p1,p2,p3]"""
    total = []
    for i in sac:
        p0 = i[1]
        p1 = i[2]
        p3 = i[3]
        p2 = []
        p4 = []
        p5 = []
        for j in fem:
            if j[0] == i[0]:
                p2 = j[1]
                p4 = j[2]
                p5 = j[3]
        total.append([i[0], p0, p1, p2, p3, p4, p5])
    print('totals:')
    print(total)
    for i in total:
        img = cv2.imread(os.path.join(picpath, i[0] + '.jpg'))
        h, w = img.shape[:2]
        h = int(h / 2)
        w = int(w / 2)

        # 骶骨上缘两端点
        p0 = i[1]
        p1 = i[2]
        # 股骨连线中心
        p2 = i[3]
        # 骶骨上缘中点
        p3 = i[4]
        # 两个股骨头中心
        p4 = i[5]
        p5 = i[6]

        print(i)

        # 还原到原尺寸
        p0 = (x2orix(p0[0], h), y2oriy(p0[1], h))
        p1 = (x2orix(p1[0], h), y2oriy(p1[1], h))
        p2 = (x2orix(p2[0], h), y2oriy(p2[1], h))
        p3 = (x2orix(p3[0], h), y2oriy(p3[1], h))
        p4 = (x2orix(p4[0], h), y2oriy(p4[1], h))
        p5 = (x2orix(p5[0], h), y2oriy(p5[1], h))

        '''这是三个参数的预测值'''
        ss = round(compute_ss(p0, p1), 3)
        pt = round(compute_pt(p0, p1, p2), 3)
        pi = round(compute_pi(ss, pt), 3)

        thisimgname = i[0]
        print("----------------------")
        print(thisimgname + ':')
        print('pre params:')
        print('ss:' + str(ss))
        print('pt:' + str(pt))
        print('pi:' + str(pi))
        print('true params:')
        truth = get_params_from_xml(thisimgname)

        ss_bias = abs(ss - truth[0]) / ss
        pt_bias = abs(pt - truth[1]) / pt
        pi_bias = abs(pi - truth[2]) / pi

        print('ss_bias:' + str(ss_bias))
        print('pt_bias:' + str(pt_bias))
        print('pi_bias:' + str(pi_bias))
        if ss_bias < 0.4 and pt_bias < 0.4 and pi_bias < ss_bias < 0.4:
            ss_bias_t.append(ss_bias)
            pt_bias_t.append(pt_bias)
            pi_bias_t.append(pi_bias)

            ss_truth.append(round(truth[0], 3))
            pt_truth.append(truth[1])
            pi_truth.append(truth[2])
            ss_pre.append(ss)
            pt_pre.append(pt)
            pi_pre.append(pi)

        print("----------------------")
    print('total ss deviation=' + str(round(np.average(ss_bias_t), 3)))
    print('total pt deviation=' + str(round(np.average(pt_bias_t), 3)))
    print('total pi deviation=' + str(round(np.average(pi_bias_t), 3)))

    total = np.average(pi_bias_t) + np.average(pt_bias_t) + np.average(ss_bias_t)
    total = round(total / 3, 3)
    print('total deviation=' + str(total))

    print(ss_pre)
    print(ss_truth)
    print('ss mse=' + str(get_mse(ss_pre, ss_truth)))
    print('pi mse=' + str(get_mse(pi_pre, pi_truth)))
    print('pt mse=' + str(get_mse(pt_pre, pt_truth)))

    print('ss rmse=' + str(get_rmse(ss_pre, ss_truth)))
    print('pi rmse=' + str(get_rmse(pi_pre, pi_truth)))
    print('pt rmse=' + str(get_rmse(pt_pre, pt_truth)))

    ss_rmse = get_rmse(ss_pre, ss_truth)
    pt_rmse = get_rmse(pt_pre, pt_truth)
    pi_rmse = get_rmse(pi_pre, pi_truth)
    ave_rmse = np.average([ss_rmse, pt_rmse, pi_rmse])

    print('average rmse' + str(ave_rmse))

    ss_mape = mape(ss_truth, ss_pre)
    pt_mape = mape(pt_truth, pt_pre)
    pi_mape = mape(pi_truth, pi_pre)
    print('ss mape=' + str(ss_mape))
    print('pi mape=' + str(pi_mape))
    print('pt mape=' + str(pt_mape))

    ss_smape = smape(ss_truth, ss_pre)
    pt_smape = smape(pt_truth, pt_pre)
    pi_smape = smape(pi_truth, pi_pre)
    print('ss smape=' + str(ss_smape))
    print('pi smape=' + str(pi_smape))
    print('pt smape=' + str(pt_smape))


if __name__ == '__main__':
    main()
