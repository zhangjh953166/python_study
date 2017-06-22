# -*- coding: utf-8 -*-
'''
Created on 2017年6月21日

@author: Administrator
'''
import pandas as pd
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
sql = pd.read_sql('cleaned_gzdata',engine,chunksize=10000)

for i in sql:#逐块变换并去重
    d = i.copy()
    d['fullURL'] = d['fullURL'].str.replace('_\d[0,2].html','.html')#将下划线后面部分去掉，规范为标准网址
    d = d.drop_duplicates() #删除重复记录
    d.to_sql('changed_gzdata', engine, index = False, if_exists = 'append') #保存