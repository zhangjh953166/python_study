# -*- coding:utf-8 -*
'''
Created on 2017年6月14日

@author: Administrator
'''
import pandas as pd
s = pd.Series([1,2,3],index=['a','b','c'])
d = pd.DataFrame([[1,2,3],[4,5,6]],columns=['a','b','c'])
d2 = pd.DataFrame(s)

print(d.head())
print(d.describe())
