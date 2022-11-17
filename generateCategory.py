#!/usr/bin/env python
#coding: utf-8

# 林业和煤炭喜欢在进策略隔两日后拉升【需要考虑连续两日进策略的情况，后一日拉升后的情况】

from meepwn import crawl_earning_of_stocks, crawl_highest, crawl_length, crawl_lost_of_stocks, crawl_index, crawl_stock_data
from tushareUtils import getCurrentTradeDay, getLastTradeDay, getTushareInstance
from utils.common import letter
import xlsxwriter
import datetime
import os
no_need_industry = []
# no_need_industry = ['养殖业', '医疗器械', '生物制品']
second_day_industry = ['煤炭开采加工', '机场航运', '油气开采及服务']

no_st = " 非st 非北交所票 非退市"
no_new = ' 非新股'
no_sub_new = ' 非次新股'

fileName = 'totalValue.xlsx'
workbook = xlsxwriter.Workbook(fileName)
cell_format = workbook.add_format({
    'bold': True,
    'align':    'center',
    'valign':   'vcenter',
})

industry_cell_format = workbook.add_format({
    'bold': True,
    'valign':   'vcenter',
})

hasWriteHeader = False

worksheet = workbook.add_worksheet()
yCursor = 1

def getTodayCategory(industry='房地产'):
    currentDay = getCurrentTradeDay()
    lastTradeDay = getLastTradeDay(currentDay)
    cate = '%s成交额小于%s成交额 %s涨跌幅小于-3%s %s的非涨停并且%s的非曾涨停 所属行业是%s %s' % (currentDay, lastTradeDay, currentDay, '%', lastTradeDay, lastTradeDay, industry, no_st + no_new + no_sub_new)
    return cate

def getCategories(day, industry='房地产'):
    currentDay = day
    lastTradeDay = getLastTradeDay(currentDay)
    theDayBeforeLastTradeDay = getLastTradeDay(lastTradeDay)
    # threeDayBefore = getLastTradeDay(theDayBeforeLastTradeDay)
    # cate = '%s涨停 %s 市值大于0亿小于20亿' % (currentDay, no_st + no_new)
    cate = '%s涨跌幅 %s成交额小于%s成交额 %s涨跌幅排名最后三位 %s涨跌幅小于-3%s  %s的非涨停并且%s的非曾涨停 %s的非跌停 所属行业是%s %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay,lastTradeDay, lastTradeDay, '%', theDayBeforeLastTradeDay, theDayBeforeLastTradeDay,lastTradeDay, industry, no_st + no_new + no_sub_new)
    return cate

def getEarn(category, day):
    # crawl_earning_of_stocks('%s涨跌幅 %s涨停 %s未涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new), currentDay)
    return crawl_earning_of_stocks(category, day)

def getIndustries(day):
    currentDay = day
    lastTradeDay = getLastTradeDay(currentDay)
    stockList = crawl_stock_data('行业 %s跌幅前十 二级行业' % lastTradeDay)
    stockNames=list()
    for stock in stockList:
        stockNames.append(stock['指数简称'])
    # print(stockNames)
    return stockNames

def getEarnOfOneIndustry(day, industry='房地产'):
    category = getCategories(day, industry)
    return getEarn(category, day)

def getEarnOfAll(day):
    industries = getIndustries(day)
    total = 0
    # len = 0
    stocks = list()
    for i in industries:
        if i in no_need_industry:
            continue
        value = getEarnOfOneIndustry(day, i)
        if value != '-':
            print(i, value)
            stocks.append(i)
            stocks.append(value)
            total = total + float(value)
    print('总收益:', total, '\n参与的板块数量：', len(stocks), '\n分别是:', stocks)
    if len(stocks) != 0:
        stocks.insert(0, '总收益')
        stocks.insert(1, total/len(stocks))
    return stocks

def getHistoryData():
    global hasWriteHeader, a, yCursor
    daylength = 60
    # currentDay = '20220505'
    currentDay = getCurrentTradeDay()

    for i in range(0, daylength):
        values = getEarnOfAll(currentDay)
        # values= a[currentDay]
        worksheet.write(letter[0] + str(daylength-(i-1)), datetime.datetime.strptime(currentDay, '%Y%m%d').strftime("%Y/%m/%d"))
        for index, value in enumerate(values):
            worksheet.write(letter[index+1] + str(daylength-(i-1)), value)
        print(i, currentDay, values)
        currentDay = getLastTradeDay(currentDay)
        hasWriteHeader = True

def setColumnWidth():
    # 日期
    worksheet.set_column(0, 0, 10, cell_format)
    # 总收益
    worksheet.set_column(1, 1, 7, cell_format)
    # 行业收益
    for i in range(1, 10):
        # 行业名称
        worksheet.set_column(i*2+1, i*2+1, 10, industry_cell_format)
        # 收益
        worksheet.set_column(i*2+2, i*2+2, 3.5, cell_format)

if __name__ == "__main__":
    # print(getEarnOfOneIndustry(getCurrentTradeDay(), '互联网电商'))
    try:
        getHistoryData()
        setColumnWidth()
        workbook.close()
    except Exception as e:
        print(e)
        setColumnWidth()
        workbook.close()
    os.system('open %s' % fileName)
    

      
      