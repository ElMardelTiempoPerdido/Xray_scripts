#统计xml中某一目标出现的总框数和总图片数
import os
import xml.dom.minidom
from shutil import copyfile

def sum_img(xmlpath,objectname):
    num=0
    for name in os.listdir(xmlpath):
        dom = xml.dom.minidom.parse(os.path.join(xmlpath, name))
        root = dom.documentElement
        # 获取标签对之间的值
        obj = root.getElementsByTagName('name')

        #统计在该xml中，指定的目标是否出现
        for j in range(len(obj)):
            name_tmp=obj[j].firstChild.data
            if name_tmp==objectname:
                num+=1
                break

    return num


def sum_box(xmlpath, objectname):
    num = 0
    for name in os.listdir(xmlpath):
        dom = xml.dom.minidom.parse(os.path.join(xmlpath, name))
        root = dom.documentElement
        # 获取标签对之间的值
        obj = root.getElementsByTagName('name')

        # 统计在该xml中，指定的目标出现的次数
        for j in range(len(obj)):
            name_tmp = obj[j].firstChild.data
            if name_tmp == objectname:
                num += 1

    return num


'''把训练集验证集测试集的xml划分摘出来'''
srcdir=r'D:\pyth\PythonApplication9\PythonApplication9\res\femoral+sacrum\VOCdevkit2007（femoral+sacrum）\VOC2007\Annotations'
testdir=r'D:\pyth\PythonApplication9\PythonApplication9\res\testxml'
traindir=r'D:\pyth\PythonApplication9\PythonApplication9\res\trainvalxml'
txtdir=r'D:\pyth\PythonApplication9\PythonApplication9\res\femoral+sacrum\VOCdevkit2007（femoral+sacrum）\VOC2007\ImageSets\Main'
'''
with open(os.path.join(txtdir,'test.txt'), 'r')as f:
    l = f.readlines()
    f.close()
for i in l:
    copyfile(os.path.join(srcdir,i[:6]+'.xml'), os.path.join(testdir,i[:6]+'.xml'))

with open(os.path.join(txtdir,'trainval.txt'), 'r')as f:
    l = f.readlines()
    f.close()
for i in l:
    copyfile(os.path.join(srcdir,i[:6]+'.xml'), os.path.join(traindir,i[:6]+'.xml'))
'''