# -*- coding: utf-8 -*-
'''
Created on 2017年6月21日

@author: Administrator
'''
import numpy as np

def Jaccard(a,b):#自定义杰卡德相似系数函数，仅对0-1矩阵有效
    return 1.0*(a*b).sum()/(a+b-a*b).sum()

class Recommender():
    sim = None#相似度矩阵
    
    def similarity(self,x,distance):#计算相似度矩阵的函数
        y = np.ones((len(x), len(x)))
        for i in range(len(x)):
            for j in range(len(x)):
                y[i,j] = distance(x[i],x[j])
        return y
    
    def fit(self,x,distance=Jaccard):#训练函数
        self.sim = self.similarity(x,distance)
        
    def recommend(self,a):#推荐函数
        return np.dot(self.sim, a)*(1-a)
        

t = Recommender()
data1 = np.array([(1,0,1,1,1,0,1),
                  (1,1,1,1,1,0,0),
                  (0,0,1,0,0,0,0),
                  (0,1,1,1,0,1,0),
                  (1,0,1,0,1,0,0)])
t.fit(data1)
print(t.sim)

# b = np.array([(1.5,2,3),(4,5,6)])

# t1 = np.array([1,0,1,1,1,0,1])
# t2 = np.array([1,1,1,1,1,0,0])
# print(1.0*(t1*t2).sum()/(t1+t2-t1*t2).sum())