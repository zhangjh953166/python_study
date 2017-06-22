# -*- coding: utf-8 -*-
'''
Created on 2017年6月21日

@author: Administrator
'''
import pandas as pd
from sqlalchemy import create_engine
from email.header import UTF8
from configparser import ConfigParser

cf = ConfigParser()
cf.read("dev.conf", 'UTF-8')
host = cf.get("db", "db_host")
port = cf.get("db", "db_port")
user = cf.get("db", "db_user")
password = cf.get("db", "db_pass")
database_name = cf.get("db","db_database")
engine = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+':'+port+'/'+database_name+'?charset=utf8')
sql = pd.read_sql('changed_gzdata',engine,chunksize=10000)

for i in sql: #逐块变换并去重
    d = i.copy()
    d['type_1'] = d['fullURL']
    d['type_1'][d['fullURL'].str.contains('(ask)|(askzt)')] = 'zixun' #将含有ask、askzt关键字的网址的类别一归为咨询（后面的规则就不详细列出来了，实际问题自己添加即可）
    d.to_sql('splited_gzdata', engine, index = False, if_exists = 'append') #保存