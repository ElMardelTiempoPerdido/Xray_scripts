import os
import random

# 制作划分voc2007数据集的4个txt

trainval_percent = 0.8
train_percent = 0.75

voc2007path = r'D:\pyth\PythonApplication9\PythonApplication9\res\VOCdevkit2007\VOC2007'
txtsavepath = os.path.join(voc2007path, 'ImageSets', 'Main')
xmlfilepath = os.path.join(voc2007path, 'Annotations')

total_xml = os.listdir(xmlfilepath)
num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

ftrainval = open(os.path.join(txtsavepath, 'trainval.txt'), 'w')
ftest = open(os.path.join(txtsavepath, 'test.txt'), 'w')
ftrain = open(os.path.join(txtsavepath, 'train.txt'), 'w')
fval = open(os.path.join(txtsavepath, 'val.txt'), 'w')

for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()
