# -*- coding: utf-8 -*-
'''
Created on 2017年6月22日

@author: Administrator
'''
import pandas as pd
import numpy as np
# from sqlalchemy import create_engine
# from configparser import ConfigParser
# 
# cf = ConfigParser()
# cf.read("dev.conf", 'UTF-8')
# host = cf.get("db", "db_host")
# port = cf.get("db", "db_port")
# user = cf.get("db", "db_user")
# password = cf.get("db", "db_pass")
# database_name = cf.get("db","db_database")
# engine = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+':'+port+'/'+database_name+'?charset=utf8')
# sql = pd.read_sql('splited_gzdata',engine,chunksize=10000)
# 
# for i in sql:#逐块变换并去重
#     d = i.drop_duplicates(subset=['fullURL'],keep='first',inplace=False)[['fullURL']]


i = pd.DataFrame({'realIP':[2683657840,973705742,3104681075],
                 'fullURL':['http://www.lawtime.cn/info/hunyin/hunyinfagui/201404102884290_6.html',
                            'http://www.lawtime.cn/ask/exp/17199.html',
                            'http://www.lawtime.cn/ask/exp/17199.html']})

url = i.drop_duplicates(subset=['fullURL'], keep='first', inplace=False)[['fullURL']]
ip = i.drop_duplicates(subset=['realIP'], keep='first', inplace=False)[['realIP']]
# print(url)
print(url)
for index,row in ip.iterrows():
    ip_str = str(row['realIP'])
    url[ip_str]=np.zeros(url.ndim)
    url_str = i[i['realIP']==row['realIP']]['fullURL']
    for tt in range(url_str.ndim):
        for match in range((url['fullURL']==url_str.values[tt]).values.size) :
            if (url['fullURL']==url_str.values[tt]).values[match] :
                url.loc[match,(ip_str)]=1.0
#         url[url['fullURL']==url_str.values[tt]][ip_str]=1.0
print(url)
