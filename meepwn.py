
#!/usr/bin/env python
#coding: utf-8

from copy import deepcopy
import requests
import re

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


def crawl_data_from_wencai(question="今日涨停后开板"):
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
            stockList = set(re.findall("\"(\d{6}(?!\d))\"",html,re.S))
            return stockList
        else:
            print("连接访问接口失败")           
    except Exception as e:
        print(e)


if __name__ == "__main__":
    stock = crawl_data_from_wencai("今日涨停后开板")
    print(stock)