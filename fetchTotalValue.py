#!/usr/bin/env python
#coding: utf-8

# 此文件用于获取各类策略的收益率

from meepwn import crawl_earning_of_stocks, crawl_highest, crawl_length, crawl_lost_of_stocks, crawl_index, crawl_stock_data
from tushareUtils import getCurrentTradeDay, getLastTradeDay, getTushareInstance
import xlsxwriter
import os
import datetime
fileName = 'totalValue.xlsx'
workbook = xlsxwriter.Workbook(fileName)
cell_format = workbook.add_format({
    'bold': True,
    'align':    'center',
    'valign':   'vcenter',
})

worksheet = workbook.add_worksheet()
letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
          'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM']

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
    lastTradeDay = getLastTradeDay(currentDay)
    theDayBeforeLastTradeDay = getLastTradeDay(lastTradeDay)
    threeDayBefore = getLastTradeDay(theDayBeforeLastTradeDay)
    return[
    # 超小票
    {
      'text': '0-20亿',
      'func': crawl_length('%s涨停 %s 市值大于0亿小于20亿' % (currentDay, no_st + no_new))
    },
    # 小票
    {
      'text': '20-30亿',
      'func': crawl_length('%s涨停 %s 市值大于20亿小于30亿' % (currentDay, no_st + no_new))
    },
    # 中小票
    {
      'text': '30-50亿',
      'func': crawl_length('%s涨停 %s 市值大于40亿小于50亿' % (currentDay, no_st + no_new))
    },
    # 中票
    {
      'text': '50-100亿',
      'func': crawl_length('%s涨停 %s 市值大于50亿小于100亿' % (currentDay, no_st + no_new))
    },
    # 大票
    {
      'text': '100-500亿',
      'func': crawl_length('%s涨停 %s 市值大于100亿小于500亿' % (currentDay, no_st + no_new))
    },
    # 超大票
    {
      'text': '500亿+',
      'func': crawl_length('%s涨停 %s 市值大于500亿' % (currentDay, no_st + no_new))
    },
    # 价格<10
    {
      'text': '价格<10',
      'func': crawl_length('%s涨停 %s 股价小于10' % (currentDay, no_st + no_new))
    },
    # 30>价格>10
    {
      'text': '10-30',
      'func': crawl_length('%s涨停 %s 股价大于10小于30' % (currentDay, no_st + no_new))
    },
    # 100>价格>30
    {
      'text': '30-100',
      'func': crawl_length('%s涨停 %s 股价大于30小于100' % (currentDay, no_st + no_new))
    },
    # 价格>100
    {
      'text': '>100',
      'func': crawl_length('%s涨停 %s 股价大于100' % (currentDay, no_st + no_new))
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

def doFetch():
    pass

def getHistoryData():
    global hasWriteHeader, a
    daylength = 1
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
    worksheet.set_column(1, 9, 8, cell_format)
    # 率
    worksheet.set_column(10, 37, 5.2, cell_format)
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

