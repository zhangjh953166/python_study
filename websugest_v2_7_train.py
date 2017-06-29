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
# sql = pd.read_sql('SELECT realIP,fullURL FROM train_v2_gzdata',engine,chunksize=1000)

sql = pd.DataFrame([[2282069774,'http://www.lawtime.cn/ask/question_3335133.html'],
                    ])

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

import  sanmao.RecommenderV1
logger.info('start load db')
t = sanmao.RecommenderV1.Recommender() 
for i in sql:
    d = i[['fullURL']]
    e = i[['realIP']]
    f = create_array(d,e)
    url_index = f[['fullURL']].iloc[:,0].values
    del(f['fullURL'])
    logger.info('load from db finish')
    t.fit(f.as_matrix())
    logger.info('fit model finish')
    print(t.sim)
    result = pd.DataFrame(t.sim,index=url_index,columns=url_index)
    np.savetxt("sim_v2.csv", t.sim, fmt="%.2f",delimiter=",")
    logger.info('save to file finish')
    break