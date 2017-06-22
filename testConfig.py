# -*- coding: utf-8 -*-
'''
Created on 2017年6月21日

@author: Administrator
'''
from configparser import ConfigParser

cf = ConfigParser()
cf.read("dev.conf", 'UTF-8')
host = cf.get("db", "db_host")
print(host)