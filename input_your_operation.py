#from img_resize import img_scale
#from xml_resize import resize_xml
#from unify_xml_path import unify_xml_path

#from cal_vis_c7side_sacrum import *
from vis_femoral_sacrum import *
from vis_label_from_xml import *
#from sum_objects_in_xml import *

scale = 5

xmlpath = r'D:\pyth\PythonApplication9\PythonApplication9\res\femoral+sacrum\all_xml-originalSize-236'
out_xmlpath = r'D:\pyth\PythonApplication9\PythonApplication9\res\c7side-data\xml-236-refined-small'

picpath = r'D:\pyth\PythonApplication9\PythonApplication9\res\xray-imgs\testset-48'
out_picpath = r'D:\pyth\xray_preprocess_collection\efficient-no-sacrum'

# resize_xml(xmlpath, out_xmlpath,scale)
# unify_xml_path(xmlpath,out_xmlpath)
# img_scale(picpath,out_picpath,scale)
# vis_sva()

vis_fem_sac(out_picpath,out_picpath)
vis_label(xmlpath,out_picpath,out_picpath,(255,0,0))

'''
print(sum_img(xmlpath, 'femoralhead'))
print(sum_box(xmlpath, 'femoralhead'))

print(sum_img(xmlpath, 'sacrum'))
print(sum_box(xmlpath, 'sacrum'))
'''
#sacs = get_sacrum_rec()
#vis_rec(picpath, out_picpath, sacs, (0, 0, 255))