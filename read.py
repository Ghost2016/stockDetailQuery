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

arr = ['股票简称', 'hqCode']
timearr = ['几天几板','涨停类型', '涨停原因类别']
def getPropertyStr(stcok):
    t = str(datetime.datetime.now().date()).replace('-', '')
    # t= '20220121'
    inner_str = ""
    for p1 in arr:
        inner_str += stcok[p1] + ' '
    for p2 in timearr:
        inner_str += stcok[p2 + '[' + t +']'] +' '
    return inner_str + '\n'

# 兴业矿业(000426)  8.31 10.07 122.60亿 首板涨停 [放量涨停] 小金属
# question = '数字货币 区块链 大数据  2022年1月13号至今涨停次数大于2 非st 非新股 非科创板 '
question = '数字货币 区块链 大数据  2022年1月13号至今涨停次数大于0 非st 非新股 非科创板 '
if __name__ == '__main__':
    response = crawl_source_data(question)
    if response.status_code == 200:
        html = response.text
        data = json.loads(html)['data']
        data = json.loads(html)['data']
        stockList=list()
        stock_str = ""
        if 'data' in data:
            for index, stock in enumerate(data['data']):
                # stock_str += getPropertyStr(stock)
                stockList.append(stock['股票代码'])
                if index != 0:
                    stock_str += ','
                stock_str+=stock['股票代码']
                # stockList.append(stock['股票简称'])
        print(len(stock_str))
    basic = pro.stock_basic(ts_code=stock_str)
    basic = basic[['ts_code', 'name']]
    df = pro.daily(ts_code=stock_str, start_date='20220104', end_date='20220220')
    print(basic)
    tmp2=df.set_index(['ts_code', 'trade_date'])['pct_chg'].unstack()
    tmp2=tmp2.rename_axis(columns=None).reset_index()
    tmp3=pd.merge(basic,tmp2)
    print(tmp3)

    writer = pd.ExcelWriter('my.xlsx')
    tmp3.to_excel(writer,float_format='%.5f')
    writer.save()