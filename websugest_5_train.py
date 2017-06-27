# -*- coding: utf-8 -*-
'''
Created on 2017年6月22日

@author: Administrator
'''
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from configparser import ConfigParser
import  sanmao.RecommenderV1
import logging

console = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# console.setFormatter(formatter)
logger = logging.getLogger('mylogger')
logger.addHandler(console)
logger.setLevel(logging.INFO)

def create_array(url,ip):
    url_size = url.size # 因为url的元素个数会随着np.zeros增长
    for index,row in ip.iterrows():
        ip_str = str(row['realIP']) #因为row['realip']得到的数据类型是INt
        url[ip_str]=np.zeros(url_size)
        url_str = i[i['realIP']==row['realIP']]['fullURL']   #需要对values和index都进行操作。这里为了代码简洁容易理解
        for tt in range(url_str.size):
            match_array = url['fullURL']==url_str.values[tt]
            for match in range(match_array.values.size) :
                if match_array.values[match] :
                    url.loc[match_array.index[match],(ip_str)]=1# 不能使用[][]进行赋值，因为这是query会复制查询结果。所以赋值并不会真正生效
    return url

logger.info('starting')

cf = ConfigParser()
cf.read("dev.conf", 'UTF-8')
host = cf.get("db", "db_host")
port = cf.get("db", "db_port")
user = cf.get("db", "db_user")
password = cf.get("db", "db_pass")
database_name = cf.get("db","db_database")
engine = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+':'+port+'/'+database_name+'?charset=utf8')
sql = pd.read_sql('splited_gzdata',engine,chunksize=1000)

t = sanmao.RecommenderV1.Recommender() 

logger.info('start load db')

for i in sql:#逐块变换并去重
    d = i.drop_duplicates(subset=['fullURL'],keep='first',inplace=False)[['fullURL']]
    e = i.drop_duplicates(subset=['realIP'], keep='first', inplace=False)[['realIP']]
    f = create_array(d,e)
    del f['fullURL']
    logger.info('load from db finish')
#     logger.info(f)
    t.fit(f.as_matrix())
    logger.info('fit model finish')
    break
# print(t.sim)

np.savetxt("sim.csv", t.sim, fmt="%.2f",delimiter=",")
logger.info('save to file finish')
# i = pd.DataFrame({'realIP':[2683657840,973705742,3104681075,2683657840,2683657840],
#                  'fullURL':['http://www.lawtime.cn/info/hunyin/hunyinfagui/201404102884290_6.html',
#                             'http://www.lawtime.cn/ask/exp/17199.html',
#                             'http://www.lawtime.cn/ask/exp/17199.html',
#                             'http://www.lawtime.cn/info/hunyin/hunyinfagui/201404102884290_6.html',
#                             'http://www.lawtime.cn/ask/question_10190986.html']})

# url = i.drop_duplicates(subset=['fullURL'], keep='first', inplace=False)[['fullURL']]
# ip = i.drop_duplicates(subset=['realIP'], keep='first', inplace=False)[['realIP']]
# print(url)
# print(url)


    
    
    
    
        
        
            
                
#         url[url['fullURL']==url_str.values[tt]][ip_str]=1.0
