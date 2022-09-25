# basic
import numpy as np
import pandas as pd
pd.set_option("display.max_rows", 1000)
pd.set_option("display.max_columns", 1000)

#requests
import requests

import os

def financial_statement(company, year, season):

    if year >= 1000:
        year -= 1911
        
    url = 'https://mops.twse.com.tw/mops/web/ajax_t164sb03'
    form_data = {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':'all',
        'queryName': 'co_id',
        'inpuType': 'co_id',
        'isnew': 'false',
        'co_id': company,
        'year': year,
        'season': season,
    }

    response = requests.post(url,form_data)
    response.encoding = 'utf8'
    
    df = pd.read_html(response.text)[1]
    return df

stock = financial_statement(2002, 107, 2)
print(stock)
stock.to_excel('sample.xlsx', sheet_name='sheet1')
#stock = stock.astype(float)
