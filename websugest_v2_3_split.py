# -*- coding: utf-8 -*-
'''
Created on 2017年6月21日

@author: Administrator
'''
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
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
    row_size = len(d)
    d['type_1'] = np.zeros(row_size)
    d.loc[d['fullURL'].str.contains('(ask)|(askzt)'),'type_1'] = 'zixun'
    d['type_2'] = np.zeros(row_size)
    d.loc[d['fullURL'].str.contains('(browse_)|(ranking.)'),'type_2'] = 'no_cal'
    d['type_3'] = np.zeros(row_size)
    d.loc[d['fullURL'].str.contains('(exp/)'),'type_3'] = 'exp'
    d.to_sql('splited_v2_gzdata', engine, index = False, if_exists = 'append') #保存
#     d['type_1'] = d['fullURL']
#     d['type_1'][d['fullURL'].str.contains('(ask)|(askzt)')] = 'zixun' #将含有ask、askzt关键字的网址的类别一归为咨询（后面的规则就不详细列出来了，实际问题自己添加即可）
#     d['type_2'] = d['fullURL']
#     d['type_2'][d['fullURL'].str.contains('(browse_)|(ranking.)')] = 'del' 
#     d['type_2'][d['fullURL'].str.contains('question_')] = 'question'
#     d['type_2'][d['fullURL'].str.contains('exp/')] = 'exp'
#     d.to_sql('splited_v2_gzdata', engine, index = False, if_exists = 'append') #保存

