
#!/usr/bin/env python
#coding: utf-8

from copy import deepcopy
import requests
import re
import json

from utils.user_agent import getUserAgent

from verifyCode.codeUtils import handleSessionError
from sentiment import Sentiment

import datetime
from mysql import insert
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
    response = crawl_source_data(question)
    if response.status_code == 200:
        try:
            html = response.text
            data = json.loads(html)['data']
            stockList=set()
            if 'data' in data:
                for stock in data['data']:
                    stockList.add(stock['股票简称'])
                return stockList
            else:
                return stockList
        except Exception as e:
            print('解析页面失败：', e)
            return crawl_data_from_wencai(question)
    else:
        print("连接访问接口失败")
        handleSessionError()
        return crawl_data_from_wencai(question)

def crawl_source_data(question="上一交易日没有涨停 今天涨停后开板 非st"):
    """通过问财接口抓取数据
    
    Arguments:
        trade_date {[type]} -- [description]
        fields {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    payload = {
        # 查询问句
        "question": question,
        # 返回查询记录总数 
        "perpage": 5000,
        "query_type": "stock"
    }
    headers_wc = deepcopy(headers)
    headers_wc['User-Agent'] = getUserAgent()

    try:
        response = requests.get(Question_url, params=payload, headers=headers_wc)
        return response
    except Exception as e:
        print(e)
        handleSessionError()
        return crawl_source_data(question)

def crawl_highest(question="非st 非创业板 非科创板 非新股 二连板以上"):
    response = crawl_source_data(question)
    if response.status_code == 200:
        html = response.text
        data = json.loads(html)['data']
        height=0
        innerHeight=0
        if 'data' in data:
            for stock in data['data']:
                print(stock)
                pro = '连续涨停天数[%s]' % str(datetime.datetime.now().date()).replace('-', '')
                if pro in stock:
                    innerHeight = stock[pro]
                if height < innerHeight:
                    height = innerHeight
            return height
        else:
            return height
    else:
        print("连接访问接口失败")
        handleSessionError()
        return crawl_data_from_wencai(question)

def partOne():
    _day="今日"
    # _day="昨日"
    height_10cm="非st 非创业板 非科创板 非新股"
    up_all=len(crawl_data_from_wencai(_day + "涨幅大于0"))
    down_all=len(crawl_data_from_wencai( _day+ "涨幅小于0"))
    up_5=len(crawl_data_from_wencai(_day+ "涨幅大于5 " + height_10cm))
    down_5=len(crawl_data_from_wencai(_day+ "跌幅大于5 " + height_10cm))
    up_num=len(crawl_data_from_wencai(_day+ "涨停" + height_10cm))
    down_num=len(crawl_data_from_wencai(_day+ "跌停 " + height_10cm))
    up_10_2=len(crawl_data_from_wencai(_day+ "二连板 " + height_10cm))
    up_highest=crawl_highest(_day+ "二连板以上 " + height_10cm)
    
    a=Sentiment(str(datetime.datetime.now().date()),up_5=up_5,down_5=down_5,up_num=up_num,down_num=down_num,up_all=up_all,down_all=down_all,up_10_2=up_10_2,up_highest=up_highest)
    # a=Sentiment('2022-01-14',up_5=up_5,down_5=down_5,up_num=up_num,down_num=down_num,up_all=up_all,down_all=down_all,up_10_2=up_10_2,up_highest=up_highest)
    # a = Sentiment('2021-11-30', 166, 1740, 64, 2, 2899, 1583, 9, 5)
    print(a)
    insert(a)

def partTwo():
    pass


if __name__ == "__main__":
    partOne()

