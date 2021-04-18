import re
import os
import xml.dom.minidom

xmlpath = r'D:\pyth\PythonApplication9\PythonApplication9\res\femoral+sacrum\VOCdevkit2007（femoral+sacrum）\VOC2007\Annotations'
for name in os.listdir(xmlpath):
    dom = xml.dom.minidom.parse(os.path.join(xmlpath, name))
    root = dom.documentElement
    # 获取标签对之间的值
    xmin = root.getElementsByTagName('xmin')
    ymin = root.getElementsByTagName('ymin')

    xmax = root.getElementsByTagName('xmax')
    ymax = root.getElementsByTagName('ymax')

    width = int(root.getElementsByTagName('width')[0].firstChild.data)
    height = int(root.getElementsByTagName('height')[0].firstChild.data)

    for i in range(len(xmin)):
        xmin_=int(xmin[i].firstChild.data)
        ymin_ = int(ymin[i].firstChild.data)
        xmax_ = int(xmax[i].firstChild.data)
        ymax_ = int(ymax[i].firstChild.data)
        if xmin_<0:
            print(name,' xmin<0!')
        elif ymin_<0:
            print(name,' ymin<0!')
        elif xmax_ > width:
            print(name, ' xmax too big!')
        elif ymax_ > height:
            print(name, ' ymax too big!')
        else:
            print(name,' ok!')
            print("------------")
