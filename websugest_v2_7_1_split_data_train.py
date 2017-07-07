# encoding: utf-8
'''
Created on 2017年7月6日
@author: Administrator
<![CDATA[
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

i = pd.DataFrame([[1,'a.html'],
                    [1,'b.html'],
                    [1,'e.html'],
                    [2,'b.html'],
                    [2,'d.html'],
                    [3,'a.html'],
                    [3,'b.html'],
                    [3,'c.html'],
                    [3,'d.html'],
                    [3,'e.html']
                    ],
               columns=['realIP','fullURL'])
i2 = pd.DataFrame([[4,'a.html'],
                    [4,'b.html'],
                    [4,'d.html'],
                    [5,'a.html'],
                    [5,'b.html'],
                    [5,'e.html'],
                    [6,'d.html'],
                    [7,'a.html']
                    ],
               columns=['realIP','fullURL'])

def create_array(url,ip,data):
    train_data_matrix = np.zeros((url.size,ip.size))
    for line in data.itertuples():
        train_data_matrix[url.query('fullURL=="'+line[2]+'"').index[0],ip.query('realIP=='+str(line[1])).index[0]] = 1
    return train_data_matrix

logger.info('start load db')

def Jaccard(a,b):#自定义杰卡德相似系数函数，仅对0-1矩阵有效
    return str((a*b).sum())+","+str((a+b-a*b).sum())

class Recommender():
    sim = None#相似度矩阵
    def similarity(self,x,distance):#计算相似度矩阵的函数
        y = np.empty([len(x), len(x)],dtype=object)
        for i in range(len(x)):
            for j in range(len(x)-len(x)+i+1):
                y[i,j] = distance(x[i],x[j])
        return y
    
    def fit(self,x,distance=Jaccard):#训练函数
        self.sim = self.similarity(x,distance)
        
    def recommend(self,a):#推荐函数
        return np.dot(self.sim, a)*(1-a)

def calArray(i):
    t = Recommender() 
    d = i[['fullURL']]
    e = i[['realIP']]
    d = d.drop_duplicates(subset=['fullURL']) #去重
    d = pd.DataFrame(d.as_matrix(),columns=['fullURL'])
    e = e.drop_duplicates(subset=['realIP'])
    e = pd.DataFrame(e.as_matrix(),columns=['realIP'])
    f = create_array(d,e,i)
    t.fit(f)
    logger.info('fit model finish')
# print(t.sim)
    return pd.DataFrame(t.sim,columns=d[['fullURL']].iloc[:,0].values,index=d[['fullURL']].iloc[:,0].values)  #重新构建dataframe
#     print(result)
# np.savetxt("sim_v2.csv", t.sim, fmt="%.2f",delimiter=",", header=",".join(d[['fullURL']].iloc[:,0].values), comments="")
# logger.info('save to file finish')
a1 = calArray(i)
a2 = calArray(i2)
column_arr = np.unique(np.append(a1.columns.values,a2.columns.values))   #合并两个数组的columns,并且去重

a_matrix = np.zeros((column_arr.size,column_arr.size))  #生成合并后的相关度矩阵
for line in column_arr :
    index = np.where(column_arr==line)[0][0] #找到A物品的下标，行下标
    for line_j in column_arr :
        if line in a1 and line_j in a1 :    #判断a1矩阵是否存在a物品和b物品的相关度
            if a1[line][line_j] == None :   #因为只计算了半个矩阵，所以存在none值
                continue
            stat1 = a1[line][line_j].split(',')    #拿到交集汇总，和并集汇总
        else:
            stat1 = ['0.0','0.0']           #如果a1矩阵没有那么赋予零值
        if line in a2 and line_j in a2 :
            if a2[line][line_j] == None :
                continue
            stat2 = a2[line][line_j].split(',')
        else:
            stat2 = ['0.0','0.0']
        stat = (float(stat1[0])+float(stat2[0]))/(float(stat1[1])+float(stat2[1]))   #汇总得到走后的值，如果有递归调用，那么这里应该还要设置为[交集汇总，并集汇总]
        index_j = np.where(column_arr==line_j)[0][0]     #找到B物品的下标，列下标
        a_matrix[index][index_j] = stat
end = pd.DataFrame(a_matrix ,columns=column_arr,index=column_arr)    #重新生成dataframe
pass