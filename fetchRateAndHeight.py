#!/usr/bin/env python
#coding: utf-8

# 此文件用于获取各类策略的收益率

from meepwn import crawl_earning_of_stocks, crawl_highest, crawl_length, crawl_lost_of_stocks
from tushareUtils import getCurrentTradeDay, getLastTradeDay, getTushareInstance
import xlsxwriter
import os
import datetime
fileName = 'rateAndHeight.xlsx'
workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
          'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ']

no_st = " 非st 非退市"
no_new = ' 非新股'
# 定义填充头部
hasWriteHeader = False

# 思考， 4天3板这种算不算3板？
def getSpecificHeightData(num, day):
    currentDay = day
    return {
        'category': '%s涨停 %s连续涨停天数为%d %s' % (currentDay, currentDay, num, no_st + no_new),
        'text': '%d板' % num,
        'method': crawl_length
    }

def autoCal(text):
    return {
        'text': text,
        'func': '自动计算'
    }


# 新股需要手动去进行修正
# 搜索首板的时候不能搜索首板，匹配的是【几天几板是首板】，如果之前有过涨停的就不会被归纳到这个里面来
def getCategories(day):
    currentDay = day
    pro=getTushareInstance()
    lastTradeDay = getLastTradeDay(currentDay)
    theDayBeforeLastTradeDay = getLastTradeDay(lastTradeDay)
    threeDayBefore = getLastTradeDay(theDayBeforeLastTradeDay)
    return[
    {
      'category': '%s曾涨停 %s未涨停 %s' % (currentDay, lastTradeDay, no_st + no_new),
      'text': '首板炸',
      'method': crawl_length
    },
    {
      'category': '%s曾涨停 %s' % (currentDay, no_st + no_new),
      'text': '涨停炸',
      'method': crawl_length
    },
    {
      'category': '%s涨停 %s未涨停 %s' % (currentDay, lastTradeDay, no_st + no_new),
      'text': '首板',
      'method': crawl_length
    },
    getSpecificHeightData(2, currentDay),
    getSpecificHeightData(3, currentDay),
    getSpecificHeightData(4, currentDay),
    getSpecificHeightData(5, currentDay),
    {
      'category': '%s涨停 %s连续涨停天数大于5 %s' % (currentDay, currentDay, no_st + no_new),
      'text': '5板+',
      'method': crawl_length
    },
    {
      'text': '最高板',
      'func': crawl_highest('非st 非创业板 非科创板 非新股 %s二连板以上' % (currentDay), currentDay)
    },
    autoCal('涨停数'),
    autoCal('连板数'),
    autoCal('整体封板率'),
    autoCal('首板成功率'),
    autoCal('1进2晋级率'),
    autoCal('2进3晋级率'),
    autoCal('3进4晋级率'),
    autoCal('4进5晋级率'),
    autoCal('5板以上晋级率'),
    autoCal('连板晋级率(2板+)'),
    autoCal('中高位晋级率(3板+)'),
    autoCal('总情绪'),
    {
      'category': '%s跌停 %s' % (currentDay, no_st + no_new),
      'text': '跌停',
      'method': crawl_length
    },
    {
      'text': '昨日首板成功收益率',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s涨停 %s未涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new), currentDay)
    },
    {
      'text': '昨日首板失败收益率',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s曾涨停 %s未涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new), currentDay)
    },
    {
      'text': '昨日首板真实收益率（包含炸板）',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s涨停或曾涨停 %s未涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new), currentDay)
    },
    {
      'text': '昨日1进2成功收益率',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s连续涨停天数为2 %s' % (currentDay, lastTradeDay, no_st + no_new), currentDay)
    },
    {
      'text': '昨日1进2失败收益率',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s曾涨停 %s涨停 %s未涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, threeDayBefore, no_st + no_new), currentDay, True)
    },
    {
      'text': '昨日1进2真实收益率（包含炸板）',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s涨停或者曾涨停 %s涨停 %s未涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, threeDayBefore, no_st + no_new), currentDay)
    },
    {
      'text': '昨日连板成功收益率',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s连续涨停天数为2以上 %s' % (currentDay, lastTradeDay, no_st + no_new), currentDay)
    },
    {
      'text': '昨日连板失败收益率',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s曾涨停 %s涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new), currentDay)
    },
    {
      'text': '昨日连板真实收益率',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s涨停或者曾涨停 %s涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new), currentDay)
    },
    {
      'text': '前日连板失败收益率',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s未涨停 %s涨停 %s' % (currentDay, theDayBeforeLastTradeDay, threeDayBefore, no_st + no_new), currentDay)
    },
    {
      'text': '当日破板平均亏损',
      'func': crawl_lost_of_stocks('%s曾涨停 %s涨停价 %s收盘价 %s收盘价不为空 %s' % (currentDay, currentDay, currentDay, lastTradeDay,  no_st + no_new), currentDay)
    },
    {
      'text': '昨日破板平均收益',
      'func': crawl_earning_of_stocks('%s曾涨停 %s' % (lastTradeDay,  no_st + no_new), currentDay)
    },
    {
      'text': '昨日所有涨停真实收益率（包含炸板）',
      'func': crawl_earning_of_stocks('%s涨停或者曾涨停 %s' % (lastTradeDay,  no_st + no_new), currentDay)
    },
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

a={
  # '20220408': [19, 20, 48, 8, 4, 1, 1, 2, 6, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 13, 2.91, 1.25, 2.02, 3.75, 0.97, 2.36, 4.77, 1.75, 3.33, 0.03, -3.04, 0.98, 2.46],
  # '20220407': [22, 37, 19, 6, 1, 2, 2, 0, 5, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 29, -0.72, -4.45, -1.67, -4.21, -6.29, -4.5, -2.35, -7.14, -3.24, -4.37, -6.43, 0.14, 0.2],
  # '20220406': [20, 27, 58, 12, 5, 5, 0, 1, 7, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 12, 3.4, -0.6, 2.98, 1.83, -0.43, 1.48, 4.11, -3.99, 2.35, 1.63, -4.73, -0.31, 0.23],
  # '20220401': [6, 11, 52, 11, 5, 1, 0, 1, 6, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 13, 1.4, -1.93, -0.15, 7.22, -1.05, 2.44, 4.47, -2.43, 1.02, -2.03, -7.44, -0.12, 0.22],
  # '20220331': [33, 48, 38, 8, 4, 1, 1, 1, 6, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 5, 1.32, 0.51, 1.1, 5.08, -4.81, 2.88, 4.53, -2.42, 2.99, 0.22, -5.45, -1.85, 0.23],
  # '20220330': [24, 28, 65, 7, 4, 2, 1, 0, 5, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 1, 1.24, -1.53, 0.35, 6.01, 6.83, 6.19, 3.34, 7.36, 4.19, 0.23, -4.58, 0.69, -1.35],
  # '20220329': [19, 23, 40, 7, 3, 3, 1, 1, 11, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 16, 0.8, -2.6, -0.3, -0.31, -3.84, -0.89, 2.63, -7.17, 0.4, -2.34, -4.94, -0.32, -1.3],
  # '20220328': [21, 27, 44, 10, 3, 1, 0, 3, 10, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 16, -0.17, -1.1, -0.46, 0.72, -7.72, -3.23, -0.2, -6.18, -2.27, -0.34, -5.51, -0.55, -1.36],
  # '20220325': [25, 38, 56, 9, 2, 1, 1, 4, 12, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 9, 1.64, -1.48, 0.65, 3.59, -2.78, 0.4, 5.04, -0.65, 3.56, 0.68, -5.56, -0.36, -1.3],
  # '20220324': [21, 27, 45, 5, 4, 1, 1, 6, 11, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 4, -0.82, -3.59, -1.77, 4.56, -1.33, 1.62, 4.42, 0.15, 3.05, -0.38, -5.25, -0.79, -0.58],
  # '20220323': [26, 35, 50, 7, 2, 4, 1, 5, 10, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 8, 0.86, -0.22, 0.55, -1.46, -5.1, -2.27, 1.5, -4.06, 0.36, -1.14, -4.86, -0.11, -0.82],
  # '20220322': [19, 27, 48, 14, 7, 3, 3, 4, 9, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 8, 0.89, -5.58, -0.21, 0.51, -5.39, -0.39, 1.57, -5.39, 0.89, -0.3, -5.98, -1.09, -0.81],
  # '20220321': [16, 23, 78, 21, 7, 5, 3, 2, 8, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 0, 4.85, -0.76, 4.41, 9.32, 3.33, 8.23, 8.05, 3.33, 7.68, 1.64, -2.83, 0.17, -0.12],
  '20220411': [35, 43, 38, 10, 2, 2, 0, 1, 6, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 41, 0.18, -1.86, -0.4, -1.6, 2.14, -1.18, -1.74, 2.14, -1.51, -3.22, -5.97, -1.66, -0.62]
}

def getHistoryData():
    global hasWriteHeader, a
    daylength = 1
    # currentDay = '20220218'
    currentDay = getCurrentTradeDay()
    for i in range(0, daylength):
        values = getData(currentDay)
        # values= a[currentDay]
        worksheet.write(letter[0] + str(daylength-(i-1)), datetime.datetime.strptime(currentDay, '%Y%m%d').strftime("%Y/%m/%d"))
        for index, value in enumerate(values):
            worksheet.write(letter[index+1] + str(daylength -(i-1)), value)
        print(currentDay, values)
        currentDay = getLastTradeDay(currentDay)
        hasWriteHeader = True


if __name__ == "__main__":
    getHistoryData()
    workbook.close()
    os.system('open %s' % fileName)
        
# 昨天连板数量前5 非新股 非st

