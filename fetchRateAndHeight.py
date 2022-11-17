#!/usr/bin/env python
#coding: utf-8

# 此文件用于获取各类策略的收益率

from meepwn import crawl_earning_of_stocks, crawl_highest, crawl_length, crawl_lost_of_stocks, crawl_index
from tushareUtils import getCurrentTradeDay, getLastTradeDay, getTushareInstance
import xlsxwriter
import os
import datetime
fileName = 'rateAndHeight.xlsx'
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
      'category': '%s跌停 %s' % (currentDay, no_st),
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
      'func': crawl_earning_of_stocks('%s涨跌幅 %s曾涨停 %s涨停 %s未涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, threeDayBefore, no_st + no_new), currentDay)
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
      'func': crawl_earning_of_stocks('%s曾涨停 %s涨跌幅 %s' % (lastTradeDay, currentDay,  no_st + no_new), currentDay)
    },
    {
      'text': '昨日所有涨停真实收益率（包含炸板）',
      'func': crawl_earning_of_stocks('%s涨停或者曾涨停 %s涨跌幅 %s' % (lastTradeDay, currentDay, no_st + no_new), currentDay)
    },
    {
      'text': '上证涨跌幅',
      'func': crawl_index('%s上证涨跌幅' % currentDay, currentDay)
    },
    {
      'category': '%s最低价格/%s收盘价格小于0.95 %s' % (currentDay, lastTradeDay, no_st),
      'text': '盘中超跌-5%计数',
      'method': crawl_length
    },
    {
      'text': '昨日的首板今日红盘个数',
      'func': crawl_length('%s涨跌幅大于0 %s涨停 %s未涨停 %s' % (currentDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new))
      },
      {
      'text': '昨日的首板今日大面个数',
      'func': crawl_length('(%s的收盘价格/开盘价格小于0.95)或者(%s的收盘价格/%s收盘价格小于0.95) %s涨停 %s未涨停 %s' % (currentDay, currentDay, lastTradeDay, lastTradeDay, theDayBeforeLastTradeDay, no_st + no_new))
      },
      {
      'text': '昨日的连板今日红盘个数',
      'func': crawl_length('%s涨跌幅大于0 %s连续涨停天数为2以上 %s' % (currentDay, lastTradeDay, no_st + no_new))
      },
      {
      'text': '昨日的连板今日大面个数',
      'func': crawl_length('(%s的收盘价格/开盘价格小于0.95)或者(%s的收盘价格/%s收盘价格小于0.95) %s连续涨停天数为2以上 %s' % (currentDay, currentDay, lastTradeDay, lastTradeDay, no_st + no_new))
      },
      {
      'text': '昨日的连板今日绿盘个数',
      'func': crawl_length('%s涨跌幅小于0 %s连续涨停天数为2以上 %s' % (currentDay, lastTradeDay, no_st + no_new))
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
  '20211214': [17, 23, 62, 15, 7, 3, 1, 4, 11, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 1, 3.2, -0.58, 2.09, 7.21, -1.91, 5.11, 7.74, -4.47, 5.3, 0.23, -4.34, -1.89, -1.94],
}

def getHistoryData():
    global hasWriteHeader, a
    daylength = 2
    # currentDay = '20220617'
    currentDay = getCurrentTradeDay()
    # currentDay = getLastTradeDay(currentDay)
    for i in range(0, daylength):
        values = getData(currentDay)
        # values= a[currentDay]
        worksheet.write(letter[0] + str(daylength-(i-1)), datetime.datetime.strptime(currentDay, '%Y%m%d').strftime("%Y/%m/%d"))
        for index, value in enumerate(values):
            worksheet.write(letter[index+1] + str(daylength -(i-1)), value)
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

if __name__ == "__main__":
    try:
        getHistoryData()
        setColumnWidth()
        workbook.close()
    except Exception as e:
        print(e)
        setColumnWidth()
        workbook.close()
    os.system('open %s' % fileName)

