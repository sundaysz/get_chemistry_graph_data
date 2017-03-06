# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 22:35:21 2017

@author: Sundays
"""

import urllib
import re
import time
import codecs
import jieba
jieba.load_userdict("E:\\recently\\graph\\py\\makedic\\dic_final.txt")
import jieba.posseg as pseg
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

substance_op = codecs.open('E:\\recently\\graph\\py\\substance.txt','w',encoding='utf-8')
relationship_op = codecs.open('E:\\recently\\graph\\py\\relationship.txt','w',encoding='utf-8')
only_table = SoupStrainer("table") #节省内存只读页面一部分，用strainer

def get_data(soup_obj):
    nametitle = soup_obj.find(string=re.compile("中文名"))
    name = nametitle.parent.next_sibling.next_sibling.contents #name返回的是个list，就算是只有一个名字也是
    if len(name)>1:
        fname = name[0][:-1] #处理多个名字，只保留一个
    else:
        fname = name[0] #处理单个名字，[0]是因为一个名字也是list
#以上获得名字,fname为名字的字符串

    preparation = soup_obj.find(string=re.compile("生产方法"))
    prepa = preparation.parent.next_sibling.contents    
#去除list
    prepa_str = ''
    for thing in prepa:
        prepa_str = prepa_str + str(thing)
#去除标签
    dr = re.compile(r'<[^>]+>',re.S)
    prepa_str = dr.sub('',prepa_str)
#以上获得制法，prepa_str为制法的字符串     

#写进‘物质’文件
    substance_op.write(fname + '\r\n')
#写进‘关系’文件
    words = pseg.cut(prepa_str)
    for word,flag in words:
        if flag ==('nz'):
            substance_op.write(word + '\r\n')#先写到物质文件里，之后再去重
            relationship_op.write(fname + ',' + word + '\r\n')#写关系
                         
for i in range(50,100000):
    for j in (0,99):
        for k in (0,9):
            url = "http://www.ichemistry.cn/chemistry/%d-%02d-%d.htm" % (i,j,k)#%02d是保留两位
            time.sleep(10)
            try: #检查是否页面不存在
                html = urllib.request.urlopen(url).read()
            except urllib.error.HTTPError:
                continue
            html = html.decode('gb2312').encode('utf-8')
            soup = BeautifulSoup(html,"lxml",parse_only=only_table,from_encoding='utf-8')
            #上面一行第一个参数是上面的页面，第二个参数系统警告才加的，第三个参数节省内存只搞table
            #下面一行规定当中文名和制法都存在的时候才抓
            if (soup.find(string=re.compile("中文名")) and soup.find(string=re.compile("生产方法"))) != None:
                get_data(soup)
            else:
                continue
substance_op.close()
relationship_op.close()
            

