import cv2
import numpy as np
import os
import xml.dom.minidom

# xml预处理：裁掉上1/2,取余下部分缩小至原来1/5
scale = 5
xmlpath = r'D:\pyth\PythonApplication9\PythonApplication9\res\femoral+sacrum\VOCdevkit2007（femoral+sacrum）\VOC2007\new\\'
out_xmlpath = r'D:\pyth\PythonApplication9\PythonApplication9\res\femoral+sacrum\VOCdevkit2007（femoral+sacrum）\VOC2007\new\\'

for name in os.listdir(xmlpath):

    print('-----------------------------------------------------------------------')

    name = name[:6] + '.xml'

    dom = xml.dom.minidom.parse(xmlpath + name)
    root = dom.documentElement
    # 获取标签对之间的值
    xmin = root.getElementsByTagName('xmin')
    ymin = root.getElementsByTagName('ymin')

    xmax = root.getElementsByTagName('xmax')
    ymax = root.getElementsByTagName('ymax')

    width = root.getElementsByTagName('width')
    height = root.getElementsByTagName('height')
    sub=int(height[0].firstChild.data)//2

    # 修改相应标签的值
    # width
    # new width=width/scale
    for j in range(len(width)):
        print('width:' + width[j].firstChild.data)
        width[j].firstChild.data = str(int(int(width[j].firstChild.data) / scale))
        print('new width:' + width[j].firstChild.data)

    # height
    # new height=height/(2*scale)
    for j in range(len(height)):
        print('height:' + height[j].firstChild.data)
        height[j].firstChild.data = str(int(int(height[j].firstChild.data) / (2 * scale)))
        print('new height:' + height[j].firstChild.data)

        # xmin
    # new xmin=xmin/scale
    for i in range(len(xmin)):
        print('xmin:' + xmin[i].firstChild.data)
        a = xmin[i].firstChild.data
        xmin[i].firstChild.data = str(int(int(xmin[i].firstChild.data) / scale))
        print('new xmin:' + xmin[i].firstChild.data)

    # ymin new ymin=(ymin-(h/2))/scale)
    for j in range(len(ymin)):
        print('ymin:' + ymin[j].firstChild.data)
        ymin[j].firstChild.data = str(int((int(ymin[j].firstChild.data) - sub) / scale))
        print('new ymin:' + ymin[j].firstChild.data)

    # xmax
    for j in range(len(xmax)):
        print('xmax:' + xmax[j].firstChild.data)
        xmax[j].firstChild.data = str(int(int(xmax[j].firstChild.data) / scale))
        print('new xmax:' + xmax[j].firstChild.data)

        # ymax
    for j in range(len(ymax)):
        print('ymax:' + ymax[j].firstChild.data)
        ymax[j].firstChild.data = str(int((int(ymax[j].firstChild.data) - sub) / scale))
        print('new ymin:' + ymax[j].firstChild.data)

    # 保存修改到xml文件中
    with open(os.path.join(out_xmlpath, name), 'w') as fh:
        dom.writexml(fh)
    print(out_xmlpath + name + ' written')
