# encoding: utf-8
'''
Created on 2017年6月26日

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
sql = pd.read_sql('SELECT * FROM splited_gzdata WHERE type_1=\'zixun\'',engine,chunksize=10000)
#统计点击次数
c = [i['fullURL'].value_counts() for i in sql] #分块统计各个IP的出现次数
count3 = pd.concat(c).groupby(level = 0).sum() #合并统计结果，level=0表示按index分组
count3 = pd.DataFrame(count3) #Series转为DataFrame
# count3[1] = 1 #添加一列，全为1
# count3.groupby('realIP').sum() #统计各个“不同的点击次数”分别出现的次数
# print(count3.groupby('realIP').sum())

writer = pd.ExcelWriter('pandas_stat_url.xlsx',engine='xlsxwriter',options={'strings_to_urls': False})
count3.to_excel(writer,sheet_name="Sheet1")
writer.save()