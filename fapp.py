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

from bokeh.plotting import figure
from bokeh.embed import components

import datetime
epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

# d = datetime.datetime(2012, 10, 1)
# unix_time_millis(d)
# datetime.datetime(df['年月'])
# df['年月']=to_datetime(df['年月'])
# df['年月']=df['年月'].apply(unix_time_millis)

app = Flask(__name__)

if __name__ == '__main__':
    app.run()

@app.route('/bokeh/', methods=['POST'])
def bokeh():
    # from bokeh import *
    # from bokeh.plotting import figure, output_file, show
    global i
    i += 1
    d['i']=i
    print(i)
    cols = [request.form['plt']]   # list object, empty is allowed
    d['cols1'] = cols
    if '年月日' in cols:
        cols.remove('年月日')
        cols.insert(0, '年月日')
    else:
        cols.insert(0, '年月日')

    for c in cols:
        print(c)

    database = 'mysum'
    conn = connect('{}.sqlite3'.format(database))
    c = conn.cursor()
    table = 'forr'
    # c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(c.fetchall())
    cols=['年月日', '最高價', '最低價']
    df = read_sql_query('select `{}` from `{}`'.format('`,`'.join(cols), table), conn)
    list(df)
    df = df[cols]
    df['年月日'] = to_datetime(df['年月日'])
    df = df.dropna()
    output_file('temp.html')
    numlines = len(df.columns)
    # mypalette = Spectral11[0:numlines]
    df[['最高價', '最低價']] = df[['最高價', '最低價']].astype(int)
    p = figure(width=1000, height=600, x_axis_type="datetime")
    p.multi_line(xs=[df.index.values] * numlines,
                 ys=[df[name].values for name in df],
                 line_width=5)
    show(p)
    df.dtypes

    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # output to static HTML file
    output_file("C:/Users/ak66h_000/Documents/db/lines.html")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(array(df.最低價), array(df.最高價), legend="Temp.", line_width=2)
    # len(df)
    # show the results
    show(p)

    df['年月日'] = df['年月日'].apply(unix_time_millis)
    df = df.dropna(subset=['年月日'])
    df1 = df
    l = array(df1).tolist()
    d['data1'] = [['NaN' if isnull(x) else x for x in i] for i in l]
    d['labels1'] = list(df1)
    d['y1'] = list(df1)[1:]
    list(df1)
    d['ymd1'] = df1.年月日.tolist()
    # l=array(df).tolist()
    # d['q'] =[list(df)]+[['NaN' if isnull(x) else x for x in i] for i in l]
    # return render_template('c3.html', d=d)
    return render_template('testlist.html', d=d)
    # return render_template('dygraph.html', d=d)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# @app.route('/test', methods=['POST'])
# def test():
#     print(request.form.getlist('username'))
#     return '{}'.format(request.form.getlist('username'))  # only text type can get value

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

d = dict()

@app.route('/', methods=['GET', 'POST'])   # should contain '/' in tail
def index():
    global d
    d['mops'], d['mysum'], d['summary'], d['tse'] = mops, mysum, summary, tse
    d['mops1'], d['mysum1'], d['summary1'], d['tse1'] = mops, mysum, summary, tse
    l = request.form.getlist('choice')   #list object, empty is allowed
    d['l'] = l
    for i in l:
        print(i)
    d['tab'] = '#tabs-1'

    return render_template('testlist.html', d=d)  #d is a dictionary, should appear in template


@app.route('/listfield/', methods=['GET', 'POST'])
def listfield():
    global tab
    tab ='#tabs-1'
    d['tab'] = tab
    if request.method == 'POST':
        global df, dbtable
        dbtable = request.form['dbtable']  # string object, empty is not allowed
        conn = connect('{}.sqlite3'.format(dic[dbtable]))
        df = read_sql_query("SELECT * from `{}`".format(dbtable), conn)
        d['fields'] = list(df)
        d['tbdata'] = array(df).tolist()
        return render_template('testlist.html', d=d)
    else:
        return render_template('testlist.html', d=d)

@app.route('/listfieldajax/', methods=['GET', 'POST'])
def listfieldajax():
    global tab, df, dbtable
    tab ='#tabs-1'
    d['tab'] = tab
    dbtable = request.args.get('data')   # list object, empty is allowed
    dbtable = dbtable.replace('=', '').replace('dbtable', '')
    dbtable = [parse.unquote(i) for i in dbtable.split('&')][0]
    conn = connect('{}.sqlite3'.format(dic[dbtable]))
    df = read_sql_query("SELECT * from `{}`".format(dbtable), conn)
    d['fields'] = list(df)
    d['tbdata'] = array(df).tolist()
    return jsonify({'fields': list(df)})



@app.route('/listfield1/', methods=['GET', 'POST'])
def listfield1():
    global tab
    tab ='#tabs-5'
    d['tab'] = tab
    if request.method == 'POST':
        global df, dbtable1
        dbtable1 = request.form['dbtable1']  # string object, empty is not allowed
        conn = connect('{}.sqlite3'.format(dic[dbtable1]))
        df = read_sql_query("SELECT * from `{}`".format(dbtable1), conn)
        d['fields1'] = list(df)
        return render_template('testlist.html', d=d)
    else:
        return render_template('testlist.html', d=d)

@app.route('/listfield1ajax/', methods=['GET', 'POST'])
def listfield1ajax():
    global tab, df, dbtable1
    tab ='#tabs-5'
    d['tab'] = tab
    dbtable1 = request.args.get('data')   # list object, empty is allowed
    dbtable1 = dbtable1.replace('=', '').replace('dbtable1', '')
    dbtable1 = [parse.unquote(i) for i in dbtable1.split('&')][0]
    conn = connect('{}.sqlite3'.format(dic[dbtable1]))
    df = read_sql_query("SELECT * from `{}`".format(dbtable1), conn)
    d['fields1'] = list(df)
    d['tbdata1'] = array(df).tolist()
    return jsonify({'fields1': list(df)})

@app.route('/listfield2/', methods=['GET', 'POST'])
def listfield2():
    global tab, fields2
    tab ='#tabs-7'
    d['tab'] = tab
    if request.method == 'POST':
        global df, dbtable2
        dbtable2 = request.form['dbtable2']  # string object, empty is not allowed
        conn = connect('{}.sqlite3'.format(dic[dbtable2]))
        df = read_sql_query("SELECT * from `{}`".format(dbtable2), conn)
        fields2 = list(df)
        d['fields2'] = fields2
        return render_template('testlist.html', d=d)
    else:
        return render_template('testlist.html', d=d)

@app.route('/listfield2ajax/', methods=['GET', 'POST'])
def listfield2ajax():
    global tab, df, dbtable2, fields2
    tab ='#tabs-7'
    d['tab'] = tab
    dbtable2 = request.args.get('data')   # list object, empty is allowed
    dbtable2 = dbtable2.replace('=', '').replace('dbtable2', '')
    dbtable2 = [parse.unquote(i) for i in dbtable2.split('&')][0]
    conn = connect('{}.sqlite3'.format(dic[dbtable2]))
    df = read_sql_query("SELECT * from `{}`".format(dbtable2), conn)
    fields2 = list(df)
    d['fields2'] = list(df)
    d['tbdata2'] = array(df).tolist()
    return jsonify({'fields2': list(df)})

@app.route('/listfield3ajax/', methods=['GET', 'POST'])
def listfield3ajax():
    global tab, df, dbtable3, fields3
    tab ='#tabs-7'
    d['tab'] = tab
    dbtable3 = request.args.get('data')   # list object, empty is allowed
    dbtable3 = dbtable3.replace('=', '').replace('dbtable3', '')
    dbtable3 = [parse.unquote(i) for i in dbtable3.split('&')][0]
    conn = connect('{}.sqlite3'.format(dic[dbtable3]))
    df = read_sql_query("SELECT * from `{}`".format(dbtable3), conn)
    fields3 = list(df)
    d['fields3'] = list(df)
    d['tbdata3'] = array(df).tolist()
    return jsonify({'fields3': list(df)})

@app.route('/query/', methods=['POST'])
def query():
    global mll, df, df1
    cols = request.form.getlist('cols')   # list object, empty is allowed
    d['cols'] = cols
    if '年月日' in cols:
        cols.remove('年月日')
        cols.insert(0, '年月日')
    else:
        cols.insert(0, '年月日')

    for i in cols:
        print(i)

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

mll, mll1 = [], []
i=0
j=0
@app.route('/mline/', methods=['POST'])
def mline():
    global i, j, mll, mll1, tab, d
    j += 1
    # global df
    # global df1
    cols = request.form.getlist('cols')   # list object, empty is allowed
    # d['cols'] = cols
    if '年月日' in cols:
        cols.remove('年月日')
        cols.insert(0, '年月日')
    else:
        cols.insert(0, '年月日')

    for c in cols:
        print(c)

    # database = 'mysum'
    # conn = connect('{}.sqlite3'.format(database))
    # table = 'forr'
    # c = conn.cursor()
    # # cols=['年月日', '開盤價', '最高價']
    # df = read_sql_query('select `{}` from `{}`'.format('`,`'.join(cols), table), conn)
    # df = df[cols]
    df.to_json(orient='records')
    array(df).tolist()
    conn = connect('{}.sqlite3'.format(dic[dbtable]))
    df = read_sql_query("SELECT `{}` from `{}`".format('`,`'.join(cols), dbtable), conn)
    list(df)
    df.ix[:, 1:] = df.ix[:, 1:].astype(float)
    d['labels'] = list(df)
    d['data'] = array(df).tolist()
    df['年月日'] = to_datetime(df['年月日'])
    df['年月日'] = df['年月日'].apply(unix_time_millis)
    df = df.dropna(subset=['年月日']).dropna(subset=cols[1:])
    df1 = df.copy()
    l = array(df1).tolist()
    data = [['NaN' if isnull(x) else x for x in i] for i in l]
    data = str(data).replace('NaN', "null").replace("'", "")
    # str(['NaN', 2]).replace('NaN',"null").replace("'","")
    labels = list(df1)
    y = list(df1)[1:]
    ymd = df1.年月日.tolist()
    list(df1)
    width = request.form['width']
    height = request.form['height']
    try:
        rangeselector = request.form['rangeselector']
    except:
        rangeselector = 'false'
        pass
    print(rangeselector)
    mll.append([j, cols, data, labels, y, ymd, df1, width, height, rangeselector])
    mll1.append([j, cols, data, labels, y, ymd, df1, width, height, rangeselector])
    d['mll'] = mll1
    tab ='#tabs-2'
    d['tab'] = tab
    d['tableid']='true'
    # l=array(df).tolist()
    # d['q'] =[list(df)]+[['NaN' if isnull(x) else x for x in i] for i in l]
    # return render_template('c3.html', d=d)
    return render_template('testlist.html', d=d)

@app.route('/scale/', methods=['POST'])
def scale():
    global mll, mll1, tab
    for i, l in enumerate(mll1):
        try:
# without try, program will break if request.form['dy'+str(l[0])] is invalid
            if request.form['dy'+str(l[0])] == 'raw':
                mll1[i][6] = mll[i][6].copy()
                print(mll[i][6])
                print(i)
                print(mll1[i][6].ix[:, 1:])
                li = array(mll1[i][6]).tolist()
                mll1[i][2] = [['NaN' if isnull(x) else x for x in a] for a in li].copy()
                print(request.form['dy'+str(l[0])])
                d['mll'] = mll1
                return render_template('testlist.html', d=d)

            if request.form['dy'+str(l[0])] == 'normalize':
                df = mll1[i][6].copy()
                print(df.ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy())
                df.ix[:, 1:] = df.ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy()
                mll1[i][6] = df.copy()
                # mll1[l[0]][6].ix[:, 1:] = mll[l[0]][6].ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy()

                print(mll1[i][6])
                # print(mll1[l[0]][6].ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy())
                print(i)
                print(request.form['dy' + str(l[0])])
                li = array(mll1[i][6]).tolist()
                mll1[i][2] = [['NaN' if isnull(x) else x for x in a] for a in li].copy()
                d['mll'] = mll1
                return render_template('testlist.html', d=d)

            if request.form['dy' + str(l[0])] == 'remove':
                mll1.pop(i)
                mll.pop(i)
                d['mll'] = mll1
                return render_template('testlist.html', d=d)

            tab = '#tabs-2'
            d['tab'] = tab
        except Exception as e:
            print(e)
            pass

@app.route('/mp/', methods=['POST'])
def mp():
    global df, df1, i, L, tab
    L = []
    cols1 = request.form.getlist('cols1')   # list object, empty is allowed
    # cols2 = [x.replace('(%)', '') for x in cols1]
    cols2 = [x.replace('%', '').replace('(', '').replace(')', '').replace(' ', '').replace('/', '').replace('+', '') for x in cols1]
    print(cols2)
    d['cols1'] = cols1
    cols3 = list(zip(cols1, cols2))
    d['cols3'] = cols3
    for col in cols1:
        cols = [col]
        i += 1
        print(i)
        if '年月日' in cols:
            cols.remove('年月日')
            cols.insert(0, '年月日')
        else:
            cols.insert(0, '年月日')
        for c in cols:
            print(c)

        # database = 'mysum'
        # conn = connect('{}.sqlite3'.format(database))
        # c = conn.cursor()
        # table = 'forr'
        # df = read_sql_query('select `{}` from `{}`'.format('`,`'.join(cols), table), conn)
        # df = df[cols]

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
    return render_template('testlist.html', d=d)
    # return render_template('dygraph.html', d=d)

@app.route('/mpajax/', methods=['GET', 'POST'])
def mpajax():
    global df, df1, i, L, tab
    L = []
    cols1 = request.args.get('data')
    print('cols1:', cols1)
    cols1 = cols1.replace('=', '').replace('cols1', '')
    cols1 = [parse.unquote(i) for i in cols1.split('&')]

    # cols2 = [x.replace('(%)', '') for x in cols1]
    cols2 = [x.replace('%', '').replace('(', '').replace(')', '').replace(' ', '').replace('/', '').replace('+', '') for x in cols1]
    print('cols2:',cols2)
    d['cols1'] = cols1
    cols3 = list(zip(cols1, cols2))
    d['cols3'] = cols3
    for col in cols1:
        cols = [col]
        i += 1
        print(i)
        if '年月日' in cols:
            cols.remove('年月日')
            cols.insert(0, '年月日')
        else:
            cols.insert(0, '年月日')
        for c in cols:
            print(c)

        # database = 'mysum'
        # conn = connect('{}.sqlite3'.format(database))
        # c = conn.cursor()
        # table = 'forr'
        # df = read_sql_query('select `{}` from `{}`'.format('`,`'.join(cols), table), conn)
        # df = df[cols]

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

@app.route('/plot/', methods=['POST'])
def plot():
    global i
    i += 1
    d['i'] = i
    print(i)
    cols = [request.form['plt']]   # list object, empty is allowed
    d['cols1'] = cols
    if '年月日' in cols:
        cols.remove('年月日')
        cols.insert(0, '年月日')
    else:
        cols.insert(0, '年月日')

    for c in cols:
        print(c)

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
    d['data1'] = [['NaN' if isnull(x) else x for x in i] for i in l]
    d['labels1'] = list(df1)
    d['y1'] = list(df1)[1:]
    list(df1)
    d['ymd1'] = df1.年月日.tolist()
    # l=array(df).tolist()
    # d['q'] =[list(df)]+[['NaN' if isnull(x) else x for x in i] for i in l]
    # return render_template('c3.html', d=d)
    return render_template('testlist.html', d=d)
    # return render_template('dygraph.html', d=d)

L=[]
# @app.route('/plot1/')
@app.route('/plot1/', methods=['POST'])
def plot1():
    global i, L, tab
    i += 1
    print(i)
    cols = [request.form['plot1']]   # list object, empty is allowed
    cols1 = cols
    if '年月日' in cols:
        cols.remove('年月日')
        cols.insert(0, '年月日')
    else:
        cols.insert(0, '年月日')

    for c in cols:
        print(c)

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
    list(df1)
    ymd1 = df1.年月日.tolist()
    title = cols[1]
    print(title)
    L.append([i, cols1, data1, labels1, y1, ymd1, title])
    # d['L'] = [[1,2,3],[4,5,6]]
    d['L'] = L
    tab = '#tabs-3'
    d['tab'] = tab
    # l=array(df).tolist()
    # d['q'] =[list(df)]+[['NaN' if isnull(x) else x for x in i] for i in l]
    # return render_template('c3.html', d=d)
    return render_template('testlist.html', d=d)

@app.route('/plot1ajax/', methods=['GET','POST'])
def plot1ajax():
    global i, L, tab
    print(i)
    cols = request.args.get('data')
    cols = cols.replace('=', '').replace('plot1', '')
    cols = [parse.unquote(i) for i in cols.split('&')]
    print('plot1:', cols)

    # cols = [request.form['plot1']]   # list object, empty is allowed
    cols1 = cols
    if '年月日' in cols:
        cols.remove('年月日')
        cols.insert(0, '年月日')
    else:
        cols.insert(0, '年月日')

    for c in cols:
        print(c)

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
    list(df1)
    ymd1 = df1.年月日.tolist()
    title = cols[1]
    print(title)
    L.append([i, cols1, data1, labels1, y1, ymd1, title])
    # d['L'] = [[1,2,3],[4,5,6]]
    d['L'] = L
    tab = '#tabs-3'
    d['tab'] = tab
    i += 1
    print(L)
    return jsonify({'L':L})

import datetime
from calendar import monthrange
s_m ={1:3, 2:6, 3:9, 4:12}
def sm(x):
    return(s_m[x])
mllys, mllys1, comp=[], [], []
k=0
@app.route('/ys/', methods=['POST'])
def ys():
    global mllys, d, k, comp
    k += 1
    cols = request.form.getlist('cols2')
    compid = request.form['compid']
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
        df['年月日'] = df['年月日'].apply(lambda x: datetime.datetime(x.year, x.month, monthrange(x.year, x.month)[1]))
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

    return render_template('testlist.html', d=d)

@app.route('/ysajax/', methods=['GET','POST'])
def ysajax():
    global mllys, d, k, comp
    k += 1
    cols = request.args.get('data')
    print('cols:', cols)
    cols = cols.replace('=', '').replace('cols2', '').replace('compid', '')
    cols = [parse.unquote(i) for i in cols.split('&')]
    compid = cols[-1]
    cols = cols[:-1]
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
        df['年月日'] = df['年月日'].apply(lambda x: datetime.datetime(x.year, x.month, monthrange(x.year, x.month)[1]))
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

@app.route('/remove/', methods=['POST'])
def remove():
    global mllys, mllys1, tab, d
    for i, l in enumerate(mllys1):
        try:
# without try, program will break if request.form['dy'+str(l[0])] is invalid
            print(request.form['c3' + str(l[0])])
            if request.form['c3' + str(l[0])] == 'X':
                mllys1.pop(i)
                print(mllys1)
                mllys.pop(i)
                comp.pop(i)
                d['mllys'] = mllys1
                tab = '#tabs-7'
                d['tab'] = tab
                return render_template('testlist.html', d=d)
        except Exception as e:
            print(e)
            pass

@app.route('/removeajax/', methods=['GET','POST'])
def removeajax():
    global mllys, mllys1, tab, d
    print('removeajax')
    name = request.args.get('name')
    name = name.replace('=', '').replace('name', '')
    name = [parse.unquote(i) for i in name.split('&')][0]
    for i, l in enumerate(mllys1):
        print(i, 'c3' + str(l[0]), name, 'c3' + str(l[0]) == name)

    for i, l in enumerate(mllys1):
        if 'c3' + str(l[0]) == name:
            mllys1.pop(i)
            print(mllys1)
            mllys.pop(i)
            comp.pop(i)
            d['mllys'] = mllys1
            tab = '#tabs-7'
            d['tab'] = tab
            return jsonify({'s':'removeajax'})

@app.route('/changeall/', methods=['POST'])
def changeall():
    global mllys, mllys1, d, k, comp
    mllys, mllys1 =[], []
    compid=request.form['compid1']
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
            df['年月日'] = df['年月日'].apply(lambda x: datetime.datetime(x.year, x.month, monthrange(x.year, x.month)[1]))
            df = df.drop(['年', '季', '月', '日'], axis=1)
            df['年月日'] = df['年月日'].astype(str)  # must be string

        df = df[[list(df)[-1]]+list(df)[:-1]]
        df = df.replace('--', 'NaN', regex=True)
        df.ix[:,1:] = df.ix[:,1:].astype(float)
        print(df)
        l = array(df).tolist()
        data = [list(df)]+[['NaN' if isnull(x) else x for x in i] for i in l]
        print(data)
        mllys.append([k, data, compid])
        mllys1.append([k, data, compid])
        d['mllys'] = mllys
    return render_template('testlist.html', d=d)

@app.route('/changeallajax/', methods=['GET','POST'])
def changeallajax():
    global mllys, mllys1, d, k, comp
    mllys, mllys1 =[], []
    compid = request.args.get('data')
    compid = compid.replace('=', '').replace('compid1', '')
    compid = [parse.unquote(i) for i in compid.split('&')][0]
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
            df['年月日'] = df['年月日'].apply(lambda x: datetime.datetime(x.year, x.month, monthrange(x.year, x.month)[1]))
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
@app.route('/c3/')
def c3():
    database = 'bic'
    conn = connect('{}.sqlite3'.format(database))
    c = conn.cursor()
    table = '景氣指標及燈號-綜合指數'
    df = read_sql_query('select * from `{}`'.format(table), conn)
    df['年月']=df['年月'].str[0:]+'-28'
    # df['年月'] = df['年月'].replace('-', '/', regex=True)
    # df['年月'] = to_datetime(df['年月'], format='%Y-%m-%d')
    # df['年月'] = to_datetime(df['年月'])
    # df['年月'] = df['年月'].apply(unix_time_millis)
    d['d1'] = 'data1'
    d['d2'] = 'data2'
    d['data1'] = [30, 200, 100, 400, 150, 250]
    d['data2'] = [50, 20, 10, 40, 15, 25]
    df.ix[:, 3:] = (df.ix[:, 3:] - df.ix[:, 3:].mean()) / df.ix[:, 3:].mean()
    print(df.head(20))
    l=array(df.ix[:, 2:]).tolist()
    d['j'] = [list(df.ix[:, 2:])]+[['NaN' if isnull(x) else x for x in i] for i in l]
    print(d['j'][0:20])
    return render_template('c3.html', d=d)

@app.route('/rep/', methods=['POST'])
def rep():
    global report, tb, d, compid
    report=[]
    report1 = []
    tb=[]
    database = 'summary'
    conn = connect('{}.sqlite3'.format(database))
    c = conn.cursor()
    # compid='5522'
    compid = request.form['compid_report']
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
                    if df3.iloc[i, j]<0:
                        df2.iloc[i, j]='red'
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
            li.append(zip(l[i], lw[i], lc[i]))
        report.append(li)
        tb.append(table)
    report1.append([list(i) for i in report[0]])
    d['report'] = report
    d['tb'] = tb
    d['tab'] = '#tabs-8'
    return render_template('testlist.html', d=d)

@app.route('/repajax/', methods=['GET', 'POST'])
def repajax():
    global report, tb, d, compid
    report=[]
    tb=[]
    database = 'summary'
    conn = connect('{}.sqlite3'.format(database))
    c = conn.cursor()

    compid = request.args.get('data')   # list object, empty is allowed
    compid = compid.replace('=', '').replace('compid_report', '')
    compid = [parse.unquote(i) for i in compid.split('&')][0]
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
                    if df3.iloc[i, j]<0:
                        df2.iloc[i, j]='red'
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
    print('compname:',d['compname'],'compid_report:',d['compid_report'],'report:',report, 'tb:',tb)
    return jsonify({'compname':d['compname'],'compid_report':d['compid_report'],'report':report, 'tb':tb})

@app.route('/rep1/', methods=['POST'])
def rep1():
    global report1, tb1, d, compid1
    report1=[]
    tb1=[]
    # database = 'mops'
    database = 'summary'
    conn = connect('{}.sqlite3'.format(database))
    c = conn.cursor()
    # compid1='5522'
    compid1 = request.form['compid_report1']
    d['compid_report1'] = compid1
    # table = 'ifrs前後-綜合損益表(季)-一般業'
    # table = 'ifrs前後-資產負債表-一般業'
    # for table in ['ifrs前後-綜合損益表(季)', 'ifrs前後-資產負債表-一般業']:
    for table in ['ifrs前後-綜合損益表(季)-一般業', 'ifrs前後-資產負債表-一般業']:
        df = read_sql_query('select * from `{}` where `公司代號`="{}"'.format(table, compid1), conn)
        df['季'] = df['季'].astype(int)
        # if table =='ifrs前後-綜合損益表(季)':
        if table == 'ifrs前後-綜合損益表(季)-一般業':
            df['基本每股盈餘（元）'] = df['基本每股盈餘（元）'].map('{:,.2f}'.format)
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
        d['compname1']=df.ix[len(df)-1, '公司名稱']
        color={1:'rgb(0,255,0)', 2:'rgb(0, 190, 255)', 3:'orange', 4:'rgb(255, 75, 140)'}
        df2=df.copy()
        df3=df.copy()
        df3.ix[:, 4:] = df3.ix[:, 4:].replace('--', 0)
        df3.ix[:, 4:] = df3.ix[:, 4:].astype(float)
        if table == 'ifrs前後-資產負債表-一般業':
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
        for i in color:
            df2.ix[df.季==i, 2:]=color[i]
        smd={1:'3/31', 2:'6/30', 3:'9/30', 4:'12/31'}
        # df['年季'] = df['年'].astype(str) + '年第' + df['季'].astype(str) + '季'
        df['年季'] = df['年'].astype(str)+'/' + df['季'].apply(lambda x: smd[x])
        for i in range(len(df3)):
            for j in range(df3.shape[1]):
                try:
                    if df3.iloc[i, j]<0:
                        df2.iloc[i, j]='red'
                except:
                    pass
        df2['季'] = df2['季'].astype(int)
        df2['年季'] = df2['年'].astype(str) + df2['季'].apply(lambda x:smd[x])
        df = df.drop(['年', '季', '公司代號', '公司名稱'], axis=1)
        df = df[[list(df)[-1]] + list(df)[:-1]]
        df2 = df2.drop(['年', '季', '公司代號', '公司名稱'], axis=1)
        df2 = df2[[list(df2)[-1]] + list(df2)[:-1]]
        # l = vstack((array([list(df)]), array(df))).transpose().tolist()
        df.dtypes
        df.ix[:, 1:] = df.ix[:, 1:].replace('--', NaN)
        df.ix[:, 1:] = df.ix[:, 1:].astype(float)
        m = df.ix[:, 1:].max().max()
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

        df4 = df.copy()
        list(df4)
        df.dtypes
        if table == 'ifrs前後-綜合損益表(季)-一般業':
            for i in list(df4)[2:]:
                df4[i] = df4[i] / df4.營業收入 * 100
            df4.營業收入 = df4.營業收入 / df4.營業收入 * 100
        if table == 'ifrs前後-資產負債表-一般業':
            a = list(df4)[1:]
            a.remove('資產總額')
            for i in a:
                df4[i] = df4[i] / df4.資產總額 * 100
            df4.資產總額 = df4.資產總額 / df4.資產總額 * 100

        df4.ix[:, 1:] = df4.ix[:, 1:].applymap('{:,.0f}'.format)
        df = df.fillna('')
        df4 = df4.replace('nan', '')
        # l = vstack((array([list(df)]), array(df))).transpose().tolist()
        # lp = vstack((array([list(df4)]), array(df4))).transpose().tolist()
        # lw = vstack((array([list(df1)]), array(df1))).transpose().tolist()
        # lc = vstack((array([list(df2)]), array(df2))).transpose().tolist()

        if table == 'ifrs前後-綜合損益表(季)-一般業':
            lspan=['<span class=inc{}>sparklines</span>'.format(i) for i, j in enumerate(list(df))]

            l = vstack((array([list(df)]), array(df), array([lspan]))).transpose().tolist()
            lspan = [None for i in list(df)]
            lp = vstack((array([list(df4)]), array(df4), array([lspan]))).transpose().tolist()
            lw = vstack((array([list(df1)]), array(df1), array([lspan]))).transpose().tolist()
            lc = vstack((array([list(df2)]), array(df2), array([lspan]))).transpose().tolist()

            lspan=[]
            for x in l:
                # print(x)
                lspan.append(['null' if i=='' else i for i in x])
            l[3][2]==''
            lspan[1]
            lspan[1][1:-1]
            for i in lspan[1:]:
                print(i[1:-1])
            d['lspan'] = lspan
        if table == 'ifrs前後-資產負債表-一般業':
            lspan = ['<span class=bal{}>sparklines</span>'.format(i) for i, j in enumerate(list(df))]

            l = vstack((array([list(df)]), array(df), array([lspan]))).transpose().tolist()
            lspan = [None for i in list(df)]
            lp = vstack((array([list(df4)]), array(df4), array([lspan]))).transpose().tolist()
            lw = vstack((array([list(df1)]), array(df1), array([lspan]))).transpose().tolist()
            lc = vstack((array([list(df2)]), array(df2), array([lspan]))).transpose().tolist()

            lspan = []
            for x in l:
                # print(x)
                lspan.append(['null' if i == '' else i for i in x])
            l[3][2] == ''
            lspan[1]
            lspan[1][1:-1]
            for i in lspan[1:]:
                print(i[1:-1])
            d['lspan1'] = lspan

        shape(lp)
        for i in lw:
            i[0]=0.0
        for i in lc:
            i[0]='white'
        for i in lp:
            i[0]=''
        li = []
        for i in range(len(l)):
            li.append(zip(l[i], lw[i], lc[i], lp[i]))
        # report1.append(li)
        report1.append([list(x) for x in li])
        tb1.append(table)

    li1 = []
    for i in report1:
        li11 = []
        for j in i:
            li12 = []
            for k in j:
                k = list(k)
                print("k:",k)
                li12.append(k)
            li11.append(li12)
        li1.append(li11)
    report2 = li1.copy()
    print(report1)
    d['report1'] = report2
    d['tb1'] = tb1
    d['tab'] = '#tabs-9'
    return render_template('testlist.html', d=d)

@app.route('/rep1ajax/', methods=['GET', 'POST'])
def rep1ajax():
    global report1, tb1, d, compid1
    report1=[]
    tb1=[]
    # database = 'mops'
    database = 'summary'
    conn = connect('{}.sqlite3'.format(database))
    c = conn.cursor()
    # compid1='5522'
    compid1 = request.args.get('data')   # list object, empty is allowed
    compid1 = compid1.replace('=', '').replace('compid_report1', '')
    compid1 = [parse.unquote(i) for i in compid1.split('&')][0]
    # compid1 = request.form['compid_report1']
    d['compid_report1'] = compid1
    print('compid_report1:',compid1)
    # table = 'ifrs前後-綜合損益表(季)-一般業'
    # table = 'ifrs前後-資產負債表-一般業'
    # for table in ['ifrs前後-綜合損益表(季)', 'ifrs前後-資產負債表-一般業']:
    for table in ['ifrs前後-綜合損益表(季)-一般業', 'ifrs前後-資產負債表-一般業']:
        df = read_sql_query('select * from `{}` where `公司代號`="{}"'.format(table, compid1), conn)
        df['季'] = df['季'].astype(int)
        # if table =='ifrs前後-綜合損益表(季)':
        if table == 'ifrs前後-綜合損益表(季)-一般業':
            df['基本每股盈餘（元）'] = df['基本每股盈餘（元）'].map('{:,.2f}'.format)
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
        d['compname1']=df.ix[len(df)-1, '公司名稱']
        color={1:'rgb(0,255,0)', 2:'rgb(0, 190, 255)', 3:'orange', 4:'rgb(255, 75, 140)'}
        df2=df.copy()
        df3=df.copy()
        df3.ix[:, 4:] = df3.ix[:, 4:].replace('--', 0)
        df3.ix[:, 4:] = df3.ix[:, 4:].astype(float)
        if table == 'ifrs前後-資產負債表-一般業':
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
        for i in color:
            df2.ix[df.季==i, 2:]=color[i]
        smd={1:'3/31', 2:'6/30', 3:'9/30', 4:'12/31'}
        # df['年季'] = df['年'].astype(str) + '年第' + df['季'].astype(str) + '季'
        df['年季'] = df['年'].astype(str)+'/' + df['季'].apply(lambda x: smd[x])
        for i in range(len(df3)):
            for j in range(df3.shape[1]):
                try:
                    if df3.iloc[i, j]<0:
                        df2.iloc[i, j]='red'
                except:
                    pass
        df2['季'] = df2['季'].astype(int)
        df2['年季'] = df2['年'].astype(str) + df2['季'].apply(lambda x:smd[x])
        df = df.drop(['年', '季', '公司代號', '公司名稱'], axis=1)
        df = df[[list(df)[-1]] + list(df)[:-1]]
        df2 = df2.drop(['年', '季', '公司代號', '公司名稱'], axis=1)
        df2 = df2[[list(df2)[-1]] + list(df2)[:-1]]
        # l = vstack((array([list(df)]), array(df))).transpose().tolist()
        df.dtypes
        df.ix[:, 1:] = df.ix[:, 1:].replace('--', NaN)
        df.ix[:, 1:] = df.ix[:, 1:].astype(float)
        m = df.ix[:, 1:].max().max()
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

        df4 = df.copy()
        list(df4)
        df.dtypes
        if table == 'ifrs前後-綜合損益表(季)-一般業':
            for i in list(df4)[2:]:
                df4[i] = df4[i] / df4.營業收入 * 100
            df4.營業收入 = df4.營業收入 / df4.營業收入 * 100
        if table == 'ifrs前後-資產負債表-一般業':
            a = list(df4)[1:]
            a.remove('資產總額')
            for i in a:
                df4[i] = df4[i] / df4.資產總額 * 100
            df4.資產總額 = df4.資產總額 / df4.資產總額 * 100

        df4.ix[:, 1:] = df4.ix[:, 1:].applymap('{:,.0f}'.format)
        df = df.fillna('')
        df4 = df4.replace('nan', '')
        # l = vstack((array([list(df)]), array(df))).transpose().tolist()
        # lp = vstack((array([list(df4)]), array(df4))).transpose().tolist()
        # lw = vstack((array([list(df1)]), array(df1))).transpose().tolist()
        # lc = vstack((array([list(df2)]), array(df2))).transpose().tolist()

        if table == 'ifrs前後-綜合損益表(季)-一般業':
            lspan=['<span class=inc{}>sparklines</span>'.format(i) for i, j in enumerate(list(df))]

            l = vstack((array([list(df)]), array(df), array([lspan]))).transpose().tolist()
            lspan = [None for i in list(df)]
            lp = vstack((array([list(df4)]), array(df4), array([lspan]))).transpose().tolist()
            lw = vstack((array([list(df1)]), array(df1), array([lspan]))).transpose().tolist()
            lc = vstack((array([list(df2)]), array(df2), array([lspan]))).transpose().tolist()

            lspan=[]
            for x in l:
                # print(x)
                lspan.append(['null' if i=='' else i for i in x])
            l[3][2]==''
            lspan[1]
            lspan[1][1:-1]
            for i in lspan[1:]:
                print(i[1:-1])
            d['lspan'] = lspan
        if table == 'ifrs前後-資產負債表-一般業':
            lspan = ['<span class=bal{}>sparklines</span>'.format(i) for i, j in enumerate(list(df))]

            l = vstack((array([list(df)]), array(df), array([lspan]))).transpose().tolist()
            lspan = [None for i in list(df)]
            lp = vstack((array([list(df4)]), array(df4), array([lspan]))).transpose().tolist()
            lw = vstack((array([list(df1)]), array(df1), array([lspan]))).transpose().tolist()
            lc = vstack((array([list(df2)]), array(df2), array([lspan]))).transpose().tolist()

            lspan = []
            for x in l:
                # print(x)
                lspan.append(['null' if i == '' else i for i in x])
            l[3][2] == ''
            lspan[1]
            lspan[1][1:-1]
            for i in lspan[1:]:
                print(i[1:-1])
            d['lspan1'] = lspan

        shape(lp)
        for i in lw:
            i[0]=0.0
        for i in lc:
            i[0]='white'
        for i in lp:
            i[0]=''
        li = []
        for i in range(len(l)):
            li.append(zip(l[i], lw[i], lc[i], lp[i]))
        # report1.append(li)
        report1.append([list(x) for x in li])
        tb1.append(table)

    li1 = []
    for i in report1:
        li11 = []
        for j in i:
            li12 = []
            for k in j:
                k = list(k)
                k =['NaN' if isnull(m) else m for m in k]  # nan/None are undefined in javascript
                print("k:", k)
                li12.append(k)
            li11.append(li12)
        li1.append(li11)
    report2 = li1.copy()
    # print(report2)
    d['report1'] = report2
    d['tb1'] = tb1
    d['tab'] = '#tabs-9'
    # l=[1, NaN, 2]
    # l=array([1,nan,2]).tolist()
    # nan in l
    # isnull(l[1])
    # None in l
    # [['NaN' for i in report2]]
    # isnull(None)
    # for i in report2:
    #     for j in i:
    #         for k in j:
    #             for l in k:
    #                 if isnull(l):
    #                     l='NaN'

    # ['NaN' for k in [j for j in [i for i in report2]]]
    # ['']
    # isnull('')
    # return render_template('testlist.html', d=d)
    # print('lspan:', lspan, 'lspan1:', lspan, 'compid_report1:', d['compid_report1'], 'compname1:', d['compname1'], 'tb1:', tb1, 'tab:', '#tabs-9')
    # return jsonify({'lspan': lspan, 'lspan1': lspan, 'compid_report1': d['compid_report1'], 'compname1': d['compname1'], 'report1': report2, 'tb1': tb1, 'tab': '#tabs-9'})
    return jsonify({'lspan': d['lspan'], 'lspan1': d['lspan1'], 'compid_report1': d['compid_report1'], 'compname1': d['compname1'], 'report1': report2, 'tb1': tb1, 'tab': '#tabs-9'})
# report1=[]
# li=[]
# for i in report1[0][0]:
#     # print(i)
#     li.append(i)
# for i in report1:
#     for j in i:
#         li.append(j)
# li
# [list(x) for x in report1[0]]

# for i,j,k in report1[0][0][0]:
#     print(i,j,k)
#
# for i in report2[0][0][0][0]:
#     print(i)

#
# [w for w in [y for y in [x for x in report1]]]
# m=map(list, report1)
# list(m)
#
# for i in report1[0][0][0]:
#     list(i)
# list(report1[0][0][0])
# report1[0][0][1:]

# for item in report2[0][1:]:
#     print(item[0][0])


@app.route('/datatable/', methods=['GET', 'POST'])
def datatable():

    return render_template('datatable.html', d=d)

@app.route('/react/', methods=['GET', 'POST'])
def react():

    return render_template('react.html', d=d)

@app.route('/ajax/')
def ajax():
    a = request.args.get('aa', 0, type=int)
    b = request.args.get('bb', 0, type=int)
    c = request.args.get('aa')
    d = request.args.get('bb')
    print(a, b, c, d)
    return jsonify({'result1':a,'result2':b})

@app.route('/ajax1/', methods=['GET', 'POST'])
def ajax1():
    try:
        c = request.form['aa']
        print(c)
        print(c.split('&'))
        print(1)
    except Exception as e:
        print(e)
        pass
    try:
        a = request.args.getlist('aa')
        print(a)
        print(2)
    except Exception as e:
        print(e)
        pass
    try:
        b = request.args.get('aa')
        print(b)
        print(3)
        b = b.replace('=', '').replace('c1', '').split('&')
        print(b)
    except Exception as e:
        print(e)
        pass
    return jsonify({'result1':b})

@app.route('/mlinehighchart/', methods=['GET', 'POST'])
def mlinehighchart():
    global i, j, mll, mll1, tab, d
    print('j:',j)
    # global df
    # global df1
    cols = request.args.get('data')   # list object, empty is allowed
    cols = cols.replace('=', '').replace('cols', '').replace('width', '').replace('height', '').replace('rangeselector', '')
    cols = [parse.unquote(i) for i in cols.split('&')]
    width = cols[-3]
    height = cols[-2]
    rangeselector = cols[-1]
    print(width, height, rangeselector)
    cols = cols[:-3]
    # cols = request.form['cols']
    # cols = request.args.get('cols', 0)
    # d['cols'] = cols
    if '年月日' in cols:
        cols.remove('年月日')
        cols.insert(0, '年月日')
    else:
        cols.insert(0, '年月日')

    for c in cols:
        print(c)

    # database = 'mysum'
    # conn = connect('{}.sqlite3'.format(database))
    # table = 'forr'
    # c = conn.cursor()
    # # cols=['年月日', '開盤價', '最高價']
    # df = read_sql_query('select `{}` from `{}`'.format('`,`'.join(cols), table), conn)
    # df = df[cols]
    conn = connect('{}.sqlite3'.format(dic[dbtable]))
    df = read_sql_query("SELECT `{}` from `{}`".format('`,`'.join(cols), dbtable), conn)
    list(df)
    df.ix[:, 1:] = df.ix[:, 1:].astype(float)
    d['labels'] = list(df)
    d['data'] = array(df).tolist()
    df['年月日'] = to_datetime(df['年月日'])
    df['年月日'] = df['年月日'].apply(unix_time_millis)
    df = df.dropna(subset=['年月日']).dropna(subset=cols[1:])
    df1 = df.copy()
    labels = list(df1)
    l = array(df1).tolist()
    data = [['NaN' if isnull(x) else x for x in i] for i in l]
    data = [labels]+data
    # data = str(data).replace('NaN', "null").replace("'", "")
    # str(['NaN', 2]).replace('NaN',"null").replace("'","")
    y = list(df1)[1:]
    ymd = df1.年月日.tolist()
    print(df1)

    try:
        rangeselector = request.form['rangeselector']
        # rangeselector = request.args.get('rangeselector', 0)
        print(rangeselector)
    except:
        rangeselector = 'false'
        pass
    print(rangeselector)
    mll.append(['dy'+str(j), cols, data, labels, y, ymd, df1, width, height, rangeselector])
    mll1.append(['dy'+str(j), cols, data, labels, y, ymd, df1, width, height, rangeselector])
    d['mll'] = mll1
    tab ='#tabs-13'
    d['tab'] = tab
    d['tableid'] = 'true'
    # l=array(df).tolist()
    # d['q'] =[list(df)]+[['NaN' if isnull(x) else x for x in i] for i in l]
    # return render_template('c3.html', d=d)
    # return render_template('testlist.html', d=d)
    j += 1
    return jsonify({'j':'dy'+str(j), 'data': data, 'labels': labels})

@app.route('/scalehighchart/', methods=['GET', 'POST'])
def scalehighchart():
    global mll, mll1, tab
    print('/scalehighchart........................................../')
    for i, l in enumerate(mll1):
        if l[0]==request.args.get('name'):
            print("name........:",l[0])
            if request.args.get('value') == 'raw':
                mll1[i][6] = mll[i][6].copy()
                # print(mll[i][6])
                # print(i)
                # print(mll1[i][6].ix[:, 1:])
                li = array(mll1[i][6]).tolist()
                mll1[i][2] = [mll1[i][3]] + [['NaN' if isnull(x) else x for x in a] for a in li].copy()
                # print(request.form[l[0]])
                d['mll'] = mll1
                tab = '#tabs-13'
                d['tab'] = tab
                print("raw........")
                return jsonify({'j': request.args.get('name'), 'data': mll1[i][2], 'labels': mll1[i][3]})

            if request.args.get('value') == 'normalize':
                df = mll1[i][6].copy()
                # print(df.ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy())
                df.ix[:, 1:] = df.ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy()
                mll1[i][6] = df.copy()
                # mll1[l[0]][6].ix[:, 1:] = mll[l[0]][6].ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy()

                # print(mll1[i][6])
                # # print(mll1[l[0]][6].ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy())
                # print(i)
                # print(request.form[l[0]])
                li = array(mll1[i][6]).tolist()
                mll1[i][2] = [mll1[i][3]] + [['NaN' if isnull(x) else x for x in a] for a in li].copy()
                d['mll'] = mll1
                tab = '#tabs-13'
                d['tab'] = tab
                print( mll1[i][2][:100])
                print("normalize........")
                return jsonify({'j': request.args.get('name'), 'data': mll1[i][2], 'labels': mll1[i][3]})

            if request.args.get('value') == 'remove':
                mll1.pop(i)
                mll.pop(i)
                d['mll'] = mll1
                tab = '#tabs-13'
                d['tab'] = tab
                print("remove........")
                return ('', 204)

@app.route('/scaleajax/', methods=['GET', 'POST'])
def scaleajax():
    global mll, mll1, tab
    print('/scaleajax........................................../')

    for i, l in enumerate(mll1):
        print(i, l[0], request.args.get('name'))

    for i, l in enumerate(mll1):
        if l[0]==request.args.get('name'):
            print("name........:",l[0])
            if request.args.get('value') == 'raw':
                mll1[i][6] = mll[i][6].copy()
                # print(mll[i][6])
                # print(i)
                # print(mll1[i][6].ix[:, 1:])
                li = array(mll1[i][6]).tolist()
                mll1[i][2] = [['NaN' if isnull(x) else x for x in a] for a in li].copy()
                # print(request.form[l[0]])
                d['mll'] = mll1
                tab = '#tabs-2'
                d['tab'] = tab
                print("raw........")
                return jsonify({'i': i, 'j': request.args.get('name'), 'data': mll1[i][2], 'labels': mll1[i][3], 'rangeselector': mll1[i][9]})

            if request.args.get('value') == 'normalize':
                df = mll1[i][6].copy()
                # print(df.ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy())
                df.ix[:, 1:] = df.ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy()
                mll1[i][6] = df.copy()
                # mll1[l[0]][6].ix[:, 1:] = mll[l[0]][6].ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy()

                # print(mll1[i][6])
                # # print(mll1[l[0]][6].ix[:, 1:].apply(lambda x: (x - x.mean()) / x.std()).copy())
                # print(i)
                # print(request.form[l[0]])
                li = array(mll1[i][6]).tolist()
                mll1[i][2] = [['NaN' if isnull(x) else x for x in a] for a in li].copy()
                d['mll'] = mll1
                tab = '#tabs-2'
                d['tab'] = tab
                print( mll1[i][2][:100])
                print("normalize........")
                return jsonify({'i': i, 'j': request.args.get('name'), 'data': mll1[i][2], 'labels': mll1[i][3], 'rangeselector': mll1[i][9]})

            if request.args.get('value') == 'remove':
                mll1.pop(i)
                mll.pop(i)
                d['mll'] = mll1
                tab = '#tabs-2'
                d['tab'] = tab
                print("remove........")
                return jsonify({'i': i})

@app.route('/dygraphsajax/', methods=['GET', 'POST'])
def dygraphsajax():
    return ('', 204)


@app.route('/mlineajax/', methods=['GET', 'POST'])
def mlineajax():
    global i, j, mll, mll1, tab, d
    cols = request.args.get('data')   # list object, empty is allowed
    if 'rangeselector' in cols:
        print('yes')
        cols = cols.replace('=', '').replace('cols', '').replace('width', '').replace('height', '').replace('rangeselector', '')
        cols = [parse.unquote(i) for i in cols.split('&')]
        width = cols[-3]
        height = cols[-2]
        rangeselector = cols[-1]
        cols = cols[:-3]
    else:
        print('no')
        cols = cols.replace('=', '').replace('cols', '').replace('width', '').replace('height', '')
        cols = [parse.unquote(i) for i in cols.split('&')]
        width = cols[-2]
        height = cols[-1]
        rangeselector = None
        cols = cols[:-2]
    print('width:', width, 'height:', height, 'rangeselector:', rangeselector)

    if '年月日' in cols:
        cols.remove('年月日')
        cols.insert(0, '年月日')
    else:
        cols.insert(0, '年月日')

    for c in cols:
        print(c)

    # database = 'mysum'
    # conn = connect('{}.sqlite3'.format(database))
    # table = 'forr'
    # c = conn.cursor()
    # # cols=['年月日', '開盤價', '最高價']
    # df = read_sql_query('select `{}` from `{}`'.format('`,`'.join(cols), table), conn)
    # df = df[cols]

    conn = connect('{}.sqlite3'.format(dic[dbtable]))
    df = read_sql_query("SELECT `{}` from `{}`".format('`,`'.join(cols), dbtable), conn)
    list(df)
    df.ix[:, 1:] = df.ix[:, 1:].astype(float)
    d['labels'] = list(df)
    d['data'] = array(df).tolist()
    df['年月日'] = to_datetime(df['年月日'])
    df['年月日'] = df['年月日'].apply(unix_time_millis)
    df = df.dropna(subset=['年月日']).dropna(subset=cols[1:])
    df1 = df.copy()
    l = array(df1).tolist()
    data = [['NaN' if isnull(x) else x for x in i] for i in l]   # don't transfer data to string
    # data = str(data).replace('NaN', "null").replace("'", "")
    # str(['NaN', 2]).replace('NaN',"null").replace("'","")
    labels = list(df1)
    y = list(df1)[1:]
    ymd = df1.年月日.tolist()
    list(df1)

    print('rangeselector:', rangeselector)
    mll.append(['dy'+str(j), cols, data, labels, y, ymd, df1, width, height, rangeselector])
    mll1.append(['dy'+str(j), cols, data, labels, y, ymd, df1, width, height, rangeselector])
    d['mll'] = mll1
    tab ='#tabs-2'
    d['tab'] = tab
    d['tableid']='true'
    j += 1
    # l=array(df).tolist()
    # d['q'] =[list(df)]+[['NaN' if isnull(x) else x for x in i] for i in l]
    # return render_template('c3.html', d=d)
    return jsonify({'j': 'dy' + str(j), 'data': data, 'labels': labels, 'rangeselector':rangeselector})
    # return render_template('dygraph.html', d=d)

