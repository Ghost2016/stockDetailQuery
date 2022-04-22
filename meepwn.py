
#!/usr/bin/env python
#coding: utf-8

from copy import deepcopy
from time import sleep
from cv2 import sort
import requests
import re
import json
from tushareUtils import getCurrentTradeDay, getLastTradeDay

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

currentDay = getCurrentTradeDay()

def crawl_source_data(question="上一交易日没有涨停 今天涨停后开板 非st"):
    sleep(0.5)
    print(question)
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

def crawl_stock_data(question="上一交易日没有涨停 今天涨停后开板 非st"):
    response = crawl_source_data(question)
    if response.status_code == 200:
        try:
            html = response.text
            data = json.loads(html)['data']
            stockList = list()
            if 'data' in data:
                for stock in data['data']:
                    stockList.append(stock)
                return stockList
            else:
                return stockList
        except Exception as e:
            print('解析页面失败：', e)
            return crawl_stock_data(question)
    else:
        print("连接访问接口失败")
        handleSessionError()
        return crawl_stock_data(question)

def crawl_stock_name(question="上一交易日没有涨停 今天涨停后开板 非st"):
    stockNames = set()
    stockList = crawl_stock_data(question)
    for stock in stockList:
        stockNames.add(stock['股票简称'])
    return stockNames


def crawl_length(question="上一交易日没有涨停 今天涨停后开板 非st"):
    response = crawl_source_data(question)
    if response.status_code == 200:
        try:
            html = response.text
            data = json.loads(html)['data']
            stockList = set()
            if 'data' in data:
                return len(data['data'])
            else:
                return -1
        except Exception as e:
            print('解析页面失败：', e)
            return crawl_length(question)
    else:
        print("连接访问接口失败")
        handleSessionError()
        return crawl_length(question)


def crawl_highest(question="非st 非创业板 非科创板 非新股 二连板以上", day=currentDay):
    # print(question)
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
        return crawl_highest(question)

def crawl_sub_height(question="非st 非创业板 非科创板 非新股 二连板以上", day=currentDay):
    # print(question)
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
        return crawl_sub_height(question)


def crawl_length(question="非st 非创业板 非科创板 非新股 二连板以上"):
    response = crawl_source_data(question)
    if response.status_code == 200:
        html = response.text
        data = json.loads(html)['data']
        if 'data' in data:
            return len(data['data'])
        return '读取数据失败'
    else:
        print("连接访问接口失败")
        handleSessionError()
        return crawl_length(question)


def partOne():
    _day = "今日"
    # _day="昨日"
    height_10cm = "非st 非创业板 非科创板 非新股"
    up_all = crawl_length(_day + "涨幅大于0")
    down_all = crawl_length(_day + "涨幅小于0")
    up_5 = crawl_length(_day + "涨幅大于5 " + height_10cm)
    down_5 = crawl_length(_day + "跌幅大于5 " + height_10cm)
    up_num = crawl_length(_day + "涨停" + height_10cm)
    down_num = crawl_length(_day + "跌停 " + height_10cm)
    up_10_2 = crawl_length(_day + "二连板 " + height_10cm)
    up_highest = crawl_highest(_day + "二连板以上 " + height_10cm)

    a = Sentiment(str(datetime.datetime.now().date()), up_5=up_5, down_5=down_5, up_num=up_num,
                  down_num=down_num, up_all=up_all, down_all=down_all, up_10_2=up_10_2, up_highest=up_highest)
    # a=Sentiment('2022-01-14',up_5=up_5,down_5=down_5,up_num=up_num,down_num=down_num,up_all=up_all,down_all=down_all,up_10_2=up_10_2,up_highest=up_highest)
    # a = Sentiment('2021-11-30', 166, 1740, 64, 2, 2899, 1583, 9, 5)
    print(a)
    insert(a)

workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()

# 过滤空数据(可能是停牌引起的无数据的问题)，这类股票直接过滤掉
def filterNone(stock, day):
    # if stock['股票简称'] == '北方国际':
    #     print(stock)
    return stock.get('涨跌幅:前复权[%s]' % day,  stock.get('最新涨跌幅', 0)) != None


def crawl_earning_of_stocks(question='昨日涨停 非st 非新股 非退市', day=getCurrentTradeDay(), showDetail=False):
    # print(question)
    stocks = crawl_stock_data(question)
    total = 0
    index = 0
    # 过滤空数据
    stocks = filter(lambda x: filterNone(x, day), stocks)

    # 可能有停牌的票，则取0
    stocks=sorted(stocks, key=lambda stock : float(stock.get('涨跌幅:前复权[%s]' % day,  stock.get('最新涨跌幅', 0))), reverse=True)
    for stock in stocks:
        index+=1
        if showDetail:
            print(index, stock['股票简称'],stock.get('涨跌幅:前复权[%s]' % day,  stock.get('最新涨跌幅', 0)))
         # 可能有停牌的票，则取0
        total += float('%.2f' % float(stock.get('涨跌幅:前复权[%s]' % day,  stock.get('最新涨跌幅', 0))))
    if len(stocks) == 0:
        return '-'
    return float(str('%.2f' % float(total / len(stocks))))

def crawl_lost_of_stocks(question='曾涨停', day=getCurrentTradeDay()):
    # print(question)
    stocks = crawl_stock_data(question)
    total = 0
    upTotal = 0
    index = 0
    stocks=sorted(stocks, key=lambda stock : float(stock.get('涨跌幅:前复权[%s]' % day,  stock.get('最新涨跌幅', 0) )), reverse=True)
    for stock in stocks:
        topValue = stock['涨停价[%s]' % day]
        closeValue = stock['收盘价:不复权[%s]' % day]
        lastDayCloseValue = stock['收盘价:不复权[%s]' % getLastTradeDay(day)]
        percent = (float(topValue) - float(closeValue))/lastDayCloseValue * 100
        index+=1
        # print(index, stock['股票简称'], '回撤值', percent)
        total += float('%.2f' % float(percent))
    if len(stocks) == 0:
        return '-'
    return -float(str('%.2f' % float(total / len(stocks))))


def partTwo(start_date, i='1'):
    # start_date = '20220303'
    # start_date=datetime.datetime.now().strftime("%Y%m%d")
    # end_date=datetime.datetime.now().strftime("%Y%m%d")
    last_date = getLastTradeDay(start_date)
    _day = start_date
    print(_day + ':')
    no_st = "非st 非退市"
    # 今日涨停封死计数
    row_1 = crawl_length(_day + "涨停 " + no_st)
    # 今日涨停炸版计数
    row_2 = crawl_length(_day + "曾涨停 " + no_st)
    # 盘中带量曾封跌停计数
    row_3 = -crawl_length(_day + "曾跌停或者跌停 "+ no_st)
    # 收盘带量封死跌停计数
    row_4 = -crawl_length(_day + "跌停且非一字跌停 " + no_st)
    # 盘中超跌-5%计数
    row_5 = -crawl_length(("%s最低价格/%s收盘价格小于0.95 " %
                         (start_date, last_date)) + no_st)
    # 收盘超跌-5%计数
    row_6 = -crawl_length(_day + " 跌幅大于5% " + no_st)
    # 阈值
    row_7 = -250
    # 打板当日封板率
    row_8 = '自动计算'
    # 昨日所有涨停收益率（不包含炸板）
    row_9 = crawl_earning_of_stocks('%s涨停 非st 非新股 非退市' % last_date)
    # 昨日所有涨停真实收益率（包含炸板）
    row_10 = crawl_earning_of_stocks('%s涨停或%s曾涨停 %s非一字板或者%s放量 非st 非退市' % (last_date,last_date,last_date,last_date))
    # 当天两市最高连板板数
    row_11 = crawl_highest('%s非st 非创业板 非科创板 非新股 二连板以上'% _day)
    # 当天两市次高连板板数
    row_12 = crawl_sub_height('%s非st 非创业板 非科创板 非新股 二连板以上'% _day)
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
    worksheet.write('H' + i, row_7)
    worksheet.write('I' + i, row_8)
    worksheet.write('J' + i, row_9)
    worksheet.write('K' + i, row_10)
    worksheet.write('L' + i, row_11)
    worksheet.write('M' + i, row_12)
    worksheet.write('N' + i, row_13)
    worksheet.write('O' + i, row_14)
    


if __name__ == "__main__":
    cDay=getCurrentTradeDay()
    # cDay = '20220407'
    # _day = cDay
    partTwo(cDay)
    # cDay=datetime.datetime.now().strftime("%Y%m%d")
    # max=10
    # for d in range(1, max):
    #     lastDay = getLastTradeDay(cDay)
    #     # partTwo(cDay, str(21-d))
    #     r1 = str('%.2f' % crawl_earning_of_stocks('%s涨停 非st 非新股 非退市 %s涨跌幅' % (lastDay,_day), _day))
    #     r2 = str('%.2f' % crawl_earning_of_stocks('%s涨停或%s曾涨停 %s非一字板或者%s放量 非st 非退市 %s涨跌幅' % (lastDay, lastDay, lastDay, lastDay, _day), _day))
    #     print(cDay,r1, r2)
    #     worksheet.write('A' + str(max - d), cDay)
    #     worksheet.write('B' + str(max - d), r1)
    #     worksheet.write('C' + str(max - d), r2)
    #     cDay = lastDay
    workbook.close()
    os.system('open hello.xlsx')
    
    
    
