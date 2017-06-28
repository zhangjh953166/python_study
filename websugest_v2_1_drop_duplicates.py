# encoding: utf-8
'''
Created on 2017年6月26日

@author: Administrator
<![CDATA[
ltj42NXSnMLcqLjd0O3m09fljZ7KosTZiPK6vbnwg4n0GgBUEzSe1uOooO3c1uTV8+qAv9Ch4eOP
4aO9k+aEiv+N3Iac9diq+8fT27uO07iW4NXW7/Od8fSmidPewuDV8/hXAEtwSXpVdhtl2ur6
]]>
'''
import logging

console = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# console.setFormatter(formatter)
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
sql = pd.read_sql('SELECT realip,fullURL FROM splited_gzdata WHERE type_1=\'zixun\'',engine,chunksize=1000)

import  redis

r = redis.Redis(host='172.17.5.135',port=6477,db=1)
r.flushdb()
count = 1
for i in sql:#逐块变换并去重
#     tt = i['realip']
#     for gg in tt:
#         count = count + 1
#         r.sadd('p_realIP', str(gg))
#         if count % 10000 == 0 :
#             print(r.scard('p_realIP'))
    for iter in i.index:
        r.sadd('p_realIP',str(i.loc[iter,'realip']))
        r.sadd('p_fullURL',str(i.loc[iter,'fullURL']))
        count = count + 1
        if count % 10000 == 0 :
            print(r.scard('p_fullURL'))
