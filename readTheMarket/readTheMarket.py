#!/usr/bin/env python
#coding: utf-8

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options

# 复盘结果
readResult = ""
# 浏览器驱动
driver = None
chrome_options = None
# 概念，板块
# 1. 大方向（白马股与题材股）（涨跌幅区间）
# 2. 策略方向
# 3. 亏损股 ---- 
# 4. 运气
# 5. 大盘的成交量（）
# 6. 2板+以上的基本属性（价格，市值，上市的时间和当前流通股票【区分近端次新，远端次新，非次新】，基金持仓比例【可能会不准备，是放在季报里面公布】，信托持仓比例）

# 首板数量
def get1DailyUpLimitCount(num):
    if num == 0:
        return ''
    return ('今日首板%d个' % num)

# 二板数量
def get2DailyUpLimitCount(num):
    return ('今日二板%d个' % num)

# 三板数量
def get3DailyUpLimitCount(num):
    return ('今日三板%d个' % num)

# 四板数量
def get4DailyUpLimitCount(num):
    return ('今日四板%d个' % num)

# 五板数量
def get5DailyUpLimitCount(num):
    return ('今日五板%d个' % num)

# 六板数量
def get6DailyUpLimitCount(num):
    return ('今日六板%d个' % num)

# 七板数量
def get7DailyUpLimitCount(num):
    return ('今日七板%d个' % num)

# 涨停数量
def getDailyUpLimitCount(num):
    return ('今日涨停%d个' % num)

# 跌停数量
def getDailyDownLimitCount(num):
    return ('今日跌停%d个' % num)

# 首板策略成功的数量
def getFirstBanSucceedCount(num):
    return ('今日首板策略成功股票%d个' % num)

# 首板策略失败的数量
def getFirstBanFailedCount(num):
    return ('今日首板策略失败股票%d个' % num)

# 基础策略（所有都包含的）
baseStrategy = " 股票简称不包含st 上市时间大于1个月"

# 简单策略
easyStrategies = [
  {
    'name': '今天的涨停 上一个交易日没有涨停',
    'method': get1DailyUpLimitCount
  },
  # {
  #   'name': '连续2天涨停 前面第2个交易日没有涨停',
  #   'method': get2DailyUpLimitCount
  # },
  # {
  #   'name': '连续3天涨停 前面第3个交易日没有涨停',
  #   'method': get3DailyUpLimitCount
  # },
  # {
  #   'name': '连续4天涨停 前面第4个交易日没有涨停',
  #   'method': get4DailyUpLimitCount
  # },
  # {
  #   'name': '连续5天涨停 前面第5个交易日没有涨停',
  #   'method': get5DailyUpLimitCount
  # },
  # {
  #   'name': '连续6天涨停 前面第6个交易日没有涨停',
  #   'method': get6DailyUpLimitCount
  # },
  # {
  #   'name': '连续7天涨停 前面第7个交易日没有涨停',
  #   'method': get7DailyUpLimitCount
  # },
  # {
  #   'name': '今日的涨停',
  #   'method': getDailyUpLimitCount
  # },
  # {
  #   'name': '今日的跌停',
  #   'method': getDailyDownLimitCount
  # },
  {
    'name': '上一交易日没有涨停 今天涨停 今天开板次数大于0 今天涨幅大于5% 非st  流通市值小于60亿大于8亿 基金没有持股或者基金持股比例小于0.8% 信托没有持股或者基金持股比例小于0.5%',
    # 'name': '上一交易日没有涨停 今天涨停开板次数大于0 今天涨停 十大流通股东不包含信托 流通市值小于40亿大于8亿 基金没有持股或者基金持股比例小于0.8%',
    'method': getFirstBanSucceedCount
  },
  {
    'name': '上一交易日没有涨停 今天没有涨停 今天开板次数大于1 今天涨幅大于5% 非st  流通市值小于60亿大于8亿 基金没有持股或者基金持股比例小于0.8% 信托没有持股或者基金持股比例小于0.5%',
    'method': getFirstBanFailedCount
  }
]

# 复盘
def readTheMarket():
    global readResult, baseStrategy, driver
    os.system('exit')
    if not driver:
        print('打开浏览器')
        # 启动无界面化
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome('./chromedriver.81', chrome_options=chrome_options)
        # driver = webdriver.Chrome('/Users/ghost/Downloads/chromedriver', chrome_options=chrome_options)
        # driver = webdriver.Chrome('/Users/ghost/Downloads/chromedriver 76.0.3809.68',chrome_options=chrome_options)
        # 打开爱问财页面
        driver.get('http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%E8%BF%91%E4%B8%80%E4%B8%AA%E6%9C%88%E6%91%98%E5%B8%BD%E4%B8%AA%E8%82%A1&queryarea=')
        # 找到搜索框
        textarea = driver.find_element_by_css_selector('textarea')
        # 找到搜索按钮
        button = driver.find_element_by_id('qs-enter')
        # 选出的数量
        numberText = driver.find_element_by_css_selector('#boxTitle>.num')
        # 开始进入正式内容(遍历策略)
        # 策略长度
        length = len(easyStrategies)
        # 用于进行遍历的
        i = 0
        # 进行简单策略
        def easyLoop(_strategy, _method, _i):
             # 清空搜索框
            textarea.clear()
            # 输入要进行的策略
            textarea.send_keys(_strategy)
            # 点击按钮
            button.click()
            # time.sleep(0.5)
            # 等待网站上的转圈消失
            WebDriverWait(driver, 20).until(
              EC.invisibility_of_element_located((By.ID, 'robotresultTip'))
            )
            return _method(int(numberText.text)) + ("," if((_i+1) != length) else ".")
        while(i < length):
            readResult = readResult + easyLoop(easyStrategies[i]['name'] + baseStrategy, easyStrategies[i]['method'], i)
            i = i + 1
        # 退出浏览器
        print(readResult)
        driver.quit()
        # MAC下关闭Chrome进程（有时会出现调用driver.quit()无法关闭Chrome的现象）
        # os.system('pkill Google Chrome')
    else:
        driver.execute_script("window.location.reload()")
        pass
    pass

if __name__ == '__main__':
    # 复盘
    readTheMarket()
# '现价(元)\n涨跌幅(%)\na股流通市值 (元)\n2019.06.18\na股市值(不含限售股)排名\n2019.06.18\n上市天数(天)\n2019.06.17\n涨停次数(次)\n06.17-06.18\n区间成交额(元)\n06.17-06.18\n\n\n6.53\n9.93\n102.39亿\n663/3616\n7,320\n2\n3.06亿\n17.22\n102.39亿\n化工 -\n化学制品 -\n氮肥\n19990603\n10.55\n10.01\n80.07亿\n860/3616\n6,768\n2\n9,690.25万\n11.02\n80.31亿\n医药生物 -\n中药 -\n中药Ⅲ\n20001206\n4.50\n10.02\n49.17亿\n1353/3616\n9,825\n2\n1.72亿\n17.47\n49.17亿\n交运设备 -\n汽车零部件 -\n汽车零部件Ⅲ\n19920724\n7.37\n10.00\n43.77亿\n1523/3616\n2,505\n2\n3.42亿\n24.47\n50.12亿\n机械设备 -\n专用设备 -\n农用机械\n20120808\n6.62\n9.97\n42.39亿\n1558/3616\n8,387\n2\n10.41亿\n24.68\n86.51亿\n商业贸易 -\n贸易 -\n贸易Ⅲ\n19960701\n10.21\n10.02\n35.56亿\n1817/3616\n4,528\n2\n1.97亿\n11.02\n36.83亿\n医药生物 -\n中药 -\n中药Ⅲ\n20070124\n26.90\n10.02\n31.35亿\n2016/3616\n965\n2\n4.85亿\n17.54\n64.56亿\n信息服务 -\n传媒 -\n其他传媒\n20161026\n37.47\n10.01\n14.99亿\n3001/3616\n33\n2\n11.55亿\n25.61\n149.88亿\n化工 -\n化工合成材料 -\n其他纤维\n20190516\n12.24\n9.97\n12.15亿\n3187/3616\n634\n2\n6,752.87万\n15.32\n20.69亿\n医药生物 -\n中药 -\n中药Ⅲ\n20170922\n20.06\n9.98\n12.04亿\n3196/3616\n529\n2\n4.94亿\n19.84\n37.20亿\n医药生物 -\n化学制药 -\n化学制剂\n20180105'
# js
# .replace(/\n\d{4}\.\d{2}\.\d{2}\n/g, "\n")
# .replace(/\d{2}\.\d{2}-\d{2}.\d{2}\n/g, "")
# .replace(/\n\n/g, "\n")
# .replace(/\n\n/g, "\n")