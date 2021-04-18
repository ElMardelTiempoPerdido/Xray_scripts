import os
import xml.dom.minidom

# 对xml进行处理：缩小至原来1/5


def resize_xml(xmlpath, out_xmlpath,scale):
    for name in os.listdir(xmlpath):
        print('-----------------------------------------------------------------------')

        dom = xml.dom.minidom.parse(os.path.join(xmlpath, name))
        root = dom.documentElement
        # 获取标签对之间的值
        xmin = root.getElementsByTagName('xmin')
        ymin = root.getElementsByTagName('ymin')

        xmax = root.getElementsByTagName('xmax')
        ymax = root.getElementsByTagName('ymax')

        width = root.getElementsByTagName('width')
        height = root.getElementsByTagName('height')

        # h/2
        #sub = int(int(height[0].firstChild.data)) // 2

        # 修改相应标签的值
        # width
        # new width=width/scale
        for j in range(len(width)):
            print('width:' + width[j].firstChild.data)
            width[j].firstChild.data = str(int(width[j].firstChild.data) // scale)
            print('new width:' + width[j].firstChild.data)

        # height
        # new height=height/scale
        for j in range(len(height)):
            print('height:' + height[j].firstChild.data)
            height[j].firstChild.data = str(int(height[j].firstChild.data) // scale)
            print('new height:' + height[j].firstChild.data)

        # xmin
        # new xmin=xmin/scale
        for i in range(len(xmin)):
            print('xmin:' + xmin[i].firstChild.data)
            a = xmin[i].firstChild.data
            xmin[i].firstChild.data = str(int(xmin[i].firstChild.data) // scale)
            print('new xmin:' + xmin[i].firstChild.data)

        # ymin
        # new ymin=ymin/scale
        for j in range(len(ymin)):
            print('ymin:' + ymin[j].firstChild.data)
            ymin[j].firstChild.data = str(int(ymin[j].firstChild.data) // scale)
            print('new ymin:' + ymin[j].firstChild.data)

        # xmax
        for j in range(len(xmax)):
            print('xmax:' + xmax[j].firstChild.data)
            xmax[j].firstChild.data = str(int(xmax[j].firstChild.data) // scale)
            print('new xmax:' + xmax[j].firstChild.data)

        # ymax
        for j in range(len(ymax)):
            print('ymax:' + ymax[j].firstChild.data)
            ymax[j].firstChild.data = str(int(ymax[j].firstChild.data) // scale)
            print('new ymin:' + ymax[j].firstChild.data)

        # 保存修改到xml文件中
        with open(os.path.join(out_xmlpath, name), 'w') as fh:
            dom.writexml(fh)
        print(os.path.join(out_xmlpath, name), ' written')

