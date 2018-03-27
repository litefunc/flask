#----import----
from sqlite3 import *
import os
os.chdir('C:\\Users\\ak66h_000\\Documents\\db\\')
conn = connect('tse.sqlite3')
c = conn.cursor()

import requests
from bs4 import BeautifulSoup
from numpy import *
from pandas import *
from functools import *

get_option("display.max_rows")
get_option("display.max_columns")
set_option("display.max_rows", 1000)
set_option("display.max_columns", 1000)
set_option('display.expand_frame_repr', False)
set_option('display.unicode.east_asian_width', True)

def mymerge(x, y):
    m = merge(x, y, on=[col for col in list(x) if col in list(y)], how='outer')
    return m

x = '2316'
df = read_sql_query('SELECT * from `每日收盤行情(全部(不含權證、牛熊證))` where 證券代號='+ x, conn)
df = read_sql_query('SELECT * from `個股日本益比、殖利率及股價淨值比` where 證券代號='+ x, conn)
df = read_sql_query('SELECT * from `當日融券賣出與借券賣出成交量值(元)` where 證券代號='+ x, conn)
df = read_sql_query('SELECT * from `三大法人買賣超日報(股)` where 證券代號='+ x, conn)
df = read_sql_query('SELECT * from `營益分析` where 公司代號='+ x, conn)
df = read_sql_query('SELECT * from `財務分析` where 公司代號='+ x, conn)
df = read_sql_query('SELECT * from `大盤統計資訊` where 指數='+ x, conn)
df = read_sql_query('SELECT * from `大盤統計資訊` where 指數='+ x, conn)

#--- rename table ---
sql='ALTER TABLE `每日收盤行情(全部(不含權證、牛熊證))` RENAME TO close'
c.execute(sql)
sql='ALTER TABLE `個股日本益比、殖利率及股價淨值比` RENAME TO value'
c.execute(sql)
sql='ALTER TABLE `當日融券賣出與借券賣出成交量值(元)` RENAME TO margin'
c.execute(sql)
sql='ALTER TABLE `三大法人買賣超日報(股)` RENAME TO institution'
c.execute(sql)
sql='ALTER TABLE `營益分析` RENAME TO operation'
c.execute(sql)
sql='ALTER TABLE `財務分析` RENAME TO finance'
c.execute(sql)
sql='ALTER TABLE `大盤統計資訊` RENAME TO market'
c.execute(sql)
sql='ALTER TABLE `大盤成交統計` RENAME TO deal'
c.execute(sql)
sql='ALTER TABLE `投信買賣超彙總表 (股)` RENAME TO trust'
c.execute(sql)
sql='ALTER TABLE `外資及陸資買賣超彙總表 (股)` RENAME TO `finvestor`'
c.execute(sql)
sql='ALTER TABLE `自營商買賣超彙總表 (股)` RENAME TO dealer'
c.execute(sql)

sql='ALTER TABLE `close` RENAME TO `每日收盤行情(全部(不含權證、牛熊證))`'
c.execute(sql)
sql='ALTER TABLE `value` RENAME TO `個股日本益比、殖利率及股價淨值比`'
c.execute(sql)
sql='ALTER TABLE `margin` RENAME TO `當日融券賣出與借券賣出成交量值(元)`'
c.execute(sql)
sql='ALTER TABLE `institution` RENAME TO `三大法人買賣超日報(股)`'
c.execute(sql)
sql='ALTER TABLE `operation` RENAME TO `營益分析`'
c.execute(sql)
sql = 'ALTER TABLE `finance` RENAME TO `財務分析`'
c.execute(sql)
sql = 'ALTER TABLE `market` RENAME TO `大盤統計資訊`'
c.execute(sql)
sql='ALTER TABLE `deal` RENAME TO `大盤成交統計`'
c.execute(sql)
sql = 'ALTER TABLE `trust` RENAME TO `投信買賣超彙總表 (股)`'
c.execute(sql)
sql = 'ALTER TABLE `finvestor` RENAME TO `外資及陸資買賣超彙總表 (股)`'
c.execute(sql)
sql='ALTER TABLE `dealer` RENAME TO `自營商買賣超彙總表 (股)`'
c.execute(sql)






