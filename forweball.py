  # ----import----
from sqlite3 import *
import os
os.chdir('C:\\Users\\ak66h_000\\Documents\\db\\')
# os.chdir('D:/')
conn = connect('mops.sqlite3')
c = conn.cursor()

from numpy import *
from pandas import *
from functools import *
# from pandas.io import data, wb
# from pandas_datareader import data, wb
# import pandas.io.data as web
import pandas_datareader.data as web

## --- read from sqlite ---
def mymerge(x, y):
    m = merge(x, y, on=[col for col in list(x) if col in list(y)], how='outer')
    return m

# --- report---
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

sql = "SELECT * FROM '%s' "% ('ifrs前後-綜合損益表')
inc = read_sql_query(sql, conn).replace('--', 'NaN')
col = ['年', '季', '公司代號', '營業收入', '營業成本', '營業毛利（毛損）', '未實現銷貨（損）益', '已實現銷貨（損）益', '營業毛利（毛損）淨額', '營業費用',
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
inc.dtypes
inc = inc.groupby(['公司代號', '年']).apply(change1).reset_index(drop=True)  #'季' must be string
inc['grow_s'] = inc.groupby(['公司代號'])['本期綜合損益總額'].pct_change(1)
inc['grow_hy'] = inc.groupby(['公司代號'])['本期綜合損益總額'].rolling(window=2).sum().reset_index(drop=True).pct_change(2)
inc[col1] = inc.groupby(['公司代號'])[col1].rolling(window=4).sum().reset_index(drop=True)
inc['grow_y'] = inc.groupby(['公司代號'])['本期綜合損益總額'].pct_change(4)
inc['grow'] = inc.groupby(['公司代號'])['本期綜合損益總額'].pct_change(1)
# inc['grow.ma'] = inc['grow'].rolling(window=24).mean()*4
inc['本期綜合損益總額.wma'] = inc.groupby(['公司代號'])['本期綜合損益總額'].apply(lambda x: ewma(x, com=19)).mean() * 4
inc['本期綜合損益總額.ma'] =  inc.groupby(['公司代號'])['本期綜合損益總額'].rolling(window=12).mean().reset_index(drop=True) * 4
sql = "SELECT * FROM '%s'"
bal = read_sql_query(sql % ('ifrs前後-資產負債表-一般業'), conn)
bal[['年', '季']]=bal[['年', '季']].astype(str)
del bal['公司名稱']
print('mops')

#--- summary ---
conn = connect('summary.sqlite3')
sql = "SELECT * FROM '%s'" % ('會計師查核報告')
ac = read_sql_query(sql, conn).replace('--', 'NaN').rename(columns={'公司代號': '證券代號', '公司簡稱': '證券名稱', '核閱或查核日期': '年月日'}).sort_values(['年', '季', '證券代號']).drop(['簽證會計師事務所名稱', '簽證會計師','簽證會計師.1', '核閱或查核報告類型'], axis=1)
ac[['年', '季']]=ac[['年', '季']].astype(str)
del ac['證券名稱']
# ac['\u3000 核閱或查核日期'] = ac['\u3000 核閱或查核日期'].replace('-', '/', regex=True)
# ac['\u3000 核閱或查核日期'] = ac['\u3000 核閱或查核日期'].replace('\xa0', '', regex=True)
# com = "'3056%'"
sql = "SELECT * FROM '%s'"
fin = read_sql_query(sql % ('財務分析'), conn)
del fin['公司簡稱']
report = mymerge(inc, bal)
report['流動比率'] = report['流動資產'] / report['流動負債']
report['負債佔資產比率'] = report['負債總額'] / report['資產總額']
report['權益報酬率'] = report['綜合損益總額歸屬於母公司業主'] * 2 / (report['權益總額'] + report.groupby(['公司代號'])['權益總額'].shift())
report['profitbility'] = report.綜合損益總額歸屬於母公司業主 / (report.groupby(['公司代號'])['權益總額'].shift(4))
report['investment'] = report.groupby(['公司代號'])['權益總額'].pct_change(4)
report = report.rename(columns={'公司代號': '證券代號'})
report = mymerge(ac, report)
remcol = ['Unnamed: 21', '待註銷股本股數（單位：股）', 'Unnamed: 22', ]
report = report.drop(remcol, axis=1)
report[['年', '季', '綜合損益總額歸屬於母公司業主', '權益總額', 'profitbility', '權益報酬率']]
list(report)
print('summary')

#--- tse ---
def f(df):
    half = len(df.證券代號.unique()) // 3
    half = df.證券代號.unique()[0:half].tolist()
    criterion = df['證券代號'].map(lambda x: x in half)
    df = df[criterion]
    print(list(df))
    return df
conn = connect('tse.sqlite3')
sql="SELECT * FROM '%s'"
close = read_sql_query(sql% ('每日收盤行情(全部(不含權證、牛熊證))'), conn);close
close = f(close);close
value = read_sql_query(sql% ('個股日本益比、殖利率及股價淨值比'), conn).drop(['證券名稱'], 1)
value = f(value)
margin = read_sql_query(sql% ('當日融券賣出與借券賣出成交量值(元)'), conn)
margin = f(margin)
ins = read_sql_query(sql% ('三大法人買賣超日報(股)'), conn)
ins = f(ins)
# deal = read_sql_query(sql% ('自營商買賣超彙總表 (股)'), conn).drop(['證券名稱'], 1).fillna(0)
# deal = f(deal)
fore = read_sql_query(sql% ('外資及陸資買賣超彙總表 (股)'), conn).drop(['證券名稱'], 1).rename(columns={'買進股數':'外資買進股數','賣出股數':'外資賣出股數','買賣超股數':'外資買賣超股數','鉅額交易': '外資鉅額交易'}).fillna('no')
fore = f(fore)
trust = read_sql_query(sql% ('投信買賣超彙總表 (股)'), conn).drop(['證券名稱'], 1).rename(columns={'買進股數':'投信買進股數','賣出股數':'投信賣出股數','買賣超股數':'投信買賣超股數','鉅額交易': '投信鉅額交易'}).fillna('no')
trust = f(trust)
index = read_sql_query("SELECT * FROM '%s' WHERE 指數 LIKE %s"% ('大盤統計資訊', "'建材營造類指數'"), conn).rename(columns={'收盤指數':'建材營造類指數'}).drop(['指數', '漲跌(+/-)'], axis=1).replace('--', nan).replace('---', nan)
index1 = read_sql_query("SELECT * FROM '%s'"% ('index'), conn).replace('--', nan).replace('---', nan)
rindex = read_sql_query("SELECT * FROM '%s' WHERE 指數 LIKE %s"% ('大盤統計資訊', "'建材營造類報酬指數'"), conn).rename(columns={'收盤指數':'建材營造類報酬指數', '漲跌點數':'r漲跌點數','漲跌百分比(%)':'r漲跌百分比(%)'}).drop(['指數', '漲跌(+/-)'], axis=1).replace('--', nan).replace('---', nan)
fore['外資鉅額交易'] = fore['外資鉅額交易'].replace('*', 'yes').replace(' ', 'no')
trust['投信鉅額交易'] = trust['投信鉅額交易'].replace('*', 'yes').replace(' ', 'no').replace(0, 'no')
close['本益比'] = close['本益比'].replace('0.00', nan) # pe is '0.00' when pe < 0
value['本益比'] = value['本益比'].replace('-', nan)  # pe is '-' when pe < 0
value['股價淨值比'] = value['股價淨值比'].replace('-', nan)
# close['證券代號'] = close['證券代號'].str.strip()
# deal['證券代號'] = deal['證券代號'].str.strip()
# fore['證券代號'] = fore['證券代號'].str.strip()
# trust['證券代號'] = trust['證券代號'].str.strip()
# close['證券名稱'] = close['證券名稱'].str.strip()
sql="SELECT * FROM '%s'"
xdr = read_sql_query(sql% ('除權息計算結果表'), conn).rename(columns={'股票代號': '證券代號', '股票名稱': '證券名稱'})
list(close)
list(value)
list(ins)
list(inc)
list(bal)
# list(deal)
list(fin)
list(trust)
print('tse')
list(ac)
m = mymerge(close, xdr)
del close
m = mymerge(m, value)
del value
# m = mymerge(m, deal)
# m[['自營商(自行買賣)賣出股數', '自營商(自行買賣)買賣超股數', '自營商(自行買賣)買進股數', '自營商(避險)賣出股數', '自營商(避險)買賣超股數', '自營商(避險)買進股數', '自營商賣出股數', '自營商買賣超股數', '自營商買進股數']] = m[['自營商(自行買賣)賣出股數', '自營商(自行買賣)買賣超股數', '自營商(自行買賣)買進股數', '自營商(避險)賣出股數', '自營商(避險)買賣超股數', '自營商(避險)買進股數', '自營商賣出股數', '自營商買賣超股數', '自營商買進股數']].fillna(0)
m=mymerge(m, fore)
del fore
m=mymerge(m, trust)
del trust
m[['投信買進股數', '投信賣出股數', '投信買賣超股數']] = m[['投信買進股數', '投信賣出股數', '投信買賣超股數']].fillna(0)
m[['投信鉅額交易']] = m[['投信鉅額交易']].fillna('no')
m=mymerge(m, index)
m=mymerge(m, index1)
m=mymerge(m, rindex)
m=mymerge(m, report)
list(m)
print('merge')
m.dtypes

m.年月日=to_datetime(m.年月日, format='%Y/%m/%d').apply(lambda x: x.date()) # should convert to datetime before sort, or the result is  wrong
m=m.sort_values(['年月日','證券代號']).reset_index(drop=True) # reset_index make the index ascending
m[list(report)] = m[list(report)].apply(fill)
m['淨利（淨損）歸屬於母公司業主'] = m['淨利（淨損）歸屬於母公司業主'].astype(float)
m['綜合損益總額歸屬於母公司業主'] = m['綜合損益總額歸屬於母公司業主'].astype(float)
m['毛利率'] = m['營業毛利（毛損）']/m['營業收入']
m['營業利益率'] = m['營業利益（損失）']/m['營業收入']
m['綜合稅後純益率'] = m['綜合損益總額歸屬於母公司業主']/m['營業收入']
m['time'] = m.index.tolist()
col=['年月日', '證券代號', '年', '季']
m = m.replace('--', nan)
m = m[col+[x for x in list(m) if x not in col]]
col=['年月日', '證券代號', '證券名稱', '公司名稱', '年', '季', '漲跌(+/-)', '外資鉅額交易', '投信鉅額交易']
m[[x for x in list(m) if x not in col]] = m[[x for x in list(m) if x not in col]].astype(float)
col=['年月日', '證券代號','time', '成交股數', '成交筆數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '調整收盤價', '漲跌(+/-)', '漲跌價差', '最後揭示買價', '最後揭示買量', '最後揭示賣價',
  '最後揭示賣量', '本益比', '殖利率(%)', '股價淨值比', '自營商(自行買賣)賣出股數', '自營商(自行買賣)買賣超股數', '自營商(自行買賣)買進股數', '自營商(避險)賣出股數', '自營商(避險)買賣超股數',
  '自營商(避險)買進股數', '自營商賣出股數', '自營商買賣超股數', '自營商買進股數', '外資鉅額交易', '外資買進股數', '外資賣出股數', '外資買賣超股數', '投信鉅額交易', '投信買進股數',
  '投信賣出股數', '投信買賣超股數', '基本每股盈餘（元）','每股參考淨值', '流動比率', '負債佔資產比率', '權益報酬率', '毛利率', '營業利益率', '綜合稅後純益率', 'grow_s', 'grow_hy', 'grow_y', 'grow',
    '本期綜合損益總額.wma', '本期綜合損益總額.ma', 'profitbility', 'investment', '建材營造類指數', '漲跌點數', '漲跌百分比(%)', '建材營造類報酬指數', 'r漲跌點數', 'r漲跌百分比(%)']+list(index1)[1:]
col = [ii for n,ii in enumerate(col) if ii not in col[:n]]
# m[['profitbility', '權益報酬率']]
print('before dropna')
list(m)
m['a'] = m['權值+息值'].replace(NaN, 0)
m['b'] = m['a'].cumsum()
m['調整收盤價']=m.收盤價+m.b
m = m.drop(['a', 'b'], axis=1)
m=m.dropna(axis=1, how='all')

TWII = web.DataReader("^TWII", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'TWII'})
SSE = web.DataReader("000001.SS", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'SSE'})
HSI = web.DataReader("^HSI", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'HSI'})
# STI = web.DataReader("^STI", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'STI'})
N225 = web.DataReader("^N225", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'N225'})
AXJO = web.DataReader("^AXJO", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'AXJO'})
GSPC = web.DataReader("^GSPC", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'GSPC'})
IXIC = web.DataReader("^IXIC", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'IXIC'})
GDAXI = web.DataReader("^GDAXI", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'GDAXI'})
# FTSE = web.DataReader("^FTSE", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'FTSE'})
STOXX50E = web.DataReader("^STOXX50E", "yahoo").reset_index()[['Date', 'Adj Close']].rename(columns={'Date': '年月日', 'Adj Close':'STOXX50E'})
l = [TWII, SSE, HSI, N225, AXJO, GSPC, IXIC, GDAXI, STOXX50E]
index = reduce(mymerge, l).sort_values(['年月日'])
index.年月日=to_datetime(index.年月日).apply(lambda x: x.date())
print('index')

forweb=m[col]
#---- bic ----
conn = connect('bic.sqlite3')
c = conn.cursor()
sql="SELECT * FROM '%s'"
bic = read_sql_query(sql% ('景氣指標及燈號-指標構成項目'), conn)
del bic['年月']
m['年月日']=m['年月日'].astype(str)
m['年'], m['月'] = m['年月日'].str.split('-').str[0].astype(int), m['年月日'].str.split('-').str[1].astype(int)
# m.dtypes
m=mymerge(m,bic)
del m['年']
del m['月']
del bic['年']
del bic['月']
m.年月日=to_datetime(m.年月日, format='%Y/%m/%d').apply(lambda x: x.date())

forweb=m[col+list(bic)]
forweb['e'] = forweb['收盤價']/forweb['本益比']
forweb['lnmo'] = log(forweb['調整收盤價']/forweb.groupby(['證券代號'])['調整收盤價'].shift(120))
forweb['lnr'] = log(forweb['調整收盤價']/forweb.groupby(['證券代號'])['調整收盤價'].shift())
forweb['lnr025'] = log(forweb.groupby(['證券代號'])['調整收盤價'].shift(-5)/forweb['調整收盤價'])*48
forweb['lnr05'] = log(forweb.groupby(['證券代號'])['調整收盤價'].shift(-10)/forweb['調整收盤價'])*24
forweb['lnr1'] = log(forweb.groupby(['證券代號'])['調整收盤價'].shift(-20)/forweb['調整收盤價'])*12
forweb['lnr2'] = log(forweb.groupby(['證券代號'])['調整收盤價'].shift(-40)/forweb['調整收盤價'])*6
forweb['lnr3'] = log(forweb.groupby(['證券代號'])['調整收盤價'].shift(-60)/forweb['調整收盤價'])*4
forweb['lnr6'] = log(forweb.groupby(['證券代號'])['調整收盤價'].shift(-120)/forweb['調整收盤價'])*2
# forweb['lnr025'] = (forweb['lnr'].rolling(window=5).mean()*240).shift(-5)
# forweb['lnr05'] = (forweb['lnr'].rolling(window=10).mean()*240).shift(-10)
# forweb['lnr1'] = (forweb['lnr'].rolling(window=20).mean()*240).shift(-20)
# forweb['lnr2'] = (forweb['lnr'].rolling(window=40).mean()*240).shift(-40)
# forweb['lnr3'] = (forweb['lnr'].rolling(window=60).mean()*240).shift(-60)
# forweb['lnr6'] = (forweb['lnr'].rolling(window=120).mean()*240).shift(-120)
# forweb['r025'] = exp(forweb['lnr025'])-1
# forweb['r05'] = exp(forweb['lnr05'])-1
# forweb['r1'] = exp(forweb['lnr1'])-1
# forweb['r2'] = exp(forweb['lnr2'])-1
# forweb['r3'] = exp(forweb['lnr3'])-1
# forweb['r6'] = exp(forweb['lnr6'])-1
forweb['r025'] = (forweb.groupby(['證券代號'])['調整收盤價'].shift(-5)/forweb['調整收盤價'])**48-1
forweb['r05'] = (forweb.groupby(['證券代號'])['調整收盤價'].shift(-10)/forweb['調整收盤價'])**24-1
forweb['r1'] = (forweb.groupby(['證券代號'])['調整收盤價'].shift(-20)/forweb['調整收盤價'])**12-1
forweb['r2'] = (forweb.groupby(['證券代號'])['調整收盤價'].shift(-40)/forweb['調整收盤價'])**6-1
forweb['r3'] = (forweb.groupby(['證券代號'])['調整收盤價'].shift(-60)/forweb['調整收盤價'])**4-1
forweb['r6'] = (forweb.groupby(['證券代號'])['調整收盤價'].shift(-120)/forweb['調整收盤價'])**2-1
forweb['r025.s']= (forweb.r025-forweb.r025.mean())/forweb.r025.std()
forweb['r05.s']= (forweb.r05-forweb.r05.mean())/forweb.r05.std()
forweb['r1.s']= (forweb.r1-forweb.r1.mean())/forweb.r1.std()
forweb['r2.s']= (forweb.r2-forweb.r2.mean())/forweb.r2.std()
forweb['r3.s']= (forweb.r3-forweb.r3.mean())/forweb.r3.std()
forweb['r6.s']= (forweb.r6-forweb.r6.mean())/forweb.r6.std()
forweb['h_l'] = (forweb.最高價-forweb.最低價)/forweb.調整收盤價
forweb['P'] = (forweb.最高價+forweb.最低價+2*forweb.調整收盤價)/4
forweb['pch'] = (forweb.調整收盤價-forweb.調整收盤價.shift())/forweb.調整收盤價.shift()
forweb['ch'] = forweb.調整收盤價.diff()
forweb['ch_u'], forweb['ch_d'] = forweb['ch'], forweb['ch']
forweb.ix[forweb.ch_u < 0, 'ch_u'], forweb.ix[forweb.ch_d > 0, 'ch_d'] = 0, 0
forweb['ch_d'] = forweb['ch_d'].abs()
forweb['rsi'] = forweb.ch_u.ewm(alpha=1/14).mean()/(forweb.ch_u.ewm(alpha=1/14).mean()+forweb.ch_d.ewm(alpha=1/14).mean())*100 #與r和凱基同,ema的公式與一般的ema不同。公式見http://www.fmlabs.com/reference/default.htm?url=RSI.htm
forweb['MA5'] = forweb.調整收盤價.rolling(window=5).mean()
forweb['MA10'] = forweb.調整收盤價.rolling(window=10).mean()
forweb['MA20'] = forweb.調整收盤價.rolling(window=20).mean()
forweb['MA60'] = forweb.調整收盤價.rolling(window=60).mean()
forweb['MA120'] = forweb.調整收盤價.rolling(window=120).mean()
forweb['max9'] = forweb.最高價.rolling(window=9).max()
forweb['min9'] = forweb.最低價.rolling(window=9).min()
forweb['EMA12'] = forweb.P.ewm(alpha=2/13).mean()
forweb['EMA26'] = forweb.P.ewm(alpha=2/27).mean()
forweb['DIF'] = forweb['EMA12']-forweb['EMA26']
forweb['MACD'] = forweb.DIF.ewm(alpha=0.2).mean()
forweb['MACD1'] = (forweb['EMA12']-forweb['EMA26'])/forweb['EMA26']*100
forweb['OSC'] = forweb.DIF-forweb.MACD
forweb['rsv'] = (forweb.調整收盤價-forweb.min9)/(forweb.max9-forweb.min9)
forweb['k']=forweb.rsv.ewm(alpha=1/3).mean()
forweb['d']=forweb.k.ewm(alpha=1/3).mean()
forweb['P1'] = (forweb.最高價+forweb.最低價+forweb.調整收盤價)/3
forweb['mavg']=forweb.P1.rolling(window=20).mean()
forweb['up']=forweb.mavg+forweb.P1.rolling(window=20).std()
forweb['dn']=forweb.mavg-forweb.P1.rolling(window=20).std()
forweb['pctB'] = (forweb.P1-forweb.dn)/(forweb.up-forweb.dn)
forweb['c_up'] = (forweb.調整收盤價-forweb.up)/forweb.up
forweb['c_dn'] = (forweb.調整收盤價-forweb.dn)/forweb.up
forweb['std5'] = forweb.調整收盤價.rolling(window=5).std()
forweb['std10'] = forweb.調整收盤價.rolling(window=11).std()
forweb['std20'] = forweb.調整收盤價.rolling(window=20).std()
forweb['sign']=sign(forweb['pch'])
forweb['trend']=forweb['sign']
i=forweb[forweb['trend']==0].index
while i.tolist() !=[]:
    forweb.ix[i, 'trend']=forweb.ix[i-1, 'trend'].tolist()
    i = forweb[forweb['trend'] == 0].index
forweb['trend']
i=forweb[forweb['trend']==1].index
a=array(i)
l=(a[1:]-a[:-1]).tolist()
i=array([ i for i, j in enumerate(l) if j !=1])+1
a[i]
forweb['reverse']=forweb['trend']*2
forweb.ix[a[i], 'reverse']=1

i=forweb[forweb['trend']==-1].index
a=array(i)
l=(a[1:]-a[:-1]).tolist()
i=array([ i for i, j in enumerate(l) if j !=1])+1
forweb.ix[a[i], 'reverse']=-1
forweb.ix[(forweb['reverse'] ==2) | (forweb['reverse'] == -2), 'reverse']=0
i=forweb.ix[~isnull(forweb['pch']),'pch'].index[0:2]
if forweb.ix[i[1], 'pch']>forweb.ix[i[1], 'pch'] and forweb.ix[i[1], 'pch'] !=0:
    forweb.ix[i[1], 'reverse'] = 1
if forweb.ix[i[1], 'pch']<forweb.ix[i[0], 'pch'] and forweb.ix[i[1], 'pch'] !=0:
    forweb.ix[i[1], 'reverse'] = -1
forweb[['pch', 'trend', 'reverse']].head(100)
del forweb['sign']

def f(df, c):
    df['pch_{}'.format(c)] = df[c].pct_change()
    df['sign_{}'.format(c)] = sign(df['pch_{}'.format(c)])
    df['trend_{}'.format(c)] = df['sign_{}'.format(c)]
    i = df[df['trend_{}'.format(c)] == 0].index
    while i.tolist() != []:
        df.ix[i, 'trend_{}'.format(c)] = df.ix[i - 1, 'trend_{}'.format(c)].tolist()
        i = df[df['trend_{}'.format(c)] == 0].index
    df['trend_{}'.format(c)]
    i = df[df['trend_{}'.format(c)] == 1].index
    a = array(i)
    l = (a[1:] - a[:-1]).tolist()
    i = array([i for i, j in enumerate(l) if j != 1]) + 1
    a[i]
    df['reverse_{}'.format(c)] = df['trend_{}'.format(c)] * 2
    df.ix[a[i], 'reverse_{}'.format(c)] = 1

    i = df[df['trend_{}'.format(c)] == -1].index
    a = array(i)
    l = (a[1:] - a[:-1]).tolist()
    i = array([i for i, j in enumerate(l) if j != 1]) + 1
    df.ix[a[i], 'reverse_{}'.format(c)] = -1
    df.ix[(df['reverse_{}'.format(c)] == 2) | (df['reverse_{}'.format(c)] == -2), 'reverse_{}'.format(c)] = 0
    i = df.ix[~isnull(df['pch_{}'.format(c)]), 'pch_{}'.format(c)].index[0:2]
    if df.ix[i[1], 'pch_{}'.format(c)] > df.ix[i[1], 'pch_{}'.format(c)] and df.ix[i[1], 'pch_{}'.format(c)] != 0:
        df.ix[i[1], 'reverse_{}'.format(c)] = 1
    if df.ix[i[1], 'pch_{}'.format(c)] < df.ix[i[0], 'pch_{}'.format(c)] and df.ix[i[1], 'pch_{}'.format(c)] != 0:
        df.ix[i[1], 'reverse_{}'.format(c)] = -1
    del df['sign_{}'.format(c)]
    # print(df[['pch_{}'.format(c), 'trend_{}'.format(c), 'reverse_{}'.format(c)]].head(100))

f(forweb, 'MA5')
f(forweb, 'MA10')
f(forweb, 'MA20')
f(forweb, 'MA60')
f(forweb, 'MA120')

#set_option("display.max_rows", 4000)
#set_option('display.expand_frame_repr', False)
#set_option("display.max_columns", 1000)
#forweb[['年月日','調整收盤價']]
#forweb.dtypes
#forweb['MA120'].tolist()
#forweb

forweb['newhl']=forweb['reverse']*2
i=forweb.ix[forweb['reverse'] ==1, 'reverse'].index.tolist()
a=array(i)
l = (forweb['調整收盤價'][a] - forweb['調整收盤價'][a].shift()).tolist()
i = array([i for i, j in enumerate(l) if j > 0])
forweb.ix[a[i], 'newhl'] = 1
i=forweb.ix[forweb['reverse'] ==-1, 'reverse'].index.tolist()
a=array(i)
l = (forweb['調整收盤價'][a] - forweb['調整收盤價'][a].shift()).tolist()
i = array([i for i, j in enumerate(l) if j < 0])
forweb.ix[a[i], 'newhl'] = -1
forweb.ix[(forweb['newhl'] == 2) | (forweb['newhl'] == -2), 'newhl'] = 0
# print(forweb[['調整收盤價', 'trend', 'reverse', 'newhl']])

def f(df, c):
    df['newhl_{}'.format(c)] = df['reverse_{}'.format(c)] * 2
    i = df.ix[df['reverse_{}'.format(c)] == 1, 'reverse_{}'.format(c)].index.tolist()
    a = array(i)
    l = (df['{}'.format(c)][a] - df['{}'.format(c)][a].shift()).tolist()
    i = array([i for i, j in enumerate(l) if j > 0])
    df.ix[a[i], 'newhl_{}'.format(c)] = 1
    i = df.ix[df['reverse_{}'.format(c)] == -1, 'reverse_{}'.format(c)].index.tolist()
    a = array(i)
    l = (df['{}'.format(c)][a] - df['{}'.format(c)][a].shift()).tolist()
    i = array([i for i, j in enumerate(l) if j < 0])
    df.ix[a[i], 'newhl_{}'.format(c)] = -1
    df.ix[(df['newhl_{}'.format(c)] == 2) | (df['newhl_{}'.format(c)] == -2), 'newhl_{}'.format(c)] = 0
    # print(df[['{}'.format(c), 'trend_{}'.format(c), 'reverse_{}'.format(c), 'newhl_{}'.format(c)]])
f(forweb, 'MA5')
f(forweb, 'MA10')
f(forweb, 'MA20')
f(forweb, 'MA60')

forweb['d'] = forweb.調整收盤價-forweb.收盤價
forweb['調整開盤價'] = forweb.開盤價 + forweb.d
forweb['調整收盤價'] = forweb.收盤價 + forweb.ｄ
forweb['調整最高價'] = forweb.最高價 + forweb.d
forweb['調整最低價'] = forweb.最低價 + forweb.ｄ
forweb['span'] = abs(forweb.調整收盤價-forweb.調整開盤價)/forweb.調整收盤價
forweb['span_hl'] = abs(forweb.調整最高價-forweb.調整最低價)/forweb.調整收盤價
forweb['ushadow'] = (forweb.調整最高價 - forweb[['調整開盤價', '調整收盤價']].max(axis=1))/forweb.調整收盤價
forweb['lshadow'] = (forweb[['調整開盤價', '調整收盤價']].min(axis=1) - forweb.調整最低價)/forweb.調整收盤價
forweb['ushadow/span'] =forweb['ushadow']/(forweb['span']+0.1**10*forweb.調整收盤價)
forweb['lshadow/span'] =forweb['lshadow']/(forweb['span']+0.1**10*forweb.調整收盤價)
del forweb['d']
forweb['h_l_1'] = forweb['h_l'].shift()
forweb['h_l_2'] = forweb['h_l'].shift(2)
forweb['ushadow_1'] = forweb['ushadow'].shift()
forweb['lshadow_1'] = forweb['lshadow'].shift()
forweb['ushadow/span_1'] = forweb['ushadow/span'].shift()
forweb['lshadow/span_1'] = forweb['lshadow/span'].shift()
forweb['spandiff'] = forweb.span.diff()
forweb['spanldiff'] = forweb[['調整開盤價', '調整收盤價']].max(axis=1).diff()

print('forweb')

tablename='forweb'
forweb = mymerge(forweb, index).sort_values(['年月日'])
forweb['漲跌(+/-)'] = forweb['漲跌(+/-)'].replace('＋', 1).replace('－', -1).replace('X', 0).replace(' ', None).astype(float)
forweb['外資鉅額交易']=forweb['外資鉅額交易'].replace('yes', 1).replace('no', 0).astype(float)
forweb['投信鉅額交易']=forweb['投信鉅額交易'].replace('yes', 1).replace('no', 0).astype(float)
forweb.年月日=forweb.年月日.astype(str)
forweb.證券代號=forweb.證券代號.astype(str)
forweb = forweb.drop_duplicates(['年月日', '證券代號'])
# list(forweb)
conn = connect('mysum.sqlite3')
c = conn.cursor()

sql='ALTER TABLE `%s` RENAME TO `%s0`'%(tablename, tablename)
c.execute(sql)
sql='create table `%s` (`%s`, PRIMARY KEY (%s))'%(tablename, '`,`'.join(list(forweb)), '`年月日`, `證券代號`')
c.execute(sql)
sql='insert into `%s`(`%s`) values(%s)'%(tablename, '`,`'.join(list(forweb)), ','.join('?'*len(list(forweb))))
c.executemany(sql, forweb.values.tolist())
conn.commit()
sql="drop table `%s0`"%tablename
c.execute(sql)

# sql = 'DROP TABLE forweb'
# c.execute(sql)
# forweb.to_sql('forweb', conn, index=False)
list(forweb)
# forweb.to_sql('forweb1', connect('C:/Users/ak66h_000/OneDrive/webscrap/djangogirls/mysite/db.sqlite3'))
# forweb.to_sql('forweb', connect('C:/Users/ak66h_000/OneDrive/testpydev/src/db.sqlite3'), index=False)
# forweb.to_csv('C:/Users/ak66h_000/Dropbox/forspark.csv', index=False)
# forweb.to_json('C:/Users/ak66h_000/Dropbox/forspark.json',force_ascii=False)
print('finish')

list(forweb)
lf=forweb.values.tolist()