# -*- coding: utf-8 -*-
'''
Created on 2017年6月20日

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
 
#统计总体情况
counts = [i['fullURLId'].value_counts() for i in sql] #逐块统计
#value_counts用于计算一个Series中各值出现的频率
counts = pd.concat(counts).groupby(level=0).sum()  #合并统计结果，把相同的统计项合并（即按index分组并求和）
#是索引数组，所以按照第一列进行排序分组，并且求和
counts = counts.reset_index() #重新设置index，将原来的index作为counts的一列。
counts.columns = ['index', 'num'] #重新设置列名，主要是第二列，默认为0
counts['type'] = counts['index'].str.extract('(\d{3})') #提取前三个数字作为类别id
counts_ = counts[['type', 'num']].groupby('type').sum() #按类别合并
# counts_.sort('num', ascending = False) #降序排列
counts_.sort_values('num',ascending=False)
# print(counts_.sort_values('num',ascending=False))
