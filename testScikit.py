# -*- coding:utf-8 -*
'''
Created on 2017年6月15日

@author: Administrator
'''

from sklearn.linear_model import LinearRegression
model = LinearRegression()
print(model)

from sklearn import datasets
iris = datasets.load_iris()
print(iris.data.shape)

from sklearn import svm

clf = svm.LinearSVC()
clf.fit(iris.data, iris.target)
clf.predict([[5.0,3.6,1.3,0.25]])
print(clf.coef_)