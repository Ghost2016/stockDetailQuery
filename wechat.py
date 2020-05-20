#!/usr/bin/env python
#coding: utf-8

# 导入模块
# 更多API参考 https://wxpy.readthedocs.io/zh/latest/index.html
from wxpy import *
import requests

# 初始化一个用户
bot = None

# 集成图灵自动回复
# tulingApiKey="8d4f260b287d47b28390e4adee1b5a20"
# tuling=Tuling(api_key=tulingApiKey)

# 初始化机器人，扫码登陆
# bot = Bot(cache_path=True,console_qr=2)

# 机器人账号自身
# myself = bot.self


# 使用图灵机器人自动与指定好友聊天
# @bot.register(myself)
# def reply_my_friend(msg):
#     tuling.do_reply(msg)

# 给自己发送一条消息
# myself.send('hello')

# 向文件传输助手发送消息
# bot.file_helper.send('Hello from wxpy!')

def weather_friend():   #定义一个名为weather_friend的函数
    # 天气推送名单  也可以送备注来搜索好友
    my_friends = []   # 创建一个空列表，用来存放好友名单
    my_friends.append(bot.friends().search(u'iwand')[0]) # 搜索指定好友并添加至列表
    # my_friends.append(bot.friends().search(u'🔥')[0])
    # my_friends.append(bot.friends().search(u'佐之格⊙魅殇')[0])
    return my_friends
# 发送的内容
def Weather(location): # 定义一个发送天气的函数，并需要接收一个参数（该参数是好友在微信中设置的地点）
    #准备url地址
    path ='http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'
    url = path % location
    response = requests.get(url) # 对该地址和参数进行get请求
    result = response.json() # 将返回的结果转成json串
    # 为了防止因好友未设置地点而导致程序报错，所以需要对返回的error参数进行判断
    if int(result['error']) != 0:  # 当error为0时，搜索是正常的，一旦不等于0，表示存在错误
        location = '北京'  # 此时将地址设为一个默认地址 如北京
        url = path % location  # 拼接新的url
        response = requests.get(url) # 在对新的url进行get请求
        result = response.json()
    # 下面就是对正确请求到数据后的结果进行处理了
    # 问候语
    greetings = ('  早上好！这是今天的天气预报！……\n机器人：你的小野猫\n')
    try: # 此处增加异常处理是因为当好友设置的地区为国外的时候，error返回值不会报错，但不会有results
        # 取出天气结果
        results = result['results']
    except:
        return "啊哦，我迷路了，找不到地点！" # 当没有该地区的结果时，函数直接返回字符串，此时函数结束
    # 当正常取出结果后，继续进行下列操作

    # 取出数据字典第一天数据
    data1 = results[0]
    # 取出城市
    city = data1['currentCity']
    str1 = '  你的城市: %s\n' % city
    # 取出pm2.5值
    pm25 = data1['pm25']
    str2 = '  PM值: %s\n' % pm25
    # 评估空气质量
    pollution = calculate(pm25) # 此时调用calculate函数进行计算，所以该函数要写在此函数之前
    str3 = '  污染指数: %s\n' % pollution
    result1 = results[0]
    weather_data = result1['weather_data']
    data = weather_data[0]
    temperature_now = data['date']
    str4 = '  当前温度: %s\n' % temperature_now
    wind = data['wind']
    str5 = '  风向  : %s\n' % wind
    weather = data['weather']
    str6 = '  天气  : %s\n' % weather
    str7 = '  温度  : %s\n' % data['temperature']
    try: # 此处异常操作是因为有时候返回结果里面不存在下方内容
        message = data1['index']
        str8 = '  穿衣  : %s\n' % message[0]['des']
        str9 = '  我很贴心: %s\n' % message[2]['des']
        str10 = '  运动  : %s\n' % message[3]['des']
        str11 = '  紫外线 : %s\n' % message[4]['des']
        str = greetings + str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8 + str9 + str10 + str11
    except:
        str = greetings + str1 + str2 + str3 + str4 + str5 + str6 + str7

    return str

# 计算pm2.5的程度
def calculate(pm):
    if pm == '':
        pm25 = -1
    else:
        pm25 = int(pm)
        # 通过pm2.5的值大小判断污染指数
        if 0 <= pm25 < 35:
            pollution = '优'
        elif 35 <= pm25 < 75:
            pollution = '良'
        elif 75 <= pm25 < 115:
            pollution = '轻度污染'
        elif 115 <= pm25 < 150:
            pollution = '中度污染'
        elif 150 <= pm25 < 250:
            pollution = '重度污染'
        elif pm25 >= 250:
            pollution = '严重污染'
        else:
            pollution = '希望你健在'
        return pollution

# 断点
# embed()
# 搜索名称含有 "游否" 的男性深圳好友
# my_friend = bot.friends().search('刘源', sex=MALE, city="")[0]
# my_friend = bot.friends().search('刘源', sex=MALE, city="深圳")[0]

# 登录
def login():
    global bot
    # 初始化机器人，扫码登录
    bot = Bot(cache_path=True,console_qr=2)

# 给自己发信息
def sendMessageToMyself(text):
     myself = bot.self
     myself.send(text)

# 给朋友发信息
def sendMessageToFriend(text):
    my_friend = bot.friends().search('刘源', sex=MALE, city="成都")[0]
    my_friend.send(text)

if __name__ == '__main__':
    login()
    # sendMessageToMyself('hello handsome boy!')
    # sendMessageToMyself(Weather('成都'))
    # sendMessageToFriend('hello handsome boy!')