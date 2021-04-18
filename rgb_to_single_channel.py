import cv2
import os

def rgb_to_single(imgpath,outpath):
    imgs=os.listdir(imgpath)
    for i in imgs:
        print(os.path.join(imgpath,i))
        img=cv2.imread(os.path.join(imgpath,i),0)

        cv2.imwrite(os.path.join(outpath,i),img)

imgpath=r'D:\pyth\PythonApplication9\PythonApplication9\res\femoral+sacrum\VOCdevkit2007(femoral+sacrum)\VOC2007\JPEGImages'
outpath=r'D:\pyth\xray_preprocess_collection\grayJPEGImages'

rgb_to_single(imgpath,outpath)