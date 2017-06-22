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
sql = pd.read_sql('all_gzdata',engine,chunksize=10000)

for i in sql:
    d = i[['realIP','fullURL']]
    d = d[d['fullURL'].str.contains('\.html')].copy() #只要含有.html的网址
    #保存到数据库的cleaned_gzdata表中（如果表不存在则自动创建）
    d.to_sql('cleaned_gzdata', engine, index = False, if_exists = 'append')