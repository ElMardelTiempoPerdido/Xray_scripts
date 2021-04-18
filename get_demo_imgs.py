import os
import shutil

#根据test.txt文件中的文件名,把测试集的图片分离出来

txtpath=r'D:\pyth\PythonApplication9\PythonApplication9\res\c7side实验数据\VOCdevkit2007\VOC2007\ImageSets\Main'
txtname='test.txt'

jpgsrcpath=r'D:\pyth\PythonApplication9\PythonApplication9\res\c7side实验数据\VOCdevkit2007\VOC2007\JPEGImages'
jpgoutpath=r'D:\pyth\PythonApplication9\PythonApplication9\res\c7side实验数据\VOCdevkit2007\demo'

with open(os.path.join(txtpath,txtname),'r') as f:
    lines=f.readlines()
    f.close()

for l in lines:
    jpgname=l[:6]+'.jpg'
    print(jpgname)
    sourceDir=os.path.join(jpgsrcpath,jpgname)
    targetDir=os.path.join(jpgoutpath,jpgname)
    shutil.copy(sourceDir,  targetDir)

