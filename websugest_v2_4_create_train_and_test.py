# encoding: utf-8
'''
Created on 2017年6月27日

@author: Administrator
<![CDATA[
j+OtltPf2NTqnvfkqKPk3+fF2c/kgKL2rtPAj+G3sqzajbvdi+Wyk8fjpNjJDmQcjMSil9bu2MXc
ke3rq77T3OLt1fP4VwBLcEl6VXYbZdrq+g==
]]>
'''
import pandas as pd
from sqlalchemy import create_engine
from configparser import ConfigParser

import logging

console = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# console.setFormatter(formatter)
logger = logging.getLogger('mylogger')
logger.addHandler(console)
logger.setLevel(logging.INFO)

logger.info('starting')

cf = ConfigParser()
cf.read("dev.conf", 'UTF-8')
host = cf.get("db", "db_host")
port = cf.get("db", "db_port")
user = cf.get("db", "db_user")
password = cf.get("db", "db_pass")
database_name = cf.get("db","db_database")
engine = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+':'+port+'/'+database_name+'?charset=utf8')
# sql = pd.read_sql('changed_gzdata',engine,chunksize=10000)
# 交集函数  返回结果为left-right之后剩余的集合   on是索引列名
def difference(left,right,on):
    df = pd.merge(left,right,how='left',on=on)
    left_columns = left.columns
    col_y = df.columns[left_columns.size]
    df = df[df[col_y].isnull()]
    df = df.ix[:,0:left_columns.size]
    df.columns = left_columns
    return df
#  python交集处理
'''
df1 = pd.DataFrame({'key':list('bbacaab'),'data1':range(7),'war':list('war1234')})
df2 = pd.DataFrame({'key':list('abd'),'data1':range(3),'war':list('war')})
print(df1)
print(df2)
print(pd.merge(df1,df2,on=['key','data1']))
print(difference(df1, df2, ['key','data1']))
'''

sql = pd.read_sql('SELECT realIP,fullURL FROM splited_v2_gzdata WHERE type_1=\'zixun\' AND type_2<>\'no_cal\' AND type_3<>\'exp\'',engine,chunksize=10000)
for i in sql:
    logger.info('load ...')
    i['id'] = i.index
    train = i.sample(frac=0.8,replace=False)
    logger.info('create train')
    test = difference(i,train,'id')
    del(train['id'])
    del(test['id'])
    print(train.size)
    print(test.size)
    train.to_sql('train_v2_gzdata', engine, index = False, if_exists = 'append') #保存
    test.to_sql('test_v2_gzdata', engine, index = False, if_exists = 'append') #保存

