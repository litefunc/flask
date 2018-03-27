# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 20:10:01 2016

@author: ak66h_000
"""
from sqlite3 import *
import os
os.chdir('C:\\Users\\ak66h_000\\Documents\\db\\')
# os.chdir('D:/')
c = conn.cursor()

import requests
from bs4 import BeautifulSoup
from numpy import *
from pandas import *
from functools import *
conn = connect('tse.sqlite3')

sql="SELECT `證券代號`,`證券名稱` FROM '%s'"
close = read_sql_query(sql% ('每日收盤行情(全部(不含權證、牛熊證))'), conn)
close=close.drop_duplicates(['證券代號','證券名稱'])

tablename='company'
sql='create table `%s` (`%s`, PRIMARY KEY (%s))'%(tablename, '`,`'.join(list(close)), '`證券代號`, `證券名稱`')
c.execute(sql)
sql='insert into `%s`(`%s`) values(%s)'%(tablename, '`,`'.join(list(close)), ','.join('?'*len(list(close))))
c.executemany(sql, close.values.tolist())
conn.commit()
print('finish')
#sql="drop table `%s`"%tablename
#c.execute(sql)
sql="SELECT `證券代號`,`證券名稱` FROM '%s'"
company = read_sql_query(sql% ('company'), conn)
company