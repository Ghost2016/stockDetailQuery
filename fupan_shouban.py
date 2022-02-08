
from meepwn import crawl_source_data
import json
import datetime


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
question = '当天的首板 非st 涨停板类型 涨停原因类别'
if __name__ == '__main__':
    response = crawl_source_data(question)
    if response.status_code == 200:
        html = response.text
        data = json.loads(html)['data']
        data = json.loads(html)['data']
        stockList=set()
        stock_str = ""
        if 'data' in data:
            for stock in data['data']:
                stock_str += getPropertyStr(stock)
                # stockList.add(stock['股票简称'])
        print(stock_str)
    
    # for i in range(0, 6):
        # getCodeByDriver()

