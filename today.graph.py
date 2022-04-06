# 数字货币 区块链 大数据  2022年1月13号至今涨停次数大于0 非st 非新股 非科创板

from meepwn import crawl_source_data
import json
import datetime
import numpy as np
import pandas as pd

import tushare as ts
import os

from tushareUtils import getCurrentTradeDay

token='cee7373f5534cd6ac10783e468db6710767cf637007930de27ce3a08'
ts.set_token(token)
pro = ts.pro_api()
currentDay = getCurrentTradeDay()

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

# 打印基础数据
def printBaseData(data, t):
    stock_str_name=''
    stock_str_up_time=''
    stock_str_up_reaseon=''
    if 'data' in data:
        data['data'].sort(key=lambda k: (k.get('hqCode')))
        for index, stock in enumerate(data['data']):
            stock_str_name+=stock['股票简称']+'\n'
            stock_str_up_reaseon+=stock.get('涨停原因类别[%s]' % t, stock.get('涨停原因类别[%s]' % currentDay, '未知类型'))+ '\n'
            stock_str_up_time+=stock.get('几天几板[%s]' % t, '其他连扳类型')+ '\n'
    print(stock_str_name)
    print(stock_str_up_reaseon)
    print(stock_str_up_time)

start_date=datetime.datetime.now().strftime("%Y%m%d")
end_date=datetime.datetime.now().strftime("%Y%m%d")
before_start_date=(datetime.datetime.strptime(start_date, '%Y%m%d')+datetime.timedelta(days=-5)).strftime("%Y%m%d")

# 兴业矿业(000426)  8.31 10.07 122.60亿 首板涨停 [放量涨停] 小金属
question = '%s涨停 2天2板和3天2板或者连续涨停天数等于2 %s非st %s非新股 %s非创业板块 最终涨停时间先后排序' % (start_date,start_date,start_date,start_date)
# question = '%s首板 创业板块 %s涨停原因类别 %s非st' % (start_date, start_date)
print(question)



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
                stockList.append(stock['股票代码'])
                if index != 0:
                    stock_str += ','
                stock_str+=stock['股票代码']
                # stockList.append(stock['股票简称'])
        print()
        print(len(stock_str))
    basic = pro.stock_basic(ts_code=stock_str)
    basic = basic[['ts_code', 'name']]
    df = pro.daily(ts_code=stock_str, start_date=before_start_date, end_date=end_date)
    # print(basic)
    tmp2=df.set_index(['ts_code', 'trade_date'])['pct_chg'].unstack()
    tmp2=tmp2.rename_axis(columns=None).reset_index()
    tmp3=pd.merge(basic,tmp2)
    # print(tmp3)
    printBaseData(data, start_date)

    writer = pd.ExcelWriter('my.xlsx')
    tmp3.to_excel(writer,float_format='%.5f')
    writer.save()
    os.system('open my.xlsx')


