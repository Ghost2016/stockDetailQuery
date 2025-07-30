
#!/usr/bin/env python
#coding: utf-8

# 此文件用于验证策略的收益率



from meepwn import crawl_earning_of_stocks, crawl_highest, crawl_length, crawl_lost_of_stocks, crawl_index, crawl_source_data, crawl_stock_data
from tushareUtils import getCurrentTradeDay, getLastTradeDay, getTushareInstance
import xlsxwriter
import os
import datetime
fileName = 'testCategory.xlsx'
workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
          'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ']

no_st = " 非st 非北交所票 非退市"
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
    lastTradeDay = getLastTradeDay(currentDay)
    theDayBeforeLastTradeDay = getLastTradeDay(lastTradeDay)
    threeDayBefore = getLastTradeDay(theDayBeforeLastTradeDay)
    return[
    # {
    #   'text': '上证涨跌幅',
    #   'func': crawl_index('%s上证涨跌幅' % currentDay, currentDay)
    # },
    # {
    #   'text': '新策略',
    #   # 上上个交易日首板 昨日收盘价/昨日最高价<0.90 9点25分跌幅小于-5%
    #   # 'func': crawl_source_data('20220422上证涨跌幅')
    #   'func': crawl_earning_of_stocks('%s未涨停 %s涨停 %s的9:25分涨跌幅大于3%% %s的9:25分的成交额大于2千万 %s的9:25分的成交额大于%s成交额的8%% %s的最终涨停时间倒序排列' % (threeDayBefore, theDayBeforeLastTradeDay, lastTradeDay, lastTradeDay, lastTradeDay, theDayBeforeLastTradeDay, lastTradeDay ), currentDay)
    # },
    # {
    #   'text': '新策略',
    #   # 上上个交易日首板 昨日收盘价/昨日最高价<0.90 9点25分跌幅小于-5%
    #   # 'func': crawl_source_data('20220422上证涨跌幅')
    #   'func': crawl_earning_of_stocks('%s未涨停 %s涨停 %s的9:25分涨跌幅大于3%% %s的9:25分的成交额大于2千万 %s的9:25分的成交额大于%s成交额的8%% %s的最终涨停时间倒序排列' % (threeDayBefore, theDayBeforeLastTradeDay, lastTradeDay, lastTradeDay, lastTradeDay, theDayBeforeLastTradeDay, lastTradeDay ), currentDay)
    # },
    {
      'text': '昨日连板成功收益率',
      'func': crawl_earning_of_stocks('%s涨跌幅 %s连续涨停天数为2以上 %s' % (currentDay, lastTradeDay, no_st + no_new), currentDay)
    },
    # {
    #   'text': '昨日首板失败收益率',
    #   # 上上个交易日首板 昨日收盘价/昨日最高价<0.90 9点25分跌幅小于-5%
    #   'func': crawl_earning_of_stocks('%s的未涨停 %s的涨停 (%s的收盘价/%s的最高价)<0.90 %s的竞价小于-5%s %s收盘涨跌幅 %s' % (threeDayBefore, theDayBeforeLastTradeDay, lastTradeDay, lastTradeDay, currentDay, '%', currentDay, no_st + no_new), currentDay, True)
    # }
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
        print(category['text'], value)
        if not hasWriteHeader:
            worksheet.write(letter[d+1] + '1', category['text'])
        values.append(value)
    return values

a={
  '20211214': [17, 23, 62, 15, 7, 3, 1, 4, 11, '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', '自动计算', 1, 3.2, -0.58, 2.09, 7.21, -1.91, 5.11, 7.74, -4.47, 5.3, 0.23, -4.34, -1.89, -1.94],
}

def getHistoryData():
    global hasWriteHeader, a
    daylength = 4
    # currentDay = '20211214'
    currentDay = getCurrentTradeDay()
    for i in range(0, daylength):
        values = getData(currentDay)
        # values= a[currentDay]
        worksheet.write(letter[0] + str(daylength-(i-1)), datetime.datetime.strptime(currentDay, '%Y%m%d').strftime("%Y/%m/%d"))
        for index, value in enumerate(values):
            worksheet.write(letter[index+1] + str(daylength -(i-1)), value)
        print(i, currentDay, values)
        currentDay = getLastTradeDay(currentDay)
        hasWriteHeader = True



if __name__ == "__main__":
    
    try:
        getHistoryData()
        worksheet.set_column(1,3,5.2)
        workbook.close()
    except Exception as e:
        print(e)
        workbook.close()
    os.system('open %s' % fileName)

