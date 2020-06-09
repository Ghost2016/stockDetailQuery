
#!/usr/bin/env python
#coding: utf-8

import urllib
import requests
import re
import json
import operator, os
import threading, time
# 用于判断是什么系统
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from multiprocessing import Process, Pool, Queue

from selenium.webdriver.chrome.options import Options
# 本机库
# 用于存放历史股票列表
from fileUtils import saveStocks, getStocks
# 交易工具
from tradeUtils import isInTradeTime
# 封装的微信的api
from wechat import login, sendMessageToMyself, sendMessageToFriend
# 常量
from variables import const
from subprocess import call

# 如果不在交易时间，则不会进入策略
if not isInTradeTime():
    print('不在交易时间了...')
    os._exit(1)

# 是否是在Mac上进行操作
isOnMac = (platform.system() == 'Darwin')
# 是否需要使用微信来发送消息
useWeChatToSendMessage=False
# useWeChatToSendMessage=True

# 是否在进行复盘的操作

# 先登录微信
useWeChatToSendMessage and login()


# 用来进行复盘的策略
categories = [
  {"今日的涨停 股票简称不包含st": '今天涨停的个数:'},
  {"今日的跌停 股票简称不包含st": '今天跌停的个数:'},
  # 首板
  # '今天涨停 非st',
  # 首板第二日表现
  # '上上个交易日没有涨停 上一个交易日涨停 非st 今日涨幅大于3%',
  # 首板第二天接力成功
  # '上上个交易日没有涨停 上一个交易日涨停 非st 今日涨停'
]


# 存放当前的票的列表的Set
current_stock_list = set()
# 存放所有进来过的票的列表
total_stock_list = getStocks()
# print('票池已有数据: ', total_stock_list)
# chrome浏览器的驱动
driver=None
chrome_options=None
# 用于子进程间通信 获取Token
# NEED_TOKEN='needtoken'
# IS_NOT_IN_TRADE_TIME='isnotintradetime'
# 循环次数
timer=0
# 防止出现栈溢出而定义的全局变量
header=None
url=None
res=None
html=None
stockList=[]
result=[]
# 网站token信息
token=None

# 策略内容
# categoryString="昨天没有涨停 今天涨停后开板 今天涨幅大于5% 非st 十大流通股东不包含信托"
# categoryString="上一个交易日没有涨停 今日涨停后开板 非st 十大流通股东不包含信托"
categoryString="上一交易日没有涨停 今天涨停后开板 非st 流通市值小于60亿大于8亿 基金没有持股或者基金持股比例小于0.8% 信托没有持股或者信托持股比例小于0.8%"

# 使用set进行对比，得到新增加的票
def getFirstInStock(l):
    global current_stock_list, total_stock_list
    # print('存放所有的票的列表:', total_stock_list)
    current_stock_list=set(l)
    # 取并后取异或得到新进来的票
    result = (current_stock_list | total_stock_list) ^ total_stock_list
    if not len(result) == 0:
        print('新进来的票:', result)
        # 进行弹窗提示
        showMessage(list(result)[0])
        # 发送微信消息
        useWeChatToSendMessage and sendMessage(result)
        # 获取全部的股票的列表
        total_stock_list= total_stock_list | result
        # 保存全部股票的列表
        saveStocks(total_stock_list)
        # pass

# 发送信息（目前是发送到微信）
def sendMessage(result):
    sendMessageToMyself(result)
    # sendMessageToFriend(result)

# 弹出提示（目前是调用Mac自带的弹出提示，windows可能需要更换其他的提示）
def showMessage(stockname) :
    if isOnMac:
        # os.popen("osascript -e 'display notification \"" + stockname + "\" with title \"有新的票来了\"'")
        os.system("osascript -e 'beep 3'")
        os.system("osascript -e 'display notification \"软件\" with title \"更新完成\"'")

# 获取token
def getToken(q, m):
    global driver, chrome_options
    if not m.empty():
        tempString = m.get(True)
        if tempString == const.NEED_TOKEN: 
            if not driver:
                print('not driver')
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                # driver = webdriver.Chrome('/Users/ghost/Downloads/chromedriver 76.0.3809.68', chrome_options=chrome_options)
                driver = webdriver.Chrome('./chromedriver.83', chrome_options=chrome_options)
                # 打开爱问财页面
                driver.get('http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%E8%BF%91%E4%B8%80%E4%B8%AA%E6%9C%88%E6%91%98%E5%B8%BD%E4%B8%AA%E8%82%A1&queryarea=')
            else:
                driver.execute_script("window.location.reload()")
                pass
            # 拿token
            token=driver.execute_script("return window.localStorage.getItem('hexin-v')")
            q.put(token)
            # 打印token
            print('token:', token)
        # 过了交易时间了
        elif tempString == const.IS_NOT_IN_TRADE_TIME:
            # 退出浏览器
            driver.quit()

# 遍历策略
# q存放token
# d存放stockList
# m存放与其他线程通信的标签
# t代表token的值
def parseIWencai(q, d, m, t=''):
    global timer, token, header, url, res, html, stockList
    while isInTradeTime():
        print('第%s次' % timer)
        if timer % 10 == 0:
            m.put(const.NEED_TOKEN)
            time.sleep(0.3)
            try:
                getToken(q,m)
            except Exception as e:
                print('getToken Error:',e)
                continue
            finally:
                pass
        if not q.empty(): 
            token = q.get(True)
        if token != '':
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                      'hexin-v': token}
            url = 'http://www.iwencai.com/stockpick/load-data?typed=1&preParams=&ts=1&f=1&qs=result_rewrite' \
                  '&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&queryarea=&w=' + urllib.parse.quote(categoryString)
            try:
                # 解析逻辑
                res = requests.get(url,headers=header)
                html = res.text
                # 过滤出来票
                stockList = set(re.findall('(?<=&w=)\d{6}',html,re.S))
                d.put(stockList)
                # 获取首次进策略的票
                getFirstInStock(stockList)
            except Exception as e:
                print('Error:',e)
            finally:
                pass
        # 休息2s
        time.sleep(0)
        # 次数自加1
        timer=timer + 1
        # timer = 10 / 0
        # 如果过了交易时间
        if not isInTradeTime():
            print('过了交易时间了')
            m.put(const.IS_NOT_IN_TRADE_TIME)
            return false
        else:
            # 再次爬取数据
            # 不使用递归以防止产生栈溢出
            # return parseIWencai(q, d, m ,token)
            pass
# 循环
def doLoop(fn):
    global driver
    # 父进程创建一个Queue，并传递给各个子进程，存储数据
    q = Queue()
    d = Queue()
    m = Queue()
    # 子进程pw
    gt = Process(target=fn, args=(q, d, m, ''))
    getToken(q, m)
    gt.start()
    gt.join()
    # if driver:
    # driver.quit()
    print('结束了')
    # 退出
    os._exit(1)

# 复盘
def readTheMarket():
    global driver, chrome_options
    if not driver:
        print('not driver')
        # 启动无界面化
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome('/Users/ghost/Downloads/chromedriver', chrome_options=chrome_options)
        driver = webdriver.Chrome('./chromedriver.83', chrome_options=chrome_options)
        # 打开爱问财页面
        driver.get('http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%E8%BF%91%E4%B8%80%E4%B8%AA%E6%9C%88%E6%91%98%E5%B8%BD%E4%B8%AA%E8%82%A1&queryarea=')
        # 找到搜索框
        textarea = driver.find_element_by_css_selector('textarea')
        # 找到搜索按钮
        button = driver.find_element_by_id('qs-enter')
        # 选出的数量
        numberText = driver.find_element_by_css_selector('#boxTitle>.num')
        # 开始进入正式内容(遍历策略)
        
        # 清空搜索框
        textarea.clear()
        # 输入要进行的策略
        textarea.send_keys('今日的涨停 股票简称不包含st')
        # 点击按钮
        button.click()
        # time.sleep(0.5)
        # 等待网站上的转圈消失
        WebDriverWait(driver, 20).until(
          EC.invisibility_of_element_located((By.ID, 'robotresultTip'))
        )
        # 打印结果
        print('今日涨停个数' + numberText.text + '个')
        # 退出浏览器
        driver.quit()
        # MAC下关闭Chrome进程（有时会出现调用driver.quit()无法关闭Chrome的现象）
        os.system('pkill Google Chrome')
    else:
        driver.execute_script("window.location.reload()")
        pass
    pass

if __name__ == '__main__':
    # 微信消息测试
    useWeChatToSendMessage and sendMessage('这只是一条测试数据，用于检测是否能够成功从电脑端发消息')
    # 不断查询问财
    doLoop(parseIWencai)
    # 复盘
    # readTheMarket()
    # showMessage('112133')
    # cmd = 'display notification \"' + \
    #     "Notificaton memo" + '\" with title \"Titile\"'
    # call(["osascript", "-e", cmd])