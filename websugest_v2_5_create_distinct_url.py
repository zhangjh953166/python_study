# encoding: utf-8
'''
Created on 2017年6月28日
@author: Administrator
<![CDATA[
gMqLn8jvpMnj0e+6jP6GleXL38bLntj4qL7ETBkORJb66UUIK57W46ubw9zv09Xz+FcAS3BJelV2
G2Xa6vo=
]]>
'''
import logging

console = logging.StreamHandler()
logger = logging.getLogger('mylogger')
logger.addHandler(console)
logger.setLevel(logging.INFO)

logger.info('starting')

from sqlalchemy import create_engine
from configparser import ConfigParser
import pandas as pd

cf = ConfigParser()
cf.read("dev.conf", 'UTF-8')
host = cf.get("db", "db_host")
port = cf.get("db", "db_port")
user = cf.get("db", "db_user")
password = cf.get("db", "db_pass")
database_name = cf.get("db","db_database")
engine = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+':'+port+'/'+database_name+'?charset=utf8')
sql = pd.read_sql('SELECT realip,fullURL FROM train_v2_gzdata WHERE type_1=\'zixun\'',engine,chunksize=1000)

import  redis

r = redis.Redis(host='172.17.5.135',port=6477,db=1)
r.flushdb()
for i in sql:#逐块变换并去重
# 循环数据创建user的distinct set
# 循环数据创建url的distinct set
    pass
 
    