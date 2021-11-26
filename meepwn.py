
#!/usr/bin/env python
#coding: utf-8

from copy import deepcopy
import requests
import re
import json

from utils.user_agent import getUserAgent
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
           'Referer': "http://www.iwencai.com/unifiedwap/unified-wap/result/get-stock-pick",
           "Host": "www.iwencai.com",
           "X-Requested-With":"XMLHttpRequest",
}


Question_url = "http://www.iwencai.com/unifiedwap/unified-wap/result/get-stock-pick"


def crawl_data_from_wencai(question="上一交易日没有涨停 今天涨停后开板 非st"):
    """通过问财接口抓取数据
    
    Arguments:
        trade_date {[type]} -- [description]
        fields {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    payload = {
        # 查询问句
        # "question": "{},{},上市日期<={}".format(trade_date, ",".join(fields), trade_date),
        "question": question,
        # 返回查询记录总数 
        "perpage": 5000,
        "query_type": "stock"
    }
    headers_wc = deepcopy(headers)
    headers_wc['User-Agent'] = getUserAgent()

    try:
        response = requests.get(Question_url, params=payload, headers=headers_wc)
        if response.status_code == 200:
            html = response.text
            data = json.loads(html)['data']
            stockList=set()
            if 'data' in data:
              for stock in data['data']:
                  stockList.add(stock['股票简称'])
              return stockList
            else:
              return stockList
        else:
            print("连接访问接口失败")
            return '000000'
    except Exception as e:
        print(e)
        return '000000'


if __name__ == "__main__":
    stock = crawl_data_from_wencai("今日涨停后开板")
    print(stock)
