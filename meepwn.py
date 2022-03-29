
#!/usr/bin/env python
#coding: utf-8

from copy import deepcopy
import requests
import re
import json
from tushareUtils import getTushareInstance

from utils.user_agent import getUserAgent

from verifyCode.codeUtils import handleSessionError
from sentiment import Sentiment

import datetime
from mysql import insert
import xlsxwriter
import os
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
           'Referer': "http://www.iwencai.com/unifiedwap/unified-wap/result/get-stock-pick",
           "Host": "www.iwencai.com",
           "X-Requested-With": "XMLHttpRequest",
           }


Question_url = "http://www.iwencai.com/unifiedwap/unified-wap/result/get-stock-pick"


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
        response = requests.get(
            Question_url, params=payload, headers=headers_wc)
        return response
    except Exception as e:
        print(e)
        handleSessionError()
        return crawl_source_data(question)

def crawl_stock_data(question):
    response = crawl_source_data(question)
    if response.status_code == 200:
        try:
            html = response.text
            data = json.loads(html)['data']
            stockList = set()
            if 'data' in data:
                for stock in data['data']:
                    stockList.add(stock)
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


def crawl_data_from_wencai(question="上一交易日没有涨停 今天涨停后开板 非st"):
    response = crawl_source_data(question)
    if response.status_code == 200:
        try:
            html = response.text
            data = json.loads(html)['data']
            stockList = set()
            if 'data' in data:
                return data['data']
            else:
                return stockList
        except Exception as e:
            print('解析页面失败：', e)
            return crawl_data_from_wencai(question)
    else:
        print("连接访问接口失败")
        handleSessionError()
        return crawl_data_from_wencai(question)


def crawl_highest(question="非st 非创业板 非科创板 非新股 二连板以上", day=str(
                    datetime.datetime.now().date()).replace('-', '')):
    response = crawl_source_data(question)
    if response.status_code == 200:
        html = response.text
        data = json.loads(html)['data']
        height = 0
        innerHeight = 0
        if 'data' in data:
            for stock in data['data']:
                pro = '连续涨停天数[%s]' % day
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

def crawl_sub_height(question="非st 非创业板 非科创板 非新股 二连板以上", day=str(
                    datetime.datetime.now().date()).replace('-', '')):
    response = crawl_source_data(question)
    if response.status_code == 200:
        html = response.text
        data = json.loads(html)['data']
        height = 0
        subHeight = 0
        innerHeight = 0
        if 'data' in data:
            for stock in data['data']:
                pro = '连续涨停天数[%s]' % day
                if pro in stock:
                    innerHeight = stock[pro]
                if height < innerHeight:
                    subHeight = height
                    height = innerHeight
                elif (not height == innerHeight) and subHeight < innerHeight:
                    subHeight = innerHeight
            return subHeight
        else:
            return subHeight
    else:
        print("连接访问接口失败")
        handleSessionError()
        return crawl_data_from_wencai(question)


def crawl_length(question="非st 非创业板 非科创板 非新股 二连板以上"):
    print('question:', question)
    response = crawl_source_data(question)
    if response.status_code == 200:
        html = response.text
        data = json.loads(html)['data']
        if 'data' in data:
            print(len(data['data']))
            return len(data['data'])
        return '读取数据失败'
    else:
        print("连接访问接口失败")
        handleSessionError()
        return crawl_data_from_wencai(question)


def partOne():
    _day = "今日"
    # _day="昨日"
    height_10cm = "非st 非创业板 非科创板 非新股"
    up_all = len(crawl_data_from_wencai(_day + "涨幅大于0"))
    down_all = len(crawl_data_from_wencai(_day + "涨幅小于0"))
    up_5 = len(crawl_data_from_wencai(_day + "涨幅大于5 " + height_10cm))
    down_5 = len(crawl_data_from_wencai(_day + "跌幅大于5 " + height_10cm))
    up_num = len(crawl_data_from_wencai(_day + "涨停" + height_10cm))
    down_num = len(crawl_data_from_wencai(_day + "跌停 " + height_10cm))
    up_10_2 = len(crawl_data_from_wencai(_day + "二连板 " + height_10cm))
    up_highest = crawl_highest(_day + "二连板以上 " + height_10cm)

    a = Sentiment(str(datetime.datetime.now().date()), up_5=up_5, down_5=down_5, up_num=up_num,
                  down_num=down_num, up_all=up_all, down_all=down_all, up_10_2=up_10_2, up_highest=up_highest)
    # a=Sentiment('2022-01-14',up_5=up_5,down_5=down_5,up_num=up_num,down_num=down_num,up_all=up_all,down_all=down_all,up_10_2=up_10_2,up_highest=up_highest)
    # a = Sentiment('2021-11-30', 166, 1740, 64, 2, 2899, 1583, 9, 5)
    print(a)
    insert(a)


def getLastTradeDay(day):
    dat = getTushareInstance().trade_cal(exchange='', start_date=day, end_date=day)
    return dat.iat[0, 3]

workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()
def partTwo(start_date, i):
    # start_date = '20220303'
    # start_date=datetime.datetime.now().strftime("%Y%m%d")
    # end_date=datetime.datetime.now().strftime("%Y%m%d")
    end_date = getLastTradeDay(start_date)
    _day = start_date
    print(_day + ':')
    no_st = "非st"
    # 今日涨停封死计数
    row_1 = crawl_length(_day + "涨停 " + no_st)
    # 今日涨停炸版计数
    row_2 = crawl_length(_day + "曾涨停 " + no_st)
    # 盘中带量曾封跌停计数
    row_3 = -crawl_length(_day + "曾跌停或者跌停 "+ no_st)
    # 收盘带量封死跌停计数
    row_4 = -crawl_length(_day + "跌停且非一字跌停 " + no_st)
    # 盘中超跌-5%计数
    row_5 = -crawl_length((" %s最低价格/%s收盘价格小于0.95 " %
                         (start_date, end_date)) + no_st)
    # 收盘超跌-5%计数
    row_6 = -crawl_length(_day + " 跌幅大于5% " + no_st)
    # 阈值
    row_7 = '-250'
    # 打板当日封板率
    row_8 = '自动计算'
    # 昨日所有涨停收益率（不包含炸板）
    row_9 = '手动输入'
    # 昨日所有涨停真实收益率（包含炸板）
    row_10 = '手动输入'
    # 当天两市最高连板板数
    row_11 = '手动输入'
    # 当天两市次高连板板数
    row_12 = '手动输入'
    # ma3涨停
    row_13 = '自动计算'
    # 偏离幅度
    row_14 = '自动计算'
    print('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % (row_1, row_2, row_3,
          row_4, row_5, row_6, row_7, row_8, row_9, row_10, row_11, row_12, row_13, row_14))
    worksheet.write('A' + i, _day)
    worksheet.write('B' + i, row_1)
    worksheet.write('C' + i, row_2)
    worksheet.write('D' + i, row_3)
    worksheet.write('E' + i, row_4)
    worksheet.write('F' + i, row_5)
    worksheet.write('G' + i, row_6)
    


if __name__ == "__main__":
    
    cDay = '20220329'
    for d in range(1, 45):
        q = '%s非st 非创业板 非科创板 非一字未开板新股 二连板以上'% cDay
        print(q)
        # partTwo(cDay, str(21-d))
        r1 = crawl_highest(q, cDay)
        r2 = crawl_sub_height(q, cDay)
        print(r1, r2)
        worksheet.write('A' + str(46 - d), cDay)
        worksheet.write('B' + str(46 - d), r1)
        worksheet.write('C' + str(46 - d), r2)
        cDay = getLastTradeDay(cDay)
    workbook.close()
    os.system('open hello.xlsx')
    
    
    
