import json
import os
from collections import OrderedDict

#femoralhead=1,sacrum=2
def get_id_list(path):
    l=os.listdir(path)
    names=[]
    for i in l:
        names.append(i[:6])
    print(names)
    return names

def txt_to_json(txtpath, txtnames, outpath, jsonname,idlist):
    dst = []
    for txtname in txtnames:
        with open(os.path.join(txtpath, txtname), 'r') as t:
            lines = t.readlines()
            t.close()

        catid=0
        if 'femoralhead' in txtname:
            catid=1
        if 'sacrum' in txtname:
            catid=2
        for i, l in enumerate(lines):
            data = l.split(' ')

            #dd = {"image_id": namelist.index(data[0])+1,
            #      "category_id": catid,
            #      "bbox": [data[2], data[3], data[4], data[5][:-1]],
            #      "score": data[1]
            #      }

            dd =OrderedDict()
            dd['image_id']= namelist.index(data[0])+1
            dd['category_id'] = catid
            dd['bbox'] = [int(data[2]), int(data[3]), int(data[4]), int(data[5][:-1])]
            dd['score'] = float(data[1])
            print(dd)

            dst.append(dd)
    with open(os.path.join(outpath, jsonname), 'w') as js:
        jjjj=json.dumps(dst)
        js.write(jjjj)
        js.close()



namelist=get_id_list(r'D:\pyth\PythonApplication9\PythonApplication9\res\femoral+sacrum\testxml')
txt_to_json('txts', ['femoralhead_nas_filtered.txt','sacrum_nas_filtered.txt'], 'testset_json', 'nas.json',namelist)
