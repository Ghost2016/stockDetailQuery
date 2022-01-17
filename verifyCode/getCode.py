#!/usr/bin/env python
#coding: utf-8

import base64
import json
import requests
import configparser
import os

# 一、图片文字类型(默认 3 数英混合)：
# 1 : 纯数字
# 1001：纯数字2
# 2 : 纯英文
# 1002：纯英文2
# 3 : 数英混合
# 1003：数英混合2
#  4 : 闪动GIF
# 7 : 无感学习(独家)
# 11 : 计算题
# 1005:  快速计算题
# 16 : 汉字
# 32 : 通用文字识别(证件、单据)
# 66:  问答题
# 49 :recaptcha图片识别 参考 https://shimo.im/docs/RPGcTpxdVgkkdQdY
# 二、图片旋转角度类型：
# 29 :  旋转类型
#
# 三、图片坐标点选类型：
# 19 :  1个坐标
# 20 :  3个坐标
# 21 :  3 ~ 5个坐标
# 22 :  5 ~ 8个坐标
# 27 :  1 ~ 4个坐标
# 48 : 轨迹类型
#
# 四、缺口识别
# 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
# 33 : 单缺口识别（返回X轴坐标 只需要1张图）
# 五、拼图识别
# 53：拼图识别
fileName = 'getImg.png'
cf = configparser.ConfigParser()
cf.read(os.path.dirname(__file__) + "/config.ini")

def base64_api(uname, pwd, img, typeid):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]

def get_verify_code(img_path):
    uname = cf.get("TuJian", "username")
    password = cf.get("TuJian", "password")
    result = base64_api(uname, password, img=img_path, typeid=3)
    return result


def remove_verify_code():
    file = os.path.dirname(__file__) +'/' + fileName
    if os.path.isfile(file):
        os.remove(file)

def rename_and_move_verify_code(code):
    file = os.path.dirname(__file__) +'/' + fileName
    repalceFile = os.path.dirname(__file__) + '/./train/' +code + '.png'
    if os.path.isfile(file):
        os.rename(file, repalceFile)

if __name__ == "__main__":
    rename_and_move_verify_code('cwde32')