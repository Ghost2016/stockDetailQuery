#!/usr/bin/env python
#coding: utf-8

# 此文件用于获取首板烂板策略的收益率

from meepwn import crawl_earning_of_stocks, crawl_highest, crawl_length, crawl_lost_of_stocks, crawl_index
from tushareUtils import getCurrentTradeDay, getLastTradeDay, getTushareInstance
from categories.sentimentCategory import getSentimentOfFirstBrokenBan, autoCal
import xlsxwriter
import os
import datetime
import sys
import signal

fileName = 'firstBrokenBan.xlsx'
workbook = xlsxwriter.Workbook(fileName)
cell_format = workbook.add_format({
    'bold': True,
    'align':    'center',
    'valign':   'vcenter',
})

worksheet = workbook.add_worksheet()
letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
          'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT']

no_st = " 非st 非北交所票 非退市"
no_new = ' 非新股 '
# 定义填充头部
hasWriteHeader = False

def getCategories(day):
    currentDay = day
    lastTradeDay = getLastTradeDay(currentDay)
    theDayBeforeLastTradeDay = getLastTradeDay(lastTradeDay)
    return[
    {
      'category': ' %s涨停 %s开板次数大于0 %s未涨停 %s' % (currentDay, currentDay, lastTradeDay, no_st + no_new),
      'text': '今日成功个数',
      'method': crawl_length
    },
    {
      'category': ' %s未涨停 %s开板次数大于0 %s未涨停 %s' % (currentDay, currentDay, lastTradeDay, no_st + no_new),
      'text': '今日失败个数',
      'method': crawl_length
    },
    {
      'category': '%s涨停或者未涨停 %s开板次数大于0 %s未涨停 %s' % (currentDay, currentDay, lastTradeDay, no_st + no_new),
      'text': '今日触板个数',
      'method': crawl_length
    },
    *getSentimentOfFirstBrokenBan(day),
    autoCal('今日成功率'),
    {
      'text': '昨日成功收益率',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s涨停 %s开板次数大于0 %s未涨停 %s' % (currentDay, lastTradeDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new), currentDay)
    },
    {
      'text': '昨日真实收益率（包含炸板）',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s涨停或曾涨停 %s开板次数大于0 %s未涨停 %s' % (currentDay, lastTradeDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new), currentDay)
    },
    autoCal('昨日成功今日红盘比（自动计算）'),
    {
      'text': '今日破板平均亏损',
      'func': crawl_lost_of_stocks('%s曾涨停 %s开板次数大于0 %s涨停价 %s收盘价 %s收盘价不为空 %s' % (currentDay, currentDay, currentDay, currentDay, lastTradeDay,  no_st + no_new), currentDay)
    },
    {
      'text': '昨日失败收益率',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s曾涨停 %s开板次数大于0 %s未涨停 %s' % (currentDay, lastTradeDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new), currentDay)
    },
    autoCal('昨日成功今日大面比（自动计算）'),
  ]

# 获取数据
def getData(day = getCurrentTradeDay()):
    global hasWriteHeader
    categories = getCategories(day)
    max = len(categories)
    values = []
    if not hasWriteHeader:
        worksheet.write('A1', '日期')
    for d in range(0, max):
        value = None
        category = categories[d]
        if 'func' in category:
            value = category['func']
        else:
            value = category.get('method', crawl_earning_of_stocks)(category['category'])
        # print(category['text'], value)
        if not hasWriteHeader:
            worksheet.write(letter[d+1] + '1', category['text'])
        values.append(value)
    return values


def getHistoryData():
    global hasWriteHeader, a
    dayLength = 1
    # currentDay = '20221028'
    currentDay = getCurrentTradeDay()
    # currentDay = getLastTradeDay(currentDay)
    for i in range(0, dayLength):
        values = getData(currentDay)
        worksheet.write(letter[0] + str(dayLength-(i-1)), datetime.datetime.strptime(currentDay, '%Y%m%d').strftime("%Y/%m/%d"))
        for index, value in enumerate(values):
            worksheet.write(letter[index+1] + str(dayLength -(i-1)), value)
        print(i, currentDay, values)
        currentDay = getLastTradeDay(currentDay)
        hasWriteHeader = True

def setColumnWidth():
    # 日期
    worksheet.set_column(0, 0, 10, cell_format)
    # 数量
    worksheet.set_column(1, 9, 3.5, cell_format)
    # 率
    worksheet.set_column(10, 60, 5.2, cell_format)
    # 跌停数量
    worksheet.set_column(22, 22, 3.5, cell_format)

# 生成数据并打开
def exportDataAndOpen():
    setColumnWidth()
    workbook.close()
    os.system('open %s' % fileName)

# 自定义信号处理函数
# 防止因为想提前退出而没有生成数据
def beforeExit():
    print("终止")
    exportDataAndOpen()
    sys.exit(0)
   
# 自定义处理 Ctrl + C 终止程序
signal.signal(signal.SIGINT, beforeExit)

if __name__ == "__main__":
    try:
        getHistoryData()
        exportDataAndOpen()
    except Exception as e:
        # 防止因为出错退出而没有数据
        exportDataAndOpen()
    

