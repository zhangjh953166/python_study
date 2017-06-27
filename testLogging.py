# encoding: utf-8
'''
Created on 2017年6月23日

@author: Administrator
'''
import logging

console = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger('fefaewf')
logger.addHandler(console)
logger.setLevel(logging.INFO)

logger.info('starting')

v = ['a']
print(v)