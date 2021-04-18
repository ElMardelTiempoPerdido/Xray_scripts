#因为nas输出的ap把什么傻吊结果都写进去，所以写个脚本过滤一下
import os
def ap_filter(txtpath,txtname,thresh):
    with open(os.path.join(txtpath,txtname),'r') as t:
        lines=t.readlines()
        t.close()

    result=[]
    for l in lines:
        data=l.split(' ')
        if float(data[1])>thresh:
            thisline=data[0]+' '+data[1]+' '+str(int(float(data[2])))+' '+str(int(float(data[3])))+' '+str(int(float(data[4])))+' '+str(int(float(data[5])))+'\n'
            result.append(thisline)
    for r in result:
        print(r)
    return result
def write_new_txt(outpath,txtname,result):
    with open(os.path.join(outpath,txtname),'a') as t:
        t.writelines(result)
        t.close()
dir=r'D:\pyth\fstrcnn_xray_resnet\fstrcnn_xray_resnet\txts_210227'
txtname=r'sacrum-nas-0302.txt'
res=ap_filter(dir,txtname,0.5)

write_new_txt(dir,'sacrum_nas_filtered.txt',res)