# encoding: utf-8
'''
Created on 2017年6月28日
@author: Administrator
<![CDATA[
jZ/BovbagduGsrTEhIr/j/GvnM/pq/jn38yMj9KAl9Dx2MXcke3rppj53tHo
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
sql = pd.read_sql('SELECT realip,fullURL FROM train_v2_gzdata',engine,chunksize=1000)

for i in sql:
    pass