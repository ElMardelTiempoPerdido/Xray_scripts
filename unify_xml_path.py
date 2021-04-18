import os
import xml.dom.minidom

# 对xml进行处理：统一路径，用中文路径的都拖出去打一顿

def unify_xml_path(xmlpath,out_xmlpath):
    for name in os.listdir(xmlpath):
        print('-----------------------------------------------------------------------')
        dom = xml.dom.minidom.parse(os.path.join(xmlpath, name))
        root = dom.documentElement
        # 获取标签对之间的值
        path_text = root.getElementsByTagName('path')
        filename=root.getElementsByTagName('filename')
        filename=filename[0].firstChild.data
        text=r'D:\pyth\PythonApplication9\PythonApplication9\res\side-236'
        full_text=os.path.join(text,filename)


        # 修改相应标签的值
        print('old path:' + path_text[0].firstChild.data)
        path_text[0].firstChild.data = full_text
        print('new path:' + path_text[0].firstChild.data)



        # 保存修改到xml文件中
        with open(os.path.join(out_xmlpath, name), 'w') as fh:
            dom.writexml(fh)
        print(os.path.join(out_xmlpath, name), ' written')

