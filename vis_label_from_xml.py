import xml
import cv2
import os
from xml.dom import minidom

def vis_label(xmlpath, picpath, outpath, color):
    for i in os.listdir(picpath):
        img = cv2.imread(os.path.join(picpath, i))
        h, w = img.shape[:2]
        h = int(h / 2)
        w = int(w / 2)

        dom = xml.dom.minidom.parse(os.path.join(xmlpath, i[:6]) + '.xml')
        root = dom.documentElement
        # 获取标签对之间的值
        xmin = root.getElementsByTagName('xmin')
        ymin = root.getElementsByTagName('ymin')
        xmax = root.getElementsByTagName('xmax')
        ymax = root.getElementsByTagName('ymax')

        for idx in range(len(xmin)):
            points = [(int(xmin[idx].firstChild.data), int(ymin[idx].firstChild.data)),
                      (int(xmax[idx].firstChild.data), int(ymax[idx].firstChild.data))]
            cv2.rectangle(img, points[0], points[1], color, 5)
            midpoint = (int((points[0][0] + points[1][0]) / 2), int((points[0][1] + points[1][1]) / 2))
            cv2.circle(img, midpoint, 10,  color, 15)

        cv2.imwrite(os.path.join(outpath, i), img)
        print(os.path.join(outpath, i), ' written')
