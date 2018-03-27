  # ----import----
from sqlite3 import *
import os
import time
import functools
from datetime import datetime, timedelta
from copy import deepcopy

start = time.time()

def timeDelta(s):
    global start
    end = time.time()
    print(s,'timedelta: ', end - start)
    start = end

os.chdir('C:\\Users\\ak66h_000\\Documents\\db\\')
# os.chdir('D:/')
conn = connect('mops.sqlite3')
c = conn.cursor()

import requests
from bs4 import BeautifulSoup
from numpy import *
from pandas import *
from functools import *
# from pandas.io import data, wb
# from pandas_datareader import data, wb
# import pandas.io.data as web
# import pandas_datareader.data as web

def timeSpan(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        start = time.time()
        x = func(*args, **kw)
        end = time.time()
        print('Complete in {} second(s)'.format(end-start))
        return x
    return wrapper

## --- read from sqlite ---
def mymerge(x, y):
    m = merge(x, y, on=[col for col in list(x) if col in list(y)], how='outer')
    return m

# --- report---

id = '5522'
companyId = "'{}'".format(id)
sql = "SELECT * FROM '{}' WHERE 公司代號 LIKE {}".format('ifrs前後-綜合損益表', companyId)
inc = read_sql_query(sql, conn).replace('--', 'NaN').rename(columns={'公司代號': '證券代號'})
col = ['年', '季', '證券代號', '營業收入', '營業成本', '營業毛利（毛損）', '未實現銷貨（損）益', '已實現銷貨（損）益', '營業毛利（毛損）淨額', '營業費用',
       '其他收益及費損淨額', '營業利益（損失）', '營業外收入及支出', '稅前淨利（淨損）', '所得稅費用（利益）', '繼續營業單位本期淨利（淨損）', '停業單位損益', '合併前非屬共同控制股權損益',
       '本期淨利（淨損）', '其他綜合損益（淨額）', '合併前非屬共同控制股權綜合損益淨額', '本期綜合損益總額', '淨利（淨損）歸屬於母公司業主', '淨利（淨損）歸屬於共同控制下前手權益',
       '淨利（淨損）歸屬於非控制權益', '綜合損益總額歸屬於母公司業主', '綜合損益總額歸屬於共同控制下前手權益', '綜合損益總額歸屬於非控制權益', '基本每股盈餘（元）', '利息淨收益', '利息以外淨收益',
       '呆帳費用及保證責任準備提存（各項提存）', '淨收益', '保險負債準備淨變動', '支出及費用', '收入', '支出', '會計原則變動累積影響數', '呆帳費用', '會計原則變動之累積影響數', '稀釋每股盈餘',
       '利息收入', '減：利息費用', '收回(提存)各項保險責任準備淨額', '費用', '列計非常損益及會計原則變動累積影響數前損益', '營業支出']
col1 = ['營業收入', '營業成本', '營業毛利（毛損）', '未實現銷貨（損）益', '已實現銷貨（損）益', '營業毛利（毛損）淨額', '營業費用', '其他收益及費損淨額', '營業利益（損失）', '營業外收入及支出',
        '稅前淨利（淨損）', '所得稅費用（利益）', '繼續營業單位本期淨利（淨損）', '停業單位損益', '合併前非屬共同控制股權損益', '本期淨利（淨損）', '其他綜合損益（淨額）',
        '合併前非屬共同控制股權綜合損益淨額', '本期綜合損益總額', '淨利（淨損）歸屬於母公司業主', '淨利（淨損）歸屬於共同控制下前手權益', '淨利（淨損）歸屬於非控制權益', '綜合損益總額歸屬於母公司業主',
        '綜合損益總額歸屬於共同控制下前手權益', '綜合損益總額歸屬於非控制權益', '基本每股盈餘（元）', '利息淨收益', '利息以外淨收益', '呆帳費用及保證責任準備提存（各項提存）', '淨收益',
        '保險負債準備淨變動', '支出及費用', '收入', '支出', '會計原則變動累積影響數', '呆帳費用', '會計原則變動之累積影響數', '稀釋每股盈餘', '利息收入', '減：利息費用',
        '收回(提存)各項保險責任準備淨額', '費用', '列計非常損益及會計原則變動累積影響數前損益', '營業支出']
inc = inc[col]
# def change(s):
#     a = array(s)
#     return Series(append(a[0], a[1:] - a[0:len(s) - 1]),name=s.name)
for i in col1:
    if inc[i].dtypes == 'object':
        inc[[i]] = inc[[i]].astype(float)
inc[['年', '季']]=inc[['年', '季']].astype(str)
def change1(df):
    df0 = df[[x for x in list(df) if df[x].dtype == 'object']]
    df1 = df[[x for x in list(df) if df[x].dtype != 'object']]
    a0 = array(df0)
    a1 = array(df1)
    v = vstack((a1[0], a1[1:] - a1[0:len(df) - 1]))
    h = hstack((a0, v))
    return DataFrame(h, columns=list(df0) + list(df1))

inc = inc.groupby(['證券代號', '年']).apply(change1).reset_index(drop=True)  #'季' must be string

inc['淨利（淨損）歸屬於母公司業主'] = inc['淨利（淨損）歸屬於母公司業主'].astype(float)
inc['綜合損益總額歸屬於母公司業主'] = inc['綜合損益總額歸屬於母公司業主'].astype(float)
inc['毛利率'] = inc['營業毛利（毛損）']/inc['營業收入']
inc['營業利益率'] = inc['營業利益（損失）']/inc['營業收入']
inc['綜合稅後純益率'] = inc['綜合損益總額歸屬於母公司業主']/inc['營業收入']

inc['grow_s'] = inc['本期綜合損益總額'].pct_change(1)
inc['grow_hy'] = inc['本期綜合損益總額'].rolling(window=2).sum().pct_change(2)
inc[col1] = inc[col1].rolling(window=4).sum()
inc['grow_y'] = inc['本期綜合損益總額'].pct_change(4)
inc['grow'] = inc['本期綜合損益總額'].pct_change(1)
# inc['grow.ma'] = inc['grow'].rolling(window=24).mean()*4
inc['本期綜合損益總額.wma'] = inc.本期綜合損益總額.ewm(com=19).mean() * 4
inc['本期綜合損益總額.ma'] = inc['本期綜合損益總額'].rolling(window=12).mean() * 4
sql = "SELECT * FROM '{}' WHERE 公司代號 LIKE {}"
bal = read_sql_query(sql .format('ifrs前後-資產負債表-一般業', companyId), conn).rename(columns={'公司代號': '證券代號'}).drop(['Unnamed: 21', '待註銷股本股數（單位：股）', 'Unnamed: 22'], axis=1)
bal['流動比率'] = bal['流動資產'] / bal['流動負債']
bal['負債佔資產比率'] = bal['負債總額'] / bal['資產總額']
bal[['年', '季']]=bal[['年', '季']].astype(str)
del bal['公司名稱']


timeDelta('mops')

#--- summary ---
conn = connect('summary.sqlite3')
sql = "SELECT * FROM '{}' WHERE 公司代號 LIKE {}" .format('會計師查核報告', companyId)
ac = read_sql_query(sql, conn).replace('--', 'NaN').rename(columns={'公司代號': '證券代號', '公司簡稱': '證券名稱', '核閱或查核日期': '年月日'}).sort_values(['年', '季', '證券代號']).drop(['簽證會計師事務所名稱', '簽證會計師','簽證會計師.1', '核閱或查核報告類型'], axis=1)
ac[['年', '季']]=ac[['年', '季']].astype(str)
del ac['證券名稱']
# companyId = "'3056%'"
sql = "SELECT * FROM '{}' WHERE 公司代號 LIKE {}"
fin = read_sql_query(sql .format('財務分析', companyId), conn)
del fin['公司簡稱']

report = reduce(mymerge, [inc, bal, ac])

report['權益報酬率'] = report['綜合損益總額歸屬於母公司業主'] * 2 / (report['權益總額'] + report['權益總額'].shift())
report['profitbility'] = report.綜合損益總額歸屬於母公司業主 / (report.權益總額.shift(4))
report['investment'] = report.權益總額.pct_change(4)

report.dtypes
timeDelta('summary')

#--- tse ---
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

conn = connect('tse.sqlite3')
sql="SELECT * FROM '{}' WHERE 證券代號 LIKE {}"

# read from redis
close = read_msgpack(r.get("close:{}".format(companyId)))
value = read_msgpack(r.get("value:{}".format(companyId)))
margin = read_msgpack(r.get("margin:{}".format(companyId)))
ins = read_msgpack(r.get("ins:{}".format(companyId)))

# read form sqlite
# close = read_sql_query(sql.format('每日收盤行情(全部(不含權證、牛熊證))', companyId), conn)
# value = read_sql_query(sql.format('個股日本益比、殖利率及股價淨值比', companyId), conn).drop(['證券名稱'], 1)
# margin = read_sql_query(sql.format('當日融券賣出與借券賣出成交量值(元)', companyId), conn)
# ins = read_sql_query(sql.format('三大法人買賣超日報(股)', companyId), conn)
# deal = read_sql_query(sql.format('自營商買賣超彙總表 (股)', companyId), conn).drop(['證券名稱'], 1).fillna(0)

deal = read_msgpack(r.get("deal:{}".format(companyId)))
deal[['自營商(自行買賣)賣出股數', '自營商(自行買賣)買賣超股數', '自營商(自行買賣)買進股數', '自營商(避險)賣出股數', '自營商(避險)買賣超股數', '自營商(避險)買進股數', '自營商賣出股數', '自營商買賣超股數', '自營商買進股數']] = deal[['自營商(自行買賣)賣出股數', '自營商(自行買賣)買賣超股數', '自營商(自行買賣)買進股數', '自營商(避險)賣出股數', '自營商(避險)買賣超股數', '自營商(避險)買進股數', '自營商賣出股數', '自營商買賣超股數', '自營商買進股數']].fillna(0)

fore = read_sql_query(sql.format('外資及陸資買賣超彙總表 (股)', companyId), conn).drop(['證券名稱'], 1).rename(columns={'買進股數':'外資買進股數','賣出股數':'外資賣出股數','買賣超股數':'外資買賣超股數','鉅額交易': '外資鉅額交易'}).fillna('no')

trust = read_sql_query(sql.format('投信買賣超彙總表 (股)', companyId), conn).drop(['證券名稱'], 1).rename(columns={'買進股數':'投信買進股數','賣出股數':'投信賣出股數','買賣超股數':'投信買賣超股數','鉅額交易': '投信鉅額交易'}).fillna('no')
trust[['投信買進股數', '投信賣出股數', '投信買賣超股數']] = trust[['投信買進股數', '投信賣出股數', '投信買賣超股數']].fillna(0)
trust[['投信鉅額交易']] = trust[['投信鉅額交易']].fillna('no')

index = read_sql_query("SELECT * FROM '{}' WHERE 指數 LIKE {}".format('大盤統計資訊', "'建材營造類指數'"), conn).rename(columns={'收盤指數':'建材營造類指數'}).drop(['指數', '漲跌(+/-)'], axis=1).replace('--', nan).replace('---', nan)
index1 = read_sql_query("SELECT * FROM '{}'".format('index'), conn).replace('--', nan).replace('---', nan)
rindex = read_sql_query("SELECT * FROM '{}' WHERE 指數 LIKE {}".format('大盤統計資訊', "'建材營造類報酬指數'"), conn).rename(columns={'收盤指數':'建材營造類報酬指數', '漲跌點數':'r漲跌點數','漲跌百分比(%)':'r漲跌百分比(%)'}).drop(['指數', '漲跌(+/-)'], axis=1).replace('--', nan).replace('---', nan)
fore['外資鉅額交易'] = fore['外資鉅額交易'].replace('*', 'yes').replace(' ', 'no').replace('yes', 1).replace('no', 0).astype(float)
trust['投信鉅額交易'] = trust['投信鉅額交易'].replace('*', 'yes').replace(' ', 'no').replace(0, 'no').replace('yes', 1).replace('no', 0).astype(float)

close['本益比'] = close['本益比'].replace('0.00', nan) # pe is '0.00' when pe < 0
close['年月日'] = close['年月日'].astype(str)
close['年'], close['月'] = close['年月日'].str.split('/').str[0].astype(int), close['年月日'].str.split('/').str[1].astype(int)
close['漲跌(+/-)'] = close['漲跌(+/-)'].replace('＋', 1).replace('－', -1).replace('X', 0).replace(' ', None).astype(float)

value['本益比'] = value['本益比'].replace('-', nan)  # pe is '-' when pe < 0
value['股價淨值比'] = value['股價淨值比'].replace('-', nan)
sql = "SELECT * FROM '{}' WHERE 股票代號 LIKE {}"
xdr = read_sql_query(sql.format('除權息計算結果表', companyId), conn).rename(columns={'股票代號': '證券代號', '股票名稱': '證券名稱'})
xdr['a'] = xdr['權值+息值'].replace(NaN, 0)
xdr['b'] = xdr['a'].cumsum()

closeWithXdr = mymerge(close, xdr)

# fill NA with previous value
def fill(s):
    a = array(0)
    r = s[~isnull(s)].index
    a = append(a, r)
    a = append(a, len(s))
    le = a[1:] - a[:len(a) - 1]
    l = []
    for i in range(len(le)):
        l = l + repeat(s[a[i]], le[i]).tolist()
    return Series(l, name=s.name)

closeWithXdr[['b']] = closeWithXdr[['b']].apply(fill)
closeWithXdr[['開盤價', '收盤價', '最高價', '最低價']] = closeWithXdr[['開盤價', '收盤價', '最高價', '最低價']].astype(float)
del close, xdr
closeWithXdr['調整收盤價']=closeWithXdr.收盤價+closeWithXdr.b
closeWithXdr = closeWithXdr.drop(['a', 'b'], axis=1)

closeWithXdr['d'] = closeWithXdr['調整收盤價'] - closeWithXdr['收盤價']
closeWithXdr['調整開盤價'] = closeWithXdr['開盤價'] + closeWithXdr.d
closeWithXdr['調整收盤價'] = closeWithXdr['收盤價'] + closeWithXdr.d
closeWithXdr['調整最高價'] = closeWithXdr['最高價'] + closeWithXdr.d
closeWithXdr['調整最低價'] = closeWithXdr['最低價'] + closeWithXdr.d
closeWithXdr['lnmo'] = log(closeWithXdr['調整收盤價']/closeWithXdr['調整收盤價'].shift(120))

# return
@timeSpan
def Return(*period):
    for days in period:
        n = 240/days
        closeWithXdr['r' + str(days)] = (closeWithXdr['調整收盤價'].shift(-days)/closeWithXdr['調整收盤價'])**n-1
Return(5, 10, 20, 40, 60, 120)

# log return
@timeSpan
def lnReturn(*period):
    for days in period:
        n = 240/days
        closeWithXdr['lnr' + str(days)] = log(closeWithXdr['調整收盤價'].shift(-days)/closeWithXdr['調整收盤價'])*n
lnReturn(5, 10, 20, 40, 60, 120)

# return standard deviation
@timeSpan
def ReturnStd(*period):
    for days in period:
        name = 'r' + str(days)
        closeWithXdr[name + 'Std'] = (closeWithXdr[name]-closeWithXdr[name].mean())/closeWithXdr[name].std()
ReturnStd(5, 10, 20, 40, 60, 120)

# rsi
closeWithXdr['ch'] = closeWithXdr['調整收盤價'].diff()
closeWithXdr['ch_u'], closeWithXdr['ch_d'] = closeWithXdr['ch'], closeWithXdr['ch']
closeWithXdr.ix[closeWithXdr.ch_u < 0, 'ch_u'], closeWithXdr.ix[closeWithXdr.ch_d > 0, 'ch_d'] = 0, 0
closeWithXdr['ch_d'] = closeWithXdr['ch_d'].abs()
closeWithXdr['rsi'] = closeWithXdr.ch_u.ewm(alpha=1/14).mean()/(closeWithXdr.ch_u.ewm(alpha=1/14).mean()+closeWithXdr.ch_d.ewm(alpha=1/14).mean())*100 #與r和凱基同,ema的公式與一般的ema不同。公式見http://www.fmlabs.com/reference/default.htm?url=RSI.htm
closeWithXdr = closeWithXdr.drop(['ch', 'ch_u', 'ch_d'], axis=1)

# ma
@timeSpan
def ma(*period):
    for n in period:
        closeWithXdr['MA'+str(n)] = closeWithXdr['收盤價'].rolling(window=n).mean()
@timeSpan
def ma_adj(*period):
    for n in period:
        closeWithXdr['MA'+str(n)+'.adj'] = closeWithXdr['調整收盤價'].rolling(window=n).mean()
ma(5, 10, 20, 60, 120)
ma_adj(5, 10, 20, 60, 120)

# DI
closeWithXdr['DI'] = (closeWithXdr['最高價']+closeWithXdr['最低價']+2*closeWithXdr['收盤價'])/4
closeWithXdr['DI.adj'] = (closeWithXdr['調整最高價']+closeWithXdr['調整最低價']+2*closeWithXdr['調整收盤價'])/4

# macd
closeWithXdr['max9'] = closeWithXdr['最高價'].rolling(window=9).max()
closeWithXdr['min9'] = closeWithXdr['最低價'].rolling(window=9).min()
closeWithXdr['EMA12'] = closeWithXdr.DI.ewm(alpha=2/13).mean()
closeWithXdr['EMA26'] = closeWithXdr.DI.ewm(alpha=2/27).mean()
closeWithXdr['DIF'] = closeWithXdr['EMA12']-closeWithXdr['EMA26']
closeWithXdr['MACD'] = closeWithXdr.DIF.ewm(alpha=0.2).mean()
closeWithXdr['MACD1'] = (closeWithXdr['EMA12']-closeWithXdr['EMA26'])/closeWithXdr['EMA26']*100
closeWithXdr['OSC'] = closeWithXdr.DIF - closeWithXdr.MACD

# bband
closeWithXdr['std5'] = closeWithXdr['DI'].rolling(window=5).std()
closeWithXdr['std10'] = closeWithXdr['DI'].rolling(window=11).std()
closeWithXdr['std20'] = closeWithXdr['DI'].rolling(window=20).std()
closeWithXdr['mavg'] = closeWithXdr['DI'].rolling(window=20).mean()
closeWithXdr['up'] = closeWithXdr.mavg + closeWithXdr['std20']*2
closeWithXdr['dn'] = closeWithXdr.mavg - closeWithXdr['std20']*2
closeWithXdr['bband'] = (closeWithXdr['收盤價']-closeWithXdr.mavg)/closeWithXdr['std20']

# bband adj
closeWithXdr['std5.adj'] = closeWithXdr['DI.adj'].rolling(window=5).std()
closeWithXdr['std10.adj'] = closeWithXdr['DI.adj'].rolling(window=11).std()
closeWithXdr['std20.adj'] = closeWithXdr['DI.adj'].rolling(window=20).std()
closeWithXdr['mavg.adj'] = closeWithXdr['DI.adj'].rolling(window=20).mean()
closeWithXdr['up.adj'] = closeWithXdr['mavg.adj'] + closeWithXdr['std20.adj']*2
closeWithXdr['dn.adj'] = closeWithXdr['mavg.adj'] - closeWithXdr['std20.adj']*2
closeWithXdr['bband.adj'] = (closeWithXdr['調整收盤價']-closeWithXdr['mavg.adj'])/closeWithXdr['std20.adj']

# kd
closeWithXdr['rsv'] = (closeWithXdr['收盤價']-closeWithXdr.min9)/(closeWithXdr.max9-closeWithXdr.min9)
closeWithXdr['k'] = closeWithXdr.rsv.ewm(alpha=1/3).mean()
closeWithXdr['d'] = closeWithXdr.k.ewm(alpha=1/3).mean()

# others
closeWithXdr['high-low'] = (closeWithXdr['最高價']-closeWithXdr['最低價'])/closeWithXdr['收盤價']
closeWithXdr['pch'] = (closeWithXdr['收盤價']-closeWithXdr['收盤價'].shift())/closeWithXdr['收盤價'].shift()
closeWithXdr['pctB'] = (closeWithXdr.DI-closeWithXdr.dn)/(closeWithXdr.up-closeWithXdr.dn)
closeWithXdr['close-up'] = (closeWithXdr['收盤價']-closeWithXdr.up)/(closeWithXdr.DI.rolling(window=20).std()*2)
closeWithXdr['close-dn'] = (closeWithXdr['收盤價']-closeWithXdr.dn)/(closeWithXdr.DI.rolling(window=20).std()*2)

closeWithXdr['pctB.adj'] = (closeWithXdr['DI.adj']-closeWithXdr['dn.adj'])/(closeWithXdr['up.adj']-closeWithXdr['dn.adj'])
closeWithXdr['close-up.adj'] = (closeWithXdr['調整收盤價']-closeWithXdr['up.adj'])/(closeWithXdr['DI.adj'].rolling(window=20).std()*2)
closeWithXdr['close-dn.adj'] = (closeWithXdr['調整收盤價']-closeWithXdr['dn.adj'])/(closeWithXdr['DI.adj'].rolling(window=20).std()*2)

timeDelta('before trend')

@timeSpan
def pch(df, columns):
    df1 = deepcopy(df)
    for col in columns:
        df1['pch_{}'.format(col)] = df1[col].pct_change()
    return df1
@timeSpan
def trend(df, columns):
    df1 = deepcopy(df)
    for col in columns:
        df1['trend_{}'.format(col)] = sign(df1['pch_{}'.format(col)])
        i = df1[df1['trend_{}'.format(col)] == 0].index
        while i.tolist() != []:
            df1.ix[i, 'trend_{}'.format(col)] = df1.ix[i - 1, 'trend_{}'.format(col)].tolist()
            i = df1[df1['trend_{}'.format(col)] == 0].index
    return df1
@timeSpan
def reversion(df, columns):
    df1 = deepcopy(df)
    for col in columns:
        # init reversion
        df1['reversion_{}'.format(col)] = df1['trend_{}'.format(col)] - df1['trend_{}'.format(col)]

        # trend reverse to positive
        i = df1[df1['trend_{}'.format(col)] == 1].index
        a = array(i)
        l = (a[1:] - a[:-1]).tolist()
        i = array([i for i, j in enumerate(l) if j != 1]) + 1
        df1.ix[a[i], 'reversion_{}'.format(col)] = 1

        # trend reverse to negtive
        i = df1[df1['trend_{}'.format(col)] == -1].index
        a = array(i)
        l = (a[1:] - a[:-1]).tolist()
        i = array([i for i, j in enumerate(l) if j != 1]) + 1
        df1.ix[a[i], 'reversion_{}'.format(col)] = -1

        # first reversion
        i = df1.ix[df1['trend_{}'.format(col)] == 1].index[0]
        if df1.ix[i, 'trend_{}'.format(col)]>df1.ix[i-1, 'trend_{}'.format(col)] and df1.ix[i, 'trend_{}'.format(col)] !=0:
            df1.ix[i, 'reversion_{}'.format(col)] = 1
        i = df1.ix[df1['trend_{}'.format(col)] == -1].index[0]
        if df1.ix[i, 'trend_{}'.format(col)]<df1.ix[i-1, 'trend_{}'.format(col)] and df1.ix[i, 'trend_{}'.format(col)] !=0:
            df1.ix[i, 'reversion_{}'.format(col)] = -1
        # print(df1[['pch_{}'.format(col), 'trend_{}'.format(col), 'reversion_{}'.format(col)]].head(100))
    return df1

closeWithXdr = pch(closeWithXdr, ['收盤價', 'MA5', 'MA10', 'MA20', 'MA60', 'MA120'])
closeWithXdr = trend(closeWithXdr, ['收盤價', 'MA5', 'MA10', 'MA20', 'MA60', 'MA120'])
closeWithXdr = reversion(closeWithXdr, ['收盤價', 'MA5', 'MA10', 'MA20', 'MA60', 'MA120'])
@timeSpan
def local_min_or_max(df, columns):
    df1 = deepcopy(df)
    for col in columns:
        df1['local_min(max)_{}'.format(col)] = df1['reversion_{}'.format(col)] - df1['reversion_{}'.format(col)]
        i = df1.ix[df1['reversion_{}'.format(col)] == 1].index
        a = array(i)
        df1.ix[a - 1, 'local_min(max)_{}'.format(col)] = df1.ix[a, 'reversion_{}'.format(col)].tolist()
        i = df1.ix[df1['reversion_{}'.format(col)] == -1].index
        a = array(i)
        df1.ix[a - 1, 'local_min(max)_{}'.format(col)] = df1.ix[a, 'reversion_{}'.format(col)].tolist()
    return df1

closeWithXdr = local_min_or_max(closeWithXdr, ['收盤價', 'MA5', 'MA10', 'MA20', 'MA60', 'MA120'])
@timeSpan
def new_high_or_low(df, columns):
    df1 = deepcopy(df)
    for col in columns:
        df1['new_high(low)_{}'.format(col)] = df1['local_min(max)_{}'.format(col)] - df1['local_min(max)_{}'.format(col)]
        i = df1.ix[df1['local_min(max)_{}'.format(col)] == 1, 'local_min(max)_{}'.format(col)].index.tolist()
        a = array(i)
        l = (df1['{}'.format(col)][a] - df1['{}'.format(col)][a].shift()).tolist()
        i = array([i for i, j in enumerate(l) if j > 0])
        df1.ix[a[i], 'new_high(low)_{}'.format(col)] = 1
        i = df1.ix[df1['local_min(max)_{}'.format(col)] == -1, 'local_min(max)_{}'.format(col)].index.tolist()
        a = array(i)
        l = (df1['{}'.format(col)][a] - df1['{}'.format(col)][a].shift()).tolist()
        i = array([i for i, j in enumerate(l) if j < 0])
        df1.ix[a[i], 'new_high(low)_{}'.format(col)] = -1
    return df1

closeWithXdr = new_high_or_low(closeWithXdr, ['收盤價', 'MA5', 'MA10', 'MA20', 'MA60', 'MA120'])

list(closeWithXdr)

closeWithXdr[['local_min(max)_MA5', 'new_high(low)_MA5']].head(100)

closeWithXdr['span'] = abs(closeWithXdr['調整收盤價']-closeWithXdr.調整開盤價)/closeWithXdr['調整收盤價']
closeWithXdr['span_high-low'] = abs(closeWithXdr['調整最高價']-closeWithXdr['調整最低價'])/closeWithXdr['調整收盤價']
closeWithXdr['upperShadow'] = (closeWithXdr['調整最高價'] - closeWithXdr[['調整開盤價', '調整收盤價']].max(axis=1))/closeWithXdr['調整收盤價']
closeWithXdr['lowerShadow'] = (closeWithXdr[['調整開盤價', '調整收盤價']].min(axis=1) - closeWithXdr['調整最低價'])/closeWithXdr['調整收盤價']
closeWithXdr['upperShadow/span'] =closeWithXdr['upperShadow']/(closeWithXdr['span']+0.1**10*closeWithXdr['調整收盤價'])
closeWithXdr['lowerShadow/span'] =closeWithXdr['lowerShadow']/(closeWithXdr['span']+0.1**10*closeWithXdr['調整收盤價'])
# closeWithXdr['span/upperShadow'] =closeWithXdr['span']/closeWithXdr['upperShadow']
# closeWithXdr['span/lowerShadow'] =closeWithXdr['span']/closeWithXdr['lowerShadow']
closeWithXdr['span/(high-low)'] =closeWithXdr['span']/closeWithXdr['span_high-low']
del closeWithXdr['d']
closeWithXdr['high-low_1ag1'] = closeWithXdr['high-low'].shift()
closeWithXdr['high-low_lag2'] = closeWithXdr['high-low'].shift(2)
closeWithXdr['upperShadow_lag1'] = closeWithXdr['upperShadow'].shift()
closeWithXdr['lowerShadow_lag1'] = closeWithXdr['lowerShadow'].shift()
closeWithXdr['upperShadow/span_lag1'] = closeWithXdr['upperShadow/span'].shift()
closeWithXdr['lowerShadow/span_lag1'] = closeWithXdr['lowerShadow/span'].shift()
# closeWithXdr['span/upperShadow_lag1'] = closeWithXdr['span/upperShadow'].shift()
# closeWithXdr['span/lowerShadow_lag1'] = closeWithXdr['span/lowerShadow'].shift()
closeWithXdr['spandiff'] = closeWithXdr.span.diff()
closeWithXdr['spanudiff'] = closeWithXdr[['調整開盤價', '調整收盤價']].max(axis=1).diff()
closeWithXdr['spanldiff'] = closeWithXdr[['調整開盤價', '調整收盤價']].min(axis=1).diff()
closeWithXdr['span/(high-low)_lag1'] = closeWithXdr['span/(high-low)'].shift()

timeDelta('before OSCsign')

closeWithXdr['OSCsign'] = sign(closeWithXdr.OSC)
closeWithXdr['gr'] = 0

OSCsign = closeWithXdr['OSCsign'].tolist()
gr = closeWithXdr['gr'].tolist()
g = 0
for i in range(len(OSCsign)-1):
    if OSCsign[i]*OSCsign[i+1] < 0:
        g+=1
        gr[i+1] = g
    else:
        gr[i+1] = g

closeWithXdr['OSCsign'], closeWithXdr['gr'] = OSCsign, gr
del g, OSCsign, gr
@timeSpan
def minORmax(df):
    df1 = deepcopy(df)
    if df1.max()>0:
        return df1.max()
    if df1.min()<0:
        return df1.min()
    else:
        return df1

grouped = closeWithXdr.groupby('gr')
l = grouped['OSC'].apply(minORmax).tolist()

d = {}
for i, v in enumerate(l):
    d[i+2] = v
d[0], d[1] = nan, nan
closeWithXdr[['gr1']] = closeWithXdr[['gr']].applymap(lambda x:d[x])

closeWithXdr['change'] = 0
@timeSpan
def OSCbreakpoint(df):
    df1 = deepcopy(df)
    df1=df1.reset_index(drop=True)  # without this df1.ix[0,'gr1'] is only defined in first group
    if df1['OSC'].max()>0:
        for i in range(len(df1['gr1'])):
            # print(i, len(df1['gr1']))
            # print(i, df1.ix[i,'OSC'], df1.ix[i,'gr1'])
            if df1.ix[i,'OSC']>df1.ix[i,'gr1']:
                # print(i, 'yes')
                df1.ix[i, 'change'] = 1
                break
        return df1
    if df1['OSC'].min()<0:
        for i in range(len(df1['gr1'])):
            # print(i, len(df1['gr1']))
            # print(i, df1.ix[i,'OSC'], df1.ix[i,'gr1'])
            if df1.ix[i,'OSC']<df1.ix[i,'gr1']:
                # print(i, 'yes')
                df1.ix[i, 'change'] = -1
                break
        return df1
    else:
        return df1

closeWithXdr = grouped.apply(OSCbreakpoint).reset_index(drop=True)
del closeWithXdr['OSCsign'], closeWithXdr['gr'], closeWithXdr['gr1']
list(closeWithXdr)
timeDelta('closeWithXdr')

timeDelta('tse')

#---- bic ----
conn = connect('bic.sqlite3')
c = conn.cursor()
sql = "SELECT * FROM '{}'"
bic = read_sql_query(sql.format('景氣指標及燈號-指標構成項目'), conn)
del bic['年月']

m = reduce(mymerge, [closeWithXdr, value, deal, fore, trust, index, index1, rindex, report, bic]) # index1 is not up to date, which causes merge problem

mer = deepcopy(m)

list(m)
list(mer)
report.dtypes
'r5' in list(m)
timeDelta('merge')
m.dtypes

m.年月日 = to_datetime(m.年月日, format='%Y/%m/%d').apply(lambda x: x.date()) # should convert to datetime before sort, or the result is  wrong
m=m.sort_values(['年月日','證券代號']).reset_index(drop=True) # reset_index make the index ascending
m['r5']
list(m['r5'])

m[list(report)] = m[list(report)].apply(fill) # index1 is not up to date, which causes merge problem
m['time'] = m.index.tolist()
col = ['年月日', '證券代號', '年', '季']
m = m.replace('--', nan)
m = m[col+[x for x in list(m) if x not in col]]
col = ['年月日', '證券代號', '證券名稱', '公司名稱', '年', '季', '漲跌(+/-)', '外資鉅額交易', '投信鉅額交易']
m[[x for x in list(m) if x not in col]] = m[[x for x in list(m) if x not in col]].astype(float)
col = ['年月日', '證券代號', 'time', '成交股數', '成交筆數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '調整收盤價', '漲跌(+/-)', '漲跌價差', '最後揭示買價', '最後揭示買量', '最後揭示賣價',
  '最後揭示賣量', '本益比', '殖利率(%)', '股價淨值比', '自營商(自行買賣)賣出股數', '自營商(自行買賣)買賣超股數', '自營商(自行買賣)買進股數', '自營商(避險)賣出股數', '自營商(避險)買賣超股數',
  '自營商(避險)買進股數', '自營商賣出股數', '自營商買賣超股數', '自營商買進股數', '外資鉅額交易', '外資買進股數', '外資賣出股數', '外資買賣超股數', '投信鉅額交易', '投信買進股數',
  '投信賣出股數', '投信買賣超股數', '基本每股盈餘（元）','每股參考淨值', '流動比率', '負債佔資產比率', '權益報酬率', '毛利率', '營業利益率', '綜合稅後純益率', 'grow_s', 'grow_hy', 'grow_y', 'grow',
    '本期綜合損益總額.wma', '本期綜合損益總額.ma', 'profitbility', 'investment', '建材營造類指數', '漲跌點數', '漲跌百分比(%)', '建材營造類報酬指數', 'r漲跌點數', 'r漲跌百分比(%)']+list(index1)[1:]
col = [ii for n, ii in enumerate(col) if ii not in col[:n]]
timeDelta('before dropna')
del m['年'], m['季'], m['月']
m = m.dropna(axis=1, how='all')
list(m.dtypes)

list(m)
# TWII = web.DataReader("^TWII", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'TWII'})
# SSE = web.DataReader("000001.SS", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'SSE'})
# HSI = web.DataReader("^HSI", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'HSI'})
# # STI = web.DataReader("^STI", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'STI'})
# N225 = web.DataReader("^N225", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'N225'})
# AXJO = web.DataReader("^AXJO", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'AXJO'})
# GSPC = web.DataReader("^GSPC", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'GSPC'})
# IXIC = web.DataReader("^IXIC", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'IXIC'})
# GDAXI = web.DataReader("^GDAXI", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'GDAXI'})
# # FTSE = web.DataReader("^FTSE", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'FTSE'})
# STOXX50E = web.DataReader("^STOXX50E", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'STOXX50E'})
# l = [TWII, SSE, HSI, N225, AXJO, GSDIC, IXIC, GDAXI, STOXX50E]
# index = reduce(mymerge, l).sort_values(['年月日'])
# index.年月日=to_datetime(index.年月日).apply(lambda x: x.date())
# print('index')

m.dtypes

# forweb = m[col+list(bic)]

forweb = m[['年月日', '證券代號', 'time'] + [x for x in list(m) if x not in ['年月日', '證券代號', 'time']]]
forweb['earning'] = forweb['收盤價']/forweb['本益比']
list(forweb)

tablename = 'forweb'
# forweb = mymerge(forweb, index).sort_values(['年月日'])

# forweb['漲跌(+/-)'] = forweb['漲跌(+/-)'].replace('＋', 1).replace('－', -1).replace('X', 0).replace(' ', None).astype(float)
# forweb['外資鉅額交易'] = forweb['外資鉅額交易'].replace('yes', 1).replace('no', 0).astype(float)
# forweb['投信鉅額交易'] = forweb['投信鉅額交易'].replace('yes', 1).replace('no', 0).astype(float)

forweb.年月日 = forweb.年月日.astype(str)
forweb.證券代號 = forweb.證券代號.astype(str)
forweb = forweb.drop_duplicates(['年月日', '證券代號'])
# list(forweb)
conn = connect('mysum.sqlite3')
c = conn.cursor()

sql = 'ALTER TABLE `{}` RENAME TO `{}0`'.format(tablename, tablename)
c.execute(sql)
sql = 'create table `{}` (`{}`, PRIMARY KEY ({}))'.format(tablename, '`,`'.join(list(forweb)), '`年月日`, `證券代號`')
c.execute(sql)
sql = 'insert into `{}`(`{}`) values({})'.format(tablename, '`,`'.join(list(forweb)), ','.join('?'*len(list(forweb))))
c.executemany(sql, forweb.values.tolist())
conn.commit()
sql = "drop table `{}0`".format(tablename)
c.execute(sql)

# sql = 'DROP TABLE forweb'
# c.execute(sql)
# forweb.to_sql('forweb', conn, index=False)
list(forweb)
# forweb.to_sql('forweb1', connect('C:/Users/ak66h_000/OneDrive/webscrap/djangogirls/mysite/db.sqlite3'))
# forweb.to_sql('forweb', connect('C:/Users/ak66h_000/OneDrive/testpydev/src/db.sqlite3'), index=False)
# forweb.to_csv('C:/Users/ak66h_000/Dropbox/forspark.csv', index=False)
# forweb.to_json('C:/Users/ak66h_000/Dropbox/forspark.json',force_ascii=False)
forweb = forweb.reset_index(drop=True)
# del closeWithXdr, value, deal, fore, trust, index, index1, rindex, report, bic
timeDelta('finish')