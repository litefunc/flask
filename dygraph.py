from sqlite3 import *
# conn = connect('C:\\Users\\ak66h_000\\Documents\\db\\bic.sqlite3')
conn = connect('D:/summary.sqlite3')
c = conn.cursor()
from pandas import *
from numpy import *
table = '綜合損益表-一般業'
df = read_sql_query('select * from `{}`'.format(table), conn)
array(df).tolist()
str(array(df).tolist())
df.tolist()
