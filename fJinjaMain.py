# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 09:43:49 2016

@author: ak66h_000
"""
from flask import Flask, jsonify, render_template, request
from urllib import parse
from pandas import *
from numpy import *
from sqlite3 import *
import os
path = 'C:/Users/ak66h_000/Documents/db/'
os.chdir(path)

import datetime as dateTime
epoch = dateTime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

app = Flask(__name__)

if __name__ == '__main__':
    app.run()

database = 'mops'
conn = connect('{}.sqlite3'.format(database))
c = conn.cursor()
mops = []
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
for i in range(len(c.fetchall())):
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tb = c.fetchall()[i][0]
    mops.append(tb)

database = 'mysum'
conn = connect('{}.sqlite3'.format(database))
c = conn.cursor()
mysum = []
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
for i in range(len(c.fetchall())):
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tb = c.fetchall()[i][0]
    mysum.append(tb)

database = 'summary'
conn = connect('{}.sqlite3'.format(database))
c = conn.cursor()
summary = []
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
for i in range(len(c.fetchall())):
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tb = c.fetchall()[i][0]
    summary.append(tb)

database = 'tse'
conn = connect('{}.sqlite3'.format(database))
c = conn.cursor()
tse = []
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
for i in range(len(c.fetchall())):
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tb = c.fetchall()[i][0]
    tse.append(tb)

dic = dict()
for i in mops:
    dic[i] = 'mops'
for i in mysum:
    dic[i] = 'mysum'
for i in summary:
    dic[i] = 'summary'
for i in tse:
    dic[i] = 'tse'

# used with form.serialize()
def PostParameters(data):
    requestUrl = request.args.get(data)
    print(requestUrl)
    print([parse.unquote(i) for i in requestUrl.split('&')])
    return [parse.unquote(i) for i in requestUrl.split('&')]

def getPostParameter(PostParameters, par):
    l = list(filter(lambda x: par in x, PostParameters))
    l = [i.split('=')[1] for i in l]
    if len(l) == 0:
        return None
    elif len(l) == 1:
        return l[0]
    else:
        return l

# l=[i.split('=')[1] for i in []]
# len(l)
# def fn(x):
#     return x if x > 5 else None
# a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# b = filter(fn, a)
# b
# list(b)
# list(filter(lambda x: x > 5, a))
# g=(item for item in a if fn(item))
# next(g)

d = dict()
@app.route('/', methods=['GET', 'POST'])   # should contain '/' in tail
def index():
    global d
    d['mops'], d['mysum'], d['summary'], d['tse'] = mops, mysum, summary, tse
    d['mops1'], d['mysum1'], d['summary1'], d['tse1'] = mops, mysum, summary, tse
    d['tab'] = '#tabs-1'
    return render_template('testlist.html', d=d)  #d is a dictionary, should appear in template

@app.route('/listfieldajax/', methods=['GET', 'POST'])
def listfieldajax():
    global tab, df, dbtable
    tab ='#tabs-1'
    d['tab'] = tab
    dbtable = getPostParameter(PostParameters('data'), 'dbtable')
    conn = connect('{}.sqlite3'.format(dic[dbtable]))
    df = read_sql_query("SELECT * from `{}`".format(dbtable), conn)
    d['fields'] = list(df)
    return jsonify({'fields': list(df)})

@app.route('/listfield1ajax/', methods=['GET', 'POST'])
def listfield1ajax():
    global tab, df, dbtable1
    tab ='#tabs-5'
    d['tab'] = tab
    dbtable1 = getPostParameter(PostParameters('data'), 'dbtable1')
    conn = connect('{}.sqlite3'.format(dic[dbtable1]))
    df = read_sql_query("SELECT * from `{}`".format(dbtable1), conn)
    d['fields1'] = list(df)
    return jsonify({'fields1': list(df)})

@app.route('/listfield2ajax/', methods=['GET', 'POST'])
def listfield2ajax():
    global tab, df, dbtable2, fields2
    tab ='#tabs-7'
    d['tab'] = tab
    dbtable2 = getPostParameter(PostParameters('data'), 'dbtable2')
    conn = connect('{}.sqlite3'.format(dic[dbtable2]))
    df = read_sql_query("SELECT * from `{}`".format(dbtable2), conn)
    fields2 = list(df)
    d['fields2'] = list(df)
    return jsonify({'fields2': list(df)})

@app.route('/listfield3ajax/', methods=['GET', 'POST'])
def listfield3ajax():
    global tab, df, dbtable3, fields3
    tab ='#tabs-7'
    d['tab'] = tab
    dbtable3 = getPostParameter(PostParameters('data'), 'dbtable3')
    conn = connect('{}.sqlite3'.format(dic[dbtable3]))
    df = read_sql_query("SELECT * from `{}`".format(dbtable3), conn)
    fields3 = list(df)
    d['fields3'] = list(df)
    return jsonify({'fields3': list(df)})

def ymdFirstList(cols):
    if '年月日' in cols:
        cols.remove('年月日')
        cols.insert(0, '年月日')
    else:
        cols.insert(0, '年月日')
    for c in cols:
        print(c)

@app.route('/query/', methods=['POST'])
def query():
    global mll, df, df1
    cols = request.form.getlist('cols')   # list object, empty is allowed
    d['cols'] = cols
    ymdFirstList(cols)
    database = 'mysum'
    conn = connect('{}.sqlite3'.format(database))
    c = conn.cursor()
    table = 'forr'
    df = read_sql_query('select `{}` from `{}`'.format('`,`'.join(cols), table), conn)
    df = df[cols]
    df['年月日'] = to_datetime(df['年月日'])
    df['年月日'] = df['年月日'].apply(unix_time_millis)
    df = df.dropna(subset=['年月日'])
    df1 = df.copy()
    l = array(df1).tolist()
    d['data'] = [['NaN' if isnull(x) else x for x in i] for i in l]
    d['labels'] = list(df1)
    d['y'] = list(df1)[1:]
    d['ymd'] = df1.年月日.tolist()
    list(df1)
    d['tab'] = '#tabs-2'
    return render_template('testlist.html', d=d)

mll, mll1 = {}, {}
mlineIndex = -1
@app.route('/mlineajax/', methods=['GET', 'POST'])
def mlineajax():
    global mlineIndex, mll, mll1, tab, d
    mlineIndex += 1
    pars = PostParameters('data')
    width = getPostParameter(pars, 'width')
    height = getPostParameter(pars, 'height')
    rangeselector = getPostParameter(pars, 'rangeselector')
    title = getPostParameter(pars, 'title')
    cols = getPostParameter(pars, 'cols')
    ymdFirstList(cols)
    conn = connect('{}.sqlite3'.format(dic[dbtable]))
    df = read_sql_query("SELECT `{}` from `{}`".format('`,`'.join(cols), dbtable), conn)
    print(list(df))
    df.ix[:, 1:] = df.ix[:, 1:].astype(float)
    d['labels'] = list(df)
    d['data'] = array(df).tolist()
    df['年月日'] = to_datetime(df['年月日'])
    df['年月日'] = df['年月日'].apply(unix_time_millis)
    df = df.dropna(subset=['年月日']).dropna(subset=cols[1:])
    df1 = df.copy()
    l = array(df1).tolist()
    data = [['NaN' if isnull(x) else x for x in i] for i in l]   # don't transfer data to string
    labels = list(df1)
    y = list(df1)[1:]
    ymd = df1.年月日.tolist()
    print(list(df1))
    if title is not None:
        title = read_sql_query("SELECT `證券代號` from `{}`".format(dbtable), conn).dropna().證券代號.unique()
        title = list(title)
        try:
            title.remove('nan')
        except Exception as e:
            print(e)
            pass
        print(title)
        if len(title)==1:
            title = title[0]
        else:
            print('證券代號 is not unique')
    print('rangeselector:', rangeselector)
    mll['dy'+str(mlineIndex)] = {'cols':cols, 'data':data, 'labels':labels, 'y':y, 'ymd':ymd, 'df1':df1, 'width':width, 'height':height, 'rangeselector':rangeselector, 'title':title}
    mll1['dy'+str(mlineIndex)] = {'cols':cols, 'data':data, 'labels':labels, 'y':y, 'ymd':ymd, 'df1':df1, 'width':width, 'height':height, 'rangeselector':rangeselector, 'title':title}
    d['mll'] = mll1
    tab ='#tabs-2'
    d['tab'] = tab
    d['tableid']='true'
    # return jsonify({'mlineIndex':mlineIndex, 'id': 'dy' + str(mlineIndex), 'data': data, 'labels': labels, 'rangeselector':rangeselector})
    return jsonify({'mlineIndex':mlineIndex, 'id': 'dy' + str(mlineIndex), 'data': data, 'labels': labels, 'width':width, 'height':height, 'rangeselector':rangeselector, 'title':title})

@app.route('/scaleajax/', methods=['GET', 'POST'])
def scaleajax():
    global mll, mll1, tab
    print('/scaleajax........................................../')
    id = request.args.get('name')
    if request.args.get('value') == 'raw':
        mll1[id]['df1'] = mll[id]['df1'].copy()
        li = array(mll1[id]['df1']).tolist()
        mll1[id]['data'] = [['NaN' if isnull(x) else x for x in a] for a in li].copy()
        print("raw........")
        return jsonify({'mlineIndex': int(id.replace('dy', '')), 'id': id, 'data': mll1[id]['data'], 'labels': mll1[id]['labels'], 'rangeselector': mll1[id]['rangeselector'], 'title':mll1[id]['title']})
    if request.args.get('value') == 'normalize':
        df = mll1[id]['df1'].copy()
        df.ix[:, 1:] = df.ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy()
        mll1[id]['df1'] = df.copy()
        li = array(mll1[id]['df1']).tolist()
        mll1[id]['data'] = [['NaN' if isnull(x) else x for x in a] for a in li].copy()
        print("normalize........")
        return jsonify({'mlineIndex': int(id.replace('dy', '')), 'id': id, 'data': mll1[id]['data'], 'labels': mll1[id]['labels'], 'rangeselector': mll1[id]['rangeselector'], 'title':mll1[id]['title']})
    if request.args.get('value') == 'remove':
        del mll1[id]
        del mll[id]
        print("remove........")
        return jsonify({'mlineIndex': int(id.replace('dy', ''))})

i = 0
@app.route('/mpajax/', methods=['GET', 'POST'])
def mpajax():
    global df, df1, i, L, tab
    L = []
    cols1 = getPostParameter(PostParameters('data'), 'cols1')
    cols2 = [x.replace('%', '').replace('(', '').replace(')', '').replace(' ', '').replace('/', '').replace('+', '') for x in cols1]
    print('cols2:',cols2)
    d['cols1'] = cols1
    cols3 = list(zip(cols1, cols2))
    d['cols3'] = cols3
    for col in cols1:
        cols = [col]
        i += 1
        print(i)
        ymdFirstList(cols)

        conn = connect('{}.sqlite3'.format(dic[dbtable1]))
        df = read_sql_query("SELECT `{}` from `{}`".format('`,`'.join(cols), dbtable1), conn)

        df['年月日'] = to_datetime(df['年月日'])
        df['年月日'] = df['年月日'].apply(unix_time_millis)
        df = df.dropna(subset=['年月日'])
        df1 = df
        l = array(df1).tolist()
        data1 = [['NaN' if isnull(x) else x for x in i] for i in l]
        labels1 = list(df1)
        y1 = list(df1)[1:]
        list(df1)
        ymd1 = df1.年月日.tolist()
        title = cols[1]
        print(title)
        L.append([i, cols1, data1, labels1, y1, ymd1, title])
    # d['L'] = [[1,2,3],[4,5,6]]
    d['L1'] = L
    tab = '#tabs-5'
    d['tab'] = tab
    # l=array(df).tolist()
    # d['q'] =[list(df)]+[['NaN' if isnull(x) else x for x in i] for i in l]
    # return render_template('c3.html', d=d)
    return jsonify({'L1':L})

L=[]
@app.route('/plot1ajax/', methods=['GET','POST'])
def plot1ajax():
    global i, L, tab
    print(i)
    # cols = getPostParameter(PostParameters('data'), 'plot1')
    cols = request.args.get('data')
    print(cols)
    cols = cols.replace('=', '')
    cols = [parse.unquote(i) for i in cols.split('&')]
    print('plot1:', cols)
    cols1 = cols
    ymdFirstList(cols)
    database = 'mysum'
    conn = connect('{}.sqlite3'.format(database))
    c = conn.cursor()
    table = 'forr'
    df = read_sql_query('select `{}` from `{}`'.format('`,`'.join(cols), table), conn)
    df = df[cols]
    df['年月日'] = to_datetime(df['年月日'])
    df['年月日'] = df['年月日'].apply(unix_time_millis)
    df = df.dropna(subset=['年月日'])
    df1 = df
    l = array(df1).tolist()
    data1 = [['NaN' if isnull(x) else x for x in i] for i in l]
    labels1 = list(df1)
    y1 = list(df1)[1:]
    # list(df1)
    ymd1 = df1.年月日.tolist()
    title = cols[1]
    # print(title)
    L.append([i, cols1, data1, labels1, y1, ymd1, title])
    # d['L'] = [[1,2,3],[4,5,6]]
    d['L'] = L
    tab = '#tabs-3'
    d['tab'] = tab
    i += 1
    # print(L)
    return jsonify({'L':L})

import datetime
from calendar import monthrange
s_m ={1:3, 2:6, 3:9, 4:12}
def sm(x):
    return(s_m[x])
mllys, mllys1, comp=[], [], []
k=0
@app.route('/ysajax/', methods=['GET','POST'])
def ysajax():
    global mllys, mllys1, d, k, comp
    k += 1
    pars = PostParameters('data')
    compid = getPostParameter(pars, 'compid')
    cols = getPostParameter(pars, 'cols2')
    print('cols:', cols)
    print('compid:', compid)
    # cols = request.form.getlist('cols2')
    # compid = request.form['compid']
    comp.append([k, cols, dbtable2, fields2])
    conn = connect('{}.sqlite3'.format(dic[dbtable2]))
    if '季' not in fields2:
        for i in ['公司代號', '公司名稱', '公司簡稱', '年', '季']:
            if i in cols:
                cols.remove(i)
        cols.insert(0, '年')
        df = read_sql_query('select `{}` from `{}` where `公司代號`="{}"'.format('`,`'.join(cols), dbtable2, compid), conn)
        df['年月日'] = df['年'].astype(str) + '-12-31'
        df = df.drop(['年'], axis=1)
    else:
        for i in ['公司代號', '公司名稱', '年', '季']:
            if i in cols:
                cols.remove(i)
        cols.insert(0, '年')
        cols.insert(1, '季')
        for c in cols:
            print(c)
        df = read_sql_query('select `{}` from `{}` where `公司代號`="{}"'.format('`,`'.join(cols), dbtable2, compid), conn)
        df['季'] = df['季'].astype(int)
        df['月'] = df.季.apply(sm)
        list(df)
        df['日'] = 1
        df['年月日'] = df['年'].astype(str) + '/' + (df['月']).astype(str) + '/' + df['日'].astype(str)
        df['年月日'] = to_datetime(df['年月日'], format='%Y/%m/%d')
        df['年月日'] = df['年月日'].apply(lambda x: dateTime.datetime(x.year, x.month, monthrange(x.year, x.month)[1]))
        df = df.drop(['年', '季', '月', '日'], axis=1)
        df['年月日'] = df['年月日'].astype(str)  # must be string

    df = df[[list(df)[-1]]+list(df)[:-1]]
    df = df.replace('--', 'NaN', regex=True)
    df.ix[:, 1:] = df.ix[:, 1:].astype(float)
    print(df)
    l = array(df).tolist()
    data = [list(df)]+[['NaN' if isnull(x) else x for x in i] for i in l]
    print(data)
    mllys.append([k, data, compid])
    mllys1.append([k, data, compid])
    d['mllys'] = mllys
    return jsonify({'mllys':mllys})

@app.route('/removeajax/', methods=['GET','POST'])
def removeajax():
    global mllys, mllys1, tab, d
    print('removeajax')
    name = request.args.get('data')
    print('name:', name)

    for i, l in enumerate(mllys1):
        print(i, 'c3' + str(l[0]), name, 'c3' + str(l[0]) == name)

    for i, l in enumerate(mllys1):
        print('l[0]:', l[0], 'name:', name)
        if 'c3' + str(l[0]) == name:
            mllys1.pop(i)
            print(mllys1)
            mllys.pop(i)
            comp.pop(i)
            d['mllys'] = mllys1
            tab = '#tabs-7'
            d['tab'] = tab
            return jsonify({'s':'removeajax'})

@app.route('/changeallajax/', methods=['GET','POST'])
def changeallajax():
    global mllys, mllys1, d, k, comp
    mllys, mllys1 =[], []
    compid = getPostParameter(PostParameters('data'), 'compid')
    print('compid:', compid)
    # compid=request.form['compid1']
    for l in comp:
        k, cols, dbtable2, fields2 = l[0], l[1], l[2], l[3]
        conn = connect('{}.sqlite3'.format(dic[dbtable2]))
        if '季' not in fields2:
            for i in ['公司代號', '公司名稱', '公司簡稱', '年', '季']:
                if i in cols:
                    cols.remove(i)
            cols.insert(0, '年')
            df = read_sql_query('select `{}` from `{}` where `公司代號`="{}"'.format('`,`'.join(cols), dbtable2, compid), conn)
            df['年月日'] = df['年'].astype(str) + '-12-31'
            df = df.drop(['年'], axis=1)
        else:
            for i in ['公司代號', '公司名稱', '年', '季']:
                if i in cols:
                    cols.remove(i)
            cols.insert(0, '年')
            cols.insert(1, '季')
            for c in cols:
                print(c)
            df = read_sql_query('select `{}` from `{}` where `公司代號`="{}"'.format('`,`'.join(cols), dbtable2, compid), conn)
            df['月'] = df.季.apply(sm)
            list(df)
            df['日'] = 1
            df['年月日'] = df['年'].astype(str) + '/' + (df['月']).astype(str) + '/' + df['日'].astype(str)
            df['年月日'] = to_datetime(df['年月日'], format='%Y/%m/%d')
            df['年月日'] = df['年月日'].apply(lambda x: dateTime.datetime(x.year, x.month, monthrange(x.year, x.month)[1]))
            df = df.drop(['年', '季', '月', '日'], axis=1)
            df['年月日'] = df['年月日'].astype(str)  # must be string

        df = df[[list(df)[-1]]+list(df)[:-1]]
        df = df.replace('--', 'NaN', regex=True)
        df.ix[:,1:] = df.ix[:,1:].astype(float)
        print('df:', df)
        l = array(df).tolist()
        data = [list(df)]+[['NaN' if isnull(x) else x for x in i] for i in l]
        print('data:', data)
        mllys.append([k, data, compid])
        mllys1.append([k, data, compid])
        d['mllys'] = mllys
        print('mllys', mllys)
    return jsonify({'mllys':mllys})

@app.route('/repajax/', methods=['GET', 'POST'])
def repajax():
    global report, tb, d, compid
    report=[]
    tb=[]
    database = 'summary'
    conn = connect('{}.sqlite3'.format(database))
    c = conn.cursor()
    compid = getPostParameter(PostParameters('data'), 'compid_report')
    print(compid)

    # compid='5522'
    # compid = request.form['compid_report']
    d['compid_report'] = compid
    # table = '綜合損益表-一般業'
    # table = '資產負債表-一般業'
    for table in ['綜合損益表-一般業', '資產負債表-一般業']:
        df = read_sql_query('select * from `{}` where `公司代號`="{}"'.format(table, compid), conn)
        d['compname']=df.ix[len(df)-1, '公司名稱']
        color={1:'rgb(0,255,0)', 2:'rgb(0, 190, 255)', 3:'orange', 4:'rgb(255, 75, 140)'}
        df2=df.copy()
        df3=df.copy()
        df3.ix[:, 4:] = df3.ix[:, 4:].replace('--', 0)
        df3.ix[:, 4:] = df3.ix[:, 4:].astype(float)
        for i in color:
            df2.ix[df.季==i, 2:]=color[i]
        smd={1:'3/31', 2:'6/30', 3:'9/30', 4:'12/31'}
        # df['年季'] = df['年'].astype(str) + '年第' + df['季'].astype(str) + '季'
        df['年季'] = df['年'].astype(str)+'/' + df['季'].apply(lambda x: smd[x])
        for i in range(len(df3)):
            for j in range(df3.shape[1]):
                try:
                    if df3.iloc[i, j] < 0:
                        df2.iloc[i, j] = 'red'
                except:
                    pass
        df2['年季'] = df2['年'].astype(str) + df2['季'].apply(lambda x:smd[x])
        df = df.drop(['年', '季', '公司代號', '公司名稱'], axis=1)
        df = df[[list(df)[-1]] + list(df)[:-1]]
        df2 = df2.drop(['年', '季', '公司代號', '公司名稱'], axis=1)
        df2 = df2[[list(df2)[-1]] + list(df2)[:-1]]
        l = vstack((array([list(df)]), array(df))).transpose().tolist()
        m = df.max().max()
        list(df)

        df1 = df.copy()
        df1=df1.fillna('0')
        df1.ix[:, 1:] = df1.ix[:, 1:].replace('--', 0)
        df1.ix[:, 1:] = df1.ix[:, 1:].astype(float)
        df1.ix[:, 1:] = df1.ix[:, 1:].apply(lambda x: x / m * 100)

        for c in ['基本每股盈餘（元）', '預收股款（權益項下）之約當發行股數（單位：股）', '母公司暨子公司所持有之母公司庫藏股股數（單位：股）', '每股參考淨值', '待註銷股本股數（單位：股）']:
            try:
                pem = df[c].max()
                df1[c] = df[c].apply(lambda x: x / pem * 100)
            except:
                pass
        for i in range(len(df1)):
            for j in range(df1.shape[1]):
                try:
                    if df1.iloc[i, j]<0:
                        df1.iloc[i, j]=df1.iloc[i, j]*(-1)
                except:
                    pass
        lw = vstack((array([list(df1)]), array(df1))).transpose().tolist()
        lc = vstack((array([list(df2)]), array(df2))).transpose().tolist()
        shape(lc)
        for i in lw:
            i[0]=0.0
        for i in lc:
            i[0]='white'
        li = []
        for i in range(len(l)):
            a=['--' if isnull(a) else a for a in l[i]]    # nan/None is not allowed in javascript
            b = ['--' if isnull(b) else b for b in lw[i]]
            c = ['--' if isnull(c) else c for c in lc[i]]
            li.append([list(z) for z in list(zip(a, b, c))])
        report.append(li)
        tb.append(table)
    # [list(i) for i in list(zip([1, 2, 3], [1, 2, 3]))]

    # for j in report[0][1:]:
    #     for i in j:
    #         print(i[0],i[1],i[2])
    d['report'] = report
    d['tb'] = tb
    d['tab'] = '#tabs-8'
    print('compname:', d['compname'], 'compid_report:', d['compid_report'], 'report:', report, 'tb:', tb)
    return jsonify({'compname': d['compname'], 'compid_report': d['compid_report'], 'report': report, 'tb': tb})

def replaceNull(x, y=''):
    if isnull(x):
        return y
    else:
        return x
@app.route('/rep1ajax/', methods=['GET', 'POST'])
def rep1ajax():
    global incStatement, balSheet, tb1, d, companyId, sparkline
    # companyId='5522'
    # table = 'ifrs前後-綜合損益表(季)-一般業'
    # table = 'ifrs前後-資產負債表-一般業'
    tb1 = {}
    sparkline={}
    database = 'summary'
    conn = connect('{}.sqlite3'.format(database))
    c = conn.cursor()
    companyId = getPostParameter(PostParameters('data'), 'companyId')
    print('companyId:', companyId)
    #---- income statement ----
    table = 'ifrs前後-綜合損益表(季)-一般業'
    tb1['inc'] = table
    df = read_sql_query('select * from `{}` where `公司代號`="{}"'.format(table, companyId), conn)
    df.dtypes
    col2 = {
        '營業成本': '&emsp;&emsp;營業成本',
        '未實現銷貨（損）益': '&emsp;&emsp;未實現銷貨（損）益',
        '已實現銷貨（損）益': '&emsp;&emsp;已實現銷貨（損）益',
        '營業費用': '&emsp;&emsp;營業費用',
        '其他收益及費損淨額': '&emsp;&emsp;其他收益及費損淨額',
        '營業外收入及支出': '&emsp;&emsp;營業外收入及支出',
        '營業外收入及利益': '&emsp;&emsp;營業外收入及利益',
        '所得稅費用（利益）': '&emsp;&emsp;所得稅費用（利益）',
        '停業單位損益': '&emsp;&emsp;停業單位損益',
        '合併前非屬共同控制股權損益': '&emsp;&emsp;合併前非屬共同控制股權損益',
        '其他綜合損益（淨額）': '&emsp;&emsp;其他綜合損益（淨額）',
        '合併前非屬共同控制股權綜合損益淨額': '&emsp;&emsp;合併前非屬共同控制股權綜合損益淨額',
        '會計原則變動累積影響數': '&emsp;&emsp;會計原則變動累積影響數'
    }
    df = df.rename(columns=col2)

    if len(df['公司名稱'].unique()) == 1:
        d['companyName'] = df['公司名稱'].unique()[0]
    else:
        print("len(d['companyName']) is not 1")

    floatCols = [col for col in list(df) if col not in ['年', '季', '公司代號', '公司名稱']]
    df.ix[:, floatCols] = df.ix[:, floatCols].replace('--', 0).astype(float)

    smd={1:'3/31', 2:'6/30', 3:'9/30', 4:'12/31'}
    df.insert(0, '年月日', df['年'].astype(str) + '/' + df['季'].apply(lambda x: smd[x]))
    color={1:'rgb(0,255,0)', 2:'rgb(0, 190, 255)', 3:'orange', 4:'rgb(255, 75, 140)'}
    dfColor = df.copy()
    dfColor.dtypes
    for i in color:
        dfColor.ix[df.季==i, floatCols]=color[i]

    for i in range(len(df)):
        for j in range(df.shape[1]):
            try:
                if df.iloc[i, j]<0:
                    dfColor.iloc[i, j]='red'
            except:
                pass

    df = df.drop(['年', '季', '公司代號', '公司名稱'], axis=1)
    dfColor = dfColor.drop(['年', '季', '公司代號', '公司名稱'], axis=1)
    dfWidth = df.copy()
    max = dfWidth[floatCols].max().max()
    dfWidth = dfWidth.fillna(0)
    dfWidth[floatCols] = dfWidth[floatCols].apply(lambda x: x / max * 100)
    df.dtypes
    for c in ['基本每股盈餘（元）']:
        try:
            pem = df[c].max()
            dfWidth[c] = df[c].apply(lambda x: x / pem * 100)
        except:
            pass
    for i in range(len(dfWidth)):
        for j in range(dfWidth.shape[1]):
            try:
                if dfWidth.iloc[i, j]<0:
                    dfWidth.iloc[i, j]=dfWidth.iloc[i, j]*(-1)
            except:
                pass

    dfPercent = df.copy()
    dfPercent.dtypes
    for i in list(dfPercent)[2:]:
        dfPercent[i] = dfPercent[i] / dfPercent.營業收入 * 100
    dfPercent.營業收入 = dfPercent.營業收入 / dfPercent.營業收入 * 100
    dfPercent.ix[:, 1:] = dfPercent.ix[:, 1:].applymap('{:,.0f}'.format) # this will convert float to object
    # df = df.fillna('')
    dfPercent = dfPercent.replace('nan', '')
    df[['基本每股盈餘（元）']] = df[['基本每股盈餘（元）']].applymap('{:,.2f}'.format)  # this will convert float to object
    lspan=['<span class=inc{}>sparklines</span>'.format(i) for i, j in enumerate(list(df))]
    l = vstack((array([list(df)]), array(df), array([lspan]))).transpose().tolist()
    lspan = [None for i in list(df)] # None for percent, width, color
    lp = vstack((array([list(dfPercent)]), array(dfPercent), array([lspan]))).transpose().tolist()
    lw = vstack((array([list(dfWidth)]), array(dfWidth), array([lspan]))).transpose().tolist()
    lc = vstack((array([list(dfColor)]), array(dfColor), array([lspan]))).transpose().tolist()
    for i in lw:
        i[0] = 0.0
    for i in lc:
        i[0] = 'white'
    for i in lp:
        i[0] = ''

    lsparkline = []
    for x in l:
        a = ['null' if i=='' else i for i in x]
        b = [replaceNull(i) for i in a]
        lsparkline.append(b)
    sparkline['inc'] = lsparkline
    # d['lsparkline'] = lsparkline

    incStatement = []
    for i in range(shape(l)[0]):
        row = []
        for j in range(shape(l)[1]):
            row.append({'value': replaceNull(l[i][j]), 'width': replaceNull(lw[i][j]), 'color': replaceNull(lc[i][j]), 'percent': replaceNull(lp[i][j])})
        incStatement.append(row)
    d['incStatement'] = incStatement
    print('incStatement')
    #---- balance sheet ----
    table = 'ifrs前後-資產負債表-一般業'
    tb1['bal'] = table
    df = read_sql_query('select * from `{}` where `公司代號`="{}"'.format(table, companyId), conn)
    df.dtypes
    col2 = {
        '流動資產': '&emsp;&emsp;流動資產',
        '非流動資產': '&emsp;&emsp;非流動資產',
        '基金與投資': '&emsp;&emsp;&emsp;&emsp;基金與投資',
        '固定資產': '&emsp;&emsp;&emsp;&emsp;固定資產',
        '無形資產': '&emsp;&emsp;&emsp;&emsp;無形資產',
        '其他資產': '&emsp;&emsp;&emsp;&emsp;其他資產',
        '流動負債': '&emsp;&emsp;流動負債',
        '非流動負債': '&emsp;&emsp;非流動負債',
        '長期負債': '&emsp;&emsp;&emsp;&emsp;長期負債',
        '各項準備': '&emsp;&emsp;&emsp;&emsp;各項準備',
        '其他負債': '&emsp;&emsp;&emsp;&emsp;其他負債',
        '股本': '&emsp;&emsp;股本',
        '資本公積': '&emsp;&emsp;資本公積',
        '保留盈餘': '&emsp;&emsp;保留盈餘',
        '其他權益': '&emsp;&emsp;其他權益',
        '庫藏股票': '&emsp;&emsp;庫藏股票',
        '歸屬於母公司業主之權益合計': '&emsp;&emsp;歸屬於母公司業主之權益合計',
        '共同控制下前手權益': '&emsp;&emsp;共同控制下前手權益',
        '合併前非屬共同控制股權': '&emsp;&emsp;合併前非屬共同控制股權',
        '非控制權益': '&emsp;&emsp;非控制權益'
    }
    df = df.rename(columns=col2)

    if len(df['公司名稱'].unique()) == 1:
        d['companyName'] = df['公司名稱'].unique()[0]
    else:
        print("len(d['companyName']) is not 1")

    floatCols = [col for col in list(df) if col not in ['年', '季', '公司代號', '公司名稱']]
    df.ix[:, floatCols] = df.ix[:, floatCols].replace('--', 0).astype(float)

    smd={1:'3/31', 2:'6/30', 3:'9/30', 4:'12/31'}
    df.insert(0, '年月日', df['年'].astype(str) + '/' + df['季'].apply(lambda x: smd[x]))
    color={1:'rgb(0,255,0)', 2:'rgb(0, 190, 255)', 3:'orange', 4:'rgb(255, 75, 140)'}
    dfColor = df.copy()
    dfColor.dtypes
    for i in color:
        dfColor.ix[df.季==i, floatCols]=color[i]

    for i in range(len(df)):
        for j in range(df.shape[1]):
            try:
                if df.iloc[i, j]<0:
                    dfColor.iloc[i, j]='red'
            except:
                pass

    df = df.drop(['年', '季', '公司代號', '公司名稱'], axis=1)
    dfColor = dfColor.drop(['年', '季', '公司代號', '公司名稱'], axis=1)
    dfWidth = df.copy()
    max = dfWidth[floatCols].max().max()
    dfWidth = dfWidth.fillna(0)
    dfWidth[floatCols] = dfWidth[floatCols].apply(lambda x: x / max * 100)
    df.dtypes
    for c in ['預收股款（權益項下）之約當發行股數（單位：股）', '母公司暨子公司所持有之母公司庫藏股股數（單位：股）', '每股參考淨值', '待註銷股本股數（單位：股）']:
        try:
            pem = df[c].max()
            dfWidth[c] = df[c].apply(lambda x: x / pem * 100)
        except:
            pass

    for i in range(len(dfWidth)):
        for j in range(dfWidth.shape[1]):
            try:
                if dfWidth.iloc[i, j]<0:
                    dfWidth.iloc[i, j]=dfWidth.iloc[i, j]*(-1)
            except:
                pass

    dfPercent = df.copy()
    dfPercent.dtypes
    a = list(dfPercent)[1:]
    a.remove('資產總額')
    for i in a:
        dfPercent[i] = dfPercent[i] / dfPercent.資產總額 * 100
    dfPercent.資產總額 = dfPercent.資產總額 / dfPercent.資產總額 * 100
    dfPercent.ix[:, 1:] = dfPercent.ix[:, 1:].applymap('{:,.0f}'.format) # this will convert float to object
    # df = df.fillna('')
    dfPercent = dfPercent.replace('nan', '')

    lspan=['<span class=bal{}>sparklines</span>'.format(i) for i, j in enumerate(list(df))]
    l = vstack((array([list(df)]), array(df), array([lspan]))).transpose().tolist()
    lspan = [None for i in list(df)] # None for percent, width, color
    lp = vstack((array([list(dfPercent)]), array(dfPercent), array([lspan]))).transpose().tolist()
    lw = vstack((array([list(dfWidth)]), array(dfWidth), array([lspan]))).transpose().tolist()
    lc = vstack((array([list(dfColor)]), array(dfColor), array([lspan]))).transpose().tolist()
    for i in lw:
        i[0] = 0.0
    for i in lc:
        i[0] = 'white'
    for i in lp:
        i[0] = ''

    lsparkline = []
    for x in l:
        a = ['null' if i == '' else i for i in x]
        b = [replaceNull(i) for i in a]
        lsparkline.append(b)
    sparkline['bal'] = lsparkline
    # d['lsparkline1'] = lsparkline

    balSheet = []
    for i in range(shape(l)[0]):
        row = []
        for j in range(shape(l)[1]):
            row.append({'value': replaceNull(l[i][j]), 'width': replaceNull(lw[i][j]), 'color': replaceNull(lc[i][j]),
                        'percent': replaceNull(lp[i][j])})
        balSheet.append(row)

    d['balSheet'] = balSheet
    print('balSheet')

    #----cash flow----
    database = 'xbrlcash'
    conn = connect('{}.sqlite3'.format(database))
    c = conn.cursor()
    table = 'ifrs現金流量表'
    tb1['cash'] = table
    df = read_sql_query('select * from `{}-{}`'.format(table, companyId), conn)
    df['年']=df['年'].astype(int)
    df['季'] = df['季'].astype(int)
    df.dtypes

    if len(df['公司代號'].unique()) == 1:
        d['companyId'] = df['公司代號'].unique()[0]
    else:
        print("len(d['companyId']) is not 1")

    floatCols = [col for col in list(df) if col not in ['年', '季', '公司代號']]
    df.ix[:, floatCols] = df.ix[:, floatCols].replace('--', 0).astype(float)

    smd = {1:'3/31', 2:'6/30', 3:'9/30', 4:'12/31'}
    df.insert(0, '年月日', df['年'].astype(str) + '/' + df['季'].apply(lambda x: smd[x]))
    color = {1:'rgb(0,255,0)', 2:'rgb(0, 190, 255)', 3:'orange', 4:'rgb(255, 75, 140)'}
    dfColor = df.copy()
    dfColor.dtypes
    for i in color:
        dfColor.ix[df.季 == i, floatCols]=color[i]

    df = df.drop(['年', '季', '公司代號'], axis=1)
    dfColor = dfColor.drop(['年', '季', '公司代號'], axis=1)
    dfWidth = df.copy()
    max = dfWidth[floatCols].max().max()
    dfWidth = dfWidth.fillna(0)
    dfWidth[floatCols] = dfWidth[floatCols].apply(lambda x: x / max * 100)
    df.dtypes

    for i in range(len(dfWidth)):
        for j in range(dfWidth.shape[1]):
            try:
                if dfWidth.iloc[i, j]<0:
                    dfWidth.iloc[i, j]=dfWidth.iloc[i, j]*(-1)
            except:
                pass

    lspan=['<span class=inc{}>sparklines</span>'.format(i) for i, j in enumerate(list(df))]
    l = vstack((array([list(df)]), array(df), array([lspan]))).transpose().tolist()
    lspan = [None for i in list(df)] # None for percent, width, color
    lw = vstack((array([list(dfWidth)]), array(dfWidth), array([lspan]))).transpose().tolist()
    lc = vstack((array([list(dfColor)]), array(dfColor), array([lspan]))).transpose().tolist()
    for i in lw:
        i[0] = 0.0
    for i in lc:
        i[0] = 'white'

    lsparkline = []
    for x in l:
        a = ['null' if i=='' else i for i in x]
        b = [replaceNull(i) for i in a]
        lsparkline.append(b)
    sparkline['cash'] = lsparkline
    # d['lsparkline'] = lsparkline

    cashFlow = []
    for i in range(shape(l)[0]):
        row = []
        for j in range(shape(l)[1]):
            row.append({'value': replaceNull(l[i][j]), 'width': replaceNull(lw[i][j]), 'color': replaceNull(lc[i][j])})
        cashFlow.append(row)
    d['cashFlow'] = cashFlow
    print('cashFlow')
    # --------
    d['tb1'] = tb1
    d['tab'] = '#tabs-9'
    return jsonify({'incStatement':incStatement, 'balSheet':balSheet, 'cashFlow':cashFlow, 'sparkline': sparkline, 'companyId': str(d['companyId']), 'companyName': d['companyName'], 'tb1': d['tb1'], 'tab': d['tab']})


# ----import----
from sqlite3 import *
import os
import time
from datetime import datetime, timedelta

def timeDelta(s):
    global starttime
    finishtime = datetime.now()
    print(s, 'timedelta: ', finishtime - starttime)
    starttime = finishtime

import requests
from bs4 import BeautifulSoup
from numpy import *
from pandas import *
from functools import *
# from pandas.io import data, wb
# from pandas_datareader import data, wb
# import pandas.io.data as web
# import pandas_datareader.data as web

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

@app.route('/changeForwebCompany/', methods=['GET', 'POST'])
def changeForwebCompany():
    global datetime, os

    os.chdir('C:\\Users\\ak66h_000\\Documents\\db\\')
    # os.chdir('D:/')
    conn = connect('mops.sqlite3')
    c = conn.cursor()


    # id = '5522'

    companyId = getPostParameter(PostParameters('data'), 'companyId')
    print('companyId:', companyId)

    com = "'%s'" % (companyId)
    sql = "SELECT * FROM '%s' WHERE 公司代號 LIKE %s" % ('ifrs前後-綜合損益表', com)
    inc = read_sql_query(sql, conn).replace('--', 'NaN')
    col = ['年', '季', '公司代號', '營業收入', '營業成本', '營業毛利（毛損）', '未實現銷貨（損）益', '已實現銷貨（損）益', '營業毛利（毛損）淨額', '營業費用',
           '其他收益及費損淨額', '營業利益（損失）', '營業外收入及支出', '稅前淨利（淨損）', '所得稅費用（利益）', '繼續營業單位本期淨利（淨損）', '停業單位損益', '合併前非屬共同控制股權損益',
           '本期淨利（淨損）', '其他綜合損益（淨額）', '合併前非屬共同控制股權綜合損益淨額', '本期綜合損益總額', '淨利（淨損）歸屬於母公司業主', '淨利（淨損）歸屬於共同控制下前手權益',
           '淨利（淨損）歸屬於非控制權益', '綜合損益總額歸屬於母公司業主', '綜合損益總額歸屬於共同控制下前手權益', '綜合損益總額歸屬於非控制權益', '基本每股盈餘（元）', '利息淨收益', '利息以外淨收益',
           '呆帳費用及保證責任準備提存（各項提存）', '淨收益', '保險負債準備淨變動', '支出及費用', '收入', '支出', '會計原則變動累積影響數', '呆帳費用', '會計原則變動之累積影響數',
           '稀釋每股盈餘',
           '利息收入', '減：利息費用', '收回(提存)各項保險責任準備淨額', '費用', '列計非常損益及會計原則變動累積影響數前損益', '營業支出']
    col1 = ['營業收入', '營業成本', '營業毛利（毛損）', '未實現銷貨（損）益', '已實現銷貨（損）益', '營業毛利（毛損）淨額', '營業費用', '其他收益及費損淨額', '營業利益（損失）',
            '營業外收入及支出',
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
    inc[['年', '季']] = inc[['年', '季']].astype(str)

    def change1(df):
        df0 = df[[x for x in list(df) if df[x].dtype == 'object']]
        df1 = df[[x for x in list(df) if df[x].dtype != 'object']]
        a0 = array(df0)
        a1 = array(df1)
        v = vstack((a1[0], a1[1:] - a1[0:len(df) - 1]))
        h = hstack((a0, v))
        return DataFrame(h, columns=list(df0) + list(df1))

    inc = inc.groupby(['公司代號', '年']).apply(change1).reset_index(drop=True)  # '季' must be string
    print(inc)
    inc['grow_s'] = inc['本期綜合損益總額'].pct_change(1)
    inc['grow_hy'] = inc['本期綜合損益總額'].rolling(window=2).sum().pct_change(2)
    inc[col1] = inc[col1].rolling(window=4).sum()
    inc['grow_y'] = inc['本期綜合損益總額'].pct_change(4)
    inc['grow'] = inc['本期綜合損益總額'].pct_change(1)
    # inc['grow.ma'] = inc['grow'].rolling(window=24).mean()*4
    inc['本期綜合損益總額.wma'] = inc.本期綜合損益總額.ewm(com=19).mean() * 4
    inc['本期綜合損益總額.ma'] = inc['本期綜合損益總額'].rolling(window=12).mean() * 4
    sql = "SELECT * FROM '%s' WHERE 公司代號 LIKE %s"
    bal = read_sql_query(sql % ('ifrs前後-資產負債表-一般業', com), conn)
    bal[['年', '季']] = bal[['年', '季']].astype(str)
    del bal['公司名稱']
    # timeDelta('mops')

    # --- summary ---
    conn = connect('summary.sqlite3')
    sql = "SELECT * FROM '%s' WHERE 公司代號 LIKE %s" % ('會計師查核報告', com)
    ac = read_sql_query(sql, conn).replace('--', 'NaN').rename(
        columns={'公司代號': '證券代號', '公司簡稱': '證券名稱', '核閱或查核日期': '年月日'}).sort_values(['年', '季', '證券代號']).drop(
        ['簽證會計師事務所名稱', '簽證會計師', '簽證會計師.1', '核閱或查核報告類型'], axis=1)
    ac[['年', '季']] = ac[['年', '季']].astype(str)
    del ac['證券名稱']
    # ac['\u3000 核閱或查核日期'] = ac['\u3000 核閱或查核日期'].replace('-', '/', regex=True)
    # ac['\u3000 核閱或查核日期'] = ac['\u3000 核閱或查核日期'].replace('\xa0', '', regex=True)
    # com = "'3056%'"
    sql = "SELECT * FROM '%s' WHERE 公司代號 LIKE %s"
    fin = read_sql_query(sql % ('財務分析', com), conn)
    del fin['公司簡稱']
    report = mymerge(inc, bal)
    report['流動比率'] = report['流動資產'] / report['流動負債']
    report['負債佔資產比率'] = report['負債總額'] / report['資產總額']
    report['權益報酬率'] = report['綜合損益總額歸屬於母公司業主'] * 2 / (report['權益總額'] + report['權益總額'].shift())
    report['profitbility'] = report.綜合損益總額歸屬於母公司業主 / (report.權益總額.shift(4))
    report['investment'] = report.權益總額.pct_change(4)
    report = report.rename(columns={'公司代號': '證券代號'})
    report = mymerge(ac, report)
    remcol = ['Unnamed: 21', '待註銷股本股數（單位：股）', 'Unnamed: 22', ]
    report = report.drop(remcol, axis=1)
    report[['年', '季', '綜合損益總額歸屬於母公司業主', '權益總額', 'profitbility', '權益報酬率']]
    list(report)
    # timeDelta('summary')

    # --- tse ---
    conn = connect('tse.sqlite3')
    sql = "SELECT * FROM '%s' WHERE 證券代號 LIKE %s"
    close = read_sql_query(sql % ('每日收盤行情(全部(不含權證、牛熊證))', com), conn)
    value = read_sql_query(sql % ('個股日本益比、殖利率及股價淨值比', com), conn).drop(['證券名稱'], 1)
    margin = read_sql_query(sql % ('當日融券賣出與借券賣出成交量值(元)', com), conn)
    ins = read_sql_query(sql % ('三大法人買賣超日報(股)', com), conn)
    deal = read_sql_query(sql % ('自營商買賣超彙總表 (股)', com), conn).drop(['證券名稱'], 1).fillna(0)
    fore = read_sql_query(sql % ('外資及陸資買賣超彙總表 (股)', com), conn).drop(['證券名稱'], 1).rename(
        columns={'買進股數': '外資買進股數', '賣出股數': '外資賣出股數', '買賣超股數': '外資買賣超股數', '鉅額交易': '外資鉅額交易'}).fillna('no')
    trust = read_sql_query(sql % ('投信買賣超彙總表 (股)', com), conn).drop(['證券名稱'], 1).rename(
        columns={'買進股數': '投信買進股數', '賣出股數': '投信賣出股數', '買賣超股數': '投信買賣超股數', '鉅額交易': '投信鉅額交易'}).fillna('no')
    index = read_sql_query("SELECT * FROM '%s' WHERE 指數 LIKE %s" % ('大盤統計資訊', "'建材營造類指數'"), conn).rename(
        columns={'收盤指數': '建材營造類指數'}).drop(['指數', '漲跌(+/-)'], axis=1).replace('--', nan).replace('---', nan)
    index1 = read_sql_query("SELECT * FROM '%s'" % ('index'), conn).replace('--', nan).replace('---', nan)
    rindex = read_sql_query("SELECT * FROM '%s' WHERE 指數 LIKE %s" % ('大盤統計資訊', "'建材營造類報酬指數'"), conn).rename(
        columns={'收盤指數': '建材營造類報酬指數', '漲跌點數': 'r漲跌點數', '漲跌百分比(%)': 'r漲跌百分比(%)'}).drop(['指數', '漲跌(+/-)'], axis=1).replace('--', nan).replace('---', nan)
    fore['外資鉅額交易'] = fore['外資鉅額交易'].replace('*', 'yes').replace(' ', 'no')
    trust['投信鉅額交易'] = trust['投信鉅額交易'].replace('*', 'yes').replace(' ', 'no').replace(0, 'no')
    close['本益比'] = close['本益比'].replace('0.00', nan)  # pe is '0.00' when pe < 0
    value['本益比'] = value['本益比'].replace('-', nan)  # pe is '-' when pe < 0
    value['股價淨值比'] = value['股價淨值比'].replace('-', nan)

    sql = "SELECT * FROM '%s' WHERE 股票代號 LIKE %s"
    xdr = read_sql_query(sql % ('除權息計算結果表', com), conn).rename(columns={'股票代號': '證券代號', '股票名稱': '證券名稱'})

    # timeDelta('tse')
    # list(ac)
    m = mymerge(close, xdr)
    m = mymerge(m, value)
    m = mymerge(m, deal)
    m[['自營商(自行買賣)賣出股數', '自營商(自行買賣)買賣超股數', '自營商(自行買賣)買進股數', '自營商(避險)賣出股數', '自營商(避險)買賣超股數', '自營商(避險)買進股數', '自營商賣出股數',
       '自營商買賣超股數', '自營商買進股數']] = m[
        ['自營商(自行買賣)賣出股數', '自營商(自行買賣)買賣超股數', '自營商(自行買賣)買進股數', '自營商(避險)賣出股數', '自營商(避險)買賣超股數', '自營商(避險)買進股數', '自營商賣出股數',
         '自營商買賣超股數', '自營商買進股數']].fillna(0)
    m = mymerge(m, fore)
    m = mymerge(m, trust)
    m[['投信買進股數', '投信賣出股數', '投信買賣超股數']] = m[['投信買進股數', '投信賣出股數', '投信買賣超股數']].fillna(0)
    m[['投信鉅額交易']] = m[['投信鉅額交易']].fillna('no')
    m = mymerge(m, index)
    m = mymerge(m, index1)
    m = mymerge(m, rindex)
    m = mymerge(m, report)
    # list(m)
    # timeDelta('merge')
    m.dtypes

    m.年月日 = to_datetime(m.年月日, format='%Y/%m/%d').apply(
        lambda x: x.date())  # should convert to datetime before sort, or the result is  wrong
    m = m.sort_values(['年月日', '證券代號']).reset_index(drop=True)  # reset_index make the index ascending
    m[list(report)] = m[list(report)].apply(fill)
    m['淨利（淨損）歸屬於母公司業主'] = m['淨利（淨損）歸屬於母公司業主'].astype(float)
    m['綜合損益總額歸屬於母公司業主'] = m['綜合損益總額歸屬於母公司業主'].astype(float)
    m['毛利率'] = m['營業毛利（毛損）'] / m['營業收入']
    m['營業利益率'] = m['營業利益（損失）'] / m['營業收入']
    m['綜合稅後純益率'] = m['綜合損益總額歸屬於母公司業主'] / m['營業收入']
    m['time'] = m.index.tolist()
    col = ['年月日', '證券代號', '年', '季']
    m = m.replace('--', nan)
    m = m[col + [x for x in list(m) if x not in col]]
    col = ['年月日', '證券代號', '證券名稱', '公司名稱', '年', '季', '漲跌(+/-)', '外資鉅額交易', '投信鉅額交易']
    m[[x for x in list(m) if x not in col]] = m[[x for x in list(m) if x not in col]].astype(float)
    col = ['年月日', '證券代號', 'time', '成交股數', '成交筆數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '調整收盤價', '漲跌(+/-)', '漲跌價差',
           '最後揭示買價', '最後揭示買量', '最後揭示賣價',
           '最後揭示賣量', '本益比', '殖利率(%)', '股價淨值比', '自營商(自行買賣)賣出股數', '自營商(自行買賣)買賣超股數', '自營商(自行買賣)買進股數', '自營商(避險)賣出股數',
           '自營商(避險)買賣超股數',
           '自營商(避險)買進股數', '自營商賣出股數', '自營商買賣超股數', '自營商買進股數', '外資鉅額交易', '外資買進股數', '外資賣出股數', '外資買賣超股數', '投信鉅額交易', '投信買進股數',
           '投信賣出股數', '投信買賣超股數', '基本每股盈餘（元）', '每股參考淨值', '流動比率', '負債佔資產比率', '權益報酬率', '毛利率', '營業利益率', '綜合稅後純益率', 'grow_s',
           'grow_hy', 'grow_y', 'grow',
           '本期綜合損益總額.wma', '本期綜合損益總額.ma', 'profitbility', 'investment', '建材營造類指數', '漲跌點數', '漲跌百分比(%)', '建材營造類報酬指數',
           'r漲跌點數', 'r漲跌百分比(%)'] + list(index1)[1:]
    col = [ii for n, ii in enumerate(col) if ii not in col[:n]]
    # m[['profitbility', '權益報酬率']]
    # timeDelta('before dropna')
    list(m)
    m['a'] = m['權值+息值'].replace(NaN, 0)
    m['b'] = m['a'].cumsum()
    m['調整收盤價'] = m.收盤價 + m.b
    m = m.drop(['a', 'b'], axis=1)
    m = m.dropna(axis=1, how='all')


    forweb = m[col]
    # ---- bic ----
    conn = connect('bic.sqlite3')
    c = conn.cursor()
    sql = "SELECT * FROM '%s'"
    bic = read_sql_query(sql % ('景氣指標及燈號-指標構成項目'), conn)
    del bic['年月']
    m['年月日'] = m['年月日'].astype(str)
    m['年'], m['月'] = m['年月日'].str.split('-').str[0].astype(int), m['年月日'].str.split('-').str[1].astype(int)
    # m.dtypes
    m = mymerge(m, bic)
    del m['年'], m['月'], bic['年'], bic['月']
    m.年月日 = to_datetime(m.年月日, format='%Y/%m/%d').apply(lambda x: x.date())

    forweb = m[col + list(bic)]
    forweb['d'] = forweb['調整收盤價'] - forweb['收盤價']
    forweb['調整開盤價'] = forweb['開盤價'] + forweb.d
    forweb['調整收盤價'] = forweb['收盤價'] + forweb.d
    forweb['調整最高價'] = forweb['最高價'] + forweb.d
    forweb['調整最低價'] = forweb['最低價'] + forweb.d
    forweb['earning'] = forweb['收盤價'] / forweb['本益比']
    forweb['lnmo'] = log(forweb['調整收盤價'] / forweb['調整收盤價'].shift(120))

    # return
    def Return(*period):
        for days in period:
            n = 240 / days
            forweb['r' + str(days)] = (forweb['調整收盤價'].shift(-days) / forweb['調整收盤價']) ** n - 1

    Return(5, 10, 20, 40, 60, 120)

    # log return
    def lnReturn(*period):
        for days in period:
            n = 240 / days
            forweb['lnr' + str(days)] = log(forweb['調整收盤價'].shift(-days) / forweb['調整收盤價']) * n

    lnReturn(5, 10, 20, 40, 60, 120)

    # return standard deviation
    def ReturnStd(*period):
        for days in period:
            name = 'r' + str(days)
            forweb[name + 'Std'] = (forweb[name] - forweb[name].mean()) / forweb[name].std()

    ReturnStd(5, 10, 20, 40, 60, 120)

    # rsi
    forweb['ch'] = forweb['調整收盤價'].diff()
    forweb['ch_u'], forweb['ch_d'] = forweb['ch'], forweb['ch']
    forweb.ix[forweb.ch_u < 0, 'ch_u'], forweb.ix[forweb.ch_d > 0, 'ch_d'] = 0, 0
    forweb['ch_d'] = forweb['ch_d'].abs()
    forweb['rsi'] = forweb.ch_u.ewm(alpha=1 / 14).mean() / (forweb.ch_u.ewm(alpha=1 / 14).mean() + forweb.ch_d.ewm(
        alpha=1 / 14).mean()) * 100  # 與r和凱基同,ema的公式與一般的ema不同。公式見http://www.fmlabs.com/reference/default.htm?url=RSI.htm
    forweb = forweb.drop(['ch', 'ch_u', 'ch_d'], axis=1)

    # ma
    def ma(*period):
        for n in period:
            forweb['MA' + str(n)] = forweb['收盤價'].rolling(window=n).mean()

    def ma_adj(*period):
        for n in period:
            forweb['MA' + str(n) + '.adj'] = forweb['調整收盤價'].rolling(window=n).mean()

    ma(5, 10, 20, 60, 120)
    ma_adj(5, 10, 20, 60, 120)

    # DI
    forweb['DI'] = (forweb['最高價'] + forweb['最低價'] + 2 * forweb['收盤價']) / 4
    forweb['DI.adj'] = (forweb['調整最高價'] + forweb['調整最低價'] + 2 * forweb['調整收盤價']) / 4

    # macd
    forweb['max9'] = forweb['最高價'].rolling(window=9).max()
    forweb['min9'] = forweb['最低價'].rolling(window=9).min()
    forweb['EMA12'] = forweb.DI.ewm(alpha=2 / 13).mean()
    forweb['EMA26'] = forweb.DI.ewm(alpha=2 / 27).mean()
    forweb['DIF'] = forweb['EMA12'] - forweb['EMA26']
    forweb['MACD'] = forweb.DIF.ewm(alpha=0.2).mean()
    forweb['MACD1'] = (forweb['EMA12'] - forweb['EMA26']) / forweb['EMA26'] * 100
    forweb['OSC'] = forweb.DIF - forweb.MACD

    # bband
    forweb['std5'] = forweb['DI'].rolling(window=5).std()
    forweb['std10'] = forweb['DI'].rolling(window=11).std()
    forweb['std20'] = forweb['DI'].rolling(window=20).std()
    forweb['mavg'] = forweb['DI'].rolling(window=20).mean()
    forweb['up'] = forweb.mavg + forweb['std20'] * 2
    forweb['dn'] = forweb.mavg - forweb['std20'] * 2
    forweb['bband'] = (forweb['收盤價'] - forweb.mavg) / forweb['std20']

    # bband adj
    forweb['std5.adj'] = forweb['DI.adj'].rolling(window=5).std()
    forweb['std10.adj'] = forweb['DI.adj'].rolling(window=11).std()
    forweb['std20.adj'] = forweb['DI.adj'].rolling(window=20).std()
    forweb['mavg.adj'] = forweb['DI.adj'].rolling(window=20).mean()
    forweb['up.adj'] = forweb['mavg.adj'] + forweb['std20.adj'] * 2
    forweb['dn.adj'] = forweb['mavg.adj'] - forweb['std20.adj'] * 2
    forweb['bband.adj'] = (forweb['調整收盤價'] - forweb['mavg.adj']) / forweb['std20.adj']

    # kd
    forweb['rsv'] = (forweb['收盤價'] - forweb.min9) / (forweb.max9 - forweb.min9)
    forweb['k'] = forweb.rsv.ewm(alpha=1 / 3).mean()
    forweb['d'] = forweb.k.ewm(alpha=1 / 3).mean()

    # others
    forweb['high-low'] = (forweb['最高價'] - forweb['最低價']) / forweb['收盤價']
    forweb['pch'] = (forweb['收盤價'] - forweb['收盤價'].shift()) / forweb['收盤價'].shift()
    forweb['pctB'] = (forweb.DI - forweb.dn) / (forweb.up - forweb.dn)
    forweb['close-up'] = (forweb['收盤價'] - forweb.up) / (forweb.DI.rolling(window=20).std() * 2)
    forweb['close-dn'] = (forweb['收盤價'] - forweb.dn) / (forweb.DI.rolling(window=20).std() * 2)

    forweb['pctB.adj'] = (forweb['DI.adj'] - forweb['dn.adj']) / (forweb['up.adj'] - forweb['dn.adj'])
    forweb['close-up.adj'] = (forweb['調整收盤價'] - forweb['up.adj']) / (forweb['DI.adj'].rolling(window=20).std() * 2)
    forweb['close-dn.adj'] = (forweb['調整收盤價'] - forweb['dn.adj']) / (forweb['DI.adj'].rolling(window=20).std() * 2)

    # timeDelta('before trend')

    forweb['sign'] = sign(forweb['pch'])
    forweb['trend'] = forweb['sign']
    i = forweb[forweb['trend'] == 0].index
    while i.tolist() != []:
        forweb.ix[i, 'trend'] = forweb.ix[i - 1, 'trend'].tolist()
        i = forweb[forweb['trend'] == 0].index
    forweb['trend']
    i = forweb[forweb['trend'] == 1].index
    a = array(i)
    l = (a[1:] - a[:-1]).tolist()
    i = array([i for i, j in enumerate(l) if j != 1]) + 1
    a[i]
    forweb['reverse'] = forweb['trend'] * 2
    forweb.ix[a[i], 'reverse'] = 1

    i = forweb[forweb['trend'] == -1].index
    a = array(i)
    l = (a[1:] - a[:-1]).tolist()
    i = array([i for i, j in enumerate(l) if j != 1]) + 1
    forweb.ix[a[i], 'reverse'] = -1
    forweb.ix[(forweb['reverse'] == 2) | (forweb['reverse'] == -2), 'reverse'] = 0
    i = forweb.ix[~isnull(forweb['pch']), 'pch'].index[0:2]
    if forweb.ix[i[1], 'pch'] > forweb.ix[i[1], 'pch'] and forweb.ix[i[1], 'pch'] != 0:
        forweb.ix[i[1], 'reverse'] = 1
    if forweb.ix[i[1], 'pch'] < forweb.ix[i[0], 'pch'] and forweb.ix[i[1], 'pch'] != 0:
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

    # set_option("display.max_rows", 4000)
    # set_option('display.expand_frame_repr', False)
    # set_option("display.max_columns", 1000)
    # forweb[['年月日','調整收盤價']]
    # forweb.dtypes
    # forweb['MA120'].tolist()
    # forweb

    forweb['newhl'] = forweb['reverse'] * 2
    i = forweb.ix[forweb['reverse'] == 1, 'reverse'].index.tolist()
    a = array(i)
    l = (forweb['調整收盤價'][a] - forweb['調整收盤價'][a].shift()).tolist()
    i = array([i for i, j in enumerate(l) if j > 0])
    forweb.ix[a[i], 'newhl'] = 1
    i = forweb.ix[forweb['reverse'] == -1, 'reverse'].index.tolist()
    a = array(i)
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

    forweb['span'] = abs(forweb['調整收盤價'] - forweb.調整開盤價) / forweb['調整收盤價']
    forweb['span_high-low'] = abs(forweb['調整最高價'] - forweb['調整最低價']) / forweb['調整收盤價']
    forweb['upperShadow'] = (forweb['調整最高價'] - forweb[['調整開盤價', '調整收盤價']].max(axis=1)) / forweb['調整收盤價']
    forweb['lowerShadow'] = (forweb[['調整開盤價', '調整收盤價']].min(axis=1) - forweb['調整最低價']) / forweb['調整收盤價']
    forweb['upperShadow/span'] = forweb['upperShadow'] / (forweb['span'] + 0.1 ** 10 * forweb['調整收盤價'])
    forweb['lowerShadow/span'] = forweb['lowerShadow'] / (forweb['span'] + 0.1 ** 10 * forweb['調整收盤價'])
    # forweb['span/upperShadow'] =forweb['span']/forweb['upperShadow']
    # forweb['span/lowerShadow'] =forweb['span']/forweb['lowerShadow']
    forweb['span/(high-low)'] = forweb['span'] / forweb['span_high-low']
    del forweb['d']
    forweb['high-low_1ag1'] = forweb['high-low'].shift()
    forweb['high-low_lag2'] = forweb['high-low'].shift(2)
    forweb['upperShadow_lag1'] = forweb['upperShadow'].shift()
    forweb['lowerShadow_lag1'] = forweb['lowerShadow'].shift()
    forweb['upperShadow/span_lag1'] = forweb['upperShadow/span'].shift()
    forweb['lowerShadow/span_lag1'] = forweb['lowerShadow/span'].shift()
    # forweb['span/upperShadow_lag1'] = forweb['span/upperShadow'].shift()
    # forweb['span/lowerShadow_lag1'] = forweb['span/lowerShadow'].shift()
    forweb['spandiff'] = forweb.span.diff()
    forweb['spanudiff'] = forweb[['調整開盤價', '調整收盤價']].max(axis=1).diff()
    forweb['spanldiff'] = forweb[['調整開盤價', '調整收盤價']].min(axis=1).diff()
    forweb['span/(high-low)_lag1'] = forweb['span/(high-low)'].shift()

    # timeDelta('before OSCsign')

    forweb['OSCsign'] = sign(forweb.OSC)
    forweb['gr'] = 0

    OSCsign = forweb['OSCsign'].tolist()
    gr = forweb['gr'].tolist()
    g = 0
    for i in range(len(OSCsign) - 1):
        if OSCsign[i] * OSCsign[i + 1] < 0:
            g += 1
            gr[i + 1] = g
        else:
            gr[i + 1] = g

    forweb['OSCsign'], forweb['gr'] = OSCsign, gr
    del g, OSCsign, gr

    def minORmax(forweb):
        if forweb.max() > 0:
            return forweb.max()
        if forweb.min() < 0:
            return forweb.min()
        else:
            return forweb

    grouped = forweb.groupby('gr')
    l = grouped['OSC'].apply(minORmax).tolist()

    d = {}
    for i, v in enumerate(l):
        d[i + 2] = v
    d[0], d[1] = nan, nan
    forweb[['gr1']] = forweb[['gr']].applymap(lambda x: d[x])

    forweb['change'] = 0

    def OSCbreakpoint(forweb):
        forweb = forweb.reset_index(drop=True)  # without this forweb.ix[0,'gr1'] is only defined in first group
        if forweb['OSC'].max() > 0:
            for i in range(len(forweb['gr1'])):
                print(i, len(forweb['gr1']))
                print(i, forweb.ix[i, 'OSC'], forweb.ix[i, 'gr1'])
                if forweb.ix[i, 'OSC'] > forweb.ix[i, 'gr1']:
                    print(i, 'yes')
                    forweb.ix[i, 'change'] = 1
                    break
            return forweb
        if forweb['OSC'].min() < 0:
            for i in range(len(forweb['gr1'])):
                print(i, len(forweb['gr1']))
                print(i, forweb.ix[i, 'OSC'], forweb.ix[i, 'gr1'])
                if forweb.ix[i, 'OSC'] < forweb.ix[i, 'gr1']:
                    print(i, 'yes')
                    forweb.ix[i, 'change'] = -1
                    break
            return forweb
        else:
            return forweb

    forweb = grouped.apply(OSCbreakpoint).reset_index(drop=True)
    del forweb['OSCsign'], forweb['gr'], forweb['gr1']

    # timeDelta('forweb')

    tablename = 'demo'
    # forweb = mymerge(forweb, index).sort_values(['年月日'])
    forweb['漲跌(+/-)'] = forweb['漲跌(+/-)'].replace('＋', 1).replace('－', -1).replace('X', 0).replace(' ', None).astype(
        float)
    forweb['外資鉅額交易'] = forweb['外資鉅額交易'].replace('yes', 1).replace('no', 0).astype(float)
    forweb['投信鉅額交易'] = forweb['投信鉅額交易'].replace('yes', 1).replace('no', 0).astype(float)
    forweb.年月日 = forweb.年月日.astype(str)
    forweb.證券代號 = forweb.證券代號.astype(str)
    forweb = forweb.drop_duplicates(['年月日', '證券代號'])
    # list(forweb)
    conn = connect('mysum.sqlite3')
    c = conn.cursor()

    sql = 'ALTER TABLE `%s` RENAME TO `%s0`' % (tablename, tablename)
    c.execute(sql)
    sql = 'create table `%s` (`%s`, PRIMARY KEY (%s))' % (tablename, '`,`'.join(list(forweb)), '`年月日`, `證券代號`')
    c.execute(sql)
    sql = 'insert into `%s`(`%s`) values(%s)' % (tablename, '`,`'.join(list(forweb)), ','.join('?' * len(list(forweb))))
    c.executemany(sql, forweb.values.tolist())
    conn.commit()
    sql = "drop table `%s0`" % tablename
    c.execute(sql)

    # timeDelta('finish')
    return jsonify({'companyId': companyId})
