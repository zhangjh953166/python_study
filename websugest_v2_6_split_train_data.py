# encoding: utf-8
'''
Created on 2017年6月28日
@author: Administrator
<![CDATA[
nvfAqY353+Ht0/vuEUIbLheq8v7Q2ZeF17qW5/3W8tecweapm93d0dY=
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
sql = pd.read_sql('SELECT realip,fullURL FROM train_v2_gzdata',engine,chunksize=1000)

# 直接循环即可，不进行sample操作