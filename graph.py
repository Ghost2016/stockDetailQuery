# 数字货币 区块链 大数据  2022年1月13号至今涨停次数大于0 非st 非新股 非科创板

from meepwn import crawl_source_data
import json
import datetime
import numpy as np
import pandas as pd

import tushare as ts
token='cee7373f5534cd6ac10783e468db6710767cf637007930de27ce3a08'
ts.set_token(token)
pro = ts.pro_api()

arr = ['股票简称']
timearr = [ '涨停原因类别']
def getPropertyStr(stcok):
    t = str(datetime.datetime.now().date()).replace('-', '')
    # t= '20220121'
    inner_str = ""
    for p2 in timearr:
        inner_str += stcok[p2 + '[' + t +']'] +'\n'
    # for p1 in arr:
    #     inner_str += stcok[p1] + '\t'

    return inner_str + '\n'

# 兴业矿业(000426)  8.31 10.07 122.60亿 首板涨停 [放量涨停] 小金属
# question = '数字货币 区块链 大数据  2022年1月13号至今涨停次数大于2 非st 非新股 非科创板 '
t = '20220216'

question = '%s涨停 2天2板和3天2板 非st 非新股 非创业板块 开盘涨幅 ' % t
if __name__ == '__main__':
    response = crawl_source_data(question)
    if response.status_code == 200:
        html = response.text
        data = json.loads(html)['data']
        data = json.loads(html)['data']
        stockList=list()
        stock_str = ""
        # t = str(datetime.datetime.now().date()).replace('-', '')
        
        if 'data' in data:
            for index, stock in enumerate(data['data']):
                stock_str+=stock['股票简称']+'\n'
            for index, stock in enumerate(data['data']):
                stock_str+=stock['涨停原因类别[%s]' % t]+ '\n'
            for index, stock in enumerate(data['data']):
                stock_str+=stock['几天几板[%s]' % t]+ '\n'
                
        print(stock_str)
    

