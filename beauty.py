import requests
from bs4 import BeautifulSoup
from numpy import *
from pandas import *
import re
import datetime


url = 'http://127.0.0.1:5000/testlist/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'}
source_code = requests.get(url, headers)
source_code.encoding = 'utf-8'
plain_text = source_code.text
print(plain_text)
soup = BeautifulSoup(plain_text, 'html.parser')
